"=========== Meta ============
"StrID : 1692
"Title : 在64位操作系统上使用FlashDevelop的Debug功能
"Cats  : 技术
"Status: draft
"Preview: http://zengrong.net/?p=1692&preview=true
"Tags  : FlashDevelop, Flex, JAVA
"========== Content ==========
最近用上了<a href="http://www.flashdevelop.org">FlashDevelop</a>。与Flash Builder比起来，它确实优点很多：小巧，快速，灵活的定制功能，免费且开源。

使用FlashDevelop开发AS/Flex/AIR程序的时候，可以使用Flex SDK来编译和调试。Flex SDK使用JAVA写成，需要系统中安装JAVA虚拟机（JVM）。而我的系统中已经安装了64位的JAVA虚拟机。

在调试的时候，FlashDevelop报告了下面的错误。

<blockquote>Debugger startup error: System.BadImageFormatException: 试图加载格式不正确的程序。 (异常来自 HRESULT:0x8007000B)
   在 net.sf.jni4net.jni.JNI.Dll.JNI_GetDefaultJavaVMInitArgs(JavaVMInitArgs* args)
   在 net.sf.jni4net.jni.JNI.Init()
   在 net.sf.jni4net.jni.JNI.CreateJavaVM(JavaVM&amp; jvm, JNIEnv&amp; env, Boolean attachIfExists, String[] options)
   在 net.sf.jni4net.Bridge.CreateJVM()
   在 net.sf.jni4net.Bridge.CreateJVM(BridgeSetup setup)
   在 FlashDebugger.DebuggerManager.Start(Boolean alwaysStart)</blockquote>

<p>FlashDevelop是直接调用Flex SDK中的fdb进行调试的，出现这个错误的原因，是因为fdb仅支持32位的JVM。</p><!-- more -->
<p>可是，JAVA不是平台无关的么？为什么fdb却只能支持32位的JVM？</p>
<p>的确，纯JAVA程序确实是平台无关的，但是调用了JNI就不同了，JNI是受平台限制的。而通过上面的报错信息，明显能看出是JNI在报错。</p>
<p>找到了问题所在，解决起来就容易了。
下面是解决步骤：</p>

<ol>
	<li><a href="http://www.java.com/zh_CN/download/manual.jsp">安装32位的JVM</a>。JVM是允许32位和64位共存的。</li>
	<li>将环境变量JAVA_HOME改为指向32位JVM的安装路径。</li>
	<li>搞定。</li>
</ol>

但是，在64位操作系统中修改JAVA_HOME环境变量指向32位JVM是个愚蠢的做法。因为这样会导致操作系统中默认使用32位的JVM。所以，有个稍微麻烦一点的办法。

<ol>
	<li>安装32位的JVM。我的JVM 32bit安装在<code>C:\Program Files (x86)\Java\jre7</code>目录。</li>
	<li>在FlashDevelop.exe文件相同的目录下创建一个startFD.bat文件，写入如下内容：
	<code>
	set JAVA_HOME=C:\Program Files (x86)\Java\jre7
	start FlashDevelop.exe
	</code></li>
	<li>双击startFD.bat，程序会首先设置JAVA_HOME变量，然后启动FlashDevelop，并关闭cmd窗口。</li>
</ol>

使用这种方式设置的JAVA_HOME环境变量，只在启动FlashDevelop.exe的时候有效，不会影响系统的已有的环境变量。

网上还能搜到一些其它的解决方案，让我们来看看：

<strong>方案1</strong>，<a href="http://hi.baidu.com/windage1986/item/c5bc0efe19263a1da729880f">来源</a>
<blockquote>复制 jre\bin中的msvcr71.dll到Windows\System32下就可以了</blockquote>
这个方案明显是针对32位操作系统的，所以解决不了本文的问题。


<strong>方案2</strong>，<a href="http://toopro.org/blog/jvm-dll-not-found-flashdebvelop-fd4-java-problem-fix-solved">来源</a>
<blockquote>
Googling about this problem tells that many users have this in JDK 6 solved with msvcr71.dll, but not for me :(
And it's because I have latest JDK 7 which needs msvcr100.dll, so just find this DLL in "jre7/bin" directory and copy to FlashDevelop.exe folder.
For thos who had BadImage problem while building on x64 system, don't forget, that now FD4 uses x32 component, so set JAVA_HOME to point to x32 version of JDK.</blockquote>
这个方案说的比较详细，也指明了JDK7与JDK6所需的msvcr*.dll并不相同。不过按这个方案也是解决不了本文的问题的。倒是最后那句话给了我解决问题的启示。

<a href="http://www.flashdevelop.org/community/viewtopic.php?f=6&t=8374">这是FlashDevelop社区针对这个问题的讨论</a>

