使用 ZeroBrane Studio 和 Eclipse LDT 断点调试 quick-cocos2d-x

[quick-cocos2d-x][quick] 是个基于 cocos2d-x 的 Lua Binding 加强版。本文介绍在quick-cocos2d-x中进行断点调试的方法。

为了便于阅读和减少废话，本文有如下假设：

1. 读者阅读过 [quick-x-player 使用说明][quickplayer] 和 [初窥 Quick-cocos2d-x][quickfirst] ;
2. 读者了解 quick-cocos2d-x 项目的文件夹结构；
3. 读者安装了 ZeroBrane Studio 0.39 或/和 Eclipse LDT 1.0；
3. 本文基于 quick-cocos2d-x 提供的 coinflip sample 进行调试。

提纲如下：

1. 在 ZeroBrane Studio 中进行断点调试
2. 在 Eclipse LDT 中进行断点调试
3. 如何选择？
<!--more-->

## 一、 在ZeroBrane Studio中进行断点调试

ZeroBrane Studio是一个用Lua写成的跨平台Lua IDE。界面使用 [wxLua][wxlua] 实现。

### 1. 调试模块

ZeroBrane Studio 使用 modbdebug 模块（位于 [ZeroBrane]/lualibs/mobdebug/mobdebug.lua） 实现调试支持。为了让项目找到这个模块，我采用最简单的方法，将该模块复制进入 coinflip 的 scripts 文件夹。

若不希望这样粗暴，可采用另外两种方法，参考： [Remote debugging][zbdebugging]

### 2. require mobdebug

在 coinflip/scripts/main.lua 的第一行加入下面的代码，让项目启动调试支持。

<pre lang="lua">
require("mobdebug").start()
</pre>

### 3. 启动调试服务器

在 ZeroBrane Studio 中选择 `Project->Start Debugger Server` 命令。如果该命令是灰色的，说明调试服务器已经启动了。

### 4. 加断点

编辑 game.lua 文件，在32行 `game.enterChooseLevelScene()` 处选择 `Project -> Toggle BreakPoint` 加入断点。

### 5. 启动 quick-player

在 quick-player 中启动 coinflip 项目，ZeroBrane Studio 会自动停在 main.lua 中。按 `Project -> Continue` 继续运行，游戏界面出现。

单击游戏中的 "Start" 按钮，调试停止在 game.lua 中的断点处。如下图所示：

![断点调试][zbdebug1]  
[查看大图][zbdebug1]

### 6. 进入源码调试

若要进入框架内部调试，可以取消 main.lua 中的 `CCLuaLoadChunksFromZip("res/framework_precompiled.zip")` 调用，然后将 `[quick-cocos2d-x]/framework` 复制的 `coinflip/scripts/` 文件夹，这样在调试的时候，就可以进入框架内部了。如下图所示：

![框架内部][zbdebug2]  
[查看大图][zbdebug2]

## 二、 在Eclipse LDT 中进行断点调试

LDT(Lua Development Tools)是一个 Eclipse 插件，支持Lua语言的编写和调试。

[quick]: http://quick-x.com/
[quickplayer]: http://cn.quick-x.com/?p=39
[quickfirst]: http://dualface.github.io/blog/2013/07/31/quick-first-time/
[wxlua]: http://wxlua.sourceforge.net/
[zbdebugging]: http://studio.zerobrane.com/doc-remote-debugging.html#setup_environment_for_debugging
[ldt]: http://www.eclipse.org/koneki/ldt/

[zbdebug1]: /wp-content/uploads/2013/10/zbdebug1.png
[zbdebug2]: /wp-content/uploads/2013/10/zbdebug2.png
