title: WPCMD
date: 2015-06-12 09:40:22
modified: 2015-06-12 09:40:22
author: zrong
postid: 2321
slug: 2321
nicename: wpcmd
attachments: $ATTACHMENTS
posttype: page
poststatus: publish

[WPCMD(Wordpress command)][1]  是一个通过 Wordpress XML-RPC 接口在本地创建、更新 Wordpress 博客的命令行工具。 [zengrong.net][2] 就是使用该工具进行管理。

# 依赖

- python 3.4 or higher
- Markdown>=2.6.2
- Pygments>=2.0.2
- python-wordpress-xmlrpc>=2.3
- rookout>=0.4.5

# 安装

`pip3 install wpcmd`

因为包比较多，想快点也可以使用豆瓣的镜像站来安装（详情可参考 [常用镜像站整理][2]）：

`pip3 install -i https://mirrors.ustc.edu.cn/pypi/web/simple wpcmd`

# 配置

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


# 使用

（未完待续）

[1]: https://github.com/zrong/wpcmd
[2]: http://zengrong.net
[3]: http://zengrong.net/post/2374.htm
[4]: https://github.com/zrong/blog
