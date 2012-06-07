[读写FREByteArray](http://zengrong.net/post/1628.htm)
 
由于AIR的File API在Android上设备上的限制，我在[ANEToolkit](http://zengrong.net/anetoolkit)的Storage工具中，提供了[readFile](http://zrong.github.com/doc/anetoolkit/org/zengrong/ane/tool/StorageCont.html#readFile())和[writeFile](http://zrong.github.com/doc/anetoolkit/org/zengrong/ane/tool/StorageCont.html#writeFile())方法。这两个方法提供将ByteArray作为文件写入Android设备，或者从Android设备中读取一个文件，并作为ByteArray返回。

本来挺简单的一个功能，可调试来调试去总是报错。插件的调试并不那么容易，必须不断的打包插件、打包APK，测试APK。而且这样的功能只能在手机上调试才行。

弄了几个小时，把注意事项总结如下：

* 在将JAVA的byte[]数组写入FREByteArray对象之前，需要先设定FREByteArray的length属性，否则写入不会成功；
* 从FREByteArray对象中读取AS的ByteArray，不能使用ByteBuffer.array()，应该使用ByteBuffer.get(byte[])。<!--more-->


以下代码取自[ReadFile.java](https://github.com/zrong/anetoolkit/blob/master/androidANE/src/org/zengrong/ane/funs/storage/ReadFile.java)

<pre lang="JAVA">
FileInputStream __inputFile = new FileInputStream(__file);
byte[] __byte = new byte[(int) __file.length()];
__inputFile.read(__byte);
__inputFile.close();
FREByteArray __ba = FREByteArray.newByteArray();
//必须先设置length，否则写入数据不会成功，这点非常重要！
__ba.setProperty("length", FREObject.newObject(__file.length()));
//设置属性必须在捕获锁定之前
__ba.acquire();
ByteBuffer __bb = __ba.getBytes();
__bb.put(__byte);
__ba.release();
return __ba;
</pre>


以下代码取自[WriteFile.java](https://github.com/zrong/anetoolkit/blob/master/androidANE/src/org/zengrong/ane/funs/storage/WriteFile.java)

<pre lang="JAVA">
/**
 * 将FREByteArray转换成byte[]
 * @param $ba
 * @return
 * @throws FREWrongThreadException 
 * @throws FREInvalidObjectException 
 * @throws IllegalStateException 
 */
public byte[] getByteArray(FREByteArray $ba) throws IllegalStateException, FREInvalidObjectException, FREWrongThreadException
{
	//锁定参数
	$ba.acquire();
	ByteBuffer __bb = $ba.getBytes();
	//建立一个数组保存传递来的参数
	byte[] __byte = new byte[(int) $ba.getLength()];
	__bb.get(__byte);
	$ba.release();
	//获取字节数组
	return __byte;
}
</pre>
