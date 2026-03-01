"""知乎格式转换器

将 Markdown 文章转换为知乎兼容格式。
仅做格式转换，不进行自动发布（知乎无官方 API）。

知乎编辑器特点：
- 支持标准 Markdown 语法
- 图片需要手动上传（可生成占位提示）
- 代码块支持语法高亮
- 不支持 HTML 标签
- 支持数学公式（LaTeX）
"""

import re
from dataclasses import dataclass


@dataclass
class ZhihuArticle:
    """知乎文章格式"""
    title: str = ""
    content: str = ""  # 知乎兼容的 Markdown
    topic_tags: list = None  # 建议的知乎话题标签
    summary: str = ""  # 摘要（用于知乎文章简介）

    def __post_init__(self):
        if self.topic_tags is None:
            self.topic_tags = []


def convert_to_zhihu(title: str, body: str, tags: list = None) -> ZhihuArticle:
    """将标准 Markdown 转换为知乎兼容格式

    处理内容包括：
    - 移除 Hugo 特有标记（<!--more-->）
    - 处理本地图片路径为占位提示
    - 移除不支持的 HTML 标签
    - 保留标准 Markdown 语法

    Args:
        title: 文章标题
        body: Markdown 正文
        tags: 分类/标签列表

    Returns:
        ZhihuArticle 对象
    """
    content = body

    # 移除 Hugo <!--more--> 标记
    content = content.replace("<!--more-->", "")

    # 处理本地图片路径：/uploads/... -> 占位提示
    def _replace_local_img(match):
        alt = match.group(1)
        path = match.group(2)
        if path.startswith("/uploads/") or path.startswith("../"):
            return f"<!-- 【知乎发布】请手动上传图片：{alt or path} -->\n![{alt}](图片需手动上传)"
        return match.group(0)

    content = re.sub(r'!\[([^\]]*)\]\(([^)]+)\)', _replace_local_img, content)

    # 移除 HTML 注释（保留上面新加的占位注释）
    content = re.sub(r'<!--(?!.*知乎发布).*?-->', '', content)

    # 移除独立的 HTML 标签（知乎不支持）
    content = re.sub(r'<(?!img|br)[^>]+>', '', content)

    # 移除 ~~已删除~~ 的内容（知乎不支持删除线的情况可选保留）
    # 知乎实际上支持删除线，保留

    # 清理多余空行
    content = re.sub(r'\n{3,}', '\n\n', content)

    # 提取摘要
    summary = ""
    lines = content.strip().split("\n")
    for line in lines:
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("!") and not line.startswith("<!--"):
            summary = re.sub(r'[#*`\[\]()!]', '', line)[:150]
            break

    return ZhihuArticle(
        title=title,
        content=content.strip(),
        topic_tags=tags or [],
        summary=summary,
    )


def format_for_clipboard(article: ZhihuArticle) -> str:
    """生成适合复制粘贴到知乎的完整文本

    Returns:
        格式化后的文本，包含操作提示
    """
    parts = [
        f"# {article.title}",
        "",
    ]

    if article.topic_tags:
        parts.append(f"建议知乎话题标签：{', '.join(article.topic_tags)}")
        parts.append("")

    parts.append(article.content)

    if article.summary:
        parts.append("")
        parts.append(f"---")
        parts.append(f"知乎文章简介（建议）：{article.summary}")

    return "\n".join(parts)
