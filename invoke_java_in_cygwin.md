[在cygwin中调用JAVA程序](http://zengrong.net/post/1610.htm)

只要安装了JDK或者JRE，就可以在cygwin中直接使用JAVA命令。但最大的问题，是在于windows下的JAVA需要Windows格式的路径，而cygwin默认提供给JAVA的路径，JAVA是无法识别的。

例如有一个JAVA程序encrypt.jar，正确的方式应该这样调用：<!--more-->

>java -Dsource=源文件路径 -Dtarget=目标文件路径 -jar encrypt.jar

但如果直接在cygwin下这样调用，就会报错：

<pre lang="BASH">
java -Dsource=~/source.txt -Dtarget=~/target.txt -jar encrypt.jar
#Exception in thread "main" java.io.FileNotFoundException: \home\zrong\source.txt (系统找不到指定的路径。)
</pre>

所以，我们需要借助cygpath命令，将cygwin格式的路径转换成Windows格式。

<pre lang="BASH">
$ cygpath -w ~/source.txt
#D:\cygwin\home\zrong\source.txt
</pre>

这样调用就没问题了

<pre lang="BASH">
java -Dsource=`cygpath -w ~/source.txt` -Dtarget=`cygpath -w ~/target.txt` -jar encrypt.jar
</pre>

cygpath的参数不少，可以使用`cygpath --help`查看
