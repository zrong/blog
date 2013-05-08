[转]Msys/MinGW与Cygwin/gcc http://zengrong.net/post/1723.htm
 
本文转自：http://www.lupaworld.com/273398/viewspace-122539.html
 
### 一 MinGW

MinGW 官方网站为 <http://www.mingw.org/>

MinGW，即 Minimalist GNU For Windows（GCC compiler suite）。它是一些头文件和端口库的集合，该集合允许人们在没有第三方动态链接库的情况下使用 GCC（GNU Compiler C）产生 Windows32 程序。

**MinGW:**一个可自由使用和自由发布的Windows特定头文件和使用GNU工具集导入库的集合，在基本层，MinGW 是一组包含文件和端口库，其功能是允许控制台模式的程序使用微软的标准C运行时间库（MSVCRT.DLL）,该库在所有的 NT OS 上有效，在所有的 Windows 95 发行版以上的 Windows OS 有效，使用基本运行时，你可以使用 GCC 写控制台模式的符合美国标准化组织（ANSI）程序，可以使用微软提供的 C 运行时扩展。该功能是 Windows32 API 不具备的。下一个组成部分是 w32api 包，它是一组可以使用 Windows32 API 的包含文件和端口库。与基本运行时相结合，就可以有充分的权利既使用 CRT（C Runtime）又使用 Windows32 API 功能。

实际上 MinGW 并不仅是一个 C/C++ 编译器，而是一套 GNU 工具集合。除开 GCC (GNU 编译器集合) 以外，MinGW 还包含有一些其他的 GNU 程序开发工具 (比如 gawk bison 等等)。

开发 MinGW 是为了那些不喜欢工作在 Linux(FreeBSD) 操作系统而留在 Windows 的人提供一套符合 GNU 的 GNU 工作环境。所以，使用 MinGW 我们就可以像在 Linux 下一样使用 GNU 程序开发工具。

GCC 就是 MinGW 的核心所在，GCC 是一套支持众多计算机程序语言的编译系统，而且在语言标准的实现上是最接近于标准的。并且 GCC 几乎可以移植到目前所有可用的计算机平台。

GCC 本身不像VC那样拥有IDE界面（但是有很多的开源的IDE支持使用MinGW，例如codeblocks，eclipse等）。源代码编辑你可以选用任何你喜欢的文本编辑器（据说微软的开发人员包括 VC 的开发都不用 VC 所带的 IDE 编辑器，而是选用 GNU 的 VIM 编辑器）。然后使用 make 等工具来进行软件项目的编译、链接、打包乃至发布。而像 cvs(svn) 源代码版本控制工具可以让世界上任何一个角落的人都可以参与到软件项目中来。

关于 MFC，微软基础库类，这个随 VC++ 携带的一个源代码公开的开发包，和其他 Windows 程序开发包是一样的。如果有 VC++ 的授权，你完全可以使用 MFC 的源代码，也就是你使用 GCC 来编译 MFC 程序是完全可以的。

当然，GNU 下也有很多 Windows 程序开发包，甚至有一些是支持跨平台使用的。不仅仅可以直接把源代码编译为 Windows 程序，也可以不经修改编译为其他操作系统的图形程序。
 
### 二 MSYS 

官方网站为 <http://www.mingw.org/>
MSYS：Unix-like command line utilities，包括基本的bash, make, gawk and grep 等等。通常也可以认为是小型的UNIX on Windows。提供在windows上模拟Unix环境来使用MinGW。

msys-cn:<http://code.google.com/p/msys-cn/>

MSYS中国发行版，用UNIX开发环境开发Windows程序。

MSYS在windows下模拟了一个类unix的终端，它只提供了MinGW的用户载入环境，在MSYS模拟的unix环境下使用MinGW，就像在Unix使用gcc一样。

### 三 cygwin/gcc

cygwin/gcc和MinGW都是gcc在windows下的编译环境，但是它们有什么区别，在实际工作中如何选择这两种编译器。

cygwin/gcc完全可以和在linux下的gcc化做等号，这个可以从boost库的划分中可以看出来端倪，cygwin下的gcc和linux下的gcc完全使用的是相同的Toolsets。所以完全可以和linux一起同步更新gcc版本，而不用担心问题，并且在cygwin/gcc做的东西（不用win32的）可以无缝的用在linux下，没有任何问题。是在windows下开发linux程序的一个很好的选择。

但是在cygwin/gcc下编译出来的程序，在windows执行必须依赖cygwin1.dll，并且速度有些慢，如果不想依赖这个东西的化，必须在gcc的编译选项中加入-mno-cygwin。加入这个选项其实gcc编译器就会自动的选择在安装cygwin/gcc时安上的mingw,这个mingw就是gcc的一个交叉编译。

对于mingw作为gcc在windows上的一个实现，由于不像cygwin的gcc在一个模拟linux上运行，同时相当一部分linux的工具不能够使用，不过现在已经有Msys这个模拟unix的shell，可以解决很多的问题。
 
### 四 总结

MinGW是windows版本的gcc集合，不需要依赖中间层。

MSYS是小型的linux的环境的模拟，可以与MinGW结合来模拟linux环境下使用MinGW的gcc。

Cygwin是功能强大的linux环境，由于有cygwin1.dll实现了底层的windows api到linux api的转化。所以在Cygwin里开发就相当于在linux上开发，对于开发人员来说就相当于调用linux类型的api，所以这样开发的程序也可以直接移植到linux上。但是如果这样的程序要在windows上执行的话，运行时必须要cygwin1.dll支持。

根据以上的分析，如果在windows开发linux跨平台的程序，linux模拟器Cygwin以及所包含的gcc是很好的选择，但是开发的程序必须依赖一个cygwin1.dll。如果你只是想在windows下使用gcc编译器也不想依赖其他的dll，mingw是很好的一个选择。
