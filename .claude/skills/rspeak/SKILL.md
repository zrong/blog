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

### 第四步：逐个修改

使用 Edit 工具逐个修改，每次修改向用户展示：
- 原文片段
- 修正后的内容
- 修改原因

**Joplin 校对场景**：先将内容同步到 Hugo（`joplin_to_hugo`），在本地 markdown 上用 Edit 修改，最后写回 Joplin。

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

# 发布到微信公众号（创建草稿）
uv run --project tools/rspeak rspeak deploy wechat -p <postid>

# 转为知乎格式
uv run --project tools/rspeak rspeak deploy zhihu -p <postid>

# 校对文章（基础检查）
uv run --project tools/rspeak rspeak review -p <postid>
```

**Python API：** 需要更灵活的控制时，用 `uv run --project tools/rspeak python -c "..."` 调用 Python 模块（详见 [reference.md](reference.md)）。调用时需加 `sys.path.insert(0, 'tools/rspeak')`。

**Hugo→Joplin 方向特殊步骤：**
- **同步前必须执行链接转换**：将 Hugo 中的 relref 链接还原为 Joplin 内部链接（见「链接转换规则 - Hugo → Joplin」）。`hugo_to_joplin()` 函数**不会**自动转换链接，必须在同步完成后手动替换 Joplin 笔记中的 relref 为 `(:/joplin_id)` 格式
- 传入 `static_dir=Path("static")` 以支持图片上传到 Joplin
- 首次同步后 `joplin_id` 自动写回 Hugo frontmatter，后续同步通过 `source_url` 匹配已有笔记进行更新

**Joplin→Hugo 方向特殊步骤：**
- 根据笔记标题生成英文翻译 slug（≤50 字符，小写连字符格式）
- 标签会从 Joplin 自动还原：`blog:category:xxx` → Hugo category，其余 → Hugo tag
- 笔记中的 Joplin 图片资源会自动下载到 `static/uploads/{year}/{slug}-{n}.{ext}`
- 自动通过 `joplin_id` 检测已有文章，更新而非创建重复内容
- 每次同步后自动回写到 Joplin：`source_url`（博客文章 URL）、标签（category/tag → Joplin 标签）

## 链接转换规则

校对和同步时，需要在平台之间双向转换内部链接。

### Joplin → Hugo：内部链接转 relref

Joplin 笔记中引用其他笔记的链接格式为 `[文字](:/note_id)`。转换步骤：

1. 通过 `client.get_note(note_id)` 获取被引用笔记的标题
2. 在 `content/post/` 中用 Grep 搜索该标题（或通过 `joplin_id` 匹配），找到对应的 Hugo 文章文件名
3. **Hugo 中已存在**：转换为 Hugo relref 语法 `[文字]({{< relref "post/{postid}.md" >}})`
4. **Hugo 中不存在**：询问用户是否将被引用笔记同步到 Hugo
   - 用户同意 → 执行 `sync_article()`（需要生成 slug）→ 同步完成后用 relref 链接
   - 用户不同意 → 保留文字，去掉无效链接，用书名号包裹标题：`《标题》`

### Hugo → Joplin：relref 转内部链接

Hugo 文章中的 relref 链接 `[文字]({{< relref "post/{postid}.md" >}})` 需要还原为 Joplin 内部链接。转换步骤：

1. 从 relref 路径提取 postid，读取目标文章的 frontmatter 获取 `joplin_id`
2. **`joplin_id` 存在**：转换为 Joplin 内部链接 `[文字](:/joplin_id)`
3. **`joplin_id` 不存在**（目标文章未同步到 Joplin）：询问用户是否将目标文章同步到 Joplin
   - 用户同意 → 执行 `hugo_to_joplin()` → 同步完成后用 `(:/joplin_id)` 链接
   - 用户不同意 → 保留文字，去掉链接

### 微信公众号文章链接（待扩展）

预留规则：将公众号文章 URL 转换为合适的引用格式。

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
