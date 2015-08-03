title: 常用配置文件格式简析
date: 2015-08-03 15:35:14
modified: 2015-08-03 15:35:14
author: zrong
postid: $POSTID
slug: $SLUG
nicename: configuration-files
attachments: $ATTACHMENTS
posttype: draft
poststatus: publish
tags: study
category: technology

我大量使用过的配置文件主要有以下几种：

- [lua][lua]
- [python][python]
- [JSON][json]
- [XML][xml] 和 [Property list(PLIST)][plist]
- [.properties][properties]
- [INI][ini]
- [YAML][yaml]

在这些中间，我最喜欢的三种格式是： lua、INI 和 YAML ，最不喜欢的是 JSON 。下面简单的说说它们。

# 优秀的配置文件

我认为 **好的配置文件** 必须包含下面几个因素：

1\.	规则足够简单
2\. 人类友好
	在没有任何辅助工具的情况下清晰可读
3\.	支持简单的层级关系
4\.	允许注释

如果还包含下面几点，则可以认为是 **优秀的配置文件**：

5\.	逐行解析
	在数据不完整的情况下不影响解析
6\.	支持嵌套的层级关系
7\.	支持列表和字典
8\.	支持类型

# lua 和 python

在 lua 开发中，由于 lua 语言的特性，使用一个 lua 文件作为配置文件是很常见也很自然的事情。在使用 [quick-cocos2d-x][1] 进行游戏开发的日子里，我大量使用 lua 的这种特性，甚至直接在配置文件中包含简单的逻辑来替换 `_G` 中的全局变量。而在使用这些配置文件的时候，只需要简单地 `require` 它们，lua 解释器会帮我们搞定一切。

当然，lua 作为配置文件的这种方便是 lua 解释器提供的，这也限制了 lua 配置文件的通用性。我们应该尽量在 lua 程序中使用 lua 作为配置文件。离开这个框架，则不太合适了。

python 的情况也类似。在 python 中，我将一个 dict 直接 [dump][2] 成为字符串，在使用这个配置文件的时候，使用 [eval][3] 解析。显然，这样使用并没有 lua 那样方便。 

严格来说，这两种格式算不得配置文件。因为它们在特定的语言范畴易用，但缺乏跨语言和跨环境的通用性。

然而，我们可以使用语言的解析器来解析它们，可以不需要任何外部库可能直接使用它们，它们还完全符合我上面定义的 “好的配置文件” 标准。在没有其它选择（或不愿意进行选择），不考虑跨语言的前提下，它们用起来是挺不错的。

# JSON —— 糟糕
# .properties 和 INI
# XML 和 PLIST —— 虐心（也虐手）
# YAML —— 堪称完美

（未完待续）

[lua]: http://www.lua.org
[xml]: http://www.w3.org/XML/
[python]: https://www.python.org/
[json]: http://json.org
[properties]: https://en.wikipedia.org/wiki/.properties
[ini]: https://en.wikipedia.org/wiki/INI_file
[plist]: https://en.wikipedia.org/wiki/Property_list
[yaml]: http://yaml.org/
[pjava]: http://docs.oracle.com/javase/7/docs/api/java/util/Properties.html
[1]: http://zengrong.net/post/tag/cocos2d-x
[2]: https://github.com/zrong/rookout/blob/master/rookout/conf.py#L68
[3]: https://github.com/zrong/rookout/blob/master/rookout/conf.py#L93
