[在 quick-cocos2d-x 中使用 DragonBonesCPP](http://zengrong.net/post/2133.htm)

Using DragonBonesCPP in quick-cocos2d-x.

# 1 前言

在 [DragonBones 官方C++版本 for cocos2d-x][1] 这篇文章中，我已经简单地介绍过了 [DragonBonesCPP][2] 这套用于取代 CCArmature 的库。

在我自己修改的 [quick-cocos2d-x][3] 版本中，我已经把 CCArmature 库删除，完全使用 DragonBonesCPP 。

我们的产品也完全使用 Flash 和 DragonBonesCPP 来制作骨骼动画。所有AS3版本的DragonBones提供的功能，在CPP版本中都能完整地实现。

几个月之前，我就已经将 DragonBonesCPP 整合到了[quick-cocos2d-x][3] 中，只是一直没有向官方库推送PR。这也是因为有几个内存泄露的BUG还没有解决。

现在，我终于有时间可以来做这件事。我的计划如下：

1. 写一篇关于 DragonBonesCPP 的教程（quick专用哦）；
2. 解决 DragonBonesCPP 的遗留问题，并进一步封装lua api方便使用；
3. 将 DragonBonesCPP 推送到quick的官方仓库。

那么，这篇文章就是第一件事了。<!--more-->

# 2 Samples and Codes

本文用到的所有 [范例文件][4] 在这里提供。性急的同学可以直接下载代码研究。

DragonBonesCPP 在quick中的内容，包含在这样几个路径下：

* [samples/dragonbones][4] 范例项目
* [extensions/DragonBones][5] C++库支持
* [luabinding/extensions/DragonBones][6] lua绑定
* [CCDragonBonesExtend][7] framework Extend支持
* [display.newDragonBones][8] framework display支持

==未完待续==

[1]: http://zengrong.net/post/2106.htm
[2]: https://github.com/DragonBones/DragonBonesCPP
[3]: https://github.com/zrong/quick-cocos2d-x
[4]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/samples/dragonbones
[5]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/lib/cocos2d-x/extensions/DragonBones
[6]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/lib/luabinding/extensions/DragonBones
[7]: https://github.com/zrong/quick-cocos2d-x/blob/zrong/framework/cocos2dx/CCDragonBonesExtend.lua
[8]: https://github.com/zrong/quick-cocos2d-x/blob/zrong/framework/display.lua#L503
