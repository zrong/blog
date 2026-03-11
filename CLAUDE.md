# CLAUDE.md

## 项目概述

Hugo 博客项目，内容源码在 `content/post/`，静态资源在 `static/uploads/`。

## 工具

- `tools/rspeak/`：博客写作与发布工具（校对、Hugo/Joplin 同步、微信公众号、知乎）
- `.claude/skills/rspeak/`：rspeak skill 定义（SKILL.md、reference.md、style-guide.md）

## 更新日志

- **26.11.1**: rspeak 新增微信公众号账号配置支持；新增文章 2855《使用OpenClaw龙虾操作腾讯文档，分析合同+计算小说转漫剧的时长》
- **26.10.2**: 新增文章 2854《居然可以免费领一台 2C4G 主机安装 OpenClaw 养龙虾……免费！》，包含飞书机器人配置教程
- **26.10.1**: rspeak 修复两个 converter.py bug：`joplin_to_hugo` 自动移除 `[toc]` 标记、时间戳竞争导致校对后被 Joplin 覆盖；SKILL.md 补充校对后直接调用 `hugo_to_joplin` 的说明；新增文章 2852
- **26.10**: rspeak 新增微信公众号完整发布流程（多账号、图片上传、发布轮询、永久链接回写）、Joplin TOML frontmatter 跨平台元数据、Hugo↔Joplin 双向链接自动转换
- **26.9**: 新增 rspeak skill（由 publish 改名），包含文章校对、写作风格指南、双向链接转换规则；新增文章 2847/2848/2849 及配图
