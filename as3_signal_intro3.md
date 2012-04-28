#Signals框架介绍（三）原生事件

注意：本文参考[An introduction to AS3 Signals](http://www.developria.com/2010/10/an-introduction-to-as3-signals.html)写成，但不是翻译，有增删改。

* 第一部分：[Signals框架介绍（一）基本用法](http://zengrong.net/post/1504.htm)
* 第二部分：[Signals框架介绍（二）高级事件](http://zengrong.net/post/1507.htm)

<hr>

###原生事件

为了达到替换AS3事件机制的目的，Signals当然包含了对AS3原生事件的支持。这依赖于NativeSignal类。

下面的范例演示了如何在Stage上添加单击事件。由于一看就懂，这里就不废话解释了。

**[NativeSignalSample.as]**

	<pre lang="ActionScript" colla="+" line="1" file="NativeSignalSample.as">
	package
	{
	import flash.display.Sprite;
	import flash.events.MouseEvent;
	import org.osflash.signals.natives.NativeSignal;
	 
	[SWF(width=500,height=300,frameRate=30,backgroundColor=0xFFFFFF)]
	/**
	 * 测试原生事件
	 * @author zrong(zengrong.net)
	 */
	public class NativeSignalSample extends Sprite 
	{
		public function NativeSignalSample()
		{
			_click = new NativeSignal(this.stage, MouseEvent.CLICK, MouseEvent);
			_click.add(handler_click);
			//测试只发生一次的点击事件
			//_click.addOnce(handler_click);
		}
	 
		private var _click:NativeSignal;
	 
		private function handler_click($evt:MouseEvent):void
		{
			trace('currentTarget：',$evt.currentTarget);
			trace('target：',$evt.target);
		}
	}
	}
	</pre>

###其它资料

* [An introduction to AS3 Signals](http://www.developria.com/2010/10/an-introduction-to-as3-signals.html)（本文的参考）
* [AS3 Signals Tutorial](http://johnlindquist.com/2010/01/21/as3-signals-tutorial/)（一个非常棒的视频教程）
* [更多的文章，与其它框架(PureMVC,Robotlegs,Flex)的连用](https://github.com/robertpenner/as3-signals/wiki/community-examples)
* Signals的作者关于AS3事件机制的3篇吐槽文 [之一](http://robertpenner.com/flashblog/2009/08/my-critique-of-as3-events-part-1.html),[之二](http://robertpenner.com/flashblog/2009/09/my-critique-of-as3-events-part-2.html),[之三](http://robertpenner.com/flashblog/2009/09/as3-events-7-things-ive-learned-from.html)
