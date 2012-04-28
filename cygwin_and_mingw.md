[Cygwin与MingGW，如何选择？](http://zengrong.net/post/1557.htm)

在无法完全转换到Linux系统的前提下，我一直在[Cygwin](http://www.cygwin.com/)下工作，使用全套的Linux移植工具，学习Bash编程。

但Cygwin由于工作在模拟模式下，速度很慢，相比而言，[MinGW](http://www.mingw.org/)就要快不少。

下面是我选择的对比：

<TABLE style="WIDTH: 100%;border-width:1px;">
<TR>
  <TD>特点</TD>
  <TD>Cygwin</TD>
  <TD>MingGW/MSYS</TD></TR>
<TR>
  <TD>是否GNU</TD>
  <TD>否</TD>
  <TD>是</TD></TR>
<TR>
  <TD>更多软件支持？</TD>
  <TD>支持绝大多数的GNU软件</TD>
  <TD>支持常用软件，git、Vim等软件需要独立支持(详细介绍见下方）</TD></TR>
<TR>
  <TD>更类Linux？</TD>
  <TD>Cygwin在Windows中就好像Wine在Linux中</TD>
  <TD>实现了Bash等主要的Linux程序</TD></TR>
<TR>
  <TD>GCC编译</TD>
  <TD>内含MingGW32交叉编译功能，既支持依赖cygwin1.dll的程序编译，也支持独立的Windows程序编译；可以直接编译Linux下的应用程序</TD>
  <TD>支持独立的Windows程序编译</TD>
</TR>
<TR>
  <TD>中文支持</TD>
  <TD>直接支持中文显示和输入法</TD>
  <TD>需要配置才能支持中文显示和输入，删除一个中文字符需要删除2次</TD>
</TR>
<TR>
  <TD>运行速度</TD>
  <TD>慢</TD>
  <TD>快</TD>
</TR>
</TABLE>

Git for Windows是建立在MinGW的基础之上的。但如果已经安装过MinGW，希望在已有的MingGW上获得Git的功能，则会比较麻烦，详见下方的3篇文章：

* [Installing Git under MinGW (+MSys)](http://stackoverflow.com/questions/5885393/using-msysgit-from-mingw-and-vice-versa)
* [Using msysGit from MinGW and vice versa](http://groups.google.com/group/msysgit/browse_thread/thread/dbe50a1755c6000d?tvc=2&pli=1)

**最终，我还是决定继续Cygwin。git、Vim和中文是主要原因。**
