[BUG？AIR打包的iOS程序在整数比较上的问题](http://zengrong.net/post/1654.htm)

以前找到过一个[FlashPlayer在执行NetStream.play的时候崩溃的BUG](http://zengrong.net/post/1390.htm)，没想到今天又让我碰到一个AIR的BUG。

和上个BUG不同，这个BUG再现起来相当容易，但我还是找了1天才找到再现的方式。

不说了，直接上代码：

<pre lang="ActionScript">
package
{
import flash.display.Sprite;
import flash.filesystem.File;
import flash.text.TextField;

/**
 * 测试在iOS分发包中的unit与int不能比较的问题
 */
public class IOSUintTest extends Sprite
{
	public function IOSUintTest()
	{
		super();
		init();
		showInfo(-1 <= ZERO_INT);
		showInfo(-1 <= ZERO_UINT);
		showInfo(_num <= ZERO_INT);
		showInfo(_num <= ZERO_UINT);
	}
	
	private var _tf:TextField;
	
	private var _num:int = -1;
	
	public static const ZERO_INT:int = 0;
	
	public static const ZERO_UINT:uint = 0;
	
	private function init():void
	{
		_tf = new TextField();
		_tf.width = 400;
		_tf.height = 400;
		this.addChild(_tf);
	}
	
	private function showInfo($info:*):void
	{
		_tf.appendText(String($info) + File.lineEnding);
	}
}
}
</pre>

地球人都知道，showInfo中的4个比较表达式的值应该都为true。恩，是的，在adb提供的调试版ipa中，它们的值都是true。

#但是，在用于发布的ipa中，它们的值并非都是true！

我这里所说的“用于发布的ipa”，如果用Adobe的话来说，就是“限制分发的临时包”和“部署到Apple App Store的最终发行包“。

将这种包安装到iOS设备上，得到的4个值分别是 true,false,true,false

问题出在int与uint的比较上。因为AIR打包成ipa，实际上是直接将AIR程序打包成2进制代码，而不是采取虚拟机的形式（APK是采取的这种形式）。因此，使用AIR制作的ipa，理论上与使用Objective-C写的ipa没有什么不同。这也是为什么AIR写的ipa能堂而皇之的登上App Store的原因。否则，以苹果那个独裁政策，不卡死Adobe才怪！

既然是Objective-C代码，那么Objective-C的类型转换规则也同样适用与这个比较表达式。在Objective-C中，将int与uint互相比较的时候，会先将int转换成uint，得到4294967294，(4294967294 <= 0) 的值应为false。

Objective-C是基于C语言的。在C语言中，这种情况叫做整型提升。

以下摘自《The C Programming Language》

>A character, a short integer, or an integer bit-field, all either signed or not, or an object of enumeration type, may be used in an expression wherever an integer maybe used. If an int can represent all the values of the original type, then the value is converted to int; otherwise the value is converted to unsigned int. This process is called integral promotion.

在ActionScript中，int与uint比较的时候，是不会进行整型提升的。int和uint都是基于Number，在AVM中，我不知道它们是否进行了严格的划分。

从这个观点上说，这并不是BUG，而是不同语言的特性所致。但是，Adobe既然在大力推广AIR开发iOS应用，就要考虑到不同语言之间的差别，避免出现这种容易被忽视的错误。

这个BUG说起来简单，但是在一个已经存在的大型项目中发现这样的小错误，还是非常困难的。

困难的关键点在于，允许调试的ipa文件(target ipa-debug)中，并不会出现整型提升的问题。这就导致调试的时候正常的程序，在发布的时候不正常。何况发布的文件还无法调试！这绝对是Adobe的工作失误。

这个问题，我不准备报告给Adobe了。大家在开发中养成更严谨的习惯吧。
