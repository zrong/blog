# AGENTS.md

This file provides guidance to a AI Agent when working with code in this repository.

## 项目概述

Hugo 博客（https://blog.zengrong.net），内容源码在 `content/post/`，静态资源在 `static/uploads/`。需要 **Hugo Extended >= 0.158.0** 和 **Dart Sass**，主题为 `clarity`（位于 `themes/clarity/`）。

## 常用命令

```bash
# 本地预览
just dev

# 构建
just build

# 构建并部署
just deploy

# 推送搜索索引到 aid（需设置 AID_TOKEN 环境变量）
just push-index

# 部署 + 推送索引（一步完成）
just deploy-all
```

## 环境变量

- `AID_TOKEN`: API token，用于推送搜索索引到 aid.zengrong.net

## 部署

```bash
# 完整部署 + 索引推送
just deploy-all

# 仅部署（不更新索引）
just deploy

# 仅推送索引
just push-index
```

## 内容结构

- `content/post/`：博客文章（~1,056 篇，文件名通常为 `<postid>.md`）
- `content/page/`：独立页面
- `content/function/`：功能页（搜索、友链）
- `static/uploads/<year>/`：文章配图，按年份归档

## Front Matter 格式（TOML）

```toml
+++
title = "文章标题"
postid = 2863                              # 文章 ID（来自旧 WordPress，目前顺号排列）
date = "2026-05-01T13:11:25+08:00"
isCJKLanguage = true
toc = true                                 # 是否显示目录
type = "post"
slug = "url-slug"
aliases = ["/post/2863.html"]             # 旧链接重定向
thumbnail = "/uploads/2026/image.jpg"
featureImage = "/uploads/2026/image.jpg"
category = ["technology"]
tag = ["ai", "ai-skill"]
lastmod = "2026-05-01T13:11:25+08:00"

# 多平台发布（可选，显示在 copyright footer）
[wechat.rongspeak]
status = "published"                       # 或 "draft"
url = "https://mp.weixin.qq.com/..."
media_id = "..."                          # 草稿 media_id

[zhihu]
url = "https://zhuanlan.zhihu.com/..."

[xiaohongshu]
url = "https://www.xiaohongshu.com/..."
+++
```

## 架构要点

### Aid 集成

blog 通过 `aidapi.js`（Web Components）集成 aid 后端服务：
- `hooks/body-end.html`：加载 aidapi.js（开发环境自动切换到 `http://localhost:8000`）
- `<aid-search-modal>`：导航栏弹窗搜索（触发按钮 `#search-btn`）
- `<aid-search-page>`：`/search/` 搜索页（无限滚动）
- `<aid-pageview>`：文章 PV 统计
- `<aid-messageboard>`：文章留言板
- `<aid-download>`：下载列表

### 自定义覆盖

- `layouts/_default/single.html`：文章单页布局，调用自定义 copyright partial
- `layouts/partials/copyright.html`：显示文章 ID、多平台发布链接（微信/知乎/小红书）

### 主题 Shortcodes

`themes/clarity/layouts/shortcodes/` 中提供：`alert`、`label`、`mermaid`、`video`、`rawhtml`、`download`、`flash`

## 本地测试

测试搜索功能需要先启动 aid 后端：

```bash
# 1. 启动 aid（端口 8000）
cd ../aid && just dev

# 2. 启动 blog（端口 1313）
just dev    # 自动从 localhost:8000 加载 aidapi.js

# 3. 测试检查项
# - 导航栏右侧搜索按钮 → 点击打开弹窗
# - 输入关键词 → 弹窗显示 20 条结果
# - "显示更多" 链接 → 跳转 /search/?q=...
# - 搜索页自动搜索 + 无限滚动
# - 文章页 PV + 留言板
# - DevTools Console 无报错
```
