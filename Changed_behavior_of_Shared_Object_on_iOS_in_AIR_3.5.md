[在AIR3.5中，iOS上的SharedObject的行为改变](http://zengrong.net/post/1766.htm)

原文地址：<http://blogs.adobe.com/airodynamics/2012/12/10/changed-behavior-of-shared-object-on-ios-in-air-3-5/>

**对于AIR3.4和AIR3.5，它们的SharedObject的保存路径不同：**

AIR 3.4:
<pre>
AppName/Library/Application Support/com.namecompany.name/Local Store/ #SharedObjects/Filename.swf
</pre>
`Filename.swf` 就是应用程序描述文件app-xml中的 `<Filename>` 标签指定的值。

AIR 3.5:
<pre>
AppName/Library/Application Support/com.namecompany.name/Local Store/ #SharedObjects/Content.swf
</pre>
`Content.swf` 就是应用程序描述符文件app-xml中的 `<Content>` 标签包含的主swf的文件名。<!--more-->

这可能会导致在AIR 3.4升级到AIR 3.5的时候，SharedObject中保存的数据丢失。
这个问题在 [AIR3.6](http://labs.adobe.com/technologies/flashruntimes/air/) 中已经修复。所以当用户从AIR3.4升级到AIR3.6，那么应用程序不会丢失已经保存的SharedObject数据。

新发布应用的SharedObject的路径为：
<pre>AppName/Library/Application Support/com.namecompany.name/Local Store/ #SharedObjects/Content.swf</pre>

**AIR 3.5的变通方案：**

如果你准备在AIR 3.5中发布你的应用，你可以重命名你的主SWF文件，以匹配 `<Filename>`标签，下面是个例子。

在AIR 3.4中，你的app-xml文件中的配置如下所示:

<pre lang="XML">
<Filename>MysharedObject</Filename>
<Content>Root.swf</Content>
</pre>

在AIR 3.5中，将你的app-xml改成下面这样：

<pre lang="XML">
<Filename>MysharedObject</Filename>
<Content>MysharedObject.swf</Content>
</pre>

同时，也要重命名你的主swf文件名从 `Root.swf` 改为 `MysharedObject.swf`。
用这种方法，在AIR3.4升级到AIR3.5的时候，SharedObject数据会自动保存。
