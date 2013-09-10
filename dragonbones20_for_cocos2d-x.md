[cocos2d-x专用的DragonBones2.2](http://zengrong.net/post/1915.htm)

我写过一篇 [在cocos2d-x中使用DragonBones][using] ，这篇文章中提到了DragonBones插件。本篇是一个补充。

## 插件问题

在 [CocoStudio官方下载页面][dragonbones2] 中提供了一个DragonBones插件，用于导出cocos2d-x可以识别的骨骼动画格式。

**但是，这个插件有个问题。**

在导出时，如果使用“Zip(XML和分开的PNG)”类型（事实上，对于cocos2d-x来说，只能选择这个选项），同时设置“导出缩放比”选项不为1的时候，导出的元数据文件中的坐标都没有经过缩放。<!--more-->

![Export Scale][exportscale]

这将导致动画在播放的时候出现问题，就像这样：

![dragon error][dragonerr]

其实，这个问题并不是由于修改DragonBones所形成的，而是原来的DragonBones2.0就存在这个问题。

如果你有兴趣研究的话，可以看这里 [ExportDataCommand.as][db20bug] ，这里判断了 `_exportType` 值为4的情况下不缩放坐标。而“Zip(XML和分开的PNG)”就代表4。

另外，这个插件是基于2.0版本，而目前的DragonBones最新版本是2.3。当然，由于 [2.3的DataFormat改动太大][v222v23] ，暂时不能使用v2.3版本进行修改。但v2.2是可以的。

如果你再次有兴趣的话，可以找到cocos2d-x负责解析骨骼动画元数据的类 `[cocos2d-x]\extensions\CCArmature\utils\CCDataReaderHelper.cpp` ，通过修改它，来支持新的格式。

## DragonBone2.2 for cocos2d-x

基于上面的原因，我以DragonBones2.2版本为基础制作了这个插件，并重新打包发布。项目的源码在这里：[DragonBones2.2 for cocos2d-x][dbdp4cocos2dx]

我做的工作并不多，只是花了一些时间理解了DragonBonesDesignPanel的结构。

* 这个项目包含了 [SkeletonAnimationLibrary][dbl22] 和 [SkeletonAnimationDesignPanel][dbdp22] 项目v2.2的内容，做了极少量的修改；
* jsfl的修改，直接比较 [这3个文件即可][c2]。其中 `skeleton.jsfl.original` 是原始文件， `skeleton.jsfl.20cocos2dx` 是2.0修改版提供的文件， `skeketon.jsfl` 是我修改的文件；
* 导出面板中，我增加了一种导出类型 “Zip(XML and PNGs, for cocos2d-x)”；
* <img src="/wp-content/uploads/2013/08/export2.png" alt="export2" width="360" height="320" class="aligncenter size-full wp-image-1920" />
* 我修改了导入代码，现在也能在DesignPanel中导入使用上面的类型导出的资源；
* 其他的修改，请直接比较源码；
* 如何使用可以看这里： [在cocos2d-x中使用DragonBones][using]。

感谢 DragonBones Team 带来这样优秀的软件；

感谢对 DragonBones2.0 进行修改的程序员；

希望这个项目对你们有用。

[using]: http://zengrong.net/post/1911.htm
[dragonbones2]: http://bbs.cocostudio.org/forum.php?mod=viewthread&tid=4699&page=1&extra=#pid7518
[db20bug]: https://github.com/DragonBones/SkeletonAnimationDesignPanel/blob/v2.0/src/control/ExportDataCommand.as#L69
[v222v23]: https://github.com/DragonBones/SkeletonAnimationLibrary/wiki/Move-from-V2.2-to-V2.3
[dbdp4cocos2dx]: https://github.com/zrong/dragonbones-for-cocos2d-x
[dbdp22]: https://github.com/DragonBones/SkeletonAnimationDesignPanel/tree/V2.2
[dbl22]: https://github.com/DragonBones/SkeletonAnimationLibrary/tree/V2.2
[c1]: https://github.com/zrong/dragonbones-for-cocos2d-x/blob/master/src/control/ExportDataCommand.as#L222
[c2]: https://github.com/zrong/dragonbones-for-cocos2d-x/tree/master/build/DragonBonesDesignPanel
[dragonerr]: dragon_err.png
[exportscale]: export_scale.png
