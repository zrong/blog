[在cocos2d-x中使用DragonBones](http://zengrong.net/post/1911.htm)

## 基础知识

要看懂本文，你需要了解骨骼动画（或称关节动画）是什么，以及DragonBones是什么。下面提供了一些资料：

* [Skeletal Animation (Wikipedia en)][skeletalani]
* [DragonBones 2.1快速入门指南][dragonbonesstarted]
* [Skeletal Animation (cocos2d-x wiki en)][skeletalanicocos2d]
* [骨骼动画详解 (泰然网)][skeletalanicocos2d]

To flash veteran: do you remember the 'Moho'? <!-- more -->

## 不要使用官方版本的DragonBones

在写这篇文章的时候，DragonBones的官方版本为v2.3。cocos2d-x的稳定版本为2.1.5。

为了使用cocos2d-x，我们需要选择 Zip(XML and PNGs) 的方式，将图像文件导出为独立的图像帧加上XML格式的元数据文件。官方版本的DragonBones，会将元数据分成texture.xml和skeleton.xml两个文件，而cocos2d-x目前不支持这种情况。

因此，我们需要使用修改过的DragonBones插件。在[CocoStudio的官方论坛中提供了一个这样的插件][cocostudiodl]，版本是2.0。

使用这个版本的插件，在导出图像文件的时候，会将texture.xml和skeleton.xml文件合并成1个，同时会修改元数据中的部分格式，使其满足cocos2d-x的解析库要求。

**注意：下面提到DragonBones的时候，均指这个修改过的插件。**

## DragonBones输出的图像数据可以导入CocoStudio Action编辑器

可以使用CocoStudio的Action编辑器将DragonBones输出的图片导入，然后重新输出成Cocos2d-x支持的格式。这种格式包含一个把碎图拼接好的png文件，一个plist文件和一个json文件。

如何进行上面的导入操作？可以看这个视频：[flash插件 DragonBone导出以及CocoStudio动画编辑器的导入][input2cocostudio]

使用CocoStudio的Action编辑器导出的格式有什么优势呢？

* DragonBones输出的png是碎图，而CocoStudio Action编辑器将碎图拼接成大图了；
* plist文件是png碎图拼接的metadata；
* json文件是骨骼和动画信息。

但是，使用CocoStudio Action编辑器有几个问题：

* 莫名其妙的崩溃。在导入的DragonBones文件中包含空格、中文等内容的时候，编辑器经常直接退出，让人较难判断原因；
* 不支持DragonBones的层级关系。如果在DragonBones中设计了层级关系，那么CocoStudio无法识别，骨骼会发生很大的错位；
* CocoStudio Action编辑器不稳定。我在0.3.0.0版本中，可以导入DragonBones格式，但使用0.3.2.0，又不能导入同样的格式了，编辑器直接退出。

## 为什么不用CocoStudio

既然导入有这样那样的问题，那么直接用CocoStudio做骨骼动画好了，干吗还要用DragonBones？

DragonBones有如下优势：

* DragonBones的骨骼动画实现起来非常非常容易；
* 大多数做动画的同学都熟悉Flash，但极少知道CocoStudio，谁都愿意用自己熟悉的软件；
* Flash和DragonBones的操作体验优于CocoStudio太多。

加上上面提到的不稳定原因，我也无法说服自己使用CocoStudio Action编辑器，更别说把它交给美术MM了。

更何况，我们根本不必把DragonBones生成的文件导入CocoStudio！cocos2d-x能直接支持DragonBones生成的文件！

如果你还是希望用CocoStudo来做骨骼动画，可以参考这篇文章：[使用 CocoStudio 创建 Cocos2d-x 序列帧和骨骼动画][cocostudioskeleton]。

## 生成cocos2d-x支持的文件格式

上面已经提到，使用DragonBones可以生成一堆碎图文件和一个xml文件。我们首先要做的，就是把这堆碎图文件拼成一张大图。cocos2d-x支持plist格式(基于XML)的元数据。

你可以选择 [Sprite Packer(免费)][spritepacker] 或者 [Texture Packer][texturepacker] 来做这件事。[Sprite Sheet Editor][sse] 正在准备支持cocos2d的元数据格式。

拼合成功后，可以将碎图删除，现在我们有3个文件（为了方便描述，这里假设主文件名均为skeleton）：

1. 拼合后的大的png文件 skeleton.png；
2. plist元数据文件 skeleton.plist；
3. xml骨骼动画数据文件 skeleton.xml。

再次强调，这里让主文件相同只是为了方便描述， **实际使用的时候，主文件不必相同。**

但是（为什么非要有但是呢？），你不认为文件名相同更方便人类阅读么？

我先来说一下 skeleton.xml 的内部结构吧。下面是我用 DragonBones 官方提供的 Dragon.fla 生成的xml文件……呃……的一部分。

<pre lang="XML">
<skeleton version="2.1" frameRate="24" name="Dragon">
	<armatures>
		<armature name="Dragon">
			<!-- 这里是一坨b 那啥~ b标签（表想不正……） -->
		</armature>
	</armatures>
	<animations>
		<animation name="Dragon">
			<!-- 这里是一坨mov -->
		</animation>
	</animations>
	<TextureAtlas name="Dragon" height="512" width="512">
		<!-- 这里是一坨SubTexture -->
	</TextureAtlas>
</skeleton>
</pre>

好了，1和2不必再检查了。但 skeleton.xml 必须检查。如果你不希望和我一样耗费一下午来猜谜的话，就记住下面几点吧：

1. armature标签只允许有一个。你生成的xml文件中，可能由于FLA制作的问题，在armatures下面有多个armature，这是绝对不行DI。cocos2d-x碰到这种情况会直接异常没商量。  
所以，留一个最终正确的吧！
2. armature和animation的name属性必须完全相同，这个名称将是cocos2d-x中最终使用的名称。
3. TextureAtlas的name属性和skeleton的name属性就无所谓啦，可以随便填了。
4. 还是有必要再罗嗦一遍，各种name不要用中文，不要加空格，不要用特殊字符……grumble,grumble……

话说，为什么生成的xml文件中会有多个armature呢？借势淫威……你的FLA库中的某个MovieClip中的第一层中包含label！  

我们知道（我不知道你知不知道，你知道你就是我们知道中的我们，你不知道你就不是我们知道中的我们），DragonBones会将MovieClip第一层的label当作骨骼动画中的不同动作。如果你某个不开眼的MovieClip中莫名其妙的加了一个不知所谓的label，而且你这个MovieClip又被制作动画的那个主MovieClip使用了，那么这个带有label的MovieClip也会被作为armature输出。

## 使用CCArmature包实现骨骼动画

终于特码嘚进入代码阶段了，我快要累死了。

CCArmature并不是cocos2d-x核心包的内容，你可以在 cocos2d-x/extensions 中找到它。

在头文件中，需要include CCArmature包的所有内容。我不明白为什么 cocos2d-x 开发组不把这些包含文件都放到 cocos-ext.h 中去。毕竟 spine 都被放进去了啊。难道是不稳定？不敢再往下想了，一定有阴谋，借势个阴谋……

<pre lang="CPP">
#include "cocos2d.h"
#include "cocos-ext.h"
#include "VisibleRect.h"

#include "CCArmature/CCArmature.h"
#include "CCArmature/CCBone.h"
#include "CCArmature/animation/CCArmatureAnimation.h"
#include "CCArmature/datas/CCDatas.h"
#include "CCArmature/display/CCBatchNode.h"
#include "CCArmature/display/CCDecorativeDisplay.h"
#include "CCArmature/display/CCDisplayManager.h"
#include "CCArmature/display/CCSkin.h"
#include "CCArmature/physics/CCColliderDetector.h"
#include "CCArmature/physics/CCPhysicsWorld.h"
#include "CCArmature/utils/CCArmatureDataManager.h"
#include "CCArmature/utils/CCConstValue.h"
#include "CCArmature/utils/CCDataReaderHelper.h"
#include "CCArmature/utils/CCTweenFunction.h"
#include "CCArmature/external_tool/sigslot.h"
</pre>

然后，载入资源、创建动画、播放第一个动画。

VisibleRect这个类可以在 TestCpp 范例中找到。

我写得简单，是因为我只说重点和易错的地方。

埋怨我写的简单的，可以直接查看 TestCpp/ExtensionsTest/ArmatureTest 范例，那个详细得令人发指。

<pre lang="CPP">
CCArmatureDataManager::sharedArmatureDataManager()->addArmatureFileInfo("skeleton.png", "skeleton.plist", "skeleton.xml");
CCArmature* __armature = CCArmature::create("Dragon");
__armature->getAnimation()->playByIndex(0);
__armature->setPosition(VisibleRect::center().x, VisibleRect::center().y*0.3f);
addChild(__armature)
</pre>

再然后，就没有然后了……

[skeletalani]: http://en.wikipedia.org/wiki/Skeletal_animation
[dragonbonesstarted]: http://dragonbones.github.io/getting_started_cn.html
[skeletalanicocos2d]: http://www.cocos2d-x.org/projects/cocos2d-x/wiki/Skeletal_Animation
[skeletalanicocos2dcn]: http://www.ityran.com/archives/3446
[cocostudiodl]: http://bbs.cocostudio.org/forum.php?mod=viewthread&tid=4699&extra=page%3D1
[input2cocostudio]: http://v.youku.com/v_show/id_XNTU4MDY0NTU2.html
[cocostudioskeleton]: http://www.ityran.com/archives/4386
[spritepacker]: http://spritepacker.kernys.net/
[texturepacker]: http://www.texturepacker.com/
[sse]: http://zengrong.net/sprite_sheet_editor
