Title: ANE Toolkit
Date: 2012-06-07 19:19:45
Author: zrong
Postid: 1626
Slug: anetoolkit
Nicename: anetoolkit

~~据说Adobe正在开发ANE插件包，但我可能永远也等不到那一天了。~~
Adobe发布了一个闭源的水果插件包(in gaming
SDK)，写得很烂，但不知道为什么要闭源？没有Android。

写了十几年AS，被Adobe折腾得挺累，想换点口味。不过可能依然会在社区出现骗骗小白，或者用AIR的快速跨平台开发抢点钱什么的……

我把自己用的插件包放出来，算是为AS社区做点贡献。

目前只有Android版本，采用JAVA
API，~~可能以后会有iOS的版本也说不定~~应该不会有iOS版本，但我仍会撺掇别人开源，比如这个：
[PLATFORM-ANES](http://zengrong.net/platform-anes) 。

这东西没什么技术含量，就是体力活调试而已。

~~如果希望增加什么功能，可以联系我。~~

由于研究方向变化，我个人应该不会为其增加新功能了。但仍有人在继续使用它，若有修改，我会更新。

如果有人愿意接收项目，联系我。

**有能力的人，希望能多付出一点，少索取一些。**

------------------------------------------------------------------------

官方更新：
----------

-   [2013-01-25 增加电源管理功能](http://zengrong.net/post/1804.htm)
-   [2013-05-21 增加重启功能](http://zengrong.net/post/1861.htm)

官方介绍：
----------

ANEToolkit是一个非官方的稀烂的插件包，主要是zrong为苦逼的只会AS的或者不是只会AS但讨厌JAVA和Object-C和C和C++的又希望在Android或者水果设备上开发游戏或者应用的程序猿所做的一个很是不到位的努力。

提供以下功能：
--------------

-   安装APK文件
-   调用各种设置面板
-   振动
-   访问SD卡状态
-   读取AIR不能读取的文件
-   向AIR不能读取的路径写入文件
-   删除AIR不能删除的文件
-   获取硬件信息，包括CPU名称、速度、内存大小、存储器大小
-   获取手机信息，包括品牌、名称等等
-   获取网络名称，包括手机号码（部分手机可用/介是不道德DI……）、手机网络（GPRS/GSM/WCDMA...）
-   获取网络连通状态
-   电源管理，禁止休眠，保持屏幕常亮
-   重启自身

下载资源
--------

-   doc（非实时更新，最新文档请直接看源码）：<http://zrong.github.io/anetoolkit/doc/>
-   ANE：<https://github.com/zrong/anetoolkit/blob/master/bin/ANEToolkit.ane>
-   sample：<https://github.com/zrong/anetoolkit/tree/master/sample>
-   source：<https://github.com/zrong/anetoolkit>

