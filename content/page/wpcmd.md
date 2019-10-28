+++
title = "WPCMD"
postid = 2321
date = 2015-06-12T09:40:22+08:00
isCJKLanguage = true
toc = true
type = "page"
slug = "wpcmd"
url = "/wpcmd/"
+++


我 2003 年开始写博客，经历过一次数据丢失，现在的博客 [blog.zengrong.net][2] 从2005 年起开始更新，一直没有中断。虽然 WordPress 的编辑功能越来越强大，而且也有大量的博客写作工具，但我都用不习惯。我总希望用一种更方便更简单（更适合程序员）的方式来管理博客。

2014 年的时候我考虑过 [博客静态化][5]，但现有的博客静态化工具不太符合我的要求，因此我准备自己造个轮子。造轮子的工程未免复杂，为了满足在轮子诞生之前的更新欲望，[WPCMD][1] 诞生了。

WPCMD 的源码托管在 [Github][1] 上。

# 1. WPCMD 是什么

[WPCMD(WordPress command)][1]  是一个通过 WordPress XML-RPC 接口在本地创建、更新 WordPress 博客的命令行工具。 [zengrong.net][2] 就是使用该工具进行管理。

简单的说，WPCMD 就是一个用于 WordPress 的命令行工具。而且，由于没有 GUI 界面，这个工具是主要面向技术类博主的。

这是一些优点：

- 使用 MarkDown 语法写博客；
- 随意选择自己最喜欢的版本管理来保存博客文章（例如我用 [Github][4] ）；
- 随意选择自己最喜欢的编辑器编写博客（例如我一直用 [Vim][8] ）；
- 生成 [所有文章的列表][9] ；
- 生成文章的 HTML 文件；
- 不用打开 WordPress 后台就能完成：
    1. 文章和页面的创建和更新；
    2. 文章内媒体文件的自动上传；
    3. 分类和标签的创建和更新；
    4. 查看博客文章/页面/分类/标签/媒体等信息。
- 使用 [Fenced Code Extra ][6] 支持：
    1. [graphviz][7] ；
    2. 语法高亮；
    3. 代码注释。
- 同时管理多个 WordPress 博客。

<a name="hellowpcmd"><a>
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

## 3.2 安装

`pip3 install wpcmd`

因为包比较多，想快点也可以使用国内的镜像站来安装，下面使用的是中国科学技术大学的镜像源：（详情可参考 [常用镜像站整理][2]）：

`pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple wpcmd`

## 3.3 配置

输入 `wpcmd -h` ，第一次运行会生成一个默认的配置文件，必须修改这个配置文件进行设置。这个配置文件位于 `~/.wpcmd.ini`（OS X 和 Linux) 和 `%HOME%\_wpcmd.ini` （Windows） 。


配置文件默认的内容如下：

```
[site]

name        = my blog
url         = http://my blog/xmlrpc.php
user        = myname
password    = password123456
# Mac or Linux
cachefile   = /Users/zrong/.wpcmd.cache.py
# Windows
# cachefile = C:\Users\zrong\_wpcmd.cache.py

# file

ext         = .md
draftfmt    = draft_%s

# directory

# Mac or Linux
work        = /Users/zrong/blog
# Windows
# cachefile = C:\Users\zrong\blog
draft       = draft
page        = page
post        = post
output      = output
media       = media
```

其中，name 为博客的名称，url 为博客的 xmlrpc.php 地址，user 和 password 为博客的管理密码，这些都是必须填写的。

<a name="dir">
work 代表 blog 源码所在的文件夹（绝对路径），其下的几个设置为相当于 work 的文件夹：

- draft 还没发布的文章源码；
- page 已经发布的页面；
- post 已经发布的文章；
- output 若要将 markdown 源码转换成 html ，则会写入这个文件夹；
- media 博客中使用的媒体文件，例如图片、资源、提供下载的压缩包。

要了解这些文件夹的具体内容，可参考 [本博客源码][4] 。

## 3.4 多博客配置

WPCMD 可以很容易管理多个 WordPress 博客。毕竟多个博客就是多个配置而已。

在配置文件中复制一份 `[site]` section 中的内容，然后将 `[site]` 改成 `[site1]` ，再修改 `[site1]` 下面的 `name/url/user/password/work` 等重要配置即可。

在使用的时候，可以通过 `--site` 参数指定你的博客配置。例如要查看新配置的博客的基本信息，可以这样写：

```
wpcmd show --site site1 -t option
```

这样，通过为 `--site` 参数指定不同的 section 名称，就能管理你的多个博客了。

## 3.5 代码高亮配置

WPCMD 使用 [Pygments][10] 来实现代码高亮，因此，我们需要生成一个 css 文件加入到 WordPress 的模版中，代码高亮才能生效。

安装了 WPCMD 后，就可以使用 `pygmentize` 命令来生成这个 css 文件。

查看所有支持的 style：

```
-> % pygmentize -L styles
Pygments version 2.0.2, (c) 2006-2014 by Georg Brandl.

Styles:
~~~~~~~
* paraiso-dark:

* default:
    The default style (inspired by Emacs 22).
* emacs:
    The default style (inspired by Emacs 22).
* murphy:
    Murphy's style from CodeRay.
* igor:
    Pygments version of the official colors for Igor Pro procedures.
* perldoc:
    Style similar to the style used in the perldoc code blocks.
* xcode:
    Style similar to the Xcode default colouring theme.
* monokai:
    This style mimics the Monokai color scheme.
* colorful:
* manni:
* pastie:
* rrt:
* bw:

* paraiso-light:

* trac:
* tango:
* native:
* autumn:
* friendly:
* vs:
* vim:
* borland:
* fruity:
```

然后选择一个自己喜欢的格式生成 css 文件。在下面的代码中，我使用 `-S` 参数指定生成类似于 vim 7.0 的代码高亮效果，并指定了一个文件名。

```
-> % pygmentize -S vim -f html > codehilite.css
```

接着，把这个生成的 css 文件上传到 WordPress 文件夹，并在 WordPress 模版的 style.css 文件中加入这一行（注意修改路径，我使用的是子模板）：

``` css
@import url("/wp-content/themes/twentyfifteen_child/codehilite.css");
```

# 4. 使用

WPCMD 有4个子命令，主要作用如下：

- new  
创建新的文章、页面、分类或标签；
- update  
更新已有的文章、页面、分类或标签。这是使用最频繁的命令；
- show  
显示指定 WordPress 站点的文章、页面、分类、标签、选项和媒体文件信息；
- util  
一些工具，最有用的就是生成文章列表页面。

要查看这些子命令的详细帮助，可以使用 `wpcmd {subcommand} -h` 。例如 `wpcmd update -h` 就查看 update 命令的详细用法。

## 4.1 new

使用 new 命令可以创建4种类型的内容：

- category 对应 WordPress 中的分类目录。
- tag 对应 WordPress 中的标签；
- post 对应 WordPress 中的文章；
- page 对应 WordPress 中的页面；

### 4.1.1 创建分类目录

下面的命令创建一个名为 `PHP` ，别名为 `php` ，描述为 『世界上最好的语言』的分类目录。

```shell
-> % wpcmd new -t category -q php "PHP" "世界上最好的语言"
Save '/Users/zrong/.wpcmd.cache2.py' done.
Get term from WordPress, query: ['category', 'php'], result: None
The term PHP(21) has created.
Save '/Users/zrong/.wpcmd.cache2.py' done.
The term PHP has saved.
```

也可以简化一下，只为 `-q` 提供一个参数。这样就会创建一个别名和名称都是 `php` 的标签，但这样一来，PHP 就不是世界上最好的语言了：

```shell
-> % wpcmd new -t category -q php
```

### 4.1.2 创建标签

在 WordPress 的数据库中，无论是标签还是分类目录，都是放在 `wp_terms` 表中，它们的区别仅仅是 `taxonomy` 不同。一个是 `category` ，一个是 `post_tag` 。

所以，创建一个标签，只需要为 `-t` 参数传递 `post_tag` 即可。我在处理标签的时候做了简化，使用 `tag` 和 `post_tag` 都是可以的。

```shell
-> % wpcmd new -t tag -q python Python "Python 语言相关"
Save '/Users/zrong/.wpcmd.cache2.py' done.
Get term from WordPress, query: ['post_tag', 'python'], result: None
The term Python(20) has created.
Save '/Users/zrong/.wpcmd.cache2.py' done.
The term Python has saved.
```

### 4.1.3 创建文章

创建的文章处于 `draft` 文件夹中。下面的代码将创建 `draft/draft_wpcmd.md` 这篇文章：

```shell
-> % wpcmd new -t post -q wpcmd
The draft file "/Users/zrong/blog/draft/draft_wpcmd.md" has created.
```

也可以提供 `-q` 参数，这样会自动用数字作为文件名：

```shell
-> % wpcmd new -t post
The draft file "/Users/zrong/blog/draft/draft_1.md" has created.
```

创建出来的文章的默认内容如下：

```
title:
date: 2015-11-28 21:44:38
modified: 2015-11-28 21:44:38
author: zrong
postid: $POSTID
slug: $SLUG
nicename:
attachments: $ATTACHMENTS
posttype: post
poststatus: draft
tags:
category: technology
```

这里的 Metadata 是使用 [Python-Markdown][11] 的 [Metadata 插件修改版][12] 来解析的的。默认的插件认为 Metadata 是无序的，而 WPCMD 需要它们是有序的。

我们需要对这些 Metadata 填充内容。下面是个具体填写说明：

```
title: 这里填写标题
date: 创建日期
modified: 修改日期
author: 作者
postid: 不必修改，这个值会在提交到 WordPress 之后自动替换成 Post ID 的值
slug: 不必修改，将被自动替换，一般情况下值与 nicename 相同
nicename: 填写 URL 友好的名称，若不填写则会自动使用 title 的 BASE64 编码
attachments: 不必修改，文中若包含图片等上传的内容，则该值被替换成这些上传内容的 Post ID
posttype: 值为 post 或者 page
poststatus: 值为 draft（不可发布）或者 publish（允许发布到 WordPress）
tags: 标签，允许为空，使用英文半角逗号分隔，标签必须在 WordPress 中存在
category: 分类目录，必填，必须在 WordPress 中存在
```

接下来，就可以使 Markdown 语法进行博客的撰写了。支持下面的插件：

- [Fenced Code Extra ][6]
- [Tables][13]
- [CodeHilite][14]
- [Table of Contents][16]

这里有 [大量的源码][15] 可以参考。

### 4.1.4 创建页面

创建页面和创建文章的方法类似，只是需要为 `-t` 参数传递 `page` 。

```
-> % wpcmd new -t page
The draft file "/Users/zrong/blog/draft/draft_2.md" has created.
```

生成的文档也类似，不过 Metadata 会不包含 tag 和 category ：

```
title:
date: 2015-11-28 22:23:00
modified: 2015-11-28 22:23:00
author: zrong
postid: $POSTID
slug: $SLUG
nicename:
attachments: $ATTACHMENTS
posttype: page
poststatus: draft
```

## 4.2 update

使用 update 命令可以更新6种类型的内容：

- category 对应 WordPress 中的分类目录。
- tag 对应 WordPress 中的标签；
- post 对应 WordPress 中的文章；
- page 对应 WordPress 中的页面；
- option 对应 WordPress 中的设置选项；
- draft 对应在 WordPress 中尚不存在（但存在于 draft 文件夹）中的草稿。

### 4.2.1 更新分类目录和标签

更新这两者的语法和 new 完全相同，只是需要将 new 换成 update：

```
-> % wpcmd update -t category -q php "PHP" "世界上最糟的语言"
```

### 4.2.2 更新文章和页面

这分为两种情况：在 WordPress 中还不存在的文章，以及已经存在于 WordPress 中的文章。

对于在 WordPress 中 **还不存在** 的新文章来说，需要使用 `-t draft` 类型来进行更新。下面的命令把 `draft/draft_1.md` 这篇文章更新到 WordPress 上（ `-q` 参数不必添加 `draft_` 前缀）：

```
-> % wpcmd update -t draft -q 1
```

在这种更新过程中，WPCMD 将会做下面的事：

1. 将 Markdown 格式转换成 HTML 格式；
2. 将 HTML 格式发布到 WordPress 上；
3. 获取新文章的 Post ID，用它替换 Markdown 源文件的 Metadata 中的 `$POSTID`  ;
4. 更新 `$SLUG` 的值；
5. 将 `draft/draft_1.md` 文件移动并改名为 `post/{postid}.md` ，`postid` 就是刚才得到的值。

对于 **已存在** 于 WordPress 的文章或者页面，就需要使用 `-t post` 或者 `-t page` 类型了：

```
-> % wpcmd update -t page -q wpcmd
Old article:
id=2321, date=2015-06-12 01:40:22, date_modified=2015-11-22 14:04:15, slug=wpcmd, title=WPCMD, post_status=publish, post_type=page
Update 2321 successfully!
```

在这种更新过程中，WPCMD 会做上面的1、2两步，后面的步骤都不会发生。

注意，由于更新文章是最常见的操作，因此 `-t` 参数的默认值就是 `post` 。更新文章时，可以仅仅提供 `-q` 参数。

### 4.2.3 在文章和页面中包含图像

WPCMD 会自动检测文章中的图像文件，将其上传到 WordPress 中。但这需要遵循一些特殊的规则：

1. 要上传的图像必须放在 media&#47;draft&#47; 文件夹中；
2. 必须使用 media&#47;draft&#47;imagefile 的形式提供图像文件的 URL。下面是个范例：


`![myimage](media`&#47;`draft`&#47;`myimage.jpg)`

当然你也可以采用另一种语法：

`Some text ....`

`![myimage][img1]`

`Another text ....`

`[img1]: media`&#47;`draft`&#47;`myimage.jpg`

使用这种规则，在更新文章和页面的时候，WPCMD 会做下面的事：

1. 自动扫描复合规则的图像，将其上传到 WordPress 中；
2. 获得已上传文件的 Post ID ，用它替换 Markdown 源文件的 Metadata 中的 `$ATTACHMENTS` ；
3. 获取已上传文件的 URL 地址，用它替换 media&#47;draft&#47;myimage.jpg ；
4. 在 `media` 文件夹下建立对应的年、月文件夹，讲这张已经上任的图像文件移动到对应的文件夹中。

在完成上述操作后，上面的 Markdown 源码会变成如下所示（以 zengrong.net 为例）：

```
![myimage](/wp-content/upload/2015/11/myimage.jpg)
```

同时 media&#47;draft&#47;myimage.jpg 将移动到 media&#47;2015&#47;11&#47;myimage.jpg 。

### 4.2.4 输出 HTML 格式源码

为了提前查看效果，我们也可以不将内容发布到 WordPress ，而是先行输出一个 HTML 文件查看效果。使用 update 命令的 `-o` 参数指定输出文件名即可完成：

```
-> % wpcmd update -t page -q wpcmd -o wpcmd.html
```

上面的命令会生成文件 `output/wpcmd.html` 。

注意这里生成的文件是一个不完整的 HTML 文件，仅包含正文的 HTML 信息，没有 `<html> <head> <body>` 等标签。因此若包含中文，直接用浏览器打开会显示乱码。此时手动指定一下页面编码为 `UTF-8` 即可。

## 4.3 show

show 命令显示博客的信息，使用 `-t` 或 `--type` 参数指定信息的类型，目前有这样几种类型可以显示：

- option 从 Wordpress 中查询博客的基础信息并显示
- post（远程列表） 从 Wordpress 中查询博客文章列表并显示
- page（远程列表） 从 Wordpress 中查询博客页面列表并显示
- draft（本地列表） 显示位于 [draft](#dir) 文件夹中的的所有草稿 markdown 源文件路径
- tax（远程列表） 从 Wordpress 中查询所有可用的分类类型
- term 使用 tax 类型查到的分类类型，显示这些分类关键词列表
- category（本地列表） 从本地缓存中查询博客中的文章分类并显示
- tag（本地列表） 从本地缓存查询博客中的 tag 并显示
- medialib（远程列表） 从 Wordpress 中查询博客中已经上传的媒体文件信息
- mediaitem（远程列表） 从 Wordpress 中查询博客中已经上传的某个媒体文件信息，需要指定一个媒体文件 ID

### 4.3.1 post 和 page

对于 post 和 page 这两种类型，可以使用 `-n` 或者 `--number` 来指定显示几条信息。在我的博客上执行下面的命令，会显示最新的两篇文章的基本信息：


```
-> % wpcmd show -t post -n 2
id=2441, date=2016-02-12 12:30:54, date_modified=2016-02-12 13:50:44, slug=pebble-classic, title=Pebble Classic 的售后和花屏维修, post_status=publish, post_type=post
id=2434, date=2016-01-29 09:30:17, date_modified=2016-01-30 15:35:11, slug=how-to-choose-in-management-and-technology, title=在技术和管理中选择, post_status=publish, post_type=post
```

使用 `-d` 或者 `--order` 可以实现列表排序，默认是按时间倒序 `DESC` ，如果设置为 `ASC` 则显示最老的两篇文章:

```
-> % wpcmd show -t post -n 2 -d ASC
id=23, date=2005-04-25 05:21:48, date_modified=2005-10-10 05:28:52, slug=creative-commons, title=创作共用（Creative Commons） , post_status=publish, post_type=post
id=19, date=2005-04-27 15:14:22, date_modified=2007-12-30 15:03:11, slug=display_errors, title=终于解决了Mambo出错的问题, post_status=publish, post_type=post
```

使用 `-o` 或者 `--orderby` 参数可以指定是按 `post_modified` 排序还是按 `post_id` 排序。

### 4.3.2 medialib 和 mediaitem

下面的命令显示最新上传的两个媒体文件信息：

```
-> % wpcmd show -t medialib -n 2
field:{'number': 2}
id=2442, parent=2441, title=watch3, description=, caption=, date_created=2016-02-12 13:32:20, link=http://zengrong.net/wp-content/uploads/2016/02/watch3.jpg, thumbnail=http://zengrong.net/wp-content/uploads/2016/02/watch3-150x150.jpg, metadata={'width': 721, 'file': '2016/02/watch3.jpg', 'height': 1280, 'sizes': {'medium': {'width': 169, 'mime-type': 'image/jpeg', 'file': 'watch3-169x300.jpg', 'height': 300}, 'post-thumbnail': {'width': 721, 'mime-type': 'image/jpeg', 'file': 'watch3-721x510.jpg', 'height': 510}, 'thumbnail': {'width': 150, 'mime-type': 'image/jpeg', 'file': 'watch3-150x150.jpg', 'height': 150}, 'large': {'width': 577, 'mime-type': 'image/jpeg', 'file': 'watch3-577x1024.jpg', 'height': 1024}}, 'image_meta': {'iso': '0', 'orientation': '0', 'caption': '', 'credit': '', 'focal_length': '0', 'camera': '', 'title': '', 'created_timestamp': '0', 'copyright': '', 'shutter_speed': '0', 'keywords': [], 'aperture': '0'}}
id=2440, parent=2441, title=watch4.jpg, description=, caption=, date_created=2016-02-12 13:27:29, link=http://zengrong.net/wp-content/uploads/2016/02/watch4.jpg, thumbnail=http://zengrong.net/wp-content/uploads/2016/02/watch4-150x150.jpg, metadata={'width': 721, 'file': '2016/02/watch4.jpg', 'height': 1280, 'sizes': {'medium': {'width': 169, 'mime-type': 'image/jpeg', 'file': 'watch4-169x300.jpg', 'height': 300}, 'post-thumbnail': {'width': 721, 'mime-type': 'image/jpeg', 'file': 'watch4-721x510.jpg', 'height': 510}, 'thumbnail': {'width': 150, 'mime-type': 'image/jpeg', 'file': 'watch4-150x150.jpg', 'height': 150}, 'large': {'width': 577, 'mime-type': 'image/jpeg', 'file': 'watch4-577x1024.jpg', 'height': 1024}}, 'image_meta': {'iso': '0', 'orientation': '0', 'caption': '', 'credit': '', 'focal_length': '0', 'camera': '', 'title': '', 'created_timestamp': '0', 'copyright': '', 'shutter_speed': '0', 'keywords': [], 'aperture': '0'}}
```

从上面的信息中，我们可以知道 id 为 2442 的媒体文件是一张图片，也知道了它的尺寸、URL 路径以及所属的文章 ID 为 2441 。


如果希望只看特定的媒体文件信息，可以指定媒体文件的 id：

```
-> % wpcmd show -t mediaitem -q 2442
```

### 4.3.3 category/tag 和 term/tax

category 和 tag 直接显示本地缓存的文章分类和标签信息。在 Wordpress 中， `tag` 原名为 `post_tag` ，它和 `category` 一样都是 `term` 。

因此，下面两条命令是同义语：

```
-> % wpcmd show -t tag
-> % wpcmd show -t term -q post_tag
```

同样的，下面两条命令也是同义语：

```
-> % wpcmd show -t category
-> % wpcmd show -t term -q category
```

使用 tax 可以查到 Wordpress 支持哪些 term ：

```
-> % wpcmd show -t tax
category
post_tag
post_format
```

## 4.4 util

util 是一些批量处理博客的小工具，目前仅有 `-r , --readme` 这条命令有意义。它会生成一个 README.md 文件，效果请查看 [README.md][9] 。

（全文完）

[1]: https://github.com/zrong/wpcmd
[2]: https://blog.zengrong.net
[3]: https://blog.zengrong.net/post/2374.html
[4]: https://github.com/zrong/blog
[5]: https://blog.zengrong.net/post/2187.html
[6]: https://blog.zengrong.net/post/2320.html
[7]: https://blog.zengrong.net/post/2294.html
[8]: https://blog.zengrong.net/tag/#vim
[9]: https://github.com/zrong/blog/blob/master/README.md
[10]: http://pygments.org
[11]: http://pythonhosted.org/Markdown/
[12]: https://github.com/zrong/wpcmd/blob/master/wpcmd/mde/metadata.py
[13]: http://pythonhosted.org/Markdown/extensions/tables.html
[14]: http://pythonhosted.org/Markdown/extensions/code_hilite.html
[15]: https://github.com/zrong/blog/tree/master/post
[16]: http://pythonhosted.org/Markdown/extensions/toc.html
