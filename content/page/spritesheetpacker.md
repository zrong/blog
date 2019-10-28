+++
title = "SpriteSheetPacker"
postid = 1301
date = 2011-04-19T11:18:04+08:00
isCJKLanguage = true
toc = false
type = "page"
slug = "spritesheetpacker"
url = "/spritesheetpacker/"
attachments = "1358, 1359, 1360"
+++


2011-08-18：v0.5.0版发布，同时更名为[Sprite Sheet Editor](/spritesheeteditor/ "Sprite Sheet Editor")，请访问[Sprite Sheet Editor](/spritesheeteditor/ "Sprite Sheet Editor")的页面获得最新版本。本页面不再更新。

下载和安装：  

[安装AIR](http://get.adobe.com/cn/air/)

{{< download 86 >}}

[gallery link="file" columns="3"]

**2011-06-30：v0.4版发布**

1.  将菜单改为按钮，避免Mac等不支持菜单的操作系统无法显示菜单；
2.  可以打开SpriteSheet格式的图片，然后保存成其他格式。即可以在SS、JPG、PNG之间互转格式；
3.  可以打开已有的SpriteSheet，修改Metadata后保存成新的文件；
4.  解决0.3版手动提供的元数据无效的问题；
5.  播放位图动画的时候，在Sheet预览中显示当前帧的范围；
6.  解决打开的SpriteSheet格式的Label起始帧显示不正常的问题；
7.  采用SDK2.7编译。因此需要卸载原来的软件，再升级AIR
    Runtime，才能正常安装。（AIR的版本兼容性很糟糕，经常无法安装，而且给出错误的提示）

**2011-04-26：v0.3版发布**

1.  加入了XML格式的元数据导出功能。
2.  可以打开由SpriteSheetPacker保存的SS格式文件。
3.  如果以SheetSprite方式打开jpg或png文件，可以提供一个SpriteSheetPacker生成的元数据xml文件，SpriteSheetPacker会根据元数据进行解析；若没有提供元数据，会自动在图像文件所在路径寻找同名xml文件。包含mask信息的jpg文件，会自动应用Alpha通道。  
   用这个文件来测试：
{{< download 87 >}}
4.  一些界面上的修改，就不说了。

**2011-04-22：v0.2版发布**

1.  修正了图像排列的BUG；
2.  将保存图像和元数据信息合并到一个菜单，便于对照；
3.  保存元数据的时候可以“包含附加信息”。附加信息包含：是否mask、有没有label、有没有包含名称、总帧数等等。 附加信息选项只会影响元数据，SS格式嵌入的数据总是包含附加信息的。
4.  保存SS格式图像和元数据的时候，可以“包含名称”。有时候我们希望用名称来查找一个Sheet中的Sprite。包含名称功能是独立的，不受“包含附加信息”影响。 SWF视图中不能使用“包含名称”功能。名称自动使用图片的主文件名；
5.  将文件名列表截断，只显示文件名，不显示路径。

**2011-04-19：v0.1版发布**

**Q：这东东是干嘛的？**  

A：我做游戏的时候，经常需要使用SpriteSheet（也称为TileSheet）技术。网上找到的工具都不太好用，所以自己写了个。就这样。

**Q：这东东能处理SWF文件？**  

A：对，它能把SWF变成SpriteSheet，也能将SWF导出成PNG序列。即使你的SWF只有一帧，里面用的MC实现的动画，它也能做到。你知道的，Flash的导出序列图功能，基本上形同虚设。:D

**Q：能把多张小图拼成SpriteSheet么？**  

A：当然可以。你可以设定使用原图大小，也可以只拼接每张图的一个固定的区域（使用“设置-帧”面板）。

**Q：帧设置面板里面的那个“Label”是什么意思？**  

A：有时候，我们会在一个SWF文件中包含多个Label，例如一个人物形象有跑、跳、死亡等等不同的动作。在SWF中很容易表现，加帧标签或者用MC区分。使用SpriteSheet怎么办呢？就可以用这个Label了。  

你可以指定Label的起始帧和总帧数。然后添加到右边的Label列表。每个Label包含的帧允许有重复。  
（抱歉用了两段，太罗嗦了。恩？加上这段好像是三段？）

**Q：没关系的，谢谢你解释清楚。不过我还是要问一下帧设置里面的那个“使用Mask”是什么意思？**  

A：你知道的，JPG文件在文件大小上，某些时候是有一些优势的。对于一些颜色很复杂的SpriteSheet，你可能会发现PNG文件比JPG文件大很多，于是你希望用JPG格式。但是！JPG不支持透明有没有！！用JPG你伤不起啊！！！  

可是，你可以把PNG中的Alpha通道提取出来，在JPG文件中以MASK的方式保存。使用它的时候，再通过bitmapData的copyChannel合并这个MASK，就能得到透明的图了。这岂不是鱼与熊掌兼得的好事么！

**Q：你是马教主的传人么？**  

A：你也是么？我太高兴了有没有！！恩，我顺便再说一下帧面板中的“修改FPS”的功能吧。它可以直接修改AIR程序的FPS，会影响位图动画预览的速度，也会影响SWF动画位图序列生成的速度。

**Q：-\_-|||“SS格式”是一种什么格式？**  

A：不告诉你。

**Q：AIR支持自动升级，你为什么不做？**  

A：我懒。

**Q：你有参考其他人的软件或者代码么？**  

A：我盗取了Keith Peters大神的作品[<span style="text-decoration: underline;">SWFSheet</span>](http://www.bit-101.com/blog/?p=2977)的创意和思路（虽然他不认识我，也看不懂这些，但我还是要向他致敬）；还有另一位大神Grant Skinner的作品<span style="text-decoration: underline;"><span style="color: #0000ff;">[Zoe](http://easeljs.com/zoe.html)</span></span>，我也安装并测试了，对本软件有一定影响；还有TexturePacker软件，这个挺好用，可惜要收钱；还有RIAidea的一篇<span style="text-decoration: underline;"><span style="color: #0000ff;">[关于PNG瘦身的文章](http://www.riaidea.com/blog/archives/279.html)</span></span>，本软件中关于MASK部分的思路就来自这里。

**Q：你这个软件的图标好丑。**  

A：我根本没做图标好不好！你有本事帮我做个？

**Q：这个工具的源码在哪里下载？**  

A：暂时不会公开源码（主要原因是写的太烂，不好意思）。等我做成熟了可能会考虑公开。

**Q：你是谁？**  

A：Kao！问了半天你不知道我是谁！我是个写代码的家伙，<span style="color: #0000ff;"><span style="text-decoration: underline;">[zengrong.net](https://zengrong.net)</span></span>是我的博客。<span style="color: #0000ff;"><span style="text-decoration: underline;"><i@zengrong.net></span></span>是我的邮箱。
