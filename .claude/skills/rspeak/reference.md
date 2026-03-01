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

## 代码调用示例

所有脚本通过 `uv run --project tools/rspeak python -c "..."` 执行。

### 搜索 Joplin 笔记

```python
from tools.rspeak.config import get_joplin_config
from tools.rspeak.joplin import JoplinClient

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
from tools.rspeak.hugo import parse_post
from tools.rspeak.config import get_joplin_config
from tools.rspeak.joplin import JoplinClient
from tools.rspeak.converter import hugo_to_joplin

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
from tools.rspeak.config import get_joplin_config
from tools.rspeak.joplin import JoplinClient
from tools.rspeak.converter import joplin_to_hugo

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
from tools.rspeak.config import get_joplin_config
from tools.rspeak.joplin import JoplinClient
from tools.rspeak.converter import sync_article

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
from tools.rspeak.config import get_wechat_config
from tools.rspeak.converter import hugo_to_wechat
from tools.rspeak.wechat import WechatClient

article = hugo_to_wechat(post)
conf = get_wechat_config()
with WechatClient(appid=conf["appid"], appsecret=conf["appsecret"]) as client:
    media_id = client.add_draft([article])
    # 确认后发布
    publish_id = client.publish_draft(media_id)
```

### Hugo/Joplin -> 知乎

```python
from tools.rspeak.converter import hugo_to_zhihu
from tools.rspeak.zhihu import format_for_clipboard

zhihu_article = hugo_to_zhihu(post)
text = format_for_clipboard(zhihu_article)
# 将 text 输出给用户复制
```

## 链接转换

链接在 Joplin 和 Hugo 之间需要双向转换。

### Joplin → Hugo：`(:/note_id)` → relref

```python
from tools.rspeak.config import get_joplin_config
from tools.rspeak.joplin import JoplinClient

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
from tools.rspeak.hugo import parse_post

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

## 模块结构

```
tools/rspeak/
├── pyproject.toml          # uv 项目配置
├── config.toml             # 实际配置（.gitignore）
├── config.example.toml     # 配置模板
├── __init__.py
├── config.py               # 配置加载
├── hugo.py                 # Hugo 文章解析/写入/搜索
├── joplin.py               # Joplin REST API 客户端
├── wechat.py               # 微信公众号 API 客户端
├── zhihu.py                # 知乎格式转换
└── converter.py            # 跨平台格式转换
```
