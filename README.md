## 构建

下载 hugo <= 0.128.2: https://github.com/gohugoio/hugo/releases/tag/v0.128.2


```shell
hugo && rsync -avz --delete public/ app@zengrong.net:~/www/blog.zengrong.net/
```


## [blog.zengrong.net](https://blog.zengrong.net) 的历史

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