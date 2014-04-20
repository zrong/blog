谢邀。

如果按照 优秀的程序员和一般的程序员差别在哪？ 的定义来看，你已经是个程序员了。

我接触的许多程序员中，绝大多数都是知其然不知其所以然，做了AS好几年的，甚至连AVM是什么都不知道的太多了。许多程序员把快速开发出成品作为是工作的唯一目标，认为研究底层知识和周边技术是浪费时间。很多东西他们不是不能知道，而是不想知道。

更有甚者，学会了 gotoAndPlay 就敢说熟悉 Flash，会敲 ls 就敢说精通Linux。前几天有朋友发给我他膜拜了一日的逆天简历，上面洋洋洒洒写着汇编、C/C++、Linux网络编程、JAVA EE、Perl、Bash、Python、Windows驱动开发、单片机开发、HTML、CSS3、JavaScript、PHP、cocos2d-x、iOS开发、安卓开发……而且所有的项目的级别都是 精通！

我看完简历和朋友说：这位前后端桌面嵌入式系统驱动网页手机开发通吃的全栈神人10年里跳槽8次，从没在一个公司干满过2年，你敢用么？

======上面废话，不看也罢。

刚巧我也是从AS3转到了cocos2d-x，说说我的经验吧。

一、 cocos2d-x 部分

1. 技术选型。从第三个手游开始，我实在被Adobe的ANE和国内的小平台折腾得没了脾气，决定转到cocos2d-x。在选择哪种语言绑定的时候纠结了很久，最后力排众议选了 lua：Cocos2dx+lua合适还是Cocos2dx+js合适? cocos2d-x 2.x 的lua绑定做得并不好，于是我选择了 quick-cocos2d-x 。

2. 学习 C++。《C++ Primer》 是不错的入门书籍，建议看第五版，我写过一篇 C++Primer 第4版和第5版比较 。学习期间建议画一些思维导图帮助理解和整理思路。

3. 学习DEMO和熟悉开发平台。编译 cocos2d-x 自带的 TestCPP 项目，全部跑一遍。熟悉 cocos2d-x API 的用法。记得生成文档，建议每个API的功能都浏览一遍。

在学习DEMO的过程中，你还必须熟悉自己开发平台的IDE，例如Windows上必须熟悉 Visual Studio，而OS X上必须熟悉xcode，Linux平台上就熟悉Eclipse+CDT吧。

注意，quick-cocos2d-x 是不支持Linux开发平台的。

4. 了解引擎的文件夹结构。基于 cocos2d-x 源码生成的文档并不怎么详细，许多功能必须看源码。但这个阶段，我不建议纠结源码太深，倒是可以纠结一下 cocos2d-x 的文件夹结构，看看各个类放在什么地方，找一找常见的哪些宏和常量以及枚举定义在什么地方，这花不了多少时间，但能让你对cocos2d-x有更深刻的了解，同时给你很强的成就感。这种成就感冲淡了你面对大量源码时候的无力感，让你能够继续前行。

5. 重复上面的第3步：再次学习DEMO。这时候看DEMO可能会轻松不少，但是你会有更多的问题去纠结。例如多分辨率支持？例如坐标系统？例如绘图功能？例如层级管理系统？例如事件传递系统？等等等等……这时候可以去Google（注意不要用百毒和其他搜索引擎）找文档看了。我推荐一些我看过的不错的文档和博客：

    http://www.ityran.com/archives/4809
    Cocos2d-x官方中文文档 v2.x
    Cocos2D | iOS Development Tips & Tricks by BiOM
    子龙山人 - 博客园
    红孩儿的游戏编程之路
    Ray Wenderlich
    Cocos2d-x | Cross Platform Open Source 2D Game Engine

许多博客都是极好的。红孩儿写了许多源码分析，每一句源码都加了注释。虽然我不太认同他这种吃力不讨好的方法，但对于新手来说确实是有很大的帮助。

另外在 Stack Overflow 你能找到绝大部分问题的答案。当然，许多问题是针对 cocos2d 而非 cocos2d-x 的，不过用法相同，照看不误。许多优秀的文章都是基于 cocos2d 的，所以，不要介意，可以先花半天时间熟悉 OC 的语法，能看懂即可。

忘了广告了，我的博客（cocos2d-x | zrong's Blog）也有一些cocos2d-x内容，欢迎来喷。

6. 熟悉工具集。现在你应该对周边工具感兴趣了。例如帧动画使用什么制作？BMFont使用什么制作？骨骼动画呢？plist文件怎么编辑？碎图用什么工具拼合？有些项目上，你有许多选择，也可能没得选。去Google吧，如果遇到选择上的问题，欢迎找我讨论。

二、 quick-cocos2d-x 部分

1. 现在就到lua时间了。请认真读完 《Lua程序设计(第2版) 》 第一、二、三部分。第四部分可暂时不读。

2. 熟悉 quick-cocos2d-x 的文件夹结构。相信有了上面 cocos2d-x 的基础，这个应该不难理解。

3. 跑完 quick-cocos2d-x 自带的所有sample，期间熟悉 framework 中的所有封装。这期间可以参考下面的文章：http://quick.cocoachina.com/wiki/doku.php?id=zh_cn

4. 学习导出API给Lua使用。http://quick.cocoachina.com/?p=235

三、学习 OpenGL ES

熟悉Lua部分之后，作为一个有志于成为程序员的码农，依然要回到C++来，这里才是 cocos2d-x 的本质。

cocos2d-x 使用 OpenGL ES 进行渲染的，如果要对 cocos2d-x 的渲染层进行任何形式的扩展，你完全避不开 OpenGL ES。

既然逃不开，那就对她说，请张开双腿，我要上。

1. 阅读 OpenGL ES 2.0 Programming Guide - Book Website

http://www.opengles-book.com/es2/index.html

这本书写得浅显易懂，非常适合新手。有位网友花3个月时间翻译了中文版，但还是建议你不要看了。

官方文档：http://www.khronos.org/opengles/sdk/docs/man/
API 翻译： http://www.dreamingwish.com/dream-category/api-in-chinese/opengl-es-api

当然，也可以买那本著名的 OpenGL 红宝书《OpenGL编程指南（原书第7版）》来看，不过 OpenGL ES 相对与 OpenGL 来说还是有一些不同的，你要知道如何区分这些不同。

http://book.douban.com/subject/4311129/

2. 尝试理解 cocos2d-x 的渲染部分架构。相关的类我就不列出了，我正在酝酿一个这方面的系列文章准备发到博客上。如果写完了，我会在这里更新。

3. 自己写一些滤镜、绘图功能的扩展。

四、回归项目

到了这里，你可以开始你的项目了。






