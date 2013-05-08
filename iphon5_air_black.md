[让AIR3.5支持iPhone5（去掉黑边）](http://zengrong.net/post/1752.htm)

我知道，在iPhone5那个BT的长脸上，游戏会出现黑边的。

下面的代码在AIR3.5下编译，设置了全屏显示，如果在iPhone5上运行，那么显示的所有分辨率相关的尺寸都是960X640。

what？！iPhone5的脸明明是1136那么长，为啥子就得不到？没错，AIR就是得不到正确的尺寸。

解决的办法，是加一个白色半透明圆角矩形图片，图片上写上 “水果之王万岁，乔布斯永垂不朽，圆角矩形专利一万年” 这句话，放在src根目录下，然后重新发布ipa就可以了。

<!--more-->

**我承认上面在骗人和胡扯。**

正确的方法是这样的：

1. 弄一张图片，高度1136，宽度640，里面随便放点什么内容（不要放果照）；
2. 将其命名为 `Default-568h@2x.png`，放在项目的src目录下，和你的 `project-app.xml` 放在一起；
3. 重新发布ipa，在iPhone5上运行，你就能得到正确的屏幕尺寸了。

回答几个小问题：

3. 为神马一定是568h？因为568x2=1136；
4. 你不必显示这张图片，不必把在放在舞台上，不必在你的代码的任何地方使用这张图片；
5. 你只需要保证这张图片在打包的时候被加入到ipa中就行了，Flash Buidler会自动做这件事的；
6. 如果你不放心，你可以在ipa打包成功之后，随便找个压缩软件打开它，看看解压后能不能找到这个图片。

<pre lang="XML">
<?xml version="1.0" encoding="utf-8"?>
<s:Application xmlns:fx="http://ns.adobe.com/mxml/2009" 
			   xmlns:s="library://ns.adobe.com/flex/spark" 
			   applicationComplete="application1_applicationCompleteHandler(event)">
	<s:TextArea id="infoTA" left="10" right="10" top="10" bottom="100"/>
	<s:Button id="refresBTN" label="刷新" horizontalCenter="0" bottom="20" width="200" click="refresBTN_clickHandler(event)"/>
	<fx:Script>
		<![CDATA[
			import mx.events.FlexEvent;			
			protected function refresBTN_clickHandler(event:MouseEvent):void
			{
				infoTA.text = getScreen();
			}
			
			protected function application1_applicationCompleteHandler(event:FlexEvent):void
			{
				infoTA.text = getScreen();
			}
			
			private function getScreen():String
			{
				var __msg:String = "";
				__msg += "OS:"+Capabilities.os + "\n";
				__msg += "screenDPI:"+Capabilities.screenDPI + "\n";
				__msg += "screenResolutionX:"+Capabilities.screenResolutionX + "\n";
				__msg += "screenResolutionY:"+Capabilities.screenResolutionY + "\n";
				__msg += "stageWidth:"+this.stage.stageWidth+ "\n";
				__msg += "stageHeight:"+this.stage.stageHeight+ "\n";
				__msg += "stage.width:"+this.stage.width+ "\n";
				__msg += "stage.height:"+this.stage.height+ "\n";
				__msg += "stage.fullScreenWidth:"+this.stage.fullScreenWidth+ "\n";
				__msg += "stage.fullScreenHeight:"+this.stage.fullScreenHeight+ "\n";
				return __msg;
			}			
		]]>
	</fx:Script>
</s:Application>
</pre>

还可以看看下面有几篇文章，献给爱鸟语的同学：

* <http://forums.adobe.com/message/4751222>
* <http://forums.adobe.com/thread/1069815>
* <http://forums.adobe.com/thread/1073656>
* <http://forums.adobe.com/message/4727086>
