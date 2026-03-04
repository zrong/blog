"""各平台间内容格式转换核心逻辑

支持的转换路径：
- Hugo -> Joplin（博客文章同步到笔记）
- Joplin -> Hugo（笔记发布为博客文章）
- Hugo/Joplin -> 微信公众号（Markdown -> HTML）
- Hugo/Joplin -> 知乎格式（Markdown 清理）
"""

import re
import unicodedata
from pathlib import Path

import markdown

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import tomli_w

from .hugo import HugoPost, parse_post, write_post, next_postid, search_posts
from .joplin import JoplinClient, JoplinNote
from .wechat import WechatArticle
from .zhihu import convert_to_zhihu, ZhihuArticle

# 标签前缀
CATEGORY_TAG_PREFIX = "blog:category:"
MP_TAG_PREFIX = "mp:"

# Joplin frontmatter 中需要与 Hugo 同步的共享字段
_SHARED_FRONTMATTER_KEYS = {"wechat", "postid", "slug"}


# Markdown -> HTML 扩展配置
MD_EXTENSIONS = [
    'markdown.extensions.fenced_code',
    'markdown.extensions.codehilite',
    'markdown.extensions.tables',
    'markdown.extensions.toc',
    'markdown.extensions.nl2br',
]

MD_EXTENSION_CONFIGS = {
    'codehilite': {
        'css_class': 'highlight',
        'linenums': False,
    },
}

# 微信公众号文章的 CSS 样式
WECHAT_STYLE = """
<style>
h1, h2, h3 { color: #333; font-weight: bold; }
h2 { border-bottom: 1px solid #eee; padding-bottom: 8px; }
p { line-height: 1.8; margin: 10px 0; }
code { background: #f5f5f5; padding: 2px 6px; border-radius: 3px; font-size: 14px; color: #c7254e; }
pre { background: #f5f5f5; padding: 16px; border-radius: 4px; overflow-x: auto; }
pre code { background: none; padding: 0; color: inherit; }
blockquote { border-left: 4px solid #ddd; padding: 8px 16px; color: #666; margin: 10px 0; }
img { max-width: 100%; }
table { border-collapse: collapse; width: 100%; }
th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
th { background: #f5f5f5; }
</style>
"""


def markdown_to_html(md_text: str) -> str:
    """将 Markdown 转为 HTML"""
    # 移除 Hugo <!--more--> 标记
    md_text = md_text.replace("<!--more-->", "")
    return markdown.markdown(
        md_text,
        extensions=MD_EXTENSIONS,
        extension_configs=MD_EXTENSION_CONFIGS,
    )


def parse_joplin_frontmatter(body: str) -> tuple[dict, str]:
    """从 Joplin 笔记 body 中提取 TOML frontmatter

    格式与 Hugo 相同：+++ 包裹的 TOML 块。

    Returns:
        (frontmatter_dict, body_without_frontmatter)
    """
    match = re.match(r'^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n?', body, re.DOTALL)
    if not match:
        return {}, body
    fm_text = match.group(1)
    body_content = body[match.end():]
    try:
        fm = tomllib.loads(fm_text)
    except Exception:
        # frontmatter 解析失败时当作普通内容
        return {}, body
    return fm, body_content.lstrip("\n")


def write_joplin_frontmatter(fm: dict, body: str) -> str:
    """将 TOML frontmatter 写入 Joplin 笔记 body 顶部

    如果 fm 为空则直接返回 body。

    Returns:
        带 frontmatter 的完整 body
    """
    if not fm:
        return body
    fm_str = tomli_w.dumps(fm)
    return f"+++\n{fm_str}+++\n\n{body}"


def _deep_merge(base: dict, override: dict) -> dict:
    """深度合并两个字典，override 的值优先

    嵌套的 dict 递归合并，其他类型直接覆盖。
    """
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def hugo_to_joplin(
    post: HugoPost,
    client: JoplinClient,
    notebook_path: str = "Thought/Writing/Blog",
    static_dir: Path | None = None,
) -> JoplinNote:
    """Hugo 文章 -> Joplin 笔记

    转换规则：
    - Hugo category -> Joplin 标签 `blog:category:xxx`
    - Hugo tag -> Joplin 标签（直接对应）
    - 笔记本按 `/` 分隔路径嵌套创建
    - 图片上传为 Joplin 资源（带 blog: 前缀去重）
    - 创建新笔记后将 joplin_id 写回 Hugo frontmatter

    Args:
        post: Hugo 文章
        client: Joplin 客户端
        notebook_path: 目标笔记本路径（如 "Thought/Writing/Blog"）
        static_dir: Hugo static 目录（用于定位图片文件）

    Returns:
        创建/更新的 Joplin 笔记
    """
    nb = client.resolve_notebook_path(notebook_path)

    source_url = ""
    if post.slug:
        source_url = f"https://blog.zengrong.net/post/{post.slug}/"

    # 构建 Joplin 标签列表
    joplin_tags = [f"{CATEGORY_TAG_PREFIX}{cat}" for cat in post.category]
    joplin_tags.extend(post.tag)

    from datetime import datetime, timezone

    # 构建 Joplin frontmatter（从 Hugo 共享字段）
    hugo_shared_fm = {"postid": post.postid, "slug": post.slug}
    for key in _SHARED_FRONTMATTER_KEYS:
        if key in post.extra:
            hugo_shared_fm[key] = post.extra[key]

    # 检查是否已存在同名笔记（通过 source_url 匹配）
    if source_url:
        existing = client.search_notes(post.title, limit=5)
        for note in existing:
            if note.source_url == source_url:
                body = post.body_without_more
                if post.source_path:
                    body = _convert_relref_to_joplin(body, post.source_path.parent.parent)
                if static_dir:
                    body = _upload_hugo_images(body, client, static_dir, note_id=note.id)
                # 合并 Joplin 已有 frontmatter（Hugo 方向为准）
                existing_fm, _ = parse_joplin_frontmatter(note.body)
                merged_fm = _deep_merge(existing_fm, hugo_shared_fm)
                body = write_joplin_frontmatter(merged_fm, body)
                client.update_note(
                    note.id,
                    title=post.title,
                    body=body,
                )
                client.set_note_tags(note.id, joplin_tags)
                # 更新 Hugo lastmod 为当前时间
                post.lastmod = datetime.now(tz=timezone.utc).astimezone().isoformat()
                if post.source_path:
                    write_post(post)
                return client.get_note(note.id)

    body = post.body_without_more
    if post.source_path:
        body = _convert_relref_to_joplin(body, post.source_path.parent.parent)
    if static_dir:
        body = _upload_hugo_images(body, client, static_dir)
    # 写入 Joplin frontmatter
    body = write_joplin_frontmatter(hugo_shared_fm, body)

    note = client.create_note(
        title=post.title,
        body=body,
        parent_id=nb.id,
        source_url=source_url,
    )
    client.set_note_tags(note.id, joplin_tags)

    # 写回 joplin_id 和 lastmod 到 Hugo frontmatter
    post.extra["joplin_id"] = note.id
    post.lastmod = datetime.now(tz=timezone.utc).astimezone().isoformat()
    if post.source_path:
        write_post(post)

    return note


def joplin_to_hugo(
    note: JoplinNote,
    content_dir: Path,
    client: JoplinClient,
    static_dir: Path,
    slug: str,
) -> HugoPost:
    """Joplin 笔记 -> Hugo 文章

    转换规则：
    - Joplin 标签 `blog:category:xxx` -> Hugo category
    - 其余 Joplin 标签 -> Hugo tag
    - 图片资源下载到 static/uploads/{year}/{slug}-{n}.{ext}
    - slug 由调用方传入（Claude 生成英文翻译）

    Args:
        note: Joplin 笔记
        content_dir: Hugo content 目录
        client: Joplin 客户端（读取标签和下载资源）
        static_dir: Hugo static 目录（保存图片）
        slug: URL slug（由 Claude 生成，≤50 字符）

    Returns:
        创建的 HugoPost
    """
    from datetime import datetime, timezone

    slug = _slugify(slug)
    created = datetime.fromtimestamp(note.created_time / 1000, tz=timezone.utc).astimezone()
    year = str(created.year)

    # 从 Joplin 标签还原 category 和 tag
    joplin_tags = client.get_note_tags(note.id)
    category = []
    tag = []
    for t in joplin_tags:
        title = t["title"]
        if title.startswith(CATEGORY_TAG_PREFIX):
            category.append(title[len(CATEGORY_TAG_PREFIX):])
        else:
            tag.append(title)

    if not category:
        category = ["technology"]

    # 过滤掉 mp: 标签（微信公众号标记，不同步到 Hugo）
    tag = [t for t in tag if not t.startswith(MP_TAG_PREFIX)]

    # 解析并剥离 Joplin frontmatter
    joplin_fm, note_body = parse_joplin_frontmatter(note.body)

    # 处理图片和链接（在无 frontmatter 的 body 上）
    body = _extract_joplin_images(note_body, client, static_dir, year, slug)
    body = _convert_joplin_links_to_relref(body, content_dir)

    # 计算 lastmod（Joplin updated_time → ISO 字符串）
    updated = datetime.fromtimestamp(note.updated_time / 1000, tz=timezone.utc).astimezone()
    lastmod_str = updated.isoformat()

    # 从 Joplin frontmatter 提取共享字段，合并到 Hugo extra
    shared_from_joplin = {}
    for key in _SHARED_FRONTMATTER_KEYS:
        if key in joplin_fm:
            shared_from_joplin[key] = joplin_fm[key]

    # 查找已有文章（通过 joplin_id 匹配），更新而非创建
    existing = _find_post_by_joplin_id(content_dir, note.id)
    if existing:
        existing.title = note.title
        existing.category = category
        existing.tag = tag
        existing.body = body
        existing.lastmod = lastmod_str
        # 合并 Joplin frontmatter 共享字段（Joplin 方向为准）
        existing.extra = _deep_merge(existing.extra, shared_from_joplin)
        _auto_feature_image(existing)
        write_post(existing)
        post = existing
    else:
        # 创建新文章
        postid = next_postid(content_dir)
        extra = {"joplin_id": note.id}
        extra.update(shared_from_joplin)
        post = HugoPost(
            title=note.title,
            postid=postid,
            date=created.isoformat(),
            lastmod=lastmod_str,
            slug=slug,
            isCJKLanguage=True,
            toc=True,
            type="post",
            category=category,
            tag=tag,
            aliases=[f"/post/{postid}.html"],
            body=body,
            extra=extra,
        )
        _auto_feature_image(post)

        file_path = content_dir / "post" / f"{postid}.md"
        write_post(post, file_path)

    # 将 Hugo frontmatter 回写到 Joplin 笔记
    source_url = f"https://blog.zengrong.net/post/{post.slug}/"
    if note.source_url != source_url:
        client.update_note(note.id, source_url=source_url)
    # 同步标签到 Joplin（category → blog:category:xxx，tag 直接对应）
    joplin_tags = [f"{CATEGORY_TAG_PREFIX}{cat}" for cat in post.category]
    joplin_tags.extend(post.tag)
    client.set_note_tags(note.id, joplin_tags)

    return post


def _slugify(text: str, max_length: int = 50) -> str:
    """清理并格式化 slug

    小写、移除非字母数字字符、空格转连字符、截断到 max_length 字符（单词边界）。
    """
    # NFD 分解后去掉组合字符
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = text.lower()
    # 非字母数字替换为空格
    text = re.sub(r"[^a-z0-9]+", " ", text).strip()
    # 空格转连字符
    text = re.sub(r"\s+", "-", text)
    # 截断到 max_length，尽量在单词边界
    if len(text) > max_length:
        text = text[:max_length]
        last_dash = text.rfind("-")
        if last_dash > max_length // 2:
            text = text[:last_dash]
    return text.strip("-")


def _auto_feature_image(post: HugoPost) -> None:
    """从正文提取第一张图片路径，自动填充 featureImage 和 thumbnail（仅当为空时）"""
    match = re.search(r"!\[[^\]]*\]\(([^)]+)\)", post.body)
    if not match:
        return
    img_path = match.group(1)
    if not post.featureImage:
        post.featureImage = img_path
    if not post.thumbnail:
        post.thumbnail = img_path


def _find_post_by_joplin_id(content_dir: Path, joplin_id: str) -> HugoPost | None:
    """扫描 content/post/ 查找 extra["joplin_id"] 匹配的文章"""
    for f in (content_dir / "post").glob("*.md"):
        try:
            post = parse_post(f)
            if post.extra.get("joplin_id") == joplin_id:
                return post
        except (ValueError, KeyError):
            pass
    return None


def _convert_relref_to_joplin(body: str, content_dir: Path) -> str:
    """将 Hugo relref 链接转换为 Joplin 内部链接

    [text]({{< relref "post/2849.md" >}}) → [text](:/joplin_id)

    找不到 joplin_id 时打印警告并保留原始链接。
    """
    pattern = re.compile(r'\[([^\]]*)\]\({{<\s*relref\s+"post/(\d+)\.md"\s*>}}\)')
    matches = list(pattern.finditer(body))
    if not matches:
        return body

    for match in matches:
        text = match.group(1)
        postid = match.group(2)
        post_file = content_dir / "post" / f"{postid}.md"
        if not post_file.exists():
            print(f"警告：relref 目标文章不存在: post/{postid}.md，保留原始链接")
            continue
        try:
            target_post = parse_post(post_file)
            joplin_id = target_post.extra.get("joplin_id")
            if joplin_id:
                body = body.replace(match.group(0), f"[{text}](:/{joplin_id})")
            else:
                print(f"警告：post/{postid}.md 没有 joplin_id，保留原始链接")
        except (ValueError, KeyError) as e:
            print(f"警告：解析 post/{postid}.md 失败: {e}，保留原始链接")

    return body


def _convert_joplin_links_to_relref(body: str, content_dir: Path) -> str:
    """将 Joplin 内部链接转换为 Hugo relref

    [text](:/note_id) → [text]({{< relref "post/2849.md" >}})

    仅处理非图片链接（不以 ! 开头）。
    找不到对应 Hugo 文章时打印警告并保留原始链接。
    """
    # 负向回顾断言排除图片链接 ![alt](:/id)
    pattern = re.compile(r'(?<!!)\[([^\]]*)\]\(:/([\w]+)\)')
    matches = list(pattern.finditer(body))
    if not matches:
        return body

    # 构建 joplin_id → postid 映射（一次扫描，避免重复遍历）
    joplin_id_map = {}
    for f in (content_dir / "post").glob("*.md"):
        try:
            post = parse_post(f)
            jid = post.extra.get("joplin_id")
            if jid:
                joplin_id_map[jid] = post.postid
        except (ValueError, KeyError):
            pass

    for match in matches:
        text = match.group(1)
        note_id = match.group(2)
        if note_id in joplin_id_map:
            postid = joplin_id_map[note_id]
            relref = f'[{text}]({{{{< relref "post/{postid}.md" >}}}})'
            body = body.replace(match.group(0), relref)
        else:
            print(f"警告：找不到 joplin_id={note_id} 对应的 Hugo 文章，保留原始链接")

    return body


def _upload_hugo_images(body, client, static_dir, note_id=None):
    """将 Hugo 图片上传为 Joplin 资源，返回替换后的 body

    去重机制：资源 title 设为 blog:/uploads/... 前缀，
    更新已有笔记时通过 get_note_resources() 匹配跳过已上传的。
    """
    pattern = re.compile(r"!\[([^\]]*)\]\((/uploads/[^\)]+)\)")
    matches = list(pattern.finditer(body))
    if not matches:
        return body

    # 构建已有资源的 title→id 索引
    existing = {}
    if note_id:
        for r in client.get_note_resources(note_id):
            existing[r["title"]] = r["id"]

    for match in matches:
        img_path = match.group(2)               # /uploads/2024/slug-1.png
        resource_title = f"blog:{img_path}"     # blog:/uploads/2024/slug-1.png

        if resource_title in existing:
            resource_id = existing[resource_title]
        else:
            file_path = static_dir / img_path.lstrip("/")
            if not file_path.exists():
                continue
            resource = client.upload_resource(file_path, title=resource_title)
            resource_id = resource["id"]

        body = body.replace(match.group(0), f"![{match.group(1)}](:/{resource_id})")

    return body


def _extract_joplin_images(
    body: str,
    client: JoplinClient,
    static_dir: Path,
    year: str,
    slug: str,
) -> str:
    """提取 Joplin 笔记中的图片资源并保存到本地

    匹配 `![alt](:/resource_id)` 格式，下载并替换为 Hugo 本地路径。

    Args:
        body: 笔记 Markdown 内容
        client: Joplin 客户端
        static_dir: Hugo static 目录
        year: 年份字符串
        slug: 文章 slug

    Returns:
        替换图片路径后的 Markdown 内容
    """
    pattern = re.compile(r"!\[([^\]]*)\]\(:/([\w]+)\)")
    matches = list(pattern.finditer(body))
    if not matches:
        return body

    uploads_dir = static_dir / "uploads" / year
    uploads_dir.mkdir(parents=True, exist_ok=True)

    counter = 0
    for match in matches:
        alt = match.group(1)
        resource_id = match.group(2)
        counter += 1
        try:
            meta = client.get_resource(resource_id)
            resource_title = meta.get("title", "")

            # 来自 Hugo 的图片（blog: 前缀），使用原始路径
            if resource_title.startswith("blog:"):
                hugo_path = resource_title[len("blog:"):]
                body = body.replace(match.group(0), f"![{alt}]({hugo_path})")
                continue

            ext = meta.get("file_extension", "")
            if ext and not ext.startswith("."):
                ext = f".{ext}"
            if not ext:
                # 从 mime 类型推测
                mime = meta.get("mime", "")
                ext_map = {
                    "image/png": ".png",
                    "image/jpeg": ".jpg",
                    "image/gif": ".gif",
                    "image/webp": ".webp",
                    "image/svg+xml": ".svg",
                }
                ext = ext_map.get(mime, ".bin")

            file_data = client.get_resource_file(resource_id)
            filename = f"{slug}-{counter}{ext}"
            save_path = uploads_dir / filename
            save_path.write_bytes(file_data)

            hugo_path = f"/uploads/{year}/{filename}"
            body = body.replace(match.group(0), f"![{alt}]({hugo_path})")
        except Exception:
            # 资源不可用时保留原始引用
            pass

    return body


def hugo_to_wechat(
    post: HugoPost,
    author: str = "zrong",
) -> WechatArticle:
    """Hugo 文章 -> 微信公众号文章

    Args:
        post: Hugo 文章
        author: 作者名

    Returns:
        WechatArticle（content 为 HTML）
    """
    html_content = markdown_to_html(post.body)

    # 加上样式
    styled_html = WECHAT_STYLE + html_content

    # 处理本地图片路径 -> 需要先上传再替换
    # 这里标记出需要上传的图片，由调用方处理
    local_imgs = re.findall(r'src="(/uploads/[^"]+)"', styled_html)
    if local_imgs:
        styled_html += f"\n<!-- 需要上传的本地图片: {', '.join(local_imgs)} -->"

    source_url = ""
    if post.slug:
        source_url = f"https://blog.zengrong.net/post/{post.slug}/"

    return WechatArticle(
        title=post.title,
        content=styled_html,
        author=author,
        digest=post.summary[:120],
        content_source_url=source_url,
    )


def hugo_to_zhihu(post: HugoPost) -> ZhihuArticle:
    """Hugo 文章 -> 知乎格式"""
    return convert_to_zhihu(
        title=post.title,
        body=post.body,
        tags=post.tag + post.category,
    )


def joplin_to_wechat(
    note: JoplinNote,
    author: str = "zrong",
) -> WechatArticle:
    """Joplin 笔记 -> 微信公众号文章"""
    _, body = parse_joplin_frontmatter(note.body)
    html_content = markdown_to_html(body)
    styled_html = WECHAT_STYLE + html_content

    return WechatArticle(
        title=note.title,
        content=styled_html,
        author=author,
        digest=body[:120],
        content_source_url=note.source_url,
    )


def joplin_to_zhihu(note: JoplinNote) -> ZhihuArticle:
    """Joplin 笔记 -> 知乎格式"""
    _, body = parse_joplin_frontmatter(note.body)
    return convert_to_zhihu(
        title=note.title,
        body=body,
    )


def sync_article(
    client: JoplinClient,
    content_dir: Path,
    static_dir: Path,
    title: str | None = None,
    postid: int | None = None,
    notebook_path: str = "Thought/Writing/Blog",
    slug: str | None = None,
) -> dict:
    """同步 Hugo 与 Joplin 之间的文章，支持 postid 或标题搜索

    自动判断同步方向：
    - 仅 Hugo 存在 → 同步到 Joplin
    - 仅 Joplin 存在 → 同步到 Hugo（需提供 slug）
    - 双方都有 → 比较更新时间，新→旧自动同步
    - 都没有 → 返回 not_found

    Args:
        client: Joplin 客户端
        content_dir: Hugo content 目录
        static_dir: Hugo static 目录
        title: 文章标题（用于搜索，与 postid 二选一）
        postid: Hugo 文章 postid（与 title 二选一）
        notebook_path: Joplin 目标笔记本路径
        slug: Joplin→Hugo 时需要提供的 URL slug

    Returns:
        {"action": str, "post": HugoPost | None, "note": JoplinNote | None}
    """
    from datetime import datetime, timezone

    if not title and not postid:
        raise ValueError("必须提供 title 或 postid 之一")

    # --- 搜索 Hugo ---
    hugo_post = None
    if postid:
        post_file = content_dir / "post" / f"{postid}.md"
        if post_file.exists():
            hugo_post = parse_post(post_file)
    if not hugo_post and title:
        hugo_posts = search_posts(content_dir, title)
        hugo_post = hugo_posts[0] if hugo_posts else None

    # --- 搜索 Joplin ---
    joplin_note = None
    # 优先通过 joplin_id 查找
    if hugo_post and hugo_post.extra.get("joplin_id"):
        try:
            joplin_note = client.get_note(hugo_post.extra["joplin_id"])
        except Exception:
            joplin_note = None

    # 回退到标题搜索
    if not joplin_note:
        search_title = title or (hugo_post.title if hugo_post else None)
        if search_title:
            joplin_results = client.search_notes(search_title, limit=10)
            for note in joplin_results:
                if note.title == search_title:
                    joplin_note = client.get_note(note.id)
                    break

    # --- 方向判断 ---
    if hugo_post and not joplin_note:
        # 仅 Hugo → 同步到 Joplin
        note = hugo_to_joplin(hugo_post, client, notebook_path, static_dir)
        return {"action": "hugo_to_joplin", "post": hugo_post, "note": note}

    if joplin_note and not hugo_post:
        # 仅 Joplin → 同步到 Hugo
        if not slug:
            raise ValueError("Joplin→Hugo 同步需要提供 slug 参数")
        post = joplin_to_hugo(joplin_note, content_dir, client, static_dir, slug)
        return {"action": "joplin_to_hugo", "post": post, "note": joplin_note}

    if hugo_post and joplin_note:
        # 双方都有 → 比较更新时间决定方向
        hugo_dt = datetime.fromisoformat(hugo_post.lastmod or hugo_post.date)
        # 确保 hugo_dt 有时区信息
        if hugo_dt.tzinfo is None:
            hugo_dt = hugo_dt.replace(tzinfo=timezone.utc)
        joplin_dt = datetime.fromtimestamp(
            joplin_note.updated_time / 1000, tz=timezone.utc
        )

        if hugo_dt > joplin_dt:
            # Hugo 更新 → hugo_to_joplin
            note = hugo_to_joplin(hugo_post, client, notebook_path, static_dir)
            return {"action": "hugo_to_joplin", "post": hugo_post, "note": note}
        elif joplin_dt > hugo_dt:
            # Joplin 更新 → joplin_to_hugo
            post_slug = slug or hugo_post.slug
            if not post_slug:
                raise ValueError("Joplin→Hugo 同步需要提供 slug 参数")
            post = joplin_to_hugo(
                joplin_note, content_dir, client, static_dir, post_slug
            )
            return {"action": "joplin_to_hugo", "post": post, "note": joplin_note}
        else:
            # 时间相同 → already_synced
            return {
                "action": "already_synced",
                "post": hugo_post,
                "note": joplin_note,
            }

    # 都没有
    return {"action": "not_found", "post": None, "note": None}
