[AIR 15.0 提交 AppStore 错误 ERROR ITMS-9000: Invalid Segment Alignment](http://zengrong.net/post/2165.htm)

上周提交到 AppStore 的 IPA 被拒了，其中的主要错误如下：

>ITC.apps.assetvalidation.PURPLE_EXECUTABLE_OUT_OF_ALIGNMENT.error.message

我联想到有可能是因为 iOS8 支持的原因，于是在 labs.adobe.com 下载了 2014-09-24 日发布的 AIR 15.0.289 beta 版重新打包，但在提交到 AppStore 的时候收到这样的错误提示：

>ERROR ITMS-9000: "Invalid Segment Alignment. This app does not have proper segment alignment and should be rebuilt with the latest version of Xcode. Please contact Developer Technical Support if you need further assistance."

这消息看起来和上次被拒的原因一致。我可以确定是 iOS8 的原因了。最可能的情况是 Apple 要求新提审的包必须加入 iOS8 的相关字段，而 Adobe AIR SDK 的编译器没有提供这些字段。

在 Google 上搜了一通，发现不少人碰到这个问题，只是没有解决方案。<!--more-->

一旦 Adobe AIR 开发者碰到这种情况，只能等待 Adobe 解决，就像我以前发现的这些 BUG 一样：

* [AIR在iOS7上的Microphone权限问题解决][1]
* [朝鲜语/韩文字符在Anrdoid4.2.2上不显示Korean text isn’t shown in Android 4.2.2][2]
* [AIR 3.7 SDK Bug:You uploaded an unsigned APK][3]

经过努力搜索，终于找到这一篇：[No longer able to submit app to iTunes.][4] ，Adobe 的员工在论坛上给出了临时的解决方案：

<pre lang="shell">
cd <sdk>/lib/adt/bin/ld64  # 进入AIR SDK 的相关目录
mv ld64 ld64_orig # 备份原始的链接工具
ln -s /usr/bin/ld ld64 # 使用系统自带的 ld 链接工具替换 SDK 中的链接工具
</pre>

然后重新打包，顺利提交。

注意事项：

1. 此方案只能在 Mac OSX 系统上可用，Windows 神马的就不要尝试了；
2. 原作者并没有说明是否要升级到 Xcode6，但我在尝试之前将系统升级到了 OSX 10.9.5，Xcode升级到了 6.0.1。

只能在OS X上使用的原因其实很简单。AIR SDK 是通过在 Windows 上提供全套 iOS 编译和链接工具来实现交叉编译（在Windows平台上编译IPA包），现在的问题出在链接器上。上面的解决方案是通过使用OS X自带的链接器替换 AIR SDK 中的链接器。而在 Windows 平台上，我们无法直接使用 OS X 的链接器。所以只能等待 Adobe 更新了。

话说 Adobe 的动作也太慢了点。

[1]: http://zengrong.net/post/1931.htm
[2]: http://zengrong.net/post/1865.htm
[3]: http://zengrong.net/post/1838.htm
[4]: https://forums.adobe.com/thread/1584796
