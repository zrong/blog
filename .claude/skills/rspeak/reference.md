# 多平台发布 - 技术参考

## 配置文件格式

`tools/rspeak/config.toml`：

```toml
[joplin]
token = "你的 Joplin Web Clipper token"
base_url = "http://localhost:41184"
notebook_path = "Thought/Writing/Blog"

[wechat]
default_account = "main"

[wechat.accounts.main]
name = "主账号"
appid = "wx..."
appsecret = "..."

# 添加更多账号：
# [wechat.accounts.tech]
# name = "技术号"
# appid = "wx..."
# appsecret = "..."

[hugo]
content_dir = "content"
blog_url = "https://blog.zengrong.net"
author = "zrong"

[deploy]
blog_root = "../.."
output_dir = "public"
remote_host = ""
remote_user = "root"
webroot = "/srv/www/blog.zengrong.net"
```

### 微信多账号

`get_wechat_config(account=)` 支持新格式 `[wechat.accounts.xxx]` 和旧格式 `[wechat] appid=...`（向后兼容）。

```python
from rspeak.config import get_wechat_config, list_wechat_accounts

# 获取默认账号
conf = get_wechat_config()

# 获取指定账号
conf = get_wechat_config(account="tech")
# -> {"appid", "appsecret", "access_token", "account_name", "name"}

# 列出所有账号
accounts = list_wechat_accounts()
# -> [{"key": "main", "name": "主账号", "appid": "wx..."}, ...]
```

## CLI 命令

rspeak 提供 CLI 封装，通过 `uv run --project tools/rspeak rspeak <command>` 调用。

### 同步 Hugo ↔ Joplin

```bash
# 通过 postid 同步
uv run --project tools/rspeak rspeak sync -p 2850

# 通过标题搜索同步（Joplin→Hugo 时需提供 slug）
uv run --project tools/rspeak rspeak sync -t "文章标题" -s "english-slug"
```

### 部署博客

```bash
# Hugo 构建 + rsync 部署
uv run --project tools/rspeak rspeak deploy blog

# 模拟运行（不实际传输）
uv run --project tools/rspeak rspeak deploy blog --dry-run
```

### 发布到微信公众号

```bash
# 创建草稿（默认账号）
uv run --project tools/rspeak rspeak deploy wechat -p 2850

# 指定账号创建草稿
uv run --project tools/rspeak rspeak deploy wechat -p 2850 -a main

# 创建草稿 + 自动发布
uv run --project tools/rspeak rspeak deploy wechat -p 2850 -a main --publish

# 发布已有草稿
uv run --project tools/rspeak rspeak wechat-publish -m MEDIA_ID -p 2850 -a main

# 列出配置的微信账号
uv run --project tools/rspeak rspeak wechat-accounts
```

### 转知乎格式

```bash
# 输出到终端供复制粘贴
uv run --project tools/rspeak rspeak deploy zhihu -p 2850
```

### 校对文章（基础检查）

```bash
uv run --project tools/rspeak rspeak review -p 2850
```

> **注意**：`review` 命令只做基础格式检查（中英文空格、标点混用、多余空行）。完整校对（错别字、语义、风格）由 Claude 在 skill 工作流中完成。

## Python API 调用

需要更灵活控制时，通过 `uv run --project tools/rspeak python -c "..."` 调用 Python 模块。

> **重要**：在 Git Bash 环境中需添加 `sys.path.insert(0, 'tools/rspeak')`，并设置 UTF-8 输出：`sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`。

### 搜索 Joplin 笔记

```python
from rspeak.config import get_joplin_config
from rspeak.joplin import JoplinClient

conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    notes = client.search_notes("关键词", limit=10)
    for note in notes:
        print(f"ID: {note.id}  Title: {note.title}")
```

`search_notes` 返回 `list[JoplinNote]`，每个 `JoplinNote` 是 dataclass，通过属性访问字段（`note.id`、`note.title`、`note.source_url`），不是字典。

### Hugo -> Joplin

```python
from pathlib import Path
from rspeak.hugo import parse_post
from rspeak.config import get_joplin_config
from rspeak.joplin import JoplinClient
from rspeak.converter import hugo_to_joplin

post = parse_post(Path("content/post/{postid}.md"))
conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    note = hugo_to_joplin(post, client,
        notebook_path=conf.get("notebook_path", "Thought/Writing/Blog"),
        static_dir=Path("static"))
```

### Joplin -> Hugo

```python
from pathlib import Path
from rspeak.config import get_joplin_config
from rspeak.joplin import JoplinClient
from rspeak.converter import joplin_to_hugo

conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    note = client.get_note(note_id)
    # slug 由 Claude 根据笔记标题生成英文翻译（≤50 字符）
    post = joplin_to_hugo(
        note, Path("content"), client=client,
        static_dir=Path("static"), slug="my-english-slug",
    )
```

### 同步文章（自动判断方向）

通过标题搜索：

```python
from pathlib import Path
from rspeak.config import get_joplin_config
from rspeak.joplin import JoplinClient
from rspeak.converter import sync_article

conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    result = sync_article(
        client,
        content_dir=Path("content"),
        static_dir=Path("static"),
        title="文章标题",
        notebook_path=conf.get("notebook_path", "Thought/Writing/Blog"),
        slug="english-slug",  # 仅 Joplin→Hugo 时需要
    )
    print(result["action"])  # hugo_to_joplin | joplin_to_hugo | already_synced | not_found
```

通过 postid 搜索：

```python
conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    result = sync_article(
        client,
        content_dir=Path("content"),
        static_dir=Path("static"),
        postid=2842,
    )
    print(result["action"])
```

### Hugo -> 微信公众号（完整流程）

推荐使用 `deploy_wechat()` 高层函数，自动处理图片上传、封面、草稿、发布和元数据回写：

```python
from rspeak.deploy import deploy_wechat, publish_wechat_draft

# 创建草稿（默认账号）
result = deploy_wechat(postid=2850)
# -> {"media_id", "account_name", "article", "status": "draft"}

# 创建草稿 + 自动发布
result = deploy_wechat(postid=2850, account="main", publish=True)
# -> {"media_id", "account_name", "article", "article_url", "status": "published"}

# 发布已有草稿
result = publish_wechat_draft(media_id="MEDIA_ID", account="main", postid=2850)
# -> {"article_url", "account_name", "status": "published"}
```

`deploy_wechat()` 内部流程：
1. 解析 Hugo 文章 → `hugo_to_wechat()` 转 HTML
2. 上传正文图片（`/uploads/...` → 微信 `mmbiz` URL）
3. 上传封面图 → `thumb_media_id`
4. 创建草稿 → `media_id`
5. （可选）发布 → 轮询状态 → 获取永久链接
6. 元数据写回 Hugo `extra["wechat"]` 和 Joplin frontmatter
7. 在 Joplin 笔记上打 `mp:账号名` 标签

底层 API（需要更灵活控制时）：

```python
from rspeak.config import get_wechat_config
from rspeak.converter import hugo_to_wechat
from rspeak.wechat import WechatClient

article = hugo_to_wechat(post, content_dir=Path("content"), wechat_account="main")
conf = get_wechat_config(account="main")
with WechatClient(appid=conf["appid"], appsecret=conf["appsecret"]) as client:
    media_id = client.add_draft([article])
    publish_id = client.publish_draft(media_id)
    # 轮询发布状态
    result = client.get_publish_status(publish_id)
    # result["article_detail"]["item"][0]["article_url"]
```

### Hugo/Joplin -> 知乎

```python
from rspeak.converter import hugo_to_zhihu
from rspeak.zhihu import format_for_clipboard

zhihu_article = hugo_to_zhihu(post)
text = format_for_clipboard(zhihu_article)
# 将 text 输出给用户复制
```

## Joplin Frontmatter

Joplin 笔记 body 顶部可包含 `+++` 包裹的 TOML frontmatter，用于存储跨平台元数据：

```
+++
postid = 2850
slug = "magic-trackpad-3"

[wechat.main]
status = "published"
url = "https://mp.weixin.qq.com/s/xxx"
media_id = "MEDIA_ID"
+++

正文内容...
```

### 规则

- frontmatter 仅存储跨平台元数据（`wechat` 状态、`postid`、`slug` 等）
- `title`/`date`/`tag` 不存 frontmatter（已有 Joplin 原生字段）
- Hugo ↔ Joplin 同步时，共享字段（`wechat`、`postid`、`slug`）双向深度合并
- 发布到微信/知乎/小红书时，frontmatter 自动剥离，不渲染到输出

### Python API

```python
from rspeak.converter import parse_joplin_frontmatter, write_joplin_frontmatter

# 解析
fm, body = parse_joplin_frontmatter(note_body)
# fm = {"postid": 2850, "slug": "...", "wechat": {"main": {...}}}
# body = 不含 frontmatter 的正文

# 写入
new_body = write_joplin_frontmatter(fm, body)
# 返回带 +++ 包裹 frontmatter 的完整 body
```

### 元数据存储位置对照

| 字段 | Hugo frontmatter | Joplin frontmatter | Joplin 原生字段 |
|------|-----------------|-------------------|---------------|
| postid | `postid` | `postid` | — |
| slug | `slug` | `slug` | — |
| wechat 状态/URL | `extra["wechat"]` | `wechat.*` | — |
| 公众号发布标记 | — | — | 标签 `mp:xxx` |
| title | `title` | — | note.title |
| category/tag | `category`/`tag` | — | Joplin 标签 |
| joplin_id | `extra["joplin_id"]` | — | note.id |

## 链接转换

链接在 Joplin 和 Hugo 之间的转换现已**自动完成**，无需手动处理。

### 自动转换机制

- **Joplin → Hugo**（`joplin_to_hugo()` 内部调用 `_convert_joplin_links_to_relref()`）：
  - `[文字](:/note_id)` → `[文字]({{< relref "post/{postid}.md" >}})`
  - 扫描 `content/post/` 构建 `joplin_id → postid` 映射，批量替换
  - 仅处理非图片链接（图片由 `_extract_joplin_images()` 单独处理）

- **Hugo → Joplin**（`hugo_to_joplin()` 内部调用 `_convert_relref_to_joplin()`）：
  - `[文字]({{< relref "post/{postid}.md" >}})` → `[文字](:/joplin_id)`
  - 从 relref 提取 postid，读取目标文章 frontmatter 获取 `joplin_id`

**找不到对应文章时**：打印警告并保留原始链接，不会中断同步流程。

Hugo relref 语法参考：`{{< relref "post/{postid}.md" >}}`，Hugo 构建时自动解析为正确的相对路径。
Joplin 内部链接语法：`(:/note_id)`，Joplin 客户端自动解析为笔记链接。

## Windows 环境

- **rsync 不兼容**：Scoop 安装的 rsync 在 Git Bash 中无法正常工作（`dup() in/out/err failed`，或 `C:` 被误判为远程主机）
- **替代部署方式**：先单独执行 Hugo 构建，再用 tar+ssh 部署：
  ```bash
  # Hugo 构建（deploy_blog 的前半部分）
  hugo -d public
  # tar+ssh 部署
  cd public && tar czf - . | ssh ubuntu@zengrong-net "cd /srv/www/blog.zengrong.net && tar xzf -"
  ```
- **Python 中文输出乱码**：Git Bash 中需设置 UTF-8：
  ```python
  import sys, io
  sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
  ```

## 模块结构

```
tools/rspeak/
├── pyproject.toml          # uv 项目配置（CLI 入口：rspeak = "rspeak.cli:app"）
├── config.toml             # 实际配置（.gitignore）
├── config.example.toml     # 配置模板
└── rspeak/
    ├── __init__.py
    ├── cli.py              # CLI: deploy wechat/blog/zhihu, sync, review, wechat-publish, wechat-accounts
    ├── config.py           # 配置加载（含多账号支持）
    ├── deploy.py           # 部署：Hugo 构建、微信完整发布流程（图片上传/轮询/回写）、知乎
    ├── hugo.py             # Hugo 文章解析/写入/搜索
    ├── joplin.py           # Joplin REST API 客户端
    ├── converter.py        # 跨平台格式转换、Joplin frontmatter、链接转换
    ├── wechat.py           # 微信公众号 API 客户端
    └── zhihu.py            # 知乎格式转换
```

### deploy.py 关键函数

| 函数 | 说明 |
|------|------|
| `deploy_wechat(postid, account, publish)` | 完整微信发布流程（已有草稿时自动更新） |
| `publish_wechat_draft(media_id, account, postid)` | 发布已有草稿 |
| `_upload_wechat_images(article, client, static_dir, blog_url)` | 上传正文图片到微信 |
| `_resolve_cover_image(post, static_dir)` | 获取封面图本地路径 |
| `_poll_publish_status(client, publish_id)` | 轮询发布状态 |
| `_write_wechat_metadata(post, account_name, status, ...)` | 元数据写回 Hugo + Joplin |
| `_tag_joplin_mp(post, account_name)` | 在 Joplin 笔记上打 mp:xxx 标签 |

### converter.py 关键函数

| 函数 | 说明 |
|------|------|
| `parse_joplin_frontmatter(body)` | 从 Joplin note body 解析 TOML frontmatter |
| `write_joplin_frontmatter(fm, body)` | 将 TOML frontmatter 写回 note body |
| `hugo_to_joplin(post, client, ...)` | Hugo→Joplin（含链接转换 + frontmatter 合并） |
| `joplin_to_hugo(note, content_dir, ...)` | Joplin→Hugo（含链接转换 + frontmatter 解析） |
| `sync_article(client, content_dir, ...)` | 自动判断方向同步 |
| `hugo_to_wechat(post, author, content_dir, wechat_account)` | 转微信 HTML（内联样式 + TOC + relref 解析 + 微信互链） |
| `_inline_styles_for_wechat(html)` | HTML 标签添加内联样式（Joplin 风格） |
| `_generate_toc_html(html)` | 从 h2/h3 生成 TOC 目录 HTML |
| `_resolve_relref_links(body, blog_url, content_dir, wechat_account)` | Hugo relref 短代码转实际 URL（支持微信 URL 优先） |
| `_generate_digest(md_text)` | 从 Markdown 提取纯文本摘要 |
| `hugo_to_zhihu(post)` / `joplin_to_zhihu(note)` | 转知乎格式（自动剥离 frontmatter） |
