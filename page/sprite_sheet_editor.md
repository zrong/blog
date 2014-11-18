Title: Sprite Sheet Editor
Date: 2011-08-18 12:29:04
Author: zrong
Postid: 1403
Slug: sprite_sheet_editor
Nicename: sprite_sheet_editor
Attachments: 1407, 1408, 1409, 1410, 1411, 1412

[Sprite Sheet Editor](http://zengrong.net/sprite_sheet_editor)

## 关于开源

经常有网友发邮件给我，索要 Sprite Sheet Editor 的源码。其实 Sprite Sheet Editor 的源码一直都托管在 [Github][1] 上，如果有心的话，动动手指就能搜到。

Sprite Sheet Editor 和其配套类库一直是我和我所在的团队使用的工具，我们用它完成了1个页游和2个手游。我对它的修改，都是基于我自己工作中的需求。

我一直没有在这里公布的原因，是处于这样几点考虑：

1. 源码并不成熟，公布出来可能会吓到小伙伴们；
2. 没有人愿意帮助我完善这个工具。大多数人都是只知索取的，这点在我另外的两个开源项目 [ANEToolkit][2] 和 [PlatformANES][3] 上我已经深深的体会到了；
3. 我会变成免费的工具。没人愿意帮我修改一个bug或贡献一行代码，而我却需要不断实现别人要求的功能；
4. 这个工具的作者会变成别人。我指的是，把源码拿去，把我的名字删去改成另一个，再声称这是另一个名字的人的作品。在我10年的博客生涯中，这种事情发生过许多许多次。

当然，我发现我的考虑太幼稚。用江总书记的话来说，是 too young too simple sometime naive! 我也实在不该强迫别人也有开源精神，我不能要求别人和我用一样的方式思考。

再说了，谁会真的在意你这个没完成的破软件？谁会吃饱了没事干拿出时间和精力来帮你？

所以，尽管拿去吧！

**有能力的人，希望能多付出一点，少索取一些。**

----

## 下一步开发计划

* 增加编辑动画中心点功能；
* 加入自动更新功能。

Sprite Sheet Editor 是一个生成Sprite Sheet(也叫Tile Sheet)的免费工具。

## 开发平台

* Apache Flex 4.9.1
* Adobe AIR 3.7

## 特点

* 将swf转换成序列图或者Sprite Sheet格式；
* 将多张图像拼合成一张大的Sprite Sheet以降低文件尺寸和减少网络请求；
* 让Sprite Sheet也支持Label，实现类似于MovieClip中Label的功能；
* 自动修剪Sheet中每帧四周的空白像素；
* 使用Mask技术让JPEG格式也支持透明，大幅降低需要透明的文件的尺寸；
* 支持JPEG-XR格式，该格式支持Alpha通道，图像质量优于JPEG格式；
* 还有更多……

## 类似软件

Sprite sheet Editor有许多缺点，因此我必须推荐两个优秀的软件给大家。你应该在安装SpriteSheetEditor之前去尝试一下它们。

* [ShoeBox](http://renderhjs.net/shoebox/)
* [TexturePacker](http://www.codeandweb.com/texturepacker)

## 下载和安装

* <a href="http://get.adobe.com/cn/air/" target="_blank">安装AIR环境</a>
* [download id="114"]

**历史版本**

* [download id="113"]
* [download id="112"]
* [download id="109"]
* [download id="101"]
* [download id="100"]
* [download id="95"]
* [download id="92"]
* [download id="86"]

## 更新历史

这个工具原来的名字叫做<a href="http://zengrong.net/spritesheetpacker" target="_blank">Sprite Sheet Packer</a>，从v0.5.0改名为Sprite Sheet Editor。

* [2013-08-21：v0.8.2版发布](http://zengrong.net/post/1901.htm)
* [2013-06-14：v0.8.1版发布](http://zengrong.net/post/1880.htm)
* [2013-02-19：v0.8.0版发布](http://zengrong.net/post/1815.htm)
* [2012-10-15：v0.7.3版发布](http://zengrong.net/post/1706.htm)
* [2012-08-20：v0.7.2版发布](http://zengrong.net/post/1672.htm)
* [2012-08-18：v0.7.1版发布](http://zengrong.net/post/1668.htm)
* [2012-07-26：v0.7.0版发布](http://zengrong.net/post/1660.htm)
* [2011-12-21：v0.6.2版发布](http://zengrong.net/post/1482.htm)
* [2011-11-04：v0.5.9版发布](http://zengrong.net/post/1468.htm)
* [2011-09-02：v0.5.7版发布](http://zengrong.net/post/1436.htm)
* [2011-08-23：v0.5.6版发布](http://zengrong.net/post/1414.htm)
* [2011-08-18：v0.5.0版发布，同时更名为Sprite Sheet Editor](http://zengrong.net/post/1402.htm)
* [2011-06-30：v0.4版发布](http://zengrong.net/post/1357.htm)
* [2011-04-26：v0.3版发布](http://zengrong.net/post/1313.htm)
* [2011-04-22：v0.2版发布](http://zengrong.net/post/1311.htm)
* [2011-04-19：v0.1版发布](http://zengrong.net/post/1306.htm)

## 界面截图

[gallery link="file"]

[1]: https://github.com/zrong/sprite_sheet_editor
[2]: http://zengrong.net/anetoolkit
[3]: http://zengrong.net/platform-anes
