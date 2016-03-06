title: VR 时代，我们应该学习什么编程语言？
date: 2016-03-06 10:32:24
modified: 2016-03-06 10:32:24
author: zrong
postid: $POSTID
slug: $SLUG
nicename: what-program-languane-in-vr-time
attachments: $ATTACHMENTS
posttype: post
poststatus: publish
tags: vr,3D
category: technology

3月3日，我被这篇文章轰炸了： [Firefox联手Chrome合作开发网页VR标准][1] 。文中提到：

> 随着1.0版WebVR API的完成，Mozilla已经收到了许多开发者发回的反馈。值得注意的是，该公司已经改进了如下内容：
> 
> 　　—以虚拟现实为核心的设备渲染和显示标准；
> 　　—WebVR页面之间的遍历链接能力；
> 　　—能够枚举虚拟现实输入的输入处理机制，包括6轴动作手柄；
> 　　—适应坐姿和站姿两种体验；
> 　　—使用桌面和移动平台。
> 
> 在获得认可后，Mozilla还计划于今年上半年在Firefox Nightly中推出一个WebVR 1.0的工作版本。如果你勇于探索，可以从布兰登-琼斯那里下载几个实验版Chromium浏览器，体验这种API的概念验证效果。

我们知道，Mozilla 的 [WebVR API][2] 早已在 [2015年7月][4] 推出草案，那么这篇没有任何引用的语焉不详的 WebVR 1.0 是啥？有趣的是，中文互联网上该文章大部分为转载，内容完全相同（甚至更少）。这让我开始质疑其内容的完整和正确性。

稍微搜索一下，发现原文应该是这篇 [Introducing the WebVR 1.0 API Proposal][3] ，译者可能是偷懒，也可能是并非技术人员，仅仅翻译了新闻部分，没有翻译代码部分。看看 [WebVR 草案][5] 中的 Editors 信息，3 个 Mozilla 的人，1 个 Google 的人，我们就能了解到，目前暂时只有 Firefox 和 Chrome 陪玩了。

回到本文的标题，身为开发者，我们该如何更新自己的技能，才能适应这个新的平台？更准确的说，我们应该学习什么编程语言，才能适应 VR 时代的发展？

让我们先来看看现在的 VR 设备。

# VR 设备分析

目前主要的 VR 设备有 [Oculus][13] , Sumsang [Gear VR][8] ， HTC [Vive][6] ， Microsoft [HoloLens][7] ， Sony [PlayStation VR][9] ，国内的 VR 设备则太多，销量较高的有 [蚁视][10] 和 [暴风魔镜][11] 等等。

其中，

[1]: http://tech.sina.com.cn/it/2016-03-03/doc-ifxqafha0307294.shtml
[2]: https://developer.mozilla.org/en-US/docs/Web/API/WebVR_API
[3]: https://hacks.mozilla.org/2016/03/introducing-the-webvr-1-0-api-proposal
[4]: http://www.infoq.com/cn/news/2015/07/webvr-draft
[5]: http://mozvr.github.io/webvr-spec/
[6]: http://www.htc.com/cn/re/re-vive/
[7]: http://www.microsoft.com/microsoft-hololens/en-us
[8]: http://www.samsung.com/global/galaxy/wearables/gear-vr/
[9]: https://www.playstation.com/en-us/explore/playstation-vr/
[10]: http://www.antvr.com/
[11]: http://www.mojing.cn/
[13]: https://www.oculus.com
