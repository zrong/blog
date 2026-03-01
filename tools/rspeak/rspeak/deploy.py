"""博客部署模块

支持本地 Hugo 构建并通过 rsync 同步到远程服务器。
"""

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


def deploy_wechat(postid: int) -> dict:
    """将 Hugo 文章发布到微信公众号（创建草稿）

    Returns:
        {"article": WechatArticle, "media_id": str}
    """
    from .hugo import parse_post
    from .converter import hugo_to_wechat
    from .wechat import WechatClient

    config = load_config()
    hugo_conf = get_hugo_config(config)
    wechat_conf = get_wechat_config(config)
    deploy_conf = get_deploy_config(config)

    blog_root = resolve_blog_root(deploy_conf)
    content_dir = blog_root / hugo_conf.get("content_dir", "content")

    post_file = content_dir / "post" / f"{postid}.md"
    post = parse_post(post_file)
    article = hugo_to_wechat(post, author=hugo_conf.get("author", "zrong"))

    with WechatClient(
        appid=wechat_conf["appid"],
        appsecret=wechat_conf["appsecret"],
        access_token=wechat_conf.get("access_token", ""),
    ) as client:
        media_id = client.add_draft([article])

    return {"article": article, "media_id": media_id}


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
