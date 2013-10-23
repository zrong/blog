获取CCArmature当前动画的播放状态

CCArmature是cocos2d-x中包含的一个扩展功能，用来实现骨骼动画。它是从DragonBones 2.2移植而来。

要使用CCArmature来播放骨骼动画，可以查看这里：[在cocos2d-x中使用DragonBones实现骨骼动画][usage] 。

DragonBones是使用Actionscript 3写成。在 [DragonBones的文档][dbevent] 中，我们可以看到Armature提供了一组事件 `boneFrameEvent/complete/loopComplete/movementChange/movementFrameEvent/start` 来通知动画状态的改变。

那么，CCArmature是怎么实现这些事件的？答案是： [sigslot][sigslot]

sigslot 是一套 C++ 实现的调用机制，在 [Qt][qt] 和 [Boost][signals] 中都有应用。Actionscript 3中也有它的一个实现，我曾经介绍过： [Signals框架介绍][as3signals] 。

CCArmatureAnimation 中定义了 MovementEventSignal 和 FrameEventSignal 这两个sigslot来发布状态改变事件。但从源码来看，FrameEventSignal 只是做了声明，并没有实现她。

下面介绍 MovementEventSignal 的用法。

[usage]: http://zengrong.net/post/1911.htm
[dbevent]: http://dragonbones.github.io/asdoc/V2/dragonBones/Armature.html
[sigslot]: http://sigslot.sourceforge.net/
[usagesigslot]: http://blog.csdn.net/smallcraft/article/details/2237802
[signals]: http://www.boost.org/doc/libs/1_54_0/doc/html/signals.html
[qt]: http://qt-project.org/
[as3signals]: http://zengrong.net/post/1504.htm
