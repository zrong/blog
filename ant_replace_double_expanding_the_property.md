Ant 嵌套的变量扩展

## 需求

实现类似于这样的效果：

<pre lang="XML">
<property name="var1" value="foo"/>
<echo>${${var1}.bar}</echo>
</pre>

Ant 默认是不支持展开嵌套的变量扩展的，因此要用上一些技巧。

## 使用AntContrib

<pre lang="XML">
<propertycopy name="var2" from="${var1}.bar"/>
<echo>${var2}</echo>
</pre>
