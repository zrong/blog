LP总抱怨她的HTC EVO 4G速度太慢，今天终于能抽出点时间来刷个机了。

像EVO 4G这种老机器，是肯定没有官方版的ICS可以OTA升级的，只能考虑刷第三方Rom。于是我转战机锋、安卓网等多个论坛，刷了4个Rom，发现要么是吸费软件太多，要么是刷完无法启动，忙活了半个多个小时也没找到满意的Rom。

在重刷第4个Rom的时候，刷机的过程中发现原Rom作者嵌入到刷机代码中的博客地址，终于在[moonlight的博客](http://roms.blog.163.com/)找到了近乎纯净版的CyanogenMod9版本的EVO 4G Rom。而且moonlight也正在放出CM10版本的EVO 4G ROM。

刷了一个moonlight提供的基于CM9的10.18版本之后，我发现Android 4.04在EVO 4G这种老机器上，表现还真不错，似乎比以前的2.3.5都要好点。可惜的是，没有Google Apps可用。

原来的通讯录是备份在Google账户中的，而没有Google Apps就无法同步原来的通讯录，要导出成VCard格式再用Android通讯录导入。虽然LP不用Google的服务，但是这样一来，就无法再进行通讯录的同步了。我记得原来在玩Samsang i5700的时候，是单独刷过Google官方套件的，只是时间实在太久，记不清怎么弄的了。

又是Google一番，发现网上大多数的帖子都语焉不详。这也难怪，活跃的那部分玩家，能把一件事情用文字说清楚的的确很少（或许用语言都难得说清楚）。但真正的老鸟，又大都不愿意写这些入门文章。

好不容易找到的比较全面和系统的是这一篇：[Google Apps知多少与快速安装方法](http://www.padest.com/forum.php?mod=viewthread&tid=45734)

下面摘录部分：

>*1：Google Apps是什么？*
>Google Apps(简称:GApps)是谷歌公司专属的应用，用于各种安卓平台。目前Gapps里大多数的应用，都可以在谷歌市场(Google Play Store)找到并安装。这些应用主要包括：Google Play、Google Talk、Google Map、Gmail、Google Search、Google Voice Search、Google Music、Google Docs、Google Sync、Google Backup Transport 以及Car Home、YouTube、Facebook等等。
>*2：Google Apps与Roms*
>目前市场只有部分固件Roms中，已经内置了GApps。这是因为这些Roms，要么是获得官方授权定制的Rom，要么是个人编译的Rom或者从对版权不是很重视的地区流出的Rom。
>鉴于licensing issues（许可证发放）问题，大多数的AOSP、CM以及AOKP的Rom，都不会内置Google Apps。
>*3：Google Apps最新版本与下载*
>下表所列Google Apps及其下载包，均为官方最新数据。
>需要的板友，请根据使用设备的Android版本，选择合适的GApps下载包。

遗憾的是，该文中提供的GoogleApps的下载地址都是115网盘的，而115网盘已经关闭共享了。

无奈之中找到CyanogenMod的官方WIKI，惊喜地发现这里也有Google Apps提供下载！

<http://wiki.cyanogenmod.com/index.php?title=Latest_Version/Google_Apps>

在上面的链接中，根据自己的CM版本下载对应的Google Apps就可以了。至于刷入的方法，和卡刷一样，本文就不提了。
