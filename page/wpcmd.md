title: WPCMD
date: 2015-06-12 09:40:22
modified: 2015-10-23 12:47:11
author: zrong
postid: 2321
slug: 2321
nicename: wpcmd
attachments: $ATTACHMENTS
posttype: page
poststatus: publish

我 2003 年开始写博客，现在的博客 [zengrong.net][2] 从2005 年起开始更新，一直没有中断。虽然 WordPress 的编辑功能越来越强大，而且也有大量的博客写作工具，但我都用不习惯。我总希望用一种更方便更简单的（更适合程序员）的方式来管理博客。

2014 年的时候我考虑过 [博客静态化][5]，但现有的博客静态化工具不太符合我的要求，因此我准备自己造个轮子。造轮子的工程未免复杂，为了满足在轮子诞生之前的更新欲望，[WPCMD][1] 诞生了。

# 1. WPCMD 是什么

[WPCMD(Wordpress command)][1]  是一个通过 WordPress XML-RPC 接口在本地创建、更新 Wordpress 博客的命令行工具。 [zengrong.net][2] 就是使用该工具进行管理。

这是一些优点：

- 使用 MarkDown 语法写博客；
- 随意选择自己最喜欢的版本管理来保存博客文章；
- 随意选择自己最喜欢的编辑器编写博客；
- 生成所有文章的列表；
- 不用打开 WordPress 后台就能完成：
    1. 文章创建和更新；
    2. 分类和标签的创建和更新；
    3. 查看博客文章/页面/分类/标签/媒体等信息。
- 使用 [Fenced Code Extra ][6] 支持：
    1. [graphviz][7] ；
    2. 语法高亮；
    3. 代码注释。
- 同时管理多个 WordPress 博客。

# 2. Hello WPCMD

快速看一下基本用法：

## 2.1 显示博客信息

```
wpcmd show -t option

// blog_title="zrong&#039;s blog"
// image_default_size=""
// medium_size_w="300"
// blog_tagline="可能是一个程序员"
// stylesheet="responsive_child"
// thumbnail_crop="1"
// image_default_align=""
// large_size_h="1024"
// medium_size_h="300"
// thumbnail_size_h="150"
// time_format="H:i"
// default_ping_status="open"
// default_comment_status="open"
// home_url="http://zengrong.net"
// users_can_register="0"
// blog_url="http://zengrong.net"
// post_thumbnail="True"
// thumbnail_size_w="150"
// large_size_w="1024"
// date_format="m/d/Y"
// software_version="4.3.1"
// time_zone="8"
// software_name="WordPress"
// template="responsive"
// image_default_link_type=""
```

## 2.2 显示最新的5篇文章的基本信息

```
wpcmd show -t post -n 5

// id=2374, date=2015-10-17 13:52:59, date_modified=2015-10-20 08:30:41, slug=open-source-mirror-site, title=常用开源镜像站整理, post_status=publish, post_type=post
// id=2370, date=2015-09-30 02:49:44, date_modified=2015-09-30 02:57:02, slug=the-sign-of-the-beaver, title=《海狸的记号》读书笔记, post_status=publish, post_type=post
// id=2369, date=2015-09-25 03:56:49, date_modified=2015-09-25 04:13:27, slug=search-symbol-in-search-engine, title=在搜索引擎中搜索特殊字符, post_status=publish, post_type=post
// id=2367, date=2015-09-22 03:43:21, date_modified=2015-09-22 04:12:25, slug=int64-and-buffer-ts-version-for-egret, title=Int64.ts and Buffer.ts for Egret, post_status=publish, post_type=post
// id=2366, date=2015-09-13 13:02:00, date_modified=2015-09-13 13:16:32, slug=use-slimerjs-to-grab-pages-under-cloudflare-ddos-protection, title=使用 slimerjs 抓取 DDos 保护的站点, post_status=publish, post_type=post
```

## 2.3 显示所有分类信息

```
wpcmd show -t category

// use {'description': '应用技巧', 'taxonomy': 'category', 'slug': 'use', 'count': 55, 'name': '应用', 'taxonomy_id': '12', 'id': '12', 'parent': '0', 'group': '0'}
// others {'description': '什么都有', 'taxonomy': 'category', 'slug': 'others', 'count': 86, 'name': '乱弹', 'taxonomy_id': '8', 'id': '8', 'parent': '0', 'group': '0'}
// impressions {'description': '', 'taxonomy': 'category', 'slug': 'impressions', 'count': 61, 'name': '感悟', 'taxonomy_id': '1', 'id': '1', 'parent': '0', 'group': '0'}
// news {'description': '听到的消息和要说消息，某些转载的文章也在这里', 'taxonomy': 'category', 'slug': 'news', 'count': 76, 'name': '听说', 'taxonomy_id': '7', 'id': '7', 'parent': '0', 'group': '0'}
// web {'description': '与网站相关的程序、CMS系统、技巧、内容', 'taxonomy': 'category', 'slug': 'web', 'count': 54, 'name': '网站', 'taxonomy_id': '11', 'id': '11', 'parent': '0', 'group': '0'}
// technology {'description': '技术文章', 'taxonomy': 'category', 'slug': 'technology', 'count': 478, 'name': '技术', 'taxonomy_id': '22', 'id': '22', 'parent': '0', 'group': '0'}
// design {'description': '', 'taxonomy': 'category', 'slug': 'design', 'count': 8, 'name': '设计', 'taxonomy_id': '9', 'id': '9', 'parent': '0', 'group': '0'}
// tutorial {'description': '培训相关信息', 'taxonomy': 'category', 'slug': 'tutorial', 'count': 12, 'name': '培训', 'taxonomy_id': '18', 'id': '18', 'parent': '0', 'group': '0'}
```

## 2.4 更新名称为 wpcmd 的页面的内容

该命令找到名称为 wpcmd 的页面的 markdown 源码，然后将其转换成 HTML ，再将 HTML 更新到 WordPress 博客（wpcmd 页面对应的编号是2321）：

```
wpcmd update -t page -q wpcmd

// Old article:
// id=2321, date=2015-06-12 01:40:22, date_modified=2015-10-21 08:04:02, slug=wpcmd, title=WPCMD, post_status=publish, post_type=page
// Update 2321 successfully!
```

# 3. 安装和配置

## 3.1 依赖

- python 3.4 or higher
- Markdown>=2.6.2
- Pygments>=2.0.2
- python-wordpress-xmlrpc>=2.3
- rookout>=0.4.5

# 3.2 安装

`pip3 install wpcmd`

因为包比较多，想快点也可以使用豆瓣的镜像站来安装（详情可参考 [常用镜像站整理][2]）：

`pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple wpcmd`

# 3.3 配置

输入 `wpcmd -h` ，第一次运行会生成一个默认的配置文件，必须修改这个配置文件进行设置。这个配置文件位于 `~/.wpcmd.ini`（OS X 和 Linux) 和 `%HOME%\_wpcmd.ini` （Windows） 。


配置文件默认的内容如下：
```
[default]

conffile = /Users/rzeng/.wpcmd.ini

[site]

name        = my blog
url         = http://my blog/xmlrpc.php
user        = myname
password    = password123456
cachefile   = /Users/rzeng/.wpcmd.cache.py

# file

ext         = .md
draftfmt    = draft_%s

# directory

work        = /Users/rzeng/blog
draft       = draft
page        = page
post        = post
output      = output
media       = media
```

其中，name 为博客的名称，url 为博客的 xmlrpc.php 地址，user 和 password 为博客的管理密码，这些都是必须填写的。

work 代表 blog 源码所在的文件夹（绝对路径），其下的几个设置为相当于 work 的文件夹：

- draft 还没发布的文章源码；
- page 已经发布的页面；
- post 已经发布的文章；
- output 若要将 markdown 源码转换成 html ，则会写入这个文件夹；
- media 博客中使用的媒体文件，例如图片、资源、提供下载的压缩包。

要了解这些文件夹的具体内容，可参考 [本博客源码][4] 。

# 3.4 多博客配置

WPCMD 可以很容易管理多个 WordPress 博客。毕竟多个博客就是多个配置而已。

在配置文件中复制一份 `[site]` section 中的内容，然后将 `[site]` 改成 `[site1]` ，再修改 `[site1]` 下面的 `name/url/user/password/work` 等重要配置即可。

在使用的时候，可以通过 `--site` 参数指定你的博客配置。例如要查看新配置的博客的基本信息，可以这样写：

```
wpcmd show --site site1 -t option
```

这样，通过为 `--site` 参数指定不同的 section 名称，就能管理你的多个博客了。

# 4. 使用

（未完待续）

[1]: https://github.com/zrong/wpcmd
[2]: http://zengrong.net
[3]: http://zengrong.net/post/2374.htm
[4]: https://github.com/zrong/blog
[5]: http://zengrong.net/post/2187.htm
[6]: http://zengrong.net/post/2320.htm
[7]: http://zengrong.net/post/2294.htm

