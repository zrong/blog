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

在下一步之前，还需要一些必要的资源。

* DragonBones samples 这是DragonBones提供的一些FLA文件源文件，你可以自行修改他们；
* DragonBones Design Panel 这是一个Flash插件，支持Flash CS5~Flash CC 。你需要首先安装它。本文使用的是 2.4.1 版；

这些资源可以在这里下载：<http://dragonbones.github.io/download.html>

本文讲解的3个范例都在这里：[samples/dragonbones][4] ，请提前下载。

这3个范例使用的都是Dragon这个动画，就是那只可爱的绿色小龙啦！

在 DragonBones Design Panel 中，可以输出多种文件格式。但是在 DragonBonesCPP 中，目前仅能支持 PNG+XML 这种格式。

如果选择 PNG+XML 格式输出，每个骨骼动画会包含三个文件：

* skeleton.xml 骨骼数据以及动画数据
* texture.png 纹理素材，采用碎图拼接而成
* texture.xml 碎图拼接的数据文件，和TexturePacker生成的plist的作用相同

# 3 显示Dragon

打开 [samples/dragonbones/scripts/demos/DragonDemoEntry.lua][9] 这个文件，让我们看看如何显示一个骨骼动画。

这个范例的效果是这样的：

[![Dragon Demo Entry][50]][50]

下面的 `_createDB()` 方法做了两件事，一是显示一个骨骼动画，二是将这个骨骼动画中的所有动作名称提取出来，加入到 `_ANIMATION_LIST` 列表中。

<pre lang="lua">
function DragonDemoEntry:_createDB()
	print("DragonDemoEntry", display.newDragonBones)
	self._db = display.newDragonBones({
			skeleton="dragon/skeleton.xml",
			texture="dragon/texture.xml",
			dragonBonesName="Dragon",
			armatureName="Dragon",
			aniName="",
		})
		:addTo(self, 10)
		:pos(display.cx,100)
		:addMovementScriptListener(handler(self, self._onMovement))
	local aniList = self._db:getAnimationList()
	for i=0,aniList:count()-1 do
		_ANIMATION_LIST[#_ANIMATION_LIST+1] = aniList:objectAtIndex(i):getCString()
	end
end
</pre>

`display.newDragonBones` 方法封装在 `display` 库中。它需要1个table格式的参数：

* skeleton 骨骼数据的XML文件路径；
* texture 素材数据的XML文件地址；
* dragonBonesName skeleton.xml的根元素的name值，查看skeleton.xml即可看到，一般与FLA文件的文件名相同；
* armatureName 骨骼名称。一个dragonbones文件可以包含多个骨骼，这里一般指定主骨骼；
* aniName 播放这个名称指定的动画，空字符串代表不播放动画。

返回的对象是 CCDragonBones 的实例，它继承自 CCNode ，我在framework中使用了 [CCDragonBonesExtend][7] 来增加它的功能。在这个例子中，它被保存到 `self._db` 对象。

貌似quick的framework关于扩展功能这部分做了修改和整合，那么在我将DragonBonesCPP提交到quick的时候，这个类的名称可能会改变。

`getAnimationList()` 返回的是一个 `CCArray` 对象，其中每个项是 `CCString` 对象。for循环将其中的字符串提出并假如到 lua table 中。

看看 `addMovementScriptListener` 的定义：

<pre lang="lua">
function CCDragonBonesExtend:addMovementScriptListener(listener)
	self:removeMovementScriptListener()
	self:addScriptListener(CCDragonBonesExtend.EVENTS.START, listener)
	self:addScriptListener(CCDragonBonesExtend.EVENTS.COMPLETE, listener)
	self:addScriptListener(CCDragonBonesExtend.EVENTS.LOOP_COMPLETE, listener)
	return self
end
</pre>

这个方法其实是注册了三个事件，这三个事件分别在动画开始播放、播放完成和循环播放完成的时候调用。

让我们看看在点击 `Change Animation` 菜单的时候会发生什么：

<pre lang="lua">
function DragonDemoEntry:_onChangeAnimation()
	_aniIndex = _aniIndex + 1
	if _aniIndex > #_ANIMATION_LIST then
		_aniIndex = _aniIndex - #_ANIMATION_LIST
	end

	self._db:gotoAndPlay(_ANIMATION_LIST[_aniIndex])
end
</pre>

Dragon这个小龙的动作一共有4个：walk,stand,jump,fall。上面的代码做的事情就是将它们循环播放。

要停止或者播放动画，可以使用下面的代码：

<pre lang="lua">
self._db:getAnimation():stop()
self._db:getAnimation():play()
</pre>

# 4 换装

**==未完待续==**

[1]: http://zengrong.net/post/2106.htm
[2]: https://github.com/DragonBones/DragonBonesCPP
[3]: https://github.com/zrong/quick-cocos2d-x
[4]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/samples/dragonbones
[5]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/lib/cocos2d-x/extensions/DragonBones
[6]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/lib/luabinding/extensions/DragonBones
[7]: https://github.com/zrong/quick-cocos2d-x/blob/zrong/framework/cocos2dx/CCDragonBonesExtend.lua
[8]: https://github.com/zrong/quick-cocos2d-x/blob/zrong/framework/display.lua#L503
[9]: https://github.com/zrong/quick-cocos2d-x/blob/zrong/samples/dragonbones/scripts/demos/DragonDemoEntry.lua

[50]: /wp-content/uploads/2014/07/dragon_entry.png
