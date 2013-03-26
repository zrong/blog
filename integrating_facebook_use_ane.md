Integrating facebook use ANE

[使用ANE整合Facebook](http://zengrong.net/post/1831.htm)

如何在AIR编写的移动应用中整合Facebook？以下是我这两天的研究成果。

## 1. 如何阅读开发文档？

Facebook的开发文档很全，但对于一个时间紧、任务重、被Boss一天催10遍，急于实现整合的开发者来说，或许没有那么多时间去详细阅读所有文档。这里整理了一个顺序：

### 1.1 The Login Dialog  

无论如何，登录是第一步。这篇文档不但介绍了关于登录的所有细节，也详细介绍了关于Permissions的用法。去吧：[The Login Dialog](https://developers.facebook.com/docs/concepts/login/permissions-login-dialog/)

### 1.2 Dialogs Overview

各种SDK中，都提供了Dialogs的相关方法。那么Dialog是什么呢？这篇文档让你了解全部。去吧：[Dialogs Overview](https://developers.facebook.com/docs/reference/dialogs/)<!--more-->

### 1.3 Graph API

Graph API是FaceBook的核心API，不了解它是不行DI。但这篇文档基本上看一半你就懂的。去吧：[Graph API](https://developers.facebook.com/docs/getting-started/graphapi/)

## 2. 选择哪个SDK？

上面说了，Facebook的核心API是 [Graph API](https://developers.facebook.com/docs/reference/api) ，其他的SDK是架构在Graph API之上。

Facebook大力推荐了四个SDK，不用对不起观众：

* [JavaScript SDK](https://developers.facebook.com/docs/reference/javascript/)
* [PHP SDK](https://developers.facebook.com/docs/reference/php/)
* [iOS SDK](https://developers.facebook.com/docs/reference/ios)
* [Android SDK](https://developers.facebook.com/docs/reference/android)

但是，对于AIR来说，我们必须将上面的SDK进行二次封装才能用。

### 2.1 JavaScript SDK

一开始我考虑的是JavaScript SDK，因为它可以同时兼容Mobile Device和Desktop。经常做测试的同学都知道，在AIR模拟器里面测试，比在手机上测试可爽多了。

在Google Code上有这样一个项目：[facebook-actionscript-api](http://code.google.com/p/facebook-actionscript-api/)，它封装了Facebook的JavaScript SDK，采用StageWebView做登录。但是这个项目最后一次是在2011-10-19，以Facebook一日千里的变化，这个API估计很难用了。

我Checkout了该项目的代码，跑了几个Sample，看了它的所有Wiki，也没有调试成功。该项目的所有Wiki都标注成了departed，看得人心惊胆战啊……

### 2.2 Native SDK

Facebook提供了原生SDK支持，分别对应iOS和Android设备。可是要在AIR上使用它们，也必须做二次封装。

好在有人已经帮忙做好了这件事，而且直接提供ANE和 **项目源码**。请大家记住这样的好人吧：[ANE-Facebook](https://github.com/freshplanet/ANE-Facebook)。

这比那几个在Adobe Devnet上写文章，然后卖 $50 的ANE插件的 guy 们厚道多了。

## 3. ANE-Facebook使用

[ANE-Facebook](https://github.com/freshplanet/ANE-Facebook) 没有提供 Sample，所以我写了一个：[ANE-Facebook-Sample](https://github.com/zrong/ANE-Facebook-Sample)。
