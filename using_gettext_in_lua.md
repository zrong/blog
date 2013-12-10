在Lua中使用gettext实现多语言支持

[gettext][2] 是一套优秀的国际化工具。在 linux 中被大量采用。wordpress 也使用gettext实现多语言支持。

本文介绍如何在 quick-cocos2d-x 中使用 gettext 做多语言支持。同时介绍多语言翻译工具 poedit 对 Lua 语言的支持。<!--more-->

## gettext 简介

gettext 是一套工具集的名称。这套工具集包含 xgettext/msginit/msgfmt 等一套建立模版(POT)、创建PO文件和编译MO文件的工具。

使用 gettext 需要涉及这样几个概念：

* 源码  
程序的源代码，本文中是lua文件；
* POT 文件  
从源码中扫描得到的翻译模版文件，原始语言取决于源码中使用的语言，建议使用英文，纯文本格式；
* PO 文件
根据 POT 文件建立的各种语言版本的待翻译文件，其中包含原始语言和被翻译的目标语言，纯文本格式；
* MO 文件
供最终软件实际使用的文件，使用PO编译而成，二进制格式。

一般的工作流程是这样的：

1. 在源码中使用特殊的语法来书写字符串，C语言默认是 `gettext("my text")`。在本文中，将使用 `_("my text")` ；
1. 使用 xgettext 从源码中扫描出需要翻译的文本，建立 POT 文件；
1. 使用 msginit 命令根据 POT 文件建立 PO 文件。或者直接在上一步也可以直接建立PO文件；
1. 进行人工翻译（当然也可以进行机器翻译）；
1. 使用 msgfmt 命令将 PO 文件编译成 MO 文件；
1. 在程序中实现调用命令，本文中是 `_` 函数，读取 MO 文件，根据调用的原始语言文本返回翻译之后的文本。

## poedit 简介

## 翻译 PO 文件

## 在 Lua 中解析 mo 文件

## 完整范例

[1]: http://www.poedit.net
[2]: http://www.gnu.org/software/gettext/
[3]: http://www.gnu.org/software/gettext/manual/html_node/xgettext-Invocation.html#xgettext-Invocation

