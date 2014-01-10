[quick-cocos2d-x 中的 socket 技术选择：LuaSocket 和 WebSocket](http://zengrong.net/post/1965.htm)

<span style="color:red">2013-11-17更新：</span>加入SocketTCP和ByteArray类的实现链接。
<hr>

在 quick-cocos2d-x 中，默认集成了 LuaSocket 和 WebSocket 两个 Socket 库。那么，在开发需要长连接的手机游戏时，应该选择哪个库呢？下面从几个方面进行比较：

1. 跨平台；
1. 易用性；
2. 性能；
1. 流量；
1. 灵活性；
1. 二进制编码；
1. 服务器实现。

<!--more-->

## 一、跨平台

[WebSocket][6] 是跨平台的，其导出到lua的代码位于 `[quick]/lib/cocos2d-x/scripting/lua/cocos2dx_support/Lua_web_socket.cpp` 。

[LuaSocket][5] 也是跨平台的，其导出到lua的代码位于 `[quick]/lib/cocos2d-x/scripting/lua/lua_extensions/lua_extensions.c` 。quick 中集成的 LuaSocket 是 2.1RC 版本。

## 二、易用性

`[quick]/samples/websockets` 是quick提供的一个WebSocket范例。 `[quick]/samples/cocos2dx_luatest/scripts/ExtensionTest/WebProxyTest.lua` 也是一个范例。WebSocket 库封装了一些基本的事件支持 open/message/close/error ，在使用的时候比较方便。

WebSocket 天生就是非阻塞的。

在 quick 中，并没有提供 LuaSocket 的范例。好在该项目本身提供了 [不少范例][1] 和 [库][2] 。从 ftp 到 socket 服务器实现，应有尽有了。

LuaSocket 并没有封装事件支持。不过我们完全可以自己来封装。LuaSocket 支持阻塞和非阻塞的方式获取数据。

## 三、性能

我并没有做过具体的对比测试，所以无从回答具体性能。但从协议实现上来说，LuaSocket 应该会高些的。WebSocket 因为要实现 [HTTP 握手][3] 和 [数据帧][4]，性能或许会低那么一点点。

但从真实应用上来说，这个性能应该是可以忽略不计了。

## 四、流量

WebSocket [在握手阶段必须使用 HTTP协议][3] ，此时的流量消耗会比 LuaSocket 略高。但连接建立之后，就与标准的 TCP 协议相同了。

LuaSocket 就不说了，标准的 TCP 协议实现，还支持 UDP/FTP/HTTP/DNS/SMTP。

## 五、灵活性

这里是 [WebSocket API][7] 和 [LuaSocket API][8] 。毫无疑问，LuaSocket当然更灵活。

灵活和易用似乎总是一堆矛盾。为了更方便地使用 LuaSocket ，我们少不了要自己做一些封装。我参考 [quick论坛上非阻塞socket的实现][12] 做了一些修改， 在 [一个LuaSocket封装][16] 这篇文章中做了详细介绍。

## 六、二进制编码

WebSocket 支持可选的二进制数据传输。LuaSocket 的 [send 方法虽然只支持 string][9] ，但其实我们完全可以用 `string.char()` 把需要发送的数据转成二进制编码来传送，效果其实是一致的。

quick 中封装了 [lpack][10] ，能够更方便的把 lua 中的值转换成二进制数据。而 quick 自带的 luajit 还带有 [BitOp][11] 库，支持常用的二进制操作。这些都能直接使用，既能用于 WebSocket， 也能用于 LuaSocket。

例如下面这段混用了 lpack 和 BitOp 库的代码：

	require("bit")
	require("pack")
	local __pack = string.pack("<b3ihb5", 0x59, 0x7a, 0, 11, 1101, 0, 3,
	bit.bor(0,0), bit.bor(bit.lshift(1,3), 0), bit.bor(bit.lshift(2,3), 0))

	local __s = string.gsub(s,"(.)",function (x) return string.format("%02d ",string.byte(x)) end)
	print(__s)

如果不使用C模块，这里也有几个完全使用lua实现的位运算库。速度会比C慢：[1][13] [2][14] [3][15]

我基于 [lpack][10] 封装了一个 [ByteArray][17] 类，用来模仿 Actionscript 中 flash.utils.ByteArray 的行为。详情可以看这里： [用lua实现ByteArray][18] 。

## 七、服务器实现

服务端的选择就更广泛了。C/C++/JAVA/Go/Node.js/Python 等主流语言都有 WebSocket 的开源实现。标准的 TCP Socket 就更不用说了，那个是网络基础好吧。

但是，WebSocket 和 标准Socket 服务器的实现，还是有区别的。主要的问题在于WebSocket的 [握手][3] 和 [数据帧][4] 方式与标准Socket不同。


由于我们的服务端已经采用标准Socket实现，再转向 WebSocket 就有点多此一举。所以我这个客户端就苦B一点把，把 LuaSocket 封装一下直接用了。

[1]: https://github.com/diegonehab/luasocket/tree/master/samples
[2]: https://github.com/diegonehab/luasocket/tree/master/etc
[3]: https://github.com/zhangkaitao/websocket-protocol/wiki/4.%E6%89%93%E5%BC%80%E9%98%B6%E6%AE%B5%E6%8F%A1%E6%89%8B
[4]: https://github.com/zhangkaitao/websocket-protocol/wiki/5.%E6%95%B0%E6%8D%AE%E5%B8%A7
[5]: http://w3.impa.br/~diego/software/luasocket/home.html
[6]: http://www.websocket.org/
[7]: http://dev.w3.org/html5/websockets/
[8]: http://w3.impa.br/~diego/software/luasocket/reference.html
[9]: http://w3.impa.br/~diego/software/luasocket/tcp.html#send
[10]: underpop.free.fr/l/lua/lpack/
[11]: http://bitop.luajit.org/index.html
[12]: http://cn.quick-x.com/?topic=quickkydsocketfzl
[13]: https://github.com/DGAH/LuaSkillsForQSGS/blob/master/bit.lua
[14]: http://ricilake.blogspot.com/2007/10/iterating-bits-in-lua.html
[15]: http://www.cppblog.com/zhenyu/archive/2005/11/11/1050.html
[16]: http://zengrong.net/post/1980.htm
[17]: https://github.com/zrong/lua#ByteArray
[18]: http://zengrong.net/post/1968.htm
