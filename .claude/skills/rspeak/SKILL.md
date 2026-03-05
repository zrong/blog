---
name: rspeak
description: 博客写作与发布。校对文章错别字和风格、同步 Hugo/Joplin、发布到微信公众号/知乎。当用户提到"校对"、"检查错别字"、"润色"、"发布文章"、"同步到Joplin"、"发到公众号"、"转知乎格式"、"同步文章"时使用。
argument-hint: "[postid 或关键词] [校对|发布|同步]"
allowed-tools: Bash(uv run *), Read, Grep, Glob, Edit
---

你是一个博客写作与发布助手。帮助用户校对文章、将博客文章发布到多个平台。

## 支持的功能

1. **文章校对**（错别字、标点、断句、中英文混排）
2. **Hugo 博客**（本地源码 `content/post/`）
3. **Joplin**（本地 REST API `localhost:41184`）
4. **微信公众号**（通过官方 API）
5. **知乎**（仅格式转换，需手动粘贴发布）

## 校对工作流

当用户说"校对"、"检查错别字"、"润色"或类似指令时，执行以下步骤：

### 第一步：定位文章并确定校对平台

根据 `$ARGUMENTS`（postid 或关键词）同时在 Hugo 和 Joplin 中搜索：

- **仅 Hugo 存在**：在 Hugo 中校对（读取 `content/post/{postid}.md`，用 Edit 修改）
- **仅 Joplin 存在**：在 Joplin 中校对（通过 API 读取内容，校对后写回 Joplin）
- **两边都存在**：比较 Hugo `lastmod` 与 Joplin `updated_time`，校对**更新时间较晚**的那一方
- **都不存在**：提示用户未找到

搜索方式：
- Hugo：用 Grep 在 `content/post/` 中搜索 postid 或关键词
- Joplin：用 `client.search_notes()` 搜索

### 第二步：读取写作风格指南

读取 [style-guide.md](style-guide.md) 中的写作风格规则，作为校对标准。

### 第三步：逐段分析并修正

读取文章全文，对照风格指南逐段检查以下问题：

1. **错别字**：常见汉字误用（的/地/得等）
2. **标点符号**：中英文标点混用、引号规范
3. **中英文混排**：中文与英文/数字之间是否加空格
4. **断句**：过长段落拆分、不自然断句修正
5. **格式规范**：标题层级、代码块标注、列表格式
6. **链接转换**：按「链接转换规则」处理 Joplin 内部链接等平台特有链接
7. **内部链接标题一致性**：检查文章中所有 relref 链接（Hugo）或内部链接（Joplin）的显示文字是否与目标文章的当前标题一致。若不一致，以目标文章最新标题为准更新链接文字，并同步更新另一平台

### 第四步：逐个修改

使用 Edit 工具逐个修改，每次修改向用户展示：
- 原文片段
- 修正后的内容
- 修改原因

**Joplin 校对场景**：
1. 先调用 `sync_article()` 将 Joplin 同步到 Hugo（自动下载图片、转换链接）
2. 在本地 Hugo markdown 上用 Edit 工具修改
3. 修改完成后，**直接调用 `hugo_to_joplin()` Python API** 写回 Joplin，**不要**再次调用 `rspeak sync` 或 `sync_article()`

> **原因**：`joplin_to_hugo` 在写回 `source_url` 时会更新 Joplin 的 `updated_time`，导致下次 `sync` 误判为 Joplin 更新，反复覆盖 Hugo 修改。直接调用 `hugo_to_joplin` 可明确同步方向。

### 第五步：汇总并提示同步

所有修改完成后：
1. 输出修改汇总：修正了多少处，主要问题类型
2. 若另一平台也有该文章，询问用户是否同步到对方：
   - 用户同意 → 进入同步工作流（`hugo_to_joplin` 或 `joplin_to_hugo`）
   - 用户拒绝 → 结束校对

## 发布工作流

### 第一步：确认内容来源

根据 `$ARGUMENTS` 判断来源，如果未提供则询问用户：
- **Hugo 博客文章**：提供 postid 或文件名（如 `2841`），从 `content/post/` 读取
- **Joplin 笔记**：提供笔记标题关键词，通过 Joplin API 搜索

### 第二步：确认目标平台

询问用户要发布到哪些目标平台（可多选）：
- Hugo 博客（从 Joplin 导入时）
- Joplin（从 Hugo 导出时）
- 微信公众号（创建草稿 -> 可选发布）
- 知乎（生成格式化内容供手动粘贴）

### 同步工作流

当用户说"同步"或提供文章标题/postid 要求同步时，使用 `sync_article()` 自动判断方向：

1. 用户提供 **postid**（如 `2842`）或**文章标题**
2. 调用 `sync_article(client, content_dir, static_dir, postid=2842)` 或 `sync_article(client, content_dir, static_dir, title="文章标题")`
3. 双方都存在时，自动比较更新时间（Hugo `lastmod` vs Joplin `updated_time`），新→旧同步
4. 根据返回的 `action` 字段处理：
   - `hugo_to_joplin`：Hugo 更新或仅 Hugo 存在，已自动完成同步
   - `joplin_to_hugo`：Joplin 更新或仅 Joplin 存在，需要先由 Claude 根据标题生成英文 slug（≤50 字符），传入 `slug` 参数
   - `already_synced`：双方时间相同，无需同步
   - `not_found`：双方均未找到该文章

**注意**：若搜索到多个匹配结果，应先让用户确认目标文章再执行同步。

### 第三步：执行发布

优先使用 CLI 命令，也可以用 Python API。所有命令使用 `uv run --project tools/rspeak rspeak` 前缀。

**CLI 命令：**

```bash
# 同步 Hugo ↔ Joplin
uv run --project tools/rspeak rspeak sync -p <postid>
uv run --project tools/rspeak rspeak sync -t "标题关键词" -s "english-slug"

# 部署博客到远程服务器
uv run --project tools/rspeak rspeak deploy blog
uv run --project tools/rspeak rspeak deploy blog --dry-run

# 微信公众号：创建草稿（默认）
uv run --project tools/rspeak rspeak deploy wechat -p <postid> [-a <account>]

# 微信公众号：创建草稿 + 自动发布
uv run --project tools/rspeak rspeak deploy wechat -p <postid> -a <account> --publish

# 微信公众号：发布已有草稿
uv run --project tools/rspeak rspeak wechat-publish -m <media_id> -p <postid> [-a <account>]

# 微信公众号：列出配置的账号
uv run --project tools/rspeak rspeak wechat-accounts

# 转为知乎格式
uv run --project tools/rspeak rspeak deploy zhihu -p <postid>

# 校对文章（基础检查）
uv run --project tools/rspeak rspeak review -p <postid>
```

**Python API：** 需要更灵活的控制时，用 `uv run --project tools/rspeak python -c "..."` 调用 Python 模块（详见 [reference.md](reference.md)）。调用时需加 `sys.path.insert(0, 'tools/rspeak')`。

**Hugo→Joplin 方向特殊步骤：**
- **链接自动转换**：`hugo_to_joplin()` 会自动将 relref 链接还原为 Joplin 内部链接 `(:/joplin_id)`。若目标文章没有 `joplin_id`，打印警告并保留原始链接
- 传入 `static_dir=Path("static")` 以支持图片上传到 Joplin
- 首次同步后 `joplin_id` 自动写回 Hugo frontmatter，后续同步通过 `source_url` 匹配已有笔记进行更新
- **Frontmatter 同步**：Hugo `extra` 中的共享字段（`wechat`, `postid`, `slug`）自动写入 Joplin 笔记 body 顶部的 TOML frontmatter

**Joplin→Hugo 方向特殊步骤：**
- 根据笔记标题生成英文翻译 slug（≤50 字符，小写连字符格式）
- 标签会从 Joplin 自动还原：`blog:category:xxx` → Hugo category，`mp:xxx` 标签跳过（微信标记），其余 → Hugo tag
- 笔记中的 Joplin 图片资源会自动下载到 `static/uploads/{year}/{slug}-{n}.{ext}`
- **链接自动转换**：Joplin 内部链接 `[text](:/note_id)` 自动转为 Hugo relref `[text]({{< relref "post/{postid}.md" >}})`。未找到对应 Hugo 文章时打印警告并保留原始链接
- 自动通过 `joplin_id` 检测已有文章，更新而非创建重复内容
- 每次同步后自动回写到 Joplin：`source_url`（博客文章 URL）、标签（category/tag → Joplin 标签）
- **Frontmatter 同步**：Joplin body 顶部的共享 frontmatter 字段合并到 Hugo `extra`

**微信公众号发布流程：**
1. 创建或更新草稿：上传正文图片 + 封面图 + 创建/更新草稿 → `media_id`
   - **幂等性**：若 Hugo frontmatter 中已有该账号的 `media_id` 且状态为 `draft`，调用 `update_draft` 原地更新，不会创建重复草稿
   - **新建**：无已有草稿时调用 `add_draft` 创建
2. 发布：发布草稿 → 轮询状态 → 获取永久链接
3. 元数据回写：永久链接和状态写回 Hugo frontmatter `extra["wechat"]` 和 Joplin frontmatter
4. 标签标记：在 Joplin 笔记上打 `mp:账号名` 标签

**微信公众号 HTML 渲染规则：**
- 微信**不支持 `<style>` 标签**，所有样式必须内联到 HTML 元素上
- `_inline_styles_for_wechat()` 自动将 h2/h3/p/code/blockquote/img/table/strong 标签转为内联样式
- 样式参考 Joplin `userstyle.css`：h2 顶部 2px 灰色边框、strong 使用 `#ab1942` 强调色、正文 17px
- 代码块使用 `<section>` + 等宽字体内联样式，`white-space: pre-wrap` 防止溢出
- Hugo relref 短代码自动转为实际博客 URL（`_resolve_relref_links()`）
- 若 Hugo frontmatter `toc = true`，自动生成目录（Joplin 风格虚线边框）插入第一个 h2 之前

**微信公众号文章默认设置：**
- 作者：从 config.toml `[hugo] author` 读取（默认「曾嵘」）
- 留言：默认开启（`need_open_comment=1`）
- 摘要：从正文智能提取纯文本（去除代码块、图片、标记），非截取开头段落
- 原创声明/创作来源/合集：API 不支持，需在公众号后台手动操作

**微信公众号草稿管理 API：**
- `WechatClient.add_draft(articles)` — 创建草稿
- `WechatClient.update_draft(media_id, article)` — 更新已有草稿
- `WechatClient.delete_draft(media_id)` — 删除草稿
- `WechatClient.list_drafts(offset, count)` — 列出草稿

## 链接转换规则

同步时，`converter.py` 自动在平台之间双向转换内部链接。

### Joplin → Hugo：内部链接转 relref（自动）

`joplin_to_hugo()` 自动将非图片的 Joplin 内部链接转为 Hugo relref：

- `[文字](:/note_id)` → `[文字]({{< relref "post/{postid}.md" >}})`
- 通过扫描 `content/post/` 中所有文章的 `joplin_id` 字段匹配
- **找不到对应文章**：打印警告，保留原始链接

**校对时的额外处理**：若同步后发现警告（目标文章不在 Hugo 中），询问用户是否将被引用笔记也同步到 Hugo。

### Hugo → Joplin：relref 转内部链接（自动）

`hugo_to_joplin()` 自动将 relref 链接还原为 Joplin 内部链接：

- `[文字]({{< relref "post/{postid}.md" >}})` → `[文字](:/joplin_id)`
- 从 relref 路径提取 postid，读取目标文章 frontmatter 获取 `joplin_id`
- **`joplin_id` 不存在**：打印警告，保留原始链接

**校对时的额外处理**：若同步后发现警告（目标文章没有 `joplin_id`），询问用户是否将目标文章也同步到 Joplin。

### 微信公众号文章互链

发布到微信时，文章中引用的其他文章优先使用微信永久链接（而非博客 URL），让微信读者可以直接在微信内跳转。

**机制：**
- `_resolve_relref_links()` 接收 `content_dir` 和 `wechat_account` 参数
- 解析 relref 目标文章的 `[wechat.{account}].url`（状态须为 `published`）
- 找到微信 URL → 使用微信 URL；未找到 → 回退到博客 URL
- `deploy_wechat()` 自动传入这些参数

**永久链接获取：**
- **自动获取**：使用 `--publish` 参数或 `wechat-publish` 命令发布草稿，系统自动轮询获取永久链接并写回 Hugo/Joplin frontmatter
- **手动获取**：用户在微信后台手动发布后，将永久链接写入 Joplin frontmatter `[wechat.{account}] url = "..."`，下次同步时自动同步到 Hugo

### 博客文章平台链接（版权区）

当文章 frontmatter 中有已发布的平台 URL 时，Hugo 版权区自动在"原文链接"下方追加对应平台链接。

**实现：**
- `layouts/partials/copyright.html` 覆盖主题同名 partial
- 微信：遍历 `.Params.wechat`，`status = "published"` 且有 `url` 时渲染"公众号链接"
- 知乎：检测 `.Params.zhihu.url`，有则渲染"知乎链接"
- 小红书：检测 `.Params.xiaohongshu.url`，有则渲染"小红书链接"
- 账号显示名称来自 Hugo 站点配置 `[params.wechat_accounts]` 映射
- 无需修改文章正文，纯模板层面实现

**frontmatter 格式：**
```toml
[wechat.rongspeak]        # 微信（多账号支持）
status = "published"
url = "https://mp.weixin.qq.com/s/..."

[zhihu]                   # 知乎（未来扩展）
url = "https://zhuanlan.zhihu.com/p/..."

[xiaohongshu]             # 小红书（未来扩展）
url = "https://..."
```

**数据流：** Joplin frontmatter `[wechat.{account}].url` → 同步到 Hugo frontmatter → 版权区自动渲染

<!-- 未来扩展：
### 知乎链接（待扩展）
### 外部平台链接（待扩展）
-->

## 配置

配置文件位于 `tools/rspeak/config.toml`（从 `config.example.toml` 复制）。发布前先检查配置是否存在。

## 技术实现

详见 [reference.md](reference.md)。

## 转换规则

| 方向 | Hugo 字段 | Joplin 对应 |
|------|-----------|------------|
| Hugo→Joplin | `category: [xxx]` | 标签 `blog:category:xxx` |
| Hugo→Joplin | `tag: [yyy]` | 标签 `yyy` |
| Hugo→Joplin | `![alt](/uploads/...)` | Joplin 资源（`blog:` 前缀去重） |
| Hugo→Joplin | — | 笔记本 `Thought/Writing/Blog`（嵌套） |
| Hugo↔Joplin | `joplin_id`（frontmatter） | 笔记 ID（双向锚点） |
| Hugo→Joplin | `source_url`（笔记属性） | 博客文章 URL（幂等匹配） |
| Joplin→Hugo | 标签 `blog:category:xxx` | `category: [xxx]` |
| Joplin→Hugo | 其余标签 | `tag: [...]` |
| Joplin→Hugo | `created_time`（笔记创建时间） | `date`（frontmatter） |
| Joplin→Hugo | `updated_time`（笔记更新时间） | `lastmod`（frontmatter） |
| Joplin→Hugo | 正文第一张图片 | `featureImage` + `thumbnail`（自动填充） |
| Joplin→Hugo | `![alt](:/resource_id)` | `![alt](/uploads/{year}/{slug}-{n}.{ext})` |
| Joplin→Hugo | `[text](:/note_id)` | `[text](relref "post/{postid}.md")` |
| Hugo→Joplin | `[text](relref "post/{postid}.md")` | `[text](:/joplin_id)` |

**幂等性**：双向同步均为幂等操作。重复执行不会创建重复内容——Hugo→Joplin 通过 `source_url` 匹配已有笔记，Joplin→Hugo 通过 `joplin_id` 匹配已有文章。

## 注意事项

- 微信公众号发布前**必须先创建为草稿**，让用户确认后再正式发布
- 知乎仅生成格式化内容，提示用户手动登录知乎粘贴发布
- 图片处理：Hugo 本地图片路径 `/uploads/...` 在发布到外部平台时需要替换为公网可访问 URL `https://blog.zengrong.net/uploads/...`
- Joplin 操作前先 ping 确认服务可用
- 所有敏感信息（token、apikey）从配置文件读取，不硬编码
- 分类参考：影视拉片、剧评、影评等影视媒体相关内容归入 `media` 类别，而非 `impressions`

## Windows 环境注意事项

- **rsync 不可用**：Scoop 安装的 rsync 与 Git Bash 的 SSH 不兼容（`dup() in/out/err failed` 或路径中 `C:` 被误判为远程主机）。`deploy blog` 命令会失败
- **替代部署方式**：先用 `hugo_build()` 构建，再用 tar+ssh 部署：
  ```bash
  cd public && tar czf - . | ssh ubuntu@zengrong-net "cd /srv/www/blog.zengrong.net && tar xzf -"
  ```
- **Python API 编码**：在 Git Bash 中调用 Python API 输出中文时，需设置 `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')`，否则会乱码
