原文地址：http://zengrong.net/post/1374.htm

AS3中正则表达式对反斜杠的替换

一个有趣的小问题，下面的正则表达式能替换成功么？

<pre lang="actionscript">
var __str:String = '1234\6789';
trace(__str.replace(/\\/g, '5'));
</pre>

答案是：**不能**。trace出来的结果为：

>[trace] 12346789

其实正则本身并没有写错，错在被替换的字符串。反斜杠“\”在AS3中是转义符，会将其后的任何值转换为本身，因此看到的字符串其实本身就是`12346789`，也就是没有反斜杠，当然无法搜索到。

直接`trace(__str)`，结果和上面的trace相同。

希望得到正确的结果，需要将字符串设置为：`1234\\6789`，我们看到的是**两个**反斜杠，而AS3认为它是**一个**反斜杠。

如果使用RegExp来建立正则，则需要使用4个反斜杠：

<pre lang="actionscript">
var __str:String = '1234\\6789';
var __reg:RegExp = new RegExp('\\\\', '');
trace(__str.replace(__reg, '5'));
</pre>

这种情况只在硬编码字符串的时候出现，而如果字符串出现在TextField中，从TextField.text中取出的字符串，本身就自动进行了转义，看到的**一个**反斜杠，其实是**两个**反斜杠。
