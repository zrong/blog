+++
title = "cocos2d-x-filters"
postid = 2278
date = 2015-05-06T17:28:51+08:00
isCJKLanguage = true
toc = false
type = "page"
slug = "cocos2d-x-filters"
url = "/cocos2d-x-filters/"
attachments = "2310,2311,2312,2313"
+++


cocos2d-x-filters 是一个基于 cocos2d-x 开发的滤镜项目，项目托管于 [github][1] 。

目前，这个项目支持下面的几个 cocos2d-x 版本：

- [quick-cocos2d-x 2.x][2]
	- [lua封装（仅支持quick-cocos2d-x 2.x）][5]
	- [基于 quick 的范例][6]
- [quick-cocos2d-x 3.x][7]
- [cocos2d-x 2.x][3]
- [cocos2d-x 3.x][4]

# 滤镜列表

- Gray 去色滤镜，可以调整 RGB 通道的去色比例；
- RGB 和 cocos2d-x 中的 setRGB 功能一致；
- HUE 改变色调，功能同 Photoshop；
- Brightness 调整明度，功能同 Photoshop；
- Contrast 调整对比度，功能同 Photoshop；
- Exposure 曝光；
- Gamma 伽马值调整；
- Haze ；
- GaussianVBlur 高斯模糊，纵向；
- GaussianHBlur 高斯模糊，横向；
- ZoomBlur ；
- MotionBlur 运动模糊；
- Sharpen 锐化。

# 注意事项

1. 滤镜支持叠用（多重滤镜），但性能可能很糟糕；
2. 若生成的 PLIST 纹理中的帧被旋转过（TexturePacker --enable-rotation），可能会出现纹理无法显示的情况。这是一个已知的 bug，目前的解决方案是生成 PLIST 纹理时禁用旋转（TexturePacker --disable-rotation）。

# 截图

**GammaFilter(2)**

![GammaFilter(2)][51]

**HueFilter(90)**

![HueFilter(90)][52]

**ZoomBlurFilter(4, 0.7, 0.7)**

![ZoomBlurFilter(4, 0.7, 0.7)][53]

**多重滤镜  
HueFilter(240)+StaturationFilter(1.5)+BrightnessFilter(-0.4)**

![HueFilter(240)+StaturationFilter(1.5)+BrightnessFilter(-0.4)][54]

# 相关文章

- [在 cocos2d-x 中使用多组shader实现多重滤镜][8]
- [关于 cocos2d-x 滤镜][9]
- [cocos2d-x 滤镜对 dragonbones 的支持][10]

# 免责声明

该项目是我刚刚开始学习 C++ 时所作的第一个项目，因此我不能保证代码质量（可能很糟糕）。若使用中有问题，欢迎讨论。

[1]: https://github.com/zrong/cocos2d-x-filters
[2]: http://github.com/chukong/quick-cocos2d-x/tree/master/lib/cocos2d-x/extensions/filters
[3]: https://github.com/zrong/cocos2d-x-filters/tree/v2.x
[4]: https://github.com/zrong/cocos2d-x-filters/tree/v3.x
[5]: https://github.com/chukong/quick-cocos2d-x/blob/master/framework/filter.lua
[6]: https://github.com/chukong/quick-cocos2d-x/tree/master/samples/filters
[7]: https://github.com/dualface/v3quick/tree/v3/quick/lib/quick-src/extra/filters
[8]: https://blog.zengrong.net/post/2052.htm
[9]: https://blog.zengrong.net/post/2285.htm
[10]: https://blog.zengrong.net/post/2290.htm

[51]: /uploads/2015/05/filters-gamma.jpg
[52]: /uploads/2015/05/filters-hue.jpg
[53]: /uploads/2015/05/filters-zoomblur.jpg
[54]: /uploads/2015/05/filters-hsb.jpg
