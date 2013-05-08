[在Ant中替换尖括号](http://zengrong.net/post/1717.htm)

我使用`ReplaceRegexp`任务写了一段脚本替换XML的值：

<pre lang="XML">
<replaceregexp file="app.xml"
			match="<filename>"
			replace="name"
			encoding="UTF-8"/>
</pre>

由于XML规范不允许在属性值中出现尖括号，Ant会报错：

>d:\works\build\build.xml:70: 与元素类型 "null" 相关联的 "match" 属性值不能包含 '<' 字符。

把左右尖括号用他们的十六进制代码代替就可以解决这个问题：

<pre lang="XML">
<replaceregexp file="app.xml"
			match="\x3Cfilename\x3E"
			replace="name"
			encoding="UTF-8"/>
</pre>

如果希望在替换的内容中也使用尖括号，需要一点点小技巧：

<pre lang="XML">
<replaceregexp file="app.xml"
			match="(\x3C)filename(\x3E)"
			replace="\1name\2"
			encoding="UTF-8"/>
</pre>

当然，还有更简单的办法，就是使用`Replace`的`replacetoken`。

<pre lang="XML">
<replace file="app.xml" encoding="UTF-8">
	<replacetoken><![CDATA[<filename>]]></replacetoken>
	<replacevalue><![CDATA[<name>]]></replacevalue>
</replace>
</pre>
