"""博客部署模块

支持本地 Hugo 构建并通过 rsync 同步到远程服务器。
支持微信公众号发布（草稿创建、发布、状态轮询）。
"""

import re
import time
import subprocess
from pathlib import Path

from .config import CONFIG_DIR, load_config, get_deploy_config, get_hugo_config, get_wechat_config


def resolve_blog_root(deploy_config: dict) -> Path:
    """解析博客根目录路径

    blog_root 可以是相对于配置文件的路径或绝对路径。
    """
    blog_root = deploy_config.get("blog_root", "../..")
    path = Path(blog_root)
    if not path.is_absolute():
        path = (CONFIG_DIR / path).resolve()
    return path


def hugo_build(blog_root: Path, hugo_bin: str = "", output_dir: str = "public") -> Path:
    """执行 Hugo 构建

    Returns:
        构建输出目录的绝对路径

    Raises:
        subprocess.CalledProcessError: Hugo 构建失败
        FileNotFoundError: Hugo 可执行文件未找到
    """
    hugo_cmd = hugo_bin or "hugo"
    dest = blog_root / output_dir
    cmd = [hugo_cmd, "-d", str(dest)]

    result = subprocess.run(
        cmd,
        cwd=str(blog_root),
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return dest


def rsync_to_remote(
    source_dir: Path,
    remote_host: str,
    remote_user: str,
    webroot: str,
    ssh_key: str = "",
    dry_run: bool = False,
) -> subprocess.CompletedProcess:
    """通过 rsync 将本地目录同步到远程服务器

    Raises:
        subprocess.CalledProcessError: rsync 失败
    """
    # 确保 source 以 / 结尾（rsync 语义：同步目录内容而非目录本身）
    source = Path(source_dir).as_posix().rstrip("/") + "/"
    dest = f"{remote_user}@{remote_host}:{webroot}"

    cmd = ["rsync", "-avz", "--delete"]

    if ssh_key:
        cmd.extend(["-e", f"ssh -i {ssh_key}"])

    if dry_run:
        cmd.append("--dry-run")

    cmd.extend([source, dest])

    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if result.returncode != 0:
        raise subprocess.CalledProcessError(
            result.returncode, cmd,
            output=result.stdout,
            stderr=result.stderr,
        )
    return result


def deploy_blog(dry_run: bool = False) -> dict:
    """完整部署流程：Hugo 构建 + rsync 到远程

    Returns:
        {"build_dir": Path, "rsync_result": CompletedProcess}
    """
    config = load_config()
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    hugo_bin = deploy_conf.get("hugo_bin", "")
    output_dir = deploy_conf.get("output_dir", "public")

    build_dir = hugo_build(blog_root, hugo_bin=hugo_bin, output_dir=output_dir)

    rsync_result = rsync_to_remote(
        source_dir=build_dir,
        remote_host=deploy_conf["remote_host"],
        remote_user=deploy_conf.get("remote_user", "root"),
        webroot=deploy_conf["webroot"],
        ssh_key=deploy_conf.get("ssh_key", ""),
        dry_run=dry_run,
    )

    return {"build_dir": build_dir, "rsync_result": rsync_result}


def deploy_wechat(
    postid: int,
    account: str | None = None,
    publish: bool = False,
    poll_interval: int = 5,
    poll_timeout: int = 120,
) -> dict:
    """将 Hugo 文章发布到微信公众号

    完整流程：
    1. 解析 Hugo 文章
    2. 转换为 WechatArticle
    3. 上传正文图片（替换本地路径为微信 URL）
    4. 上传封面图（设置 thumb_media_id）
    5. 创建草稿
    6. （可选）发布草稿并轮询状态
    7. 写回元数据到 Hugo frontmatter 和 Joplin frontmatter

    Args:
        postid: Hugo 文章 ID
        account: 微信账号名称（None 使用默认）
        publish: 是否在创建草稿后立即发布
        poll_interval: 发布状态轮询间隔（秒）
        poll_timeout: 发布状态轮询超时（秒）

    Returns:
        {"article", "media_id", "account_name", "publish_id", "article_url", "status"}
    """
    from .hugo import parse_post, write_post
    from .converter import hugo_to_wechat
    from .wechat import WechatClient

    config = load_config()
    hugo_conf = get_hugo_config(config)
    wechat_conf = get_wechat_config(config, account=account)
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    content_dir = blog_root / hugo_conf.get("content_dir", "content")
    static_dir = blog_root / "static"
    blog_url = hugo_conf.get("blog_url", "https://blog.zengrong.net")

    post_file = content_dir / "post" / f"{postid}.md"
    post = parse_post(post_file)
    article = hugo_to_wechat(
        post,
        author=hugo_conf.get("author", "曾嵘"),
        content_dir=content_dir,
        wechat_account=wechat_conf["account_name"],
    )

    account_name = wechat_conf["account_name"]

    with WechatClient(
        appid=wechat_conf["appid"],
        appsecret=wechat_conf["appsecret"],
        access_token=wechat_conf.get("access_token", ""),
    ) as client:
        # 上传正文图片
        article = _upload_wechat_images(article, client, static_dir, blog_url)

        # 上传封面图
        cover_path = _resolve_cover_image(post, static_dir)
        if cover_path:
            media_id = client.upload_thumb(cover_path)
            article.thumb_media_id = media_id
        else:
            print("警告：未找到封面图，草稿可能创建失败（thumb_media_id 为空）")

        # 检查是否已有草稿（从 Hugo frontmatter 中读取 media_id）
        existing_media_id = None
        wechat_meta = post.extra.get("wechat", {})
        if isinstance(wechat_meta, dict):
            acct_meta = wechat_meta.get(account_name, {})
            if isinstance(acct_meta, dict) and acct_meta.get("status") == "draft":
                existing_media_id = acct_meta.get("media_id")

        if existing_media_id:
            # 更新已有草稿
            client.update_draft(existing_media_id, article)
            draft_media_id = existing_media_id
            print(f"已更新草稿: {draft_media_id}")
        else:
            # 创建新草稿
            draft_media_id = client.add_draft([article])
            print(f"已创建草稿: {draft_media_id}")

        result = {
            "article": article,
            "media_id": draft_media_id,
            "account_name": account_name,
            "publish_id": None,
            "article_url": None,
            "status": "draft",
        }

        # 写回 draft 状态
        _write_wechat_metadata(
            post, account_name, status="draft", media_id=draft_media_id,
        )

        if not publish:
            return result

        # 发布草稿
        publish_id = client.publish_draft(draft_media_id)
        result["publish_id"] = publish_id
        result["status"] = "publishing"

        # 轮询发布状态
        article_url = _poll_publish_status(
            client, publish_id, poll_interval, poll_timeout,
        )

        if article_url:
            result["article_url"] = article_url
            result["status"] = "published"
            _write_wechat_metadata(
                post, account_name, status="published",
                article_url=article_url, media_id=draft_media_id,
            )
            # 在 Joplin 上打 mp:xxx 标签
            _tag_joplin_mp(post, account_name)
        else:
            result["status"] = "failed"
            _write_wechat_metadata(
                post, account_name, status="failed", media_id=draft_media_id,
            )

    return result


def publish_wechat_draft(
    media_id: str,
    account: str | None = None,
    postid: int | None = None,
    poll_interval: int = 5,
    poll_timeout: int = 120,
) -> dict:
    """发布已有的微信草稿

    用于先创建草稿、确认后发布的场景。

    Args:
        media_id: 草稿 media_id
        account: 微信账号名称
        postid: Hugo 文章 ID（用于写回 URL，可选）

    Returns:
        {"publish_id", "article_url", "account_name", "status"}
    """
    from .hugo import parse_post
    from .wechat import WechatClient

    config = load_config()
    wechat_conf = get_wechat_config(config, account=account)
    account_name = wechat_conf["account_name"]

    with WechatClient(
        appid=wechat_conf["appid"],
        appsecret=wechat_conf["appsecret"],
        access_token=wechat_conf.get("access_token", ""),
    ) as client:
        publish_id = client.publish_draft(media_id)
        article_url = _poll_publish_status(
            client, publish_id, poll_interval, poll_timeout,
        )

    result = {
        "publish_id": publish_id,
        "article_url": article_url,
        "account_name": account_name,
        "status": "published" if article_url else "failed",
    }

    # 写回 URL 到 Hugo frontmatter
    if postid:
        hugo_conf = get_hugo_config(config)
        deploy_conf = get_deploy_config(config)
        blog_root = resolve_blog_root(deploy_conf)
        content_dir = blog_root / hugo_conf.get("content_dir", "content")
        post_file = content_dir / "post" / f"{postid}.md"
        if post_file.exists():
            post = parse_post(post_file)
            status = "published" if article_url else "failed"
            _write_wechat_metadata(
                post, account_name, status=status,
                article_url=article_url, media_id=media_id,
            )
            if article_url:
                _tag_joplin_mp(post, account_name)

    return result


def _upload_wechat_images(article, client, static_dir: Path, blog_url: str):
    """上传微信文章正文中的本地图片，替换为微信 URL

    处理 HTML content 中的 src="/uploads/..." 引用。
    文件 >1MB 或上传失败时 fallback 到公网 URL。
    """
    import copy
    result = copy.copy(article)
    content = result.content

    pattern = re.compile(r'src="(/uploads/[^"]+)"')
    matches = list(pattern.finditer(content))
    if not matches:
        # 移除 hugo_to_wechat 添加的注释
        content = re.sub(r'\n<!-- 需要上传的本地图片:.*?-->', '', content)
        result.content = content
        return result

    for match in matches:
        local_path = match.group(1)
        file_path = static_dir / local_path.lstrip("/")

        if file_path.exists() and file_path.stat().st_size < 1_000_000:
            try:
                data = client.upload_image(file_path)
                wechat_url = data["url"]
                content = content.replace(
                    f'src="{local_path}"',
                    f'src="{wechat_url}"',
                )
                continue
            except Exception as e:
                print(f"警告：上传图片失败 {local_path}: {e}，使用公网 URL")

        # fallback: 使用公网 URL
        public_url = f"{blog_url}{local_path}"
        content = content.replace(
            f'src="{local_path}"',
            f'src="{public_url}"',
        )

    # 移除注释
    content = re.sub(r'\n<!-- 需要上传的本地图片:.*?-->', '', content)
    result.content = content
    return result


def _resolve_cover_image(post, static_dir: Path) -> Path | None:
    """解析文章封面图的本地路径

    优先使用 featureImage，回退到正文第一张图。
    """
    cover_src = post.featureImage or post.thumbnail
    if not cover_src:
        match = re.search(r'!\[[^\]]*\]\((/uploads/[^)]+)\)', post.body)
        if match:
            cover_src = match.group(1)

    if cover_src and cover_src.startswith("/uploads/"):
        cover_path = static_dir / cover_src.lstrip("/")
        if cover_path.exists():
            return cover_path

    return None


def _poll_publish_status(
    client,
    publish_id: str,
    interval: int = 5,
    timeout: int = 120,
) -> str | None:
    """轮询微信发布状态，返回文章永久 URL 或 None

    publish_status: 0=成功, 1=发布中, 2=原创失败, 3=失败, 4=审核拒绝
    """
    elapsed = 0
    while elapsed < timeout:
        time.sleep(interval)
        elapsed += interval

        status_data = client.get_publish_status(publish_id)
        publish_status = status_data.get("publish_status", -1)

        if publish_status == 0:
            article_detail = status_data.get("article_detail", {})
            items = article_detail.get("item", [])
            if items:
                return items[0].get("article_url", "")
            return ""

        if publish_status in (2, 3, 4):
            print(f"发布失败：publish_status={publish_status}")
            return None

        # publish_status == 1，继续等待
        print(f"发布中...已等待 {elapsed}s")

    print(f"发布超时（{timeout}s），请手动查询 publish_id={publish_id}")
    return None


def _write_wechat_metadata(
    post,
    account_name: str,
    status: str,
    article_url: str | None = None,
    media_id: str | None = None,
) -> None:
    """写回微信元数据到 Hugo frontmatter 和 Joplin frontmatter

    Hugo: post.extra["wechat"][account_name] = {status, url, media_id}
    Joplin: 笔记 body 顶部 frontmatter 中同步更新 wechat 字段
    """
    from .hugo import parse_post, write_post
    from .converter import parse_joplin_frontmatter, write_joplin_frontmatter, _deep_merge

    # 构建 wechat 元数据
    wechat_data = {"status": status}
    if article_url:
        wechat_data["url"] = article_url
    if media_id:
        wechat_data["media_id"] = media_id

    # 写入 Hugo frontmatter
    wechat = post.extra.get("wechat", {})
    if account_name in wechat and isinstance(wechat[account_name], dict):
        wechat[account_name] = _deep_merge(wechat[account_name], wechat_data)
    else:
        wechat[account_name] = wechat_data
    post.extra["wechat"] = wechat

    if post.source_path:
        write_post(post)

    # 同步到 Joplin frontmatter
    joplin_id = post.extra.get("joplin_id")
    if not joplin_id:
        return

    try:
        from .config import get_joplin_config
        from .joplin import JoplinClient

        joplin_conf = get_joplin_config()
        with JoplinClient(
            token=joplin_conf["token"],
            base_url=joplin_conf.get("base_url", "http://localhost:41184"),
        ) as client:
            if not client.ping():
                return
            note = client.get_note(joplin_id)
            joplin_fm, joplin_body = parse_joplin_frontmatter(note.body)

            # 合并 wechat 字段
            joplin_wechat = joplin_fm.get("wechat", {})
            if account_name in joplin_wechat and isinstance(joplin_wechat[account_name], dict):
                joplin_wechat[account_name] = _deep_merge(
                    joplin_wechat[account_name], wechat_data,
                )
            else:
                joplin_wechat[account_name] = wechat_data
            joplin_fm["wechat"] = joplin_wechat

            new_body = write_joplin_frontmatter(joplin_fm, joplin_body)
            client.update_note(note.id, body=new_body)
    except Exception as e:
        print(f"警告：同步微信元数据到 Joplin 失败: {e}")


def _tag_joplin_mp(post, account_name: str) -> None:
    """在 Joplin 笔记上打 mp:xxx 标签"""
    joplin_id = post.extra.get("joplin_id")
    if not joplin_id:
        return

    try:
        from .config import get_joplin_config
        from .joplin import JoplinClient

        joplin_conf = get_joplin_config()
        with JoplinClient(
            token=joplin_conf["token"],
            base_url=joplin_conf.get("base_url", "http://localhost:41184"),
        ) as client:
            if not client.ping():
                return
            # 获取现有标签，添加 mp:xxx
            existing_tags = client.get_note_tags(joplin_id)
            tag_titles = [t["title"] for t in existing_tags]
            mp_tag = f"mp:{account_name}"
            if mp_tag not in tag_titles:
                tag_titles.append(mp_tag)
                client.set_note_tags(joplin_id, tag_titles)
    except Exception as e:
        print(f"警告：添加 Joplin 标签 mp:{account_name} 失败: {e}")


def deploy_zhihu(postid: int) -> str:
    """将 Hugo 文章转为知乎格式

    Returns:
        格式化后的文本（适合复制粘贴到知乎）
    """
    from .hugo import parse_post
    from .converter import hugo_to_zhihu
    from .zhihu import format_for_clipboard

    config = load_config()
    hugo_conf = get_hugo_config(config)
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    content_dir = blog_root / hugo_conf.get("content_dir", "content")

    post_file = content_dir / "post" / f"{postid}.md"
    post = parse_post(post_file)
    zhihu_article = hugo_to_zhihu(post)
    return format_for_clipboard(zhihu_article)
