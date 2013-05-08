[Android SDK中找不到Arrays.copyOf？](http://zengrong.net/post/1664.htm)

原因很简单——选择的API Level不对。

`java.util.Arrays.copyOf`方法对于JAVA来说，是从JAVA 1.6版本开始加入的；对于Android来说，是从API Level 9才开始有的。

如果基于Android 2.2(API Level 8)开发，当然就没有copyOf方法。

解决办法？

最简单的办法当然是将API Level设置为9。如果一定要基于API Level 8开发，可以使用System.arrayCopy。

如果要寻找copyOf的替代方法，则可以使用这段代码：

<pre lang="JAVA">
//支持基础类型，结果需要转换类型
private final Object copyOf(Object $source, int $newLength) 
{
	Class<?> __type = $source.getClass().getComponentType();
	int __oldLength = Array.getLength($source);
	Object __target = Array.newInstance(__type, $newLength);
	int __preserveLength = Math.min(__oldLength, $newLength);
	System.arraycopy($source, 0, __target, 0, __preserveLength);
	return __target;
}

//支持泛型，但不支持基础类型数组，例如要处理byte[]需要使用上面的方法。
private final <T> T[] copyOf(T[] $source, int $newLength)
{
	Class<?> __type = $source.getClass().getComponentType();
	int __oldLength = Array.getLength($source);
	@SuppressWarnings("unchecked")
	T[] __target = (T[]) Array.newInstance(__type, $newLength);
	int __preserveLength = Math.min(__oldLength, $newLength);
	System.arraycopy($source, 0, __target, 0, __preserveLength);
	return __target;
}
</pre>
