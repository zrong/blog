# 多平台发布 - 技术参考

## 配置文件格式

`tools/rspeak/config.toml`：

```toml
[joplin]
token = "你的 Joplin Web Clipper token"
base_url = "http://localhost:41184"
notebook_path = "Thought/Writing/Blog"

[wechat]
appid = "你的公众号 appid"
appsecret = "你的公众号 appsecret"

[hugo]
content_dir = "content"
blog_url = "https://blog.zengrong.net"
author = "zrong"
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
# 创建草稿（需要登录公众号后台确认发布）
uv run --project tools/rspeak rspeak deploy wechat -p 2850
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

### Hugo/Joplin -> 微信公众号

```python
from rspeak.config import get_wechat_config
from rspeak.converter import hugo_to_wechat
from rspeak.wechat import WechatClient

article = hugo_to_wechat(post)
conf = get_wechat_config()
with WechatClient(appid=conf["appid"], appsecret=conf["appsecret"]) as client:
    media_id = client.add_draft([article])
    # 确认后发布
    publish_id = client.publish_draft(media_id)
```

### Hugo/Joplin -> 知乎

```python
from rspeak.converter import hugo_to_zhihu
from rspeak.zhihu import format_for_clipboard

zhihu_article = hugo_to_zhihu(post)
text = format_for_clipboard(zhihu_article)
# 将 text 输出给用户复制
```

## 链接转换

链接在 Joplin 和 Hugo 之间需要双向转换。

### Joplin → Hugo：`(:/note_id)` → relref

```python
from rspeak.config import get_joplin_config
from rspeak.joplin import JoplinClient

conf = get_joplin_config()
with JoplinClient(token=conf["token"], base_url=conf["base_url"]) as client:
    # 1. 从正文中提取 Joplin 内部链接的 note_id
    note = client.get_note("de8b904013f940ed9114935f0b8edaba")
    print(f"Title: {note.title}")

# 2. 在 Hugo 中搜索对应文章（用 Grep 搜索 joplin_id 或标题）
#    找到对应文件如 content/post/2849.md

# 3. 转换结果：
#    找到 → [文字]({{< relref "post/2849.md" >}})
#    未找到 → 询问用户是否同步，同意则同步后用 relref，拒绝则用《标题》
```

### Hugo → Joplin：relref → `(:/note_id)`

```python
from pathlib import Path
from rspeak.hugo import parse_post

# 1. 从 relref 路径提取 postid
#    [文字]({{< relref "post/2849.md" >}}) → postid = 2849
post = parse_post(Path("content/post/2849.md"))
joplin_id = post.extra.get("joplin_id")

# 2. 转换结果：
#    joplin_id 存在 → [文字](:/joplin_id)
#    joplin_id 不存在 → 询问用户是否同步到 Joplin，同意则同步后用 (:/joplin_id)，拒绝则去掉链接
```

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
    ├── cli.py              # CLI 命令行入口（typer）
    ├── config.py           # 配置加载
    ├── deploy.py           # 部署：Hugo 构建 + rsync + 微信/知乎发布
    ├── hugo.py             # Hugo 文章解析/写入/搜索
    ├── joplin.py           # Joplin REST API 客户端
    ├── converter.py        # 跨平台格式转换
    ├── wechat.py           # 微信公众号 API 客户端
    └── zhihu.py            # 知乎格式转换
```
