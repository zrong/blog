## 构建与部署

下载 hugo <= 0.128.2: https://github.com/gohugoio/hugo/releases/tag/v0.128.2

使用 [rspeak][rspeak]（博客写作与发布工具）一键构建并部署：

```shell
uv run --project tools/rspeak rspeak deploy blog
```

也可以手动执行：

```shell
hugo && rsync -avz --delete public/ ubuntu@zengrong-net:/srv/www/blog.zengrong.net
```

> **Windows 注意**：Scoop 安装的 rsync 与 Git Bash 不兼容，需使用 tar+ssh 替代：
> ```shell
> hugo -d public && cd public && tar czf - . | ssh ubuntu@zengrong-net "cd /srv/www/blog.zengrong.net && tar xzf -"
> ```

### 其他 rspeak 命令

```shell
# Hugo ↔ Joplin 双向同步
uv run --project tools/rspeak rspeak sync -p <postid>

# 发布到微信公众号（创建草稿）
uv run --project tools/rspeak rspeak deploy wechat -p <postid>

# 转为知乎格式
uv run --project tools/rspeak rspeak deploy zhihu -p <postid>

# 基础校对检查
uv run --project tools/rspeak rspeak review -p <postid>
```

## AI 辅助写作

本项目配置了 [Claude Code][claudecode] skill（`.claude/skills/rspeak/`），可以通过自然语言指令完成博客写作流程。

### 可用指令

- **校对文章**：`校对 2850` 或 `校对这篇 Joplin 文章：标题关键词`
  自动定位文章，对照[风格指南][styleguide]逐段检查错别字、标点、中英文混排等问题，逐个修改并展示差异。
- **同步文章**：`同步 2850` 或 `同步到 Joplin`
  Hugo ↔ Joplin 双向同步，自动比较更新时间判断方向，处理图片和内部链接转换。
- **发布文章**：`发布博客` / `发到公众号` / `转知乎格式`
  Hugo 构建部署、微信公众号草稿创建、知乎格式转换。

### Skill 文件结构

```
.claude/skills/rspeak/
├── SKILL.md          # 工作流定义（校对、同步、发布流程）
├── reference.md      # 技术参考（CLI 命令、Python API、模块结构）
└── style-guide.md    # 写作风格指南（标点、混排、段落规范）
```

## [blog.zengrong.net](https://blog.zengrong.net) 的历史

### 2026年3月1日

引入 AI 辅助写作流程。使用 [Claude Code][claudecode] 的 skill 机制，将博客校对、Hugo/Joplin 同步、多平台发布封装为自然语言指令。配套工具 [rspeak][rspeak] 提供 CLI 和 Python API，支持一键部署到远程服务器、微信公众号和知乎。

### 2019年8月29日

Hexo 的生成速度无法满足博客近千篇文章的更新，我放弃了 [Hexo][hexo]，完美转换到 [Hugo][hugo]。之前的源文件可在 [hexo][hexobranch] 分支找到 。具体的转换过程见：[Hexo to Hugo][hexotohugo]。

开始使用 [maupassant][maupassant] 模版，后改用 [hugo-clarity][clarity] 模版，修改使其支持 `flash/mermaid/label/alert/download/pageview` 。

自建 [isso][isso] 实现评论服务。

写了一个专用服务 aid 用于实现 `download/pageview` 功能。

### 2017年7月15日

终于放弃了 Wordpress，将博客完美转换到 [Hexo][hexo]。之前的源文件可在 [wordpress][wordpressbranch] 分支找到 。具体转换过程见：[Wordpress to Hexo（上）][wptohexo1]，[Wordpress to Hexo（下）][wptohexo2]。

### 2015年6月

写了一个命令行工具 [WPCMD(WordPress command)][wpcmd]，通过 WordPress XML-RPC 接口在本地创建、更新 WordPress 博客。

### 2011年6月11日

开始琢磨 [博客静态化][static]，使用 Markdown 写博客，文章提交到 Github（就是这个 Respostory）上。然后再手动粘贴到 Wordpress 后台，使用 [Markdown On Save][onsave] 插件来渲染博客内容。

### 2005年4月25日

改用 [Wordpress][wordpress]，写下第一篇有记录的博客： [创作共用][cc]。

### 2003年

开始写博客。当时采用的是一套名为 oblog 的 ASP 博客程序。由于当时对运维知识不熟悉，以及博客程序自身的漏洞，虚拟主机被黑客入侵，所有文章被删除。有两年的记录没有留下来。

[wordpressbranch]: https://github.com/zrong/blog/tree/wordpress
[hexobranch]: https://github.com/zrong/blog/tree/hexo
[hexotohugo]: https://blog.zengrong.net/post/hexo-to-hugo/
[wptohexo1]: https://blog.zengrong.net/post/wordpress-to-hexo1/
[wptohexo2]: https://blog.zengrong.net/post/wordpress-to-hexo2/
[hugo]: https://gohugo.io/
[hexo]: https://hexo.io/
[wpcmd]: https://blog.zengrong.net/wpcmd/
[static]: https://blog.zengrong.net/post/blog-static/
[onsave]: https://wordpress.org/plugins/markdown-on-save/
[clarity]: https://github.com/zrong/hugo-clarity
[maupassant]: https://github.com/zrong/maupassant-hugo
[isso]: https://github.com/posativ/isso
[wordpress]: https://wordpress.org
[cc]: https://blog.zengrong.net/post/creative-commons/
[rspeak]: tools/rspeak/
[claudecode]: https://claude.com/claude-code
[styleguide]: .claude/skills/rspeak/style-guide.md