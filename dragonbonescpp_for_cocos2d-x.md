[DragonBones 官方C++版本 for cocos2d-x](http://zengrong.net/post/2106.htm)

DragonBonesCPP for cocos2d-x

[DragonBones][1] 是基于Flash技术开发的一套骨骼动画编辑工具+解析库+渲染库。详细的入门介绍可以看这里：[DragonBones快速入门指南][3] 。

cocos2d-x 中自带的 CCArmature 是移植自 DragonBones 2.1 版本，我对 DragonBones Design Panel进行了修改 [cocos2d-x专用的DragonBones2.2][4] ，使其直接输出让 CCArmature 支持的资源格式。

但是，CCArmature 有一些问题。它不支持逐帧动画，对嵌套骨骼支持不力，不支持将某个Bone替换成逐帧动画等等，还有 [cocos2d-x中CCArmature展示挤压和变形动画的问题][5] 这些硬伤。

由于 CCArmature 要支持 cocostudio 软件，因此对 CCArmature 进行了许多修改，导致新版本的 CCArmature 对 DragonBones Design Panel 生成的资源格式的支持也不够好了。详情见：[在cocos2d-x中使用DragonBones实现骨骼动画][2] 。

正是因为这些问题，[DragonBones 开发组][10] 使用 C++ 移植了 DragonBones 的解析库和动画渲染库，命名为 [DragonBonesCPP][6] 。这套库完全与ActionScript 3 库保持一致，可以实现 ActionScript 3 库的所有功能。另外，这套库还可以支持多套渲染引擎。

目前，DragonBonesCPP 首先完成了对 cocos2d-x 引擎的支持。下面是一些Demo：

* [DragonBonesCPP for cocos2d-x 2.x][7]
* [DragonBonesCPP for cocos2d-x 3.x][8]
* [DragonBonesCPP for quick-cocos2d-x][9]

目前已知的问题：

1. 仅支持 XML+PNG 格式的资源，不支持其他格式；
2. 可能有一些内存泄露；
3. 没有做异步资源加载，可能会导致在加载资源时候的性能问题。

[1]: http://dragonbones.github.io/
[2]: http://zengrong.net/post/1911.htm
[3]: http://dragonbones.github.io/DBGettingStarted_V2.0_cn.html
[4]: http://zengrong.net/post/1915.htm
[5]: http://zengrong.net/post/1922.htm
[6]: https://github.com/DragonBones/DragonBonesCPP
[7]: https://github.com/DragonBones/DragonBonesCPP/tree/dev/demos/cocos2d-x-2.x
[8]: https://github.com/DragonBones/DragonBonesCPP/tree/dev/demos/cocos2d-x-3.x
[9]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/samples/dragonbones
[10]: https://github.com/DragonBones
