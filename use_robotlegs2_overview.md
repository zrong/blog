[Robotlegs2中文教程-概述](http://zengrong.net/post/1859.htm)
====

## 废话

好久没写长文了，感觉平时写代码多了，在遣词造句上逐渐生疏起来。博客也慢慢写得七零八落，只有自己能看懂了。

趁介绍Robotlegs2的机会，锻炼一下文笔，看看自己还有没有被废掉。

本系列教程会比较长，完整目录会在这里更新：[use robotlegs2](http://zengrong.net/post/tag/userobotlegs2)。<!--more-->

## 提纲

先列个提纲，根据撰写进度会不断修改。

* 概述
* MVBundle的使用
* Context与Config
* Extension与Bundle
* hook
* ……
* SwiftSuspenders

## 前言

我的框架使用和选择过程比较有趣，先后经历了“没框架-PrueMVC-自己写框架-没框架-Robotlegs“的过程。

而使用了 [Robotlegs](http://www.robotlegs.org/) 之后，就没有再换过其他框架。Robotlegs小巧，易上手，使用也方便，非常适合中小型项目的开发。

Robotlegs2的开发进程一直很慢，但前段时间开发突然加速，接连发布了几个beta版本。到了现在的b6版本，整个框架已经比较稳定了。

Robotlegs2相对于Robotlegs1来说，是完全的重写。甚至说是两个不同的框架都不为过。v2的主要特点如下（来自官方网站） ：

* 更容易配置
* 更容易扩展
* 更好的模块支持
* 灵活的类型匹配

**我承认，上面的特点等于没说。**

每个重写的版本，大抵上都有类似的特点。因此，要深入理解Robotlegs2的特性，必须依赖实例。本系列教程也是基于实例来讲解。

## Robotlegs1

是否一定要先学习Robotlegs1，才能学习Robotlegs2？

**当然不需要。**

前面说过了，Robotlegs2是一个完全重写的版本。甚至连MVC模式都被剥离出来，使用插件来实现。熟悉Robotlegs 1对于理解Robotlegs 2必然有帮助，但并非必要。

本系列教程也不会将Robotlegs1作为阅读的必要条件。在教程中，由于某些需要，我可能会对v1和v2进行对比，但这个对比不会影响没有v1基础读者的理解。

当然，如果读者愿意学习一下Robotlegs1，我愿意提供一些资源：

* [Robotlegs最佳实践](https://github.com/robotlegs/robotlegs-documentation/blob/master/best-practices-zh-cn.textile)
* [ActionScript Developer's Guide to Robotlegs](http://shop.oreilly.com/product/0636920021216.do)

## SwiftSuspender

[SwiftSuspender](https://github.com/tschneidereit/Swiftsuspenders)是Robotlegs默认使用的注入器。在v1版本中，它是外置的。我们可以用其他注入器来替代它。

但是到了v2版本，该注入器已经被包含在了Robotlegs框架之中，而且不可替换。

## 小结

本章说了一些废话，简单介绍了Robotlegs2的一些特点。下章将从一个简单的实例来介绍Robotlegs2 MVCBundle的使用。
