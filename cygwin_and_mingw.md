[Cygwin与MinGW/MSYS，如何选择？](http://zengrong.net/post/1557.htm)

<span style="color:red;">2012-11-03更新：</span>加入msys的内容。
<span style="color:red;">2013-10-15更新：</span>修改表格格式，加入介绍链接。
<hr>

什么是Cygwin和MinGW？请看这篇：[Msys/MinGW与Cygwin/gcc][intro]。

在无法完全转换到Linux系统的前提下，我一直在[Cygwin](http://www.cygwin.com/)下工作，使用全套的Linux移植工具，学习Bash编程。

但Cygwin由于工作在模拟模式下，速度较慢，相比而言，[MinGW](http://www.mingw.org/)就要快不少。

下面是我选择的对比：<!--more-->

|特点|Cygwin|MinGW/MSYS|
|----|----|----|
|是否GNU|否|是|
|更多软件支持？|支持绝大多数的GNU软件|支持常用软件，git、Vim等软件需要独立支持(详细介绍见下方）|
|更类Linux？|Cygwin在Windows中就好像Wine在Linux中|实现了Bash等主要的Linux程序|
|GCC编译|内含MingGW32交叉编译功能，既支持依赖cygwin1.dll的程序编译，也支持独立的Windows程序编译；可以直接编译Linux下的应用程序|支持独立的Windows程序编译|
|中文支持|直接支持中文显示和输入法|需要配置才能支持中文显示和输入，删除一个中文字符需要删除2次|
|运行速度|慢|快|

[Git for Windows和msysGit](http://msysgit.github.com/)是建立在MinGW/MSYS的基础之上的。但如果已经安装过MinGW/MSYS，希望在已有的MinGW/MSYS上获得Git的功能，则会比较麻烦，详见下方的2篇文章：

* [Installing Git under MinGW (+MSys)](http://stackoverflow.com/questions/5885393/using-msysgit-from-mingw-and-vice-versa)
* [Using msysGit from MinGW and vice versa](http://groups.google.com/group/msysgit/browse_thread/thread/dbe50a1755c6000d?tvc=2&pli=1)

另外，在安装msysGit的时候，要注意cygwin的bin目录不能位于PATH环境变量中。否则msysGit会拒绝安装。

**最终，我还是决定继续Cygwin。git、Vim和中文是主要原因。**

[intro]: http://zengrong.net/post/1723.htm
