* <span style="color:red">2012-10-10更新：</span>加入Flash Player 11.5/AIR 3.5的对应关系；加入发布日期列；修改文章结构和部分内容。
* <span style="color:red">2012-08-27更新：</span>加入Flash Player 11.4/AIR 3.4的对应关系。
* <span style="color:red">2012-03-20更新：</span>本篇文章只讲了Flex SDK的情况，但Flash IDE也能通过修改配置文件的方式支持新的Flash Player功能，详见这里：[让Flash支持更新的Flash Player功能](http://zengrong.net/post/1568.htm)
* <span style="color:red">2012-04-08更新：</span>加入AIR的版本说明；加入Flash Player 11.3的对应关系。

在[Flex 4.6 SDK](http://opensource.adobe.com/wiki/display/flexsdk/Download+Flex+4.6)中，可以发现`framework/flex-config.xml`中的默认-swf-version的值变成了14，而-target-player则变成了11.1。

记得在[Flash Player 10.2发布](http://zengrong.net/post/1244.htm)的时候，为了使用Flash 10.2提供的原生位图鼠标光标功能，需要在编译的时候将`-swf-version`编译器属性值设置为11。以此推算，14这个值是针对Flash Player 11.1的。

那么-swf-version和-target-player的对应关系如何？见下表：<!--more-->

<table>
<tr>
<td>Flash Player</td>
<td>AIR</td>
<td>Flex</td>
<td>-swf-version</td>
<td>-target-player</td>
<td>发布日期</td>
</tr>
<tr>
<td>9</td>
<td>&nbsp;</td>
<td>3</td>
<td>9</td>
<td>9</td>
<td></td>
</tr>
<tr>
<td>10.0</td>
<td>1.5</td>
<td> 4.0</td>
<td>10</td>
<td>10.0.0</td>
<td></td>
</tr>
<tr>
<td>10.1</td>
<td>2.0/2.5</td>
<td>4.1</td>
<td>10</td>
<td>10.1.0</td>
<td></td>
</tr>
<tr>
<td>10.2</td>
<td>2.6</td>
<td>4.5/4.5.1</td>
<td>11</td>
<td>10.2.0</td>
<td>2011-2-9</td>
</tr>
<tr>
<td>10.3</td>
<td>2.7</td>
<td></td>
<td>12</td>
<td>10.3.0</td>
<td></td>
</tr>
<tr>
<td>11.0</td>
<td>3.0</td>
<td></td>
<td>13</td>
<td>11.0.0</td>
<td>2011-10-4</td>
</tr>
<tr>
<td>11.1</td>
<td>3.1</td>
<td>4.6</td>
<td>14</td>
<td>11.1</td>
<td>2011-11-7</td>
</tr>
<tr>
<td>11.2</td>
<td>3.2</td>
<td></td>
<td>15</td>
<td>11.2</td>
<td>2012-3-28</td>
</tr>
<tr>
<td>11.3</td>
<td>3.3</td>
<td></td>
<td>16</td>
<td>11.3</td>
<td>2012-6-8</td>
</tr>
<tr>
<td>11.4</td>
<td>3.4</td>
<td>Adobe Flex 4.6/Apache Flex 4.8</td>
<td>17</td>
<td>11.4</td>
<td>2012-8-21</td>
</tr>
<tr>
<td>11.5</td>
<td>3.5</td>
<td>Adobe Flex 4.6/Apache Flex 4.8</td>
<td>18</td>
<td>11.5</td>
<td>2012-9-26 beta</td>
</tr>
</table>

##-target-player和-swf-version

上面的这份表格，一部分是根据[Targeting Flash Player versions](http://help.adobe.com/en_US/flex/using/WS2db454920e96a9e51e63e3d11c0bf69084-7ee0.html)整理出来的，最新的部分是我自己根据Flash Player/AIR的更新不断增加的。但这个表格是**不精确**的。

因为，-swf-version的值能支持到那个程度，其实与Flex SDK并没有直接的关系，而是依赖于Flex SDK中的playerglobal.swc（位于frameworks/libs/player）。

打开Flex 4.6 SDK的frameworks/libs/player文件夹，可以看到其中只有一个11.1子文件夹，放置着针对Flash Player 11.1的playerglobal.swc。这个swc的作用有2个：
（这里是基于Flex SDK和Flash Builder讲解，如果你使用Flash Professional，可以看这里：[让Flash支持更新的Flash Player功能](http://zengrong.net/post/1568.htm)）

1. 在程序编写期间，Flash Builder使用它来提供自动完成功能。当然，如果直接用mxml编译器（[比如我](http://zengrong.net/post/1307.htm)），就没多大关系；
2. 在程序编译期间，mxmlc编译器需要调用它。

那么`-target-player`是干嘛的？它用来告诉Flex编译器，在哪里去找`playerglobal.swc`。

在Flash Builder 4.6 的项目的 ActionScrip编译器 设置中，可以设置`-target-player`参数的值。默认是“使用SDK所需的最低版本”。对于我目前安装的Flex SDK 4.6来说，这个“最低版本”就是11.1。

而我们可以使用特定的版本，例如下图中是11.2.0。

<img src="/wp-content/uploads/2011/12/as_compiler_config.png" alt="" title="as_compiler_config" width="275" height="393" class="aligncenter size-full wp-image-1704" />

在程序编写期间，Flash Builder会自动去`frameworks/libs/player/11.2`这个目录中寻找`playerglobal.swc`，如果找不到，一些11.2才支持的功能（例如MouseEvent.RIGHT_CLICK）就无法得到语法提示。

而在调试和发布程序的时候，编译器使用`frameworks/libs/player/11.2/playerglobal.swc`进行编译。如果依然找不到这个文件，编译会报错`无法打开“D:\flex_sdks\4.6.0\frameworks\libs\player\11.2\playerglobal.swc”`，如下图所示：

<img src="/wp-content/uploads/2011/12/no_playerglobal.png" alt="" title="no_playerglobal" width="784" height="109" class="aligncenter size-full wp-image-1703" />

##不同步性

在每个新版本的Flash Player 发布的时候，Adobe都一起提供了`playerglobal.swc`文件，而且会在发布文档中说明这个版本的Flash Player对应的`-swf-version`是多少。

因为SDK的发布，和Flash Player的发布**并非总是同步的**。

在Flash 8时代，编译器和Flash Player是完全同步的。因为那时，只有Flash IDE可以生成swf文件。而Flex问世，以及MacroMedia被Adobe收购以后，Flash的发展就变得多样了，FlashIDE和Flex都可以生成swf文件，Flash Player的发展也更加独立。现在的情况，Flash CS，Flash Builder，Flex SDK，Flash Player的发布已经完全不同步了。尤其是当Adobe将Flex SDK交给Apache发展后，SDK的更新速度估计会更快。Adobe自己又会紧紧将Flash Player攥在手里，保持自己的步调来更新。（关于这段历史，我在[Actionscript,AS3,MXML,Flex,Flex Builder,Flash Builder,Flash,AIR,Flash Player之关系](http://zengrong.net/post/1295.htm)一文中做了详述）

Flex SDK可以和不同版本的Flash Player相配。即使是使用Flex SDK 3.6，同样也可以开发出Flash Player 11.1支持的swf程序。（当然，前提是不使用Flex frameworks提供的组件，仅仅使用Flash Player提供的API）。通过使用不同版本Flash Player提供的playerglobal.swc文件，就可以让旧的Flex SDK兼容新的-swf-version和 -target-player编译属性。当然，也可以让新的Flex SDK兼容旧的-swf-version和-target-player。

例如，目前Adobe官方提供的最新版（也是Adobe Flex的最终版，因为后面会更名为Apache Flex SDK）Flex SDK版本为4.6。根据Adobe的说法，这个版本的Flex SDK的最低支持的-target-player为11.1。这是因为frameworks/libs/player中仅仅提供了11.1版本的playerglobal.swc。我们可以将其他版本的playerglobal.swc复制到该目录下，并修改frameworks/flex-config.xml中的target-player标签，以改变Flex SDK默认编译的swf目标。当然，更方便和灵活的做法是在Flex项目的编译属性中设置-target-player属性。

这里还有一篇文章介绍：[Versioning in Flash Runtime (-swf-version)](http://blogs.adobe.com/airodynamics/2011/08/16/versioning-in-flash-runtime-swf-version/)
