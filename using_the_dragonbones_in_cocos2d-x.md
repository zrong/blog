在cocos2d-x中使用DragonBones

## 基础知识

要看懂本文，你需要了解骨骼动画（或称关节动画）是什么，以及DragonBones是什么。下面提供了一些资料：

* [Skeletal Animation (Wikipedia en)][skeletalani]
* [DragonBones 2.1快速入门指南][dragonbonesstarted]
* [Skeletal Animation (cocos2d-x wiki en)][skeletalanicocos2d]
* [骨骼动画详解 (泰然网)][skeletalanicocos2d]

## 不要使用官方版本的DragonBones

在写这篇文章的时候，DragonBones的官方版本为v2.3。cocos2d-x的稳定版本为2.1.5。

为了使用cocos2d-x，我们需要选择 Zip(XML and PNGs) 的方式，将图像文件导出为独立的图像帧加上XML格式的元数据文件。官方版本的DragonBones，会将元数据分成texture.xml和skeleton.xml两个文件，而cocos2d-x目前不支持这种情况。

因此，我们需要使用修改过的DragonBones插件。在CocoStudio的官方论坛中提供了一个这样的插件，版本是2.0版本。

使用这个版本的插件，在导出图像文件的时候，会将texture.xml和skeleton.xml文件合并成1个，同时会修改元数据中的部分格式，使其满足cocos2d-x的解析库要求。

## 为什么不用CocoStudio

CocoStudio 

[skeletalani]: http://en.wikipedia.org/wiki/Skeletal_animation
[dragonbonesstarted]: http://dragonbones.github.io/getting_started_cn.html
[skeletalanicocos2d]: http://www.cocos2d-x.org/projects/cocos2d-x/wiki/Skeletal_Animation
[skeletalanicocos2dcn]: http://www.ityran.com/archives/3446
[cocostudiodl]: http://bbs.cocostudio.org/forum.php?mod=viewthread&tid=4699&extra=page%3D1
