"""Hugo 博客文章解析与写入模块

解析 content/post/ 下的 markdown 文件，提取 TOML frontmatter 和正文内容。
"""

import re
from pathlib import Path
from dataclasses import dataclass, field

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import tomli_w


@dataclass
class HugoPost:
    """Hugo 博客文章数据结构"""
    title: str = ""
    postid: int = 0
    date: str = ""
    slug: str = ""
    description: str = ""
    draft: bool = False
    toc: bool = False
    isCJKLanguage: bool = True
    type: str = "post"
    category: list = field(default_factory=list)
    tag: list = field(default_factory=list)
    aliases: list = field(default_factory=list)
    thumbnail: str = ""
    lastmod: str = ""
    featureImage: str = ""
    body: str = ""
    # 保留原始 frontmatter 中的额外字段
    extra: dict = field(default_factory=dict)
    # 源文件路径
    source_path: Path | None = None

    @property
    def body_without_more(self) -> str:
        """去除 <!--more--> 标记的正文"""
        return self.body.replace("<!--more-->", "")

    @property
    def summary(self) -> str:
        """提取 <!--more--> 之前的摘要"""
        if "<!--more-->" in self.body:
            return self.body.split("<!--more-->")[0].strip()
        # 没有 more 标记时取前 200 字
        text = re.sub(r'[#*`\[\]()!]', '', self.body)
        return text[:200].strip()


# TOML frontmatter 中直接映射到 HugoPost 的已知字段
_KNOWN_FIELDS = {
    'title', 'postid', 'date', 'slug', 'description', 'draft',
    'toc', 'isCJKLanguage', 'type', 'category', 'tag', 'aliases',
    'thumbnail', 'lastmod', 'featureImage'
}


def parse_post(file_path: Path) -> HugoPost:
    """从 markdown 文件解析 Hugo 文章

    Args:
        file_path: markdown 文件路径

    Returns:
        HugoPost 数据对象
    """
    text = file_path.read_text(encoding='utf-8')

    # 提取 TOML frontmatter（+++ 包裹）
    match = re.match(r'^\+\+\+\s*\n(.*?)\n\+\+\+\s*\n', text, re.DOTALL)
    if not match:
        raise ValueError(f"无法解析 frontmatter: {file_path}")

    fm_text = match.group(1)
    body = text[match.end():]
    fm = tomllib.loads(fm_text)

    # 分离已知字段和额外字段
    known = {}
    extra = {}
    for k, v in fm.items():
        if k in _KNOWN_FIELDS:
            known[k] = v
        else:
            extra[k] = v

    # 处理 date / lastmod 字段：转为字符串
    for date_key in ('date', 'lastmod'):
        if date_key in known:
            date_val = known[date_key]
            if hasattr(date_val, 'isoformat'):
                known[date_key] = date_val.isoformat()
            else:
                known[date_key] = str(date_val)

    return HugoPost(
        **known,
        extra=extra,
        body=body.strip(),
        source_path=file_path,
    )


def write_post(post: HugoPost, file_path: Path | None = None) -> Path:
    """将 HugoPost 写入 markdown 文件

    Args:
        post: 文章数据
        file_path: 目标路径，为 None 时使用 source_path

    Returns:
        写入的文件路径
    """
    target = file_path or post.source_path
    if target is None:
        raise ValueError("未指定目标文件路径")

    # 构建 frontmatter dict
    fm = {}
    fm['title'] = post.title
    fm['postid'] = post.postid
    fm['date'] = post.date
    fm['isCJKLanguage'] = post.isCJKLanguage
    fm['toc'] = post.toc
    fm['type'] = post.type
    fm['slug'] = post.slug

    if post.description:
        fm['description'] = post.description
    if post.draft:
        fm['draft'] = post.draft
    if post.aliases:
        fm['aliases'] = post.aliases
    if post.thumbnail:
        fm['thumbnail'] = post.thumbnail
    if post.lastmod:
        fm['lastmod'] = post.lastmod
    if post.featureImage:
        fm['featureImage'] = post.featureImage

    fm['category'] = post.category
    fm['tag'] = post.tag

    # 合并额外字段
    fm.update(post.extra)

    fm_str = tomli_w.dumps(fm)
    content = f"+++\n{fm_str}+++\n\n{post.body}\n"

    target.write_text(content, encoding='utf-8')
    return target


def list_posts(content_dir: Path, limit: int = 0) -> list[HugoPost]:
    """列出所有博客文章，按 postid 降序排列

    Args:
        content_dir: content/post/ 目录路径
        limit: 返回数量限制，0 表示全部

    Returns:
        HugoPost 列表
    """
    post_dir = content_dir / "post"
    files = list(post_dir.glob("*.md"))
    files.sort(key=lambda f: int(f.stem) if f.stem.isdigit() else 0, reverse=True)

    if limit > 0:
        files = files[:limit]

    posts = []
    for f in files:
        try:
            posts.append(parse_post(f))
        except (ValueError, KeyError) as e:
            print(f"跳过 {f.name}: {e}")
    return posts


def search_posts(content_dir: Path, keyword: str) -> list[HugoPost]:
    """按关键词搜索博客文章

    两层搜索策略：
    1. 先遍历所有文章，对 title 做子串匹配
    2. 若标题无结果，回退到正文关键词搜索
    3. 两层结果合并去重，标题匹配排在前面

    Args:
        content_dir: content 目录路径（包含 post/ 子目录）
        keyword: 搜索关键词

    Returns:
        匹配的 HugoPost 列表（标题匹配优先）
    """
    post_dir = content_dir / "post"
    keyword_lower = keyword.lower()

    title_matches = []
    body_matches = []
    seen_paths = set()

    for f in post_dir.glob("*.md"):
        try:
            post = parse_post(f)
        except (ValueError, KeyError) as e:
            print(f"跳过 {f.name}: {e}")
            continue

        if keyword_lower in post.title.lower():
            title_matches.append(post)
            seen_paths.add(f)

    # 标题有结果时直接返回，无需回退到正文搜索
    if not title_matches:
        for f in post_dir.glob("*.md"):
            if f in seen_paths:
                continue
            try:
                post = parse_post(f)
            except (ValueError, KeyError):
                continue
            if keyword_lower in post.body.lower():
                body_matches.append(post)

    return title_matches + body_matches


def next_postid(content_dir: Path) -> int:
    """获取下一个可用的 postid"""
    post_dir = content_dir / "post"
    ids = []
    for f in post_dir.glob("*.md"):
        if f.stem.isdigit():
            ids.append(int(f.stem))
    return max(ids) + 1 if ids else 1
