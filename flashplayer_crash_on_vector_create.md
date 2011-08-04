[FlashPlayer/AIR在new Vector(-1)的时候崩溃](http://zengrong.net/post/1396.htm)

试试这段代码：

<pre lang="actionscript">
var __length:int = -1;
var __v:Vector.<String> = new Vector.<String>(__length);
</pre>

如果你用Flash builder编译，不会显示任何错误。编译后的swf无法双击打开，或打开后立即退出。

如果你用编译的是AIR程序，程序运行后会立即崩溃，同时弹出下面的提示信息:

![ADL错误](flashplayer_crash_on_vector_create/flashplayer_crash_vector.png)

如果你用Flash IDE来编译，则会看到错误提示：

>Error: Error #1000: 系统内存不足。
>	at Vector$object/set length()
>	at Vector$object()
>	at aaa_fla::MainTimeline/frame1()

这本来不是什么大问题，毕竟极少极少有人会使用 `-1` 这个值来作为Vector的length属性。

可是，起码给点提示好不好？起码让我不要找错方向！

**测试平台：**

* FlashPlayer 10.3
* Flash Builder 4.5.1
* Flex SDK 4.5.1
* AIR 1.7
