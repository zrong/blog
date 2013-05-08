[在天朝调试Android In-app-billing](http://zengrong.net/post/1801.htm)

历尽艰难险阻终于在中国大陆调试Google Play In-app Billing成功，过程记录如下，方便后来之人。

## 一、错误描述

Android的文档写得相当好，根据下面两篇教程，理应顺利通过调试。

* [In-app Billing Overview](http://developer.android.com/google/play/billing/billing_overview.html)
* [Preparing Your In-app Billing Application](http://developer.android.com/training/in-app-billing/preparing-iab-app.html)
可郁闷的事情，是在使用Google提供的[TrivalDrive Sample](http://developer.android.com/training/in-app-billing/preparing-iab-app.html#GetSample)进行调试的时候，Sample程序总是抛出异常：

>Error checking for billing v3 support. (response: 3:Billing Unavailable)

## 二、原因

这个异常对应的是 `BILLING_RESPONSE_RESULT_BILLING_UNAVAILABLE` 错误，Google对它的定义是：<!--more-->

>Billing API version is not supported for the type requested

详见这里：[In-app Billing Reference (IAB Version 3)](http://developer.android.com/google/play/billing/billing_reference.html)
这个含义其实是非常模糊的，我用非常标准和专业的中文翻译一下，它应该是这个意思：

>老子就是不支持你在天朝使用，你能怎么着？

血泪教训啊，为了翻译上面那句话，秒秒钟几十亿上下的我的track遍及大江南北，城墙内外……

## 三、解决条件

Android文档中提供的什么账户啊、产品啊、Developer Console之类的我就不说了，中文不好的就去看英文，英文好的就去看英文。我要说的内容绝不违反党的政策，和12306、GitHub以及城墙都无关。其实我只是欺骗了万恶的美帝。

Android中的In-app billing其实是调用Google Play实现的。因此要解决上面的问题，首先要让Google Play支持支付。

默认的情况下，在Google Play Store中，我们只能看到免费的App，且无法搜索到收费App。要完成这一步，需要以下条件：

1. Root过的Android手机一枚；
1. 跨墙工具一套（推荐美帝VPN）；
2. Market Enabler或者[Market Unlocker](http://support.evanhe.com/2012/03/08/introduction-to-market-unlocker-2/)；
3. 双币种信用卡一张（亲测招行VISA可用）；
3. 美帝通信地址和邮编（如果木有亲戚朋友，就随便找个大学地址）；
4. Google账户一个。

## 四、解决流程

还是先说句废话：**开机有风险，用户须谨慎**

1. Google帐号绑定信用卡  
PC拨上美帝VPN，进入 <https://wallet.google.com> ，账户选择美国，地址邮编填写上面准备好的，然后绑定一张双币种信用卡。如果绑定成功，你应该会收到银行短信说有$1的交易。不要着急，这个交易只是预授权费用，是为了检测你的卡是否正常，不用还款的。详见：[Authorizations](https://support.google.com/wallet/bin/answer.py?hl=en&answer=105940)。
2. 修改运营商  
运行上面准备的 Market Unlocker，按照界面提示开启`Enable Unlocker` 和 `Auto Unlock` 选项。这个操作将运营商改成 Verizon。
3. 取消定位服务（我不确定是否必须）  
在Android系统设置中把 `使用wifi定位` 和 `用定位数据改善google服务` 关闭。
4. 清除Google Play Store的缓存和更新  
在Android的App管理中，清除Google Play Stroe的程序数据和缓存。Android会有一个提醒，不必管它，哪些东西都会回来的。如果Google Play更新过，也写在更新。Google Play Store一般是保存在Rom中的，所以不会被卸载，只能卸载更新。
5. 完成  
在Android设备中拨上美帝VPN，重新打开Google Play Store。如果你能在首页看到收费应用，就说明已经成功了。

## 五、参考

以下是参考资料中有价值的一小部分，大部分资料都需要跨墙：

* [招行信用卡绑定Google Checkout](http://zhu8.blogspot.com/2010/01/use-cmb-card-as-google-checkout.html)
* [有人在国内成功使用过google market的in-app-billing吗？](http://www.eoeandroid.com/forum.php?mod=viewthread&tid=111797)
* [解决“此商品无法在您设备所在的国家使用”（更新）](http://bbs.gfan.com/android-1753858-1-1.html)
* [关于google checkout绑定信用卡](http://bbs.gfan.com/android-3200053-1-1.html)
* [In App Billing Implementaion](http://www.stonetrip.com/developer/forum/viewtopic.php?f=43&t=26090)
* [In-app Billing Overview](http://wiki.eoeandroid.com/In-app_Billing_Overview) （感谢这位苦B的in china兄弟，让我不至于偏的太远）
* [Android In App BIlling v3 doesn't work Nexus 7](http://stackoverflow.com/questions/13853089/android-in-app-billing-v3-doesnt-work-nexus-7)

这两篇可能用得上，一并放这里。第一篇也是字字血泪啊！！

* [串接 Google Play In-app-billing 易犯的錯誤](http://lp43.blogspot.tw/2012/04/google-play-in-app-billing.html)
* [使用针对 Android 的应用内付费 Adobe AIR 原生扩展](http://www.adobe.com/cn/devnet/air/articles/android-billing-ane.html)
