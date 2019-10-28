+++
title = "Flash＆Flex大全"
postid = 48
date = 2005-11-02T10:27:07+08:00
isCJKLanguage = true
toc = false
type = "page"
slug = "flashassistant"
url = "/flashassistant/"
+++


[Flash＆Flex大全](https://blog.zengrong.net/flashassistant/)

本文不再更新，详见： [Goodbye, Flash!](https://blog.zengrong.net/post/2231.html)

**目录**

[TOC]


<a name="history"></a>
## 更新历史

* <span style="color: #ff0000;">2010年11月29日更新：</span>修改[服务器软件](#server)部分，加入SmartFoxServer、QuickServer、Cindy、MINA的介绍。
* <span style="color: #ff0000;">2010年11月24日更新：</span>修改[服务器软件](#server)部分，加入Wowza、ErlyVideo的介绍，修改Red5的介绍。
* <span style="color: #ff0000;">2010年9月25日更新：</span>修改[编译与反编译器](#compiler)、[加密与混淆器](#encrypt)部分。
* <span style="color: #ff0000;">2010年9月18日更新：</span>加入[调试器](#debugger)。
* <span style="color: #ff0000;">2010年9月4日更新：</span>删除数个无效的[explorer](#explorer)。
* <span style="color: #ff0000;">2010年8月27日更新：</span>加入数个Flash游戏、物理、3D引擎和UI组件，加入1个Flash开发框架。
* <span style="color: #ff0000;">2010年8月25日更新：</span>继续删除和修正链接，合并类别，加入了Flash游戏引擎，增加官方在线中文帮助。
* <span style="color: #ff0000;">2010年8月24日更新：</span>删除和修正了许多链接，修改了介绍，合并了类别，加入了Flash物理引擎类别。
* <span style="color: #ff0000;">2011年5月15日更新：</span>在[UI组件](#UI)部分，加入几个轻量级纯AS组件的介绍。
* <span style="color: #ff0000;">2011年5月13日更新：</span>在[游戏引擎](#game)部分，修过多个引擎的介绍。
* <span style="color: #ff0000;">2011年4月6日更新：</span>在[游戏引擎](#game)部分，加入Flixel Power Tools等几个引擎的介绍。
* <span style="color: #ff0000;">2011年3月3日更新：</span>在[服务器](#server)部分，加入Openfire的介绍。
* <span style="color: #ff0000;">2011年1月30日更新：</span>在[混淆器](#encrypt)部分，加入C Preprocessor for ActionScript的介绍。
* <span style="color: #ff0000;">2011年1月7日更新：</span>修改[调试器](#debugger)部分，加入Kap Inspect的介绍。
* <span style="color: #ff0000;">2012年2月25日更新：</span>加入As3-Bloom的介绍。
* <span style="color: #ff0000;">2012年3月12日更新：</span>在[服务器](#server)部分，加入CRTMPServer和Mammoth Server的介绍。
* <span style="color: #ff0000;">2013年9月10日更新：</span>文章采用markdown重新排版，便于编辑；删除部分无效内容；从[游戏引擎](#game)中拆分出[2.5D引擎](#isometric)；在[UI组件](#UI)部分加入flexlite和morn UI。
* <span style="color: #ff0000;">2013年11月28日更新：</span>加入Nape引擎。

<a name="help"></a>
## 官方在线帮助（没标英文的都是中文）

* [用于 Adobe Flash Platform 的 ActionScript 3.0 参考](http://help.adobe.com/zh_CN/FlashPlatform/reference/actionscript/3/) [更多参考](http://www.adobe.com/devnet/actionscript/references.html)
使这样的链接下载离线版：http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/standalone.zip
* [用于 Adobe Flash Professional CS5 的ActionScript 3.0 参考](http://help.adobe.com/zh_CN/Flash/CS5/AS3LR/)
* [使用 Flash Professional CS5](http://help.adobe.com/zh_CN/flash/cs/using/index.html)
* [使用 Flash Builder 4](http://help.adobe.com/zh_CN/flashbuilder/using/index.html)
* [Adobe Flex 4.1 语言参考](http://help.adobe.com/zh_CN/flashbuilder/using/index.html)
* [ActionScript 3.0 开发人员指南](http://help.adobe.com/zh_CN/as3/dev/index.html)（这个一定要仔细看完）
* [使用Flex 4](http://help.adobe.com/zh_CN/flex/using/index.html)（英文）
* [Flex 的 Adobe AIR 开发人员中心-快速入门](http://www.adobe.com/cn/devnet/air/flex/quickstart/)
* [Flash Media Server 4在线文档（英文）](http://help.adobe.com/en_US/flashmediaserver/techoverview/index.html)

<!--more-->

<a name="3d"></a>
## Flash 3D([FlashPlayer11加入原生3D后的更多资料](https://blog.zengrong.net/post/1281.html "支持3D API的Flash Player 11相关资源"))

* [Minko](http://aerys.in/minko/)
* [native3D](http://code.google.com/p/native3d/) [来自](http://game-develop.net/blog/?p=232)  
比其他3d引擎动辄几百k，无位图资源时，只有3k+的native3d引擎在做一些轻量级的网页效果时，它甚至比five3d的体积还要小，确实有它一定的优势。
* Away3d [http://code.google.com/p/away3d/](http://code.google.com/p/away3d/) [http://away3d.com/](http://away3d.com/)
* [Sandy](http://www.flashsandy.org/)  
ActionScript 3D引擎，有AS2、AS3、haXe版
* [Alternativa 3D](http://blog.alternativaplatform.com/en/)
* [ASCOLLADA](http://code.google.com/p/ascollada/)  
可以解析Collada文件格式的AS3类库，Collada 是一个开放原始码的专案,它可让3D资料以XML的型态储存,并让3D人员可以轻易携带和互换资料
* [Five3D](http://five3d.mathieu-badimon.com/)
* [Papervision3D](http://code.google.com/p/papervision3d/)（很久未更新，不支持新的3DAPI，zrong不推荐使用）
	* [http://blog.davr.org/pv3d-examples/](http://blog.davr.org/pv3d-examples/)
	* 官方网站：[http://www.papervision3d.org/](http://www.papervision3d.org/%20)
	* 博客：[http://blog.papervision3d.org](http://blog.papervision3d.org)
	* 下载页面：[http://code.google.com/p/papervision3d/downloads/list](http://code.google.com/p/papervision3d/downloads/list)

<a name="physics"></a>
## Flash物理引擎

* [Nape Physics Engine](http://napephys.com/)  
一个Haxe实现的物理引擎，可以用于AS3和Haxe。开源、免费，可用于商业项目。在AS3中使用时，提供一个swc库。
* [APE](http://www.cove.org/ape/) (Aionscript Physics Engine)
* [The Fisix Engine](http://fisixengine.com/default.asp "http://fisixengine.com/default.asp")  
不开源，但文档和示例比较齐全，zrong也用的就是这个
* [Box2DFlashAS3](http://box2dflash.sourceforge.net/ "http://box2dflash.sourceforge.net/")  
脱自C++引擎，强大且复杂
* [FOAM Rigid Body Physics Engine](http://blog.generalrelativity.org/?p=17 "http://blog.generalrelativity.org/?p=17")
* [Motor](http://lab.polygonal.de/motor_physics/ "http://lab.polygonal.de/motor_physics/")
* [JigLib](http://www.jiglibflash.com/blog/) 3D物理引擎
* [WOW Engine](http://code.google.com/p/wow-engine/) 3D物理引擎

<a name="game"></a>
## Flash游戏引擎(参考来源：[1](http://www.flashrealtime.com/flash-game-library-engine-list/)|[2](http://www.fans8.com/?p=646))

* [PixelBlitz Engine](http://code.google.com/p/pixelblitz/)这个引擎提供位图管理、碰撞检测、像素字体、游戏相关数学计算、键盘和鼠标管理等等功能。但它是一个未完成版本，它的开发者[现在都去开发Flixel Power Tools了](http://www.photonstorm.com/pixelblitz-engine)。
* [flixel](http://flixel.org/)  
这是一个全位图引擎。所谓全位图，就是游戏场景中所有元件最终均绘制在一个位图对象上，在游戏过程中每帧进行重绘。也正因为如此，此引擎非常擅长处理同屏同时出现大量的游戏元件，其高效的渲染会让你激动不已。当你需要创建2D卷轴游戏或者场景中需要大量运动元素的游戏，Flixel引擎是你的首选。
	* 特性：
		* 采用QuadTree的对象链，高效的碰撞检测
		* 位图动画Sprite
		* 通过文本及图片创建Tiles地图
		* 简单易用的粒子系统
		* 高效的滚屏
		* 自定义的鼠标光标
		* 方便的debug显示终端
	* 典型案例：  
		* [Canabalt](http://adamatomic.com/canabalt/)该游戏在作者的网站上每月会消耗2.5T的流量，可见流行的程度。游戏中高速流畅的滚屏会让你惊叹Flash的效率。此游戏还移植到iOS上，并在App Store中销量不菲。
		* [Omega Crisis](http://www.kongregate.com/games/lucidrine/omega-crisis) 这个塔防类游戏，画面、游戏性与操作性都相当不错。
		* [用此引擎的游戏展示](http://flixel.org/games/)
		* [简单介绍](https://blog.zengrong.net/post/1121.html)|[功能列表](http://wiki.github.com/AdamAtomic/flixel/what-is-flixel)|[中文教程](http://bbs.9ria.com/viewthread.php?tid=77614&extra=page%3D1%26amp%3Bfilter%3Dtype%26amp%3Btypeid%3D21)
		* [Flixel Power Tools](http://www.photonstorm.com/flixel-power-tools) 在Flixel的基础上加入了一些工具。
* [Bold Pixel engine](http://blog.vortixgames.com/contact-us/bold-pixel-engine)
以copyPixels方法写的位图引擎。里面实现了缓存BitmapData贴图管理等优化，不过没有对不在显示区域的对象进行过滤，以及其它优化。
* [FlashPunk](http://useflashpunk.net/)（要翻墙才能访问）  
FlashPunk同样是个针对位图的开源引擎。它具有清晰的框架以及创建游戏需要的动画、碰撞等类库，让开发者更专注与游戏的设计与测试中。  
	* 其主要特性包括：
		* 相对独立与固定的帧频时间步长控制
		* 像素、矩形区及网格的碰撞检测
		* 运动tweening
		* sorted的渲染列表，方便深度排序
		* 粒子系统
	* 典型案例：  
		* [Tiny Hawk](http://www.kongregate.com/games/pekuja/tiny-hawk)类似超级玛丽，不过这次你脚下踩着的是滑板，一共32关。
		* [Mr. Fat Snake](http://www.kongregate.com/games/ReviveGames/mr-fat-snake?acomplete=mr+fat+snake)贪吃蛇的横轴飞速版。：）
		* [更多采用此引擎的游戏展示](http://flashpunk.net/?p=games)
* [pushbuttonengine](http://pushbuttonengine.com/)  
[简单介绍](https://blog.zengrong.net/post/1121.html)，Pushbutton引擎的特色有很多，包括建立游戏的模块片段，而不是整体式的应用；使用第三方类库更加容易；提供核心功能比如资源管理器、日志管理、调试检测、序列号、时间管理、全局命名对象等等；相关的组件包括基于Box2D的物理引擎、Rendering2D引擎、游戏常用的健康值组件、团队组件、状态机组件、贴图系统、路径查找类库、基本的网络联机和通讯服务； 将来会提供编辑器，以及网络联机组件，这两个组件都是收费组件； 该游戏引擎的官方网站还列出了[组件商店的介绍](http://pushbuttonengine.com/2009/03/component-store-coming-soon/)，作为该组织出售组件和广大开发者出售组件的场所，这不失为一个好的商业模式。典型案例：
    * [Social City](http://pushbuttonlabs.com/games/social-city/)这个在Facebook上月活跃用户超过一千万的游戏，采用了PushButton引擎。
    * [The Incredible Machine Mega Pack](http://www.gog.com/en/gamecard/the_incredible_machine_mega_pack)不可思议的机器系列想必大家不陌生，这个版本的近400兆大小的单机游戏也出自该引擎。
* [mecheye-as3-libraries](http://code.google.com/p/mecheye-as3-libraries/)  
作者可能已经放弃开发了，zrong不推荐使用

<a name="isometric"></a>
## 2.5D引擎

下面是一些2.5D游戏引擎。所谓2.5D，我们也称之为Isometric，也就是游戏视角采取倾斜视角（如斜45度角等），以平面的方式展现固定视角的3D效果。目前很多网页游戏均采用2.5D的方式。需要注意的是，前面为大家介绍的位图2D引擎同样可以用来开发2.5D游戏。运用这些引擎，你可以把一些烦人的2.5D相关的坐标转换交给引擎处理，专注在你的游戏逻辑及设计上。

* [Pixas](http://code.google.com/p/pixas/)是一个开源ActionScript引擎，它能够使程序员利用纯粹的Actionscript3来构建等距像素Flash应用程序。利用Pixas你可以很容易的将等距像素元素，比如块、立方体、锥体和图层，添加到你的应用程序中。
* [AS3 ISO LIB](http://code.google.com/p/as3isolib/)  
As3isolib是一个基于ActionScript 3的 Isometric库，开发者运用它可以方便的开发2.5D的游戏或应用。
	* 主要特性：
		* 简易的2.5D场景创建方式
		* 方便的于各种缓动（tween）引擎交互
		* 增强的2.5D元件深度排序
		* 场景显示渲染的性能优化
	* 典型案例：
		* [Zex Lex Duel](http://apps.facebook.com/cp_zexlexduel)Facebook上的一个机器对战小游戏。
		* [Down Town](http://apps.facebook.com/downtowngame/)Facebook上的虚拟城市交友。
		* [另外，还有开发者将这个2.5D的库制作成 PushButton引擎的一个组件](http://code.google.com/p/pushbutton-ooo-extras/)
* [OpenSpace](http://www.openspace-engine.com/)  
OpenSpace是一个非常不错的引擎，用户可以非常快速方便的创建2.5D游戏。配合该公司的另外一款通信服务器SmartFoxServer，可以搭建多人实时交互的虚拟场景。
	* 其特点包括：
		* 完善的地图编辑方式
		* 可缩放的场景
		* 自定义地图滚屏方式
		* 自定义的游戏角色
		* 地图自动寻径
	* 典型案例：
		* [The Settlers–My City](http://apps.facebook.com/tsmycity)殖民者的网页版，你可以创建属于自己的殖民国 。
		* [Petpet Park](http://www.petpetpark.com/)很可爱的宠物公园虚拟社区。
		* [更多的案例展示](http://www.openspace-engine.com/showcase)
* [TheoWorlds](http://www.theoworlds.com/)  
TheoWorlds 除了包含Iso引擎之外，还包含聊天、地图编辑器等组件，可以帮助开发者快速的开发2.5D的虚拟世界。
	* 主要特性有：
		* 8方向的运动角色
		* 自定义角色形象
		* 自定义角色动作
		* 快速寻径及自动滚屏
		* 与SmartFox Server及ElectroServer等第三方即时通信服务器通信
		* 聊天历史、表情图标等
	* 相关演示：
		* [场景演示](http://www.theoworlds.com/labs/09/)
		* [地图编辑器演示](http://www.theoworlds.com/mapeditor/)
* [FFlimation](http://www.ffilmation.org/website/)  
这个项目的主要目的是提供一个稳定的开发平台，这样游戏设计师就可以忘记游戏渲染引擎把精力集中在游戏内容的细节方面。从“关卡制作”的角度来看，这个引擎的可用性非常的高。
* [Citrus Engine](http://blueflamedev.com/)  
Citrus 引擎是一种基于as3和box2d的flash滚屏平台游戏引擎。Cirus引擎能让设计师和开发者非常快速的容易的创建滚屏平台游戏（又叫横版过关游戏）象超级玛丽。团队可以用citrus引擎给游戏门户制作广告游戏，市场推广游戏，搏逸游戏等等。
* [Yogurt3D](http://www.yogurt3d.com/en/)  
Yogurt3d的核心部分，swiftgl，是开源并且与opengl兼容。这意味着有opengl开发经验的开发者很容易的就可以开发出3d flash游戏和应用程序。他还可以轻易的将opengl代码转化成swiftgl并在flashplayer中运行。

<a name="UI"></a>
## UI组件与布局管理

* [flex](http://flex.apache.org)  
原本是Adobe的商品，后来被捐献给Apache。
* [flex lite](http://www.flexlite.org/)
	* FlexLite是一个为游戏而生的开源轻量级UI框架，旨在为游戏开发提供一个更加高效的UI工作流。
	* FlexLite Studio是针对FlexLite框架开发的所见即所得的可视化UI编辑软件，与传统纯AS游戏项目无缝集成。
* [Morn UI](http://www.mornui.com/)
	* 轻量级，可视化，高性能，易扩展的flash UI解决方案
	* Morn UI库以精简，直观为设计理念，代码轻量，能快速上手，减少学习成本，Morn UI全部库总大小不到30K
	* Morn UI提供强大的可视化编辑器，布局及属性均可在编辑器直观设置，实现UI和逻辑分离，让美术和程序轻松合作
	* Morn UI设计之初就以高性能为主要目标，以位图为基础，利用延迟渲染机制，实现了高性能
	* 无论UI组件还是编辑器插件，都非常易于扩展，编辑器支持即改即用，轻松实现个性化，甚至使用自己的UI库
* [Flash UI Component](/post/1192.htm/) 基于Flash CS3的UI组件，可用于纯ActionScript项目。
* [AsWing](http://www.aswing.org/)  
AsWing是一套UI组件框架，纯ActionScript开发的组件框架（有ActionScript2和ActionScript3版本），也包含一些常用的工具类，目的是让Flash/Flex开发人员方便的开发出想要的应用程序界面。另外AsWing还提供SkinBuilder和GuiBuilder工具用于制作Skin和可视化编辑生成界面。目前AsWing团队专注于ActionScript3版本的开发和维护。AsWing以 [BSD](http://www.aswing.org/license/LICENSE.txt)协议发布，不管你是商业还是非商业，都可以自由免费使用.
zrong用过一段时间AsWing。看完AsWing的架构才发现，Flex4的spark组件引以为傲大肆宣传的layout，其实AsWing早就这么做了。
但zrong在使用AsWing开发的时候，碰到过许多莫名其妙的问题，找不到什么解决方案，目前已经放弃。
* [Gfl](http://pisces.wisestar.net/gfl/)  
一个轻量级的基于纯AS的独立组件库，可以使用CSS语法。感谢smithfox的推荐。
* [Minimal Comps](http://code.google.com/p/minimalcomps/)  
一套小巧可爱的纯AS组件，除AsWing外的又一选择。<del datetime="2010-12-05T13:35:29+00:00">zrong发现纯AS的UI组件并不多，貌似除了AsWing也就只有这套了</del>。[中文使用说明](https://blog.zengrong.net/post/1142.html)
* [As3-Bloom](https://github.com/impaler/As3-Bloom)  
As-Bloom 是为开发者提供的一个轻量级用户界面。简要介绍其特性：
    * 主题编辑器
    * 边缘布局系统
    * 画刷皮肤系统，轻松改变组件风格
    * 类结构更为清晰，易于初学者上手
    * 保持短小精悍的文件尺寸，内存占用低
* [Skinnable Minimal Components](https://github.com/dgrigg/SkinnableMinimalComponents/)  
MinimalComps的官方版本是不支持皮肤的，而这个就是它支持皮肤的版本。
* [razor components](http://www.razorberry.com/blog/components/)  
一套支持皮肤的纯AS组件。
* [MadCommponents](http://code.google.com/p/mad-components/)  
一套轻量级的纯AS组件，适合用在移动设备上。
* [AS3Flobile](https://github.com/bustardcelly/as3flobile)  
这一套也是比较轻量级的
* [Base UI](http://www.soundstep.com/blog/downloads/baseui/)  
纯AS实现的布局框架，功能很全，配合Minimal Comps再好不过了。[快速查看布局效果](http://www.soundstep.com/blog/source/baseuiv4/demo/)
* [miniui](http://code.google.com/p/actionscriptiui/)
这是一个开源的flash ui 框架。支持主流框架的skin和layout等功能，但是体积却非常小。
* [FlexLib](http://code.google.com/p/flexlib/)  
一套包含很多FLEX高级组件的开源类库。包含这些组件：AdvancedForm, Base64Image,EnhancedButtonSkin, CanvasButton, ConvertibleTreeList, Draggable，Slider, Fire, Highlighter, HorizontalAxisDataSelector ImageMap,PromptingTextInput, Scrollable Menu Controls, SuperTabNavigator,Alternative Scrolling Canvases, Horizontal Accordion, TreeGrid,FlowBox, Docking ToolBar 。
* [FlexMDI](http://code.google.com/p/flexmdi/)  
是一个在Flex中轻松创建多窗口（MDI）的一个框架，提供了很多功能，包括拖拽，最大化，最小化，各种效果等。  
现在FlexMDI已经整合进入[FlexLib](http://code.google.com/p/flexlib/)组件，成为其中的一个包[flexlib.mdi](http://flexlib.googlecode.com/svn/trunk/src/flexlib/mdi/) [MDIManager介绍](http://brianjoseph31.typepad.com/smashedapples/2007/09/flexmdimanagers.html) [flexmdi中的效果](http://brianjoseph31.typepad.com/smashedapples/2007/09/flexmdi-effects.html)
* [vancura-AS3-libs](http://github.com/vancura/vancura-as3-libs)  
提供纯AS3组件的皮肤和样式的集合。支持Scale9Bitmap
* [BrowserCanvas](http://www.dncompute.com/blog/2008/06/23/browsercanvas-the-worlds-easiest-way-to-dynamically-resize-flash.html)  
提供容易的方式动态修改Flash尺寸大小
* [senocular Layout class](https://blog.zengrong.net/post/352.html)  
除了布局工具，还有其他许多有用的工具
* [Yahoo ASTRA: ActionScript Toolkit for Rich Applications](http://developer.yahoo.com/flash/)  
这是Yahoo开发的一套RIA组件包，包含以下内容
    * [Flash Components](http://developer.yahoo.com/flash/astra-flash/)
    * [Flex Components](http://developer.yahoo.com/flash/astra-flex/)
    * [Utilities Library](http://developer.yahoo.com/flash/astra-utils/) 包含动画工具[Animation Utility](http://developer.yahoo.com/flash/astra-utils/animation/)和布局工具 [Layout Utility](http://developer.yahoo.com/flash/astra-utils/layout/)
    * 还有几个这里就不介绍了，大家自己看
* [EnFlash](http://www.asual.com/enflash/) 仅支持AS2
* [XMCA](http://chq.emehmedovic.com/) 仅支持AS2
* [BIT Component Set](http://www.flashloaded.com/flashcomponents/bitcomponentset/) 商业组件 $99
* [GhostWire Components](http://ghostwire.com/go/48) 商业组件 标准版$149 精简版$99

<a name="tween"></a>
## Tween

* [ByteTween](http://code.google.com/p/thelaboratory-tween/)
* [TweenLite(TweenMax)](http://www.greensock.com/tweenlite/)
* [TweensyZero](http://code.google.com/p/tweensy/wiki/TweensyZero)
* [gTween](http://www.gskinner.com/libraries/gtween/)
* [AS3 Animation System](http://www.boostworthy.com/blog/?p=170)
* [Go](http://www.goasap.org/)
* [KitchenSync](http://code.google.com/p/kitchensynclib/)
* [Twease](http://code.google.com/p/twease/)
* [Tweener](http://code.google.com/p/tweener/)
* [Tweensy](http://code.google.com/p/tweensy/)
* [Yahoo ASTRA Animation Utility](http://developer.yahoo.com/flash/astra-utils/animation/)
* [asinmotion](http://code.google.com/p/asinmotion/)

<a name="as3api"></a>
## ActionScript3.0 API

* [swfupload 类库](http://asclass.yo2.cn/articles/fontloader-%e7%b1%bb.html)
如果想对SWF中的动态文本应用非系统的字体，方法当然是在本身的SWF中嵌入相应的字体，另外一种方法是把字体嵌入到另外的SWF中，当需要对应的字体时，把这个SWF载入，并引用相应的字体。FontLoader是一个字体载入类，它帮助你实现这个过程。
* [CASALib](http://casalib.org/)
CASA库是为了简化一些通用的编码而设计，包含collection、display、layout、math、time、load、transitions等包，也有对[Tween](#tween)的实现。
* [as3corelib](http://github.com/mikechambers/as3corelib)
用于AS3开发的一套类库，里面有很多很有用的东西。例如MD5,SHA1加密方法，图片格式转换类（将图片转为位JPG,PNG等格式）还有JSON序
列化等等有用的东西。
* [FlexUnit ](http://code.google.com/p/as3flexunitlib/)
* [Syndication library](http://code.google.com/p/as3syndicationlib/)
* [as3awss3lib](http://code.google.com/p/as3awss3lib/)
ActionScript 3 Amazon S3库
* [as3soundeditorlib](http://code.google.com/p/as3soundeditorlib/)
Actionscript 3声音编辑库
* [as3ds](http://code.google.com/p/as3ds/)
AS3数据结构库，适用于游戏开发
* [As3Crypto](http://code.google.com/p/as3crypto/)
ActionScript 3 加密库
* [ebay API](http://code.google.com/p/as3ebaylib/)
* [facebook-as3](http://code.google.com/p/facebook-as3/)
在伟大的中国基本上是用不到了
* [FZip](http://codeazur.com.br/lab/fzip/)使用AS3解压zip文件
* [lastfm-as3](http://code.google.com/p/lastfm-as3/)
Last.fm是一个音乐网站，这个库让你可以存取Last.fm公开的数据
* [MapQuest](http://company.mapquest.com/mqbs/4a.html)
* [Popforge AS3 audio library](http://popforge.googlecode.com/)
allows you to create a valid [flash.media.Sound](http://livedocs.adobe.com/labs/flex/3/langref/flash/media/Sound.html) object with your own samples
* [Salesforce Flex Toolkit](http://wiki.apexdevnet.com/index.php/Flex_Toolkit)
* [Twitter AS3 API](http://twitter.com/blog/2006/10/twitter-api-for-flash-developers.html)
* [XIFF](http://svn.igniterealtime.org/svn/repos/xiff/)XMPP client library
* [Yahoo AS3 APIs](http://developer.yahoo.com/flash/)
这个上面也介绍过，可以参考上面的介绍
* [Flare Visualization Toolkit](http://flare.prefuse.org/)
Flare 是一个用来做Data Visualization的 AS3 类库，可以用来实现图表，动画效果等
* [Adobe官方开源站点](http://opensource.adobe.com/)
* [Yahoo maps 的AS3组件](http://developer.yahoo.com/flash/maps/)
* [Graffiti Library-ActionScript 3 Bitmap Drawing Library](http://www.nocircleno.com/graffiti/)
Graffiti 是一个AS3库，可以让你方便地在Flex/Flash/AIR中使用画图功能。
* [OpenRIA提供的开源Flex/AS3项目](http://www.openria.cn/index.php/osflexas3projects)
* [Degrafa](http://www.degrafa.org/)开源的图形框架

<a name="editor"></a>
## ActionScript编辑器

* [Flash Builder](http://www.adobe.com/products/flash-builder.html)
Adobe官方提供的编辑器，没什么好说的。
* [InteliJ IDEA](http://www.jetbrains.com/idea/)  
据说是最好的JAVA IDE，Google的AndroidStudio也基于它开发。只有收费版才支持Flex和AS3开发。
* [FDT](http://fdt.powerflasher.com)
FDT是Flash Development Tool 的简称，是非常优秀的ActionScript编辑器。与FlashBuilder相同，它也是基于[Eclipse](http://www.eclipse.org/platform)开发。它支持高级的代码自动完成功能，具有强大的实时错误检测和除错功能，可以导入Flash的帮助文件，实现同Flash一样方便的帮助信息等等。有免费版。
* [FlashDevelop](http://www.flashdevelop.org/)
小巧免费快速的AS编辑器，支持Flex和AIR开发，基于.NET，启动快速，免费。zrong在用这个。
* [SEPY ActionScript Editor](http://sourceforge.net/projects/sepy)
强大的开源AS编辑器，使用python开发。最近一次更新是在2007年2月10日，估计没戏了。

<a name="debugger"></a>
## 调试器 [来自](http://zcdxzsz.javaeye.com/blog/727940) [评测](https://blog.zengrong.net/post/1143.html)

* [Kap Inspect](http://lab.kapit.fr/display/kapinspect/Kap+Inspect)如果你没用过spy工具，你可曾想实时监控swf application的的所有事件？ 你可曾想查看swf有没有内存泄漏问题？你可曾想看看到底DisplayObject tree是什么样的？你可曾想查看所有控件的属性，甚至在运行时改一下？[来自](http://www.smithfox.com/?e=44)
* [ThunderBolt ](http://code.google.com/p/flash-thunderbolt/)是个面向ActionScript 2和3的Firebug轻量级记录器扩展，无法使用Firebug的AIR程序，ThunderBolt有ThunderBolt AS3 Console可以使用。
* [Arthropod ](http://arthropod.stopp.se/)是个面向Flash和AIR开发的调试工具。其易用性非常好，下载后直接就可以使用， 开发者可以在运行期轻松调试应用。
* [Alcon](http://blog.hexagonstar.com/downloads/alcon/)是面向ActionScript开发者的一个轻量级调试工具，提供直接且快捷的方法来调试任何ActionScript 2或ActionScript 3应 用，无论这些ActionScript是来自于Web浏览器、独立的Flash Player还是AIR运行时都没有问题。
* [De MonsterDebugger](http://demonsterdebugger.com/) 是个面向Flash、Flex及AIR项目的开源、轻量级的调试器，功能完善，完全使用Adobe AIR开发。
* [reflexutil](http://code.google.com/p/reflexutil/)是个Flex调试工具,可以在运行时时实改变控件的属性。

<a name="explorer"></a>
## Flex Explorer

* [Flex3 Component Explorer](http://examples.adobe.com/flex3/componentexplorer/explorer.html)
* [Felx2 Component Explorer](http://examples.adobe.com/flex2/inproduct/sdk/explorer/explorer.html)
* [Style Explorer ](http://examples.adobe.com/flex2/consulting/styleexplorer/Flex2StyleExplorer.html)
* [Style Explorer with Kuler Import](http://www.maclema.com/content/sek/)
* [Charting Explorer](http://demo.quietlyscheming.com/ChartSampler/app.html)
* [Filter Explorer](http://www.merhl.com/flex2_samples/filterExplorer/)
* [Style Creator](http://www.flexonrails.net/stylescreator/public/)
* [Enhanced Button Skin Explorer](http://www.wabysabi.com/flex/enhancedbuttonskin/)
* [Kuler](http://kuler.adobe.com/)

<a name="framework"></a>
## Flex开发框架

* [Cairngorm](http://sourceforge.net/adobe/cairngorm/home/)  
是为方便FLEX开发企业级应用而开发的一个微架构。假如项目比较复杂，需要3个开发员以上来共同开发，Cairngorm是一个最正统的选择（官方推
荐），虽然开始时有点难学。而做小型项目或项目是由你自己一个人开发的话，那就用[PureMVC](http://www.puremvc.org/)吧。
不过即使开发不使用它，也可以参考它的源码，毕竟Iteration:two的大量企业级应用的design patterns还是很值得学习的。
* [PureMVC](http://www.puremvc.org/) zrong就用这个
* [ARP](http://osflash.org/projects/arp)
* [MVCS](http://www.adobe.com/devnet/flex/articles/blueprint.html)
* [Flest](http://code.google.com/p/flest/)
* [Model-Glue:Flex](http://www.model-glue.com/flex.cfm)
* [ServerBox Foundry](http://www.servebox.com/foundry/doku.php)
* [Guasax](http://www.guasax.com/)
* [Slide](http://www.memorphic.com/news/)
* [Luke Bayes ](http://patternpark.com/)
* [Ali Mills](http://patternpark.com/)
* [SomaUI](http://www.soundstep.com/blog/category/somaui/)

<a name="compiler"></a>
## 编译与反编译器 [部分转自](http://erniu.net/index.php/2010-07/linux-flash-decompile/)

* [硕思闪客精灵](http://www.sothink.com.cn/flashdecompiler/index.htm)（商业软件）
* [imperator](http://www.ave-imperator.com/)（商业软件）
* [Action Script Viewer](http://buraks.com/asv/)（商业软件）
* [Flasm](http://www.nowrap.de/flasm.html)（自由软件）反编译swf成字节码（bytecode），将修改的字节码再编译成swf。理论上可以反编译任何加密方式的swf，用汇编语言来写ACTION SCRIPT，FLASM能帮你将SWF里面的AS转换成汇编语言，然后你要做的是优化这些代码，最后交由FLASM再把他转回SWF，FLASM的语法与汇编类似，但只能支持到Flash 8。
* [Flare](http://www.nowrap.de/flare.html)（自由软件）Flare是一个免费的swf反编译器. 目前最高只支持Flash MX 2004 和Flash 8。
* [swfparser](http://code.google.com/p/swfparser/)（开源软件）一个 Java 编写的简单的用来反编译 swf 的工具，只支持到Flash 8。
* [swftools](http://www.swftools.org/)是一个方便，易于使用的实用程序收集专门设计，使您与Adobe的Flash文件（SWF文件）工作变得更容易，目前支持Windows和Linux。
    * PDF2SWF是一个PDF格式到SWF格式转换器。每页生成一帧。使你有完整的格式化文本，包括表格，在你的Flash电影上。它基于PDF格式的解析器。结合FlexPaper可以实现类似Baidu文库/豆丁网的Flash文档阅读器，不过要达到上面两种一样应用还需要不少改进
    * SWFCombine工具插入一个对pdf2swf转成文件的显示封装。 （模板）例如见，包括在一些浏览SWF的排序pdf2swf。
    * SWFString搜索出SWF里的文本数据。
    * SWFDump列出有关swf文件里的各种信息如：Sprite， Shape， String等。
    * JPEG2SWF添加一个或多个JPEG图片，并产生一个SWF幻灯片。
    * PNG2SWF 同JPEG2SWF相似，支持png格式。
    * GIF2SWF转换的GIF到SWF。还能够处理GIF动画。
    * WAV2SWF WAV音频文件转换为SWF文件，使用的LAME MP3编码器库。
    * AVI2SWF的AVI动画文件转换为SWF。它支持Flash MX中的H.263压缩。有些例子可以找到examples.html。
    * Font2SWF转换字体成为SWF文件。
    * SWFBBox允许调整SWF的封装Viwer。
    * SWFC的工具，从简单的脚本文件创建的SWF文件。
    * SWFExtract允许提取影片剪辑，声音，图像等从SWF文件。
    * RFXSWF 一个功能齐全的Flash库，可用于独立的SWF。包括位图，按钮，形状，文字，字体，声音等的支持，也为ActionScript支持使用明ActionCompiler。
    * AS3Compile ActionScript 3.0编译器，与官方的Flex SDK 里的mxmlc相比功能很少，你可以输入as3compile –help查看参数
* [Ming](http://www.libming.org/)可以用来生成swf文件,包括在swf文件内增加图片,声音,视频等素材,也可以在文件内增加代码,使用滤镜.可以使用php,perl,python,ruby,java生成swf文件,php5安装的时候自带,php5帮助里面用完整的函数说明。
    * swftophp - SWF to PHP converter
    * makefdb - Font Definition Ripper
    * listfdb - List Font Definition
    * listjpeg – List JPEGs
    * listswf - SWF Disassembler
    * listaction – Actions Script Disassembler
    * png2dbl - PNG convert
    * gif2dbl - GIF converter
    * gif2mask – GIF Mask extractor
    * raw2adpcm - Audio Converter
* [Swfmill](http://swfmill.org/)是一个功能可靠使用方便的命令行工具，可以使用SWFML实现的xml和swf之间的转换，还可以利用xslt生成swf文件，也是FAMES生成SWF密不可分的一部分。SWFML是一种在SWF文件格式制定后制定的XML语言。
* [Nemo 440](http://www.docsultant.com/nemo440/)（免费软件）AIR编写的ActionScript 3/ABC2/Flex 2/Flex 3/Flex 4/AIR反编译器，并不能还原成AS文件，只是反编译成类似字节码的代码。
* swfdump和swfutils.jar，包含在Flex4 SDK中，swfdump调用swfutils.jar工作，将swf编译成字节码。[可以看看这篇文章的介绍。](http://blogs.adobe.com/gosmith/2008/02/disassembling_a_swf_with_swfdu_1.html)

<a name="encrypt"></a>
## 加密与混淆器

* [C Preprocessor for ActionScript](http://sourceforge.net/projects/flex2cpp/)开源的处理AS源码的混淆器，[简单的介绍](http://www.kirupa.com/forum/showthread.php?t=266992)
* [asdec](http://code.google.com/p/asdec/)
* [Flashincrypt](http://www.flashincrypt.com/)
* [Swf Encrypt](http://www.amayeta.com/software/swfencrypt/)
* [Flash Encryption Genius](http://www.kaiyusoftware.com/)
* [irrfuscator](http://www.ambiera.com/irrfuscator/)（商业软件）一个AS3源码混淆器。

<a name="shell"></a>
## 外壳

* [mprojector](http://www.screentime.com/software/mprojector/)
* [swfKit](http://www.swfkit.com/)
swfkit打包方面的一些问题可以看[这里](http://www.lougoo.com/blog/blogview.asp?logID=518)
* [ZINC](http://www.multidmedia.com/)

<a name="video"></a>
## 视频

* [FLV MetaData Injector](http://www.buraks.com/flvmdi/)
* [Riva FLV Encoder](http://rivavx.de/)
* [FLVtool2](http://www.inlet-media.de/flvtool2/)
* [VH Screen Capture Driver](http://www.hmelyoff.com/index.php?section=1)  
免费的抓屏驱动，可以配合Flash Communication Server实现屏幕共享
* [H.264 MPEG AVC Video Codec comparison](http://compression.ru/video/codec_comparison/mpeg-4_avc_h264_en.html)
* [Flash Video比特率估算](http://www.flashsupport.com/books/fvst/files/tools/flv_bitrate.html)

<a name="server"></a>
## 服务器软件

* [C++ RTMP Server(crtmpserver/rtmpd)](http://www.rtmpd.com/)  
一个C++实现的媒体服务器，支持RTMP,RTMPE, RTMPS, RTMPT, RTMPTE协议和易懂设备，支持MPEG-TS/RTSP/RTCP/RTP协议。
* [Mammoth Server](http://mammothserver.org/)  
也是一个C++实现的支持RTMP协议的流媒体服务器。
* [Red5](http://www.red5.org/)  
使用Java编写的开源软件，可以用来替代Flash Media Server（原Flash Communication Server）
* [Wowza Media Server](http://www.wowzamedia.com/)  
商业软件，又一个FMS替代品，除了RTMP外，还支持多种协议和多种客户端（Silverlight、QuickTime等等）
* [ErlyVideo](http://erlyvideo.org)一个使用Erlang语言编写的FMS替代品，支持HTTP MPEG-TS流、RTMP流和IPhone流。  
* [SmartFoxServer](http://www.smartfoxserver.com/)  
商业软件。它是专门为Adobe Flash设计的跨平台socket服务器，让开发者高效地开发多人应用及游戏。服务器端可以使用Actionscript, Javascript, Python和Java语言进行扩展。自带数据库和HTTP服务器引擎。  
[中文介绍](http://www.smartfoxserver.com/_cn/) [中文文档](http://www.smartfoxserver.com/_cn/docs/)
* [Openfire](http://www.igniterealtime.org/projects/openfire/index.jsp)  
使用Java开发聊天和IM服务器，实现了XMPP协议。[据说Google Wave的协议也是基于它](http://initiative.yo2.cn/archives/641559)的，底层使用Apache MINA（下面有介绍）。
* [QuickServer](http://www.quickserver.org/)
它是一个免费的开源Java库，用于快速创建健壮的多线程、多客户端TCP服务器应用程序。使用QuickServer，用户可以只集中处理应用程序的逻辑/协议。
[中文开发指南](http://blog.csdn.net/clearwater21cn/category/99145.aspx)
* [MINA](http://mina.apache.org/)  
Apache MINA(Multipurpose Infrastructure for Network Applications) 是 Apache 组织一个较新的项目，它为开发高性能和高可用性的网络应用程序提供了非常便利的框架。当前发行的 MINA 版本支持基于 Java NIO 技术的 TCP/UDP 应用程序开发、串口通讯程序（只在最新的预览版中提供），MINA 所支持的功能也在进一步的扩展中。
* [Cindy](http://cindy.sourceforge.net/)  
Cindy是一个强壮，可扩展，高效的异步I/O框架。支持TCP,SSL-TCP, UDP和Pipe。
* [OneTeam Media Server](http://www.process-one.net/en/blogs/article/oneteam_media_server_by_processone/)又一个使用Erlang语言编写的开源FMS替代品 [来自](http://www.riaidea.com/blog/archives/227.html)
    1. 支持流式播放实时或已录制好的媒体内容
    2. 支持录制实时内容
    3. 支持AS3 SharedObject共享对象
    4. 支持Clustering集群
    5. 支持用Erlang/OTP编写应用程序模块
*  [TightVNC](http://www.tightvnc.org/)  
并非Flash专用，提供远程控制服务  
[参见FlashVNC](http://www.darronschall.com/weblog/archives/000192.cfm)
* [vnc2swf](http://www.unixuser.org.nyud.net:8090/%7Eeuske/vnc2swf/)  
将VNC的内容保存成SWF

<a name="dev"></a>
## 开发

* [FlashTextEditor](http://flashtexteditor.com/)  
一个基于Flash的在线编辑器，内建文件器，非常有趣和强大。但对中文支持不够好。
* [Flash Text Formatter](http://flashtexteditor.com/ftf/)  
基于Flash的语法着色器，支持ActionScript、PHP、JavaScript和Python语法
* [swfmill](http://iterative.org/swfmill/)  
swf2xml和xml2swf
* [mtasc](http://mtasc.org/)  
编译为swf
* [SWFObject（原名FlashObject）](http://blog.deconcept.com/swfobject/)  
将swf嵌入到网页中的JavaScript脚本
  	* [SWFObject的用法](https://blog.zengrong.net/post/103.html)
	* [基于SWFObject的Flash发布模版](https://blog.zengrong.net/post/185.html)
* [Xray (Flash Debugger)](http://www.osflash.org/xray)

## 应用

* [FlashTextArea](http://www.osflash.org/flashtextarea)  

<a name="remoting"></a>
## Flash Remoting
* [webORB](http://www.themidnightcoders.com/weborb/)  
包含.NET、JAVA、PHP和 Ruby on Rails版本的Remoting。
* [FluorineFx](http://www.fluorinefx.com/)  
Flash Remoting for .NET，开源
* [Zend AMF](http://framework.zend.com/download/amf)  
Zend出品，算是官方支持了。Flash Builder自带了这套框架。
* [OpenAMF](http://www.openamf.com/) [on sourceforge](http://sourceforge.net/projects/openamf/)  
JAVA Flash Remoting
* [rubyamf](https://github.com/victorcoder/rubyamf_plugin)  
RubyAMF is an open source flash remoting gateway for rails. It plugs?directly into your controllers with render :amf.
* [amfphp](http://www.amfphp.org/)（不推荐）  
Flash Remoting for PHP，开源

<a name="as"></a>
## ActionScript 1.0/2.0

* [AS2 Libiary](http://members.shaw.ca/flashprogramming/wisASLibrary/wis/index.html)
* [Flash prototype functions](http://www.sephiroth.it/prototype.php)  
Download all prototype functions in?[PDF format](http://www.sephiroth.it/pdf/pdf_output.php)
* [ActionScript Class](http://www.sephiroth.it/phpwiki/index.php?title=Category:Flash "Category:Flash")
* [AS2 to AS3](http://www.macromedia.com/go/AS2toAS3)

* * *
