package
{
import flash.display.MovieClip;
import flash.display.DisplayObject;
import flash.display.StageAlign;
import flash.display.StageScaleMode;
import flash.events.Event;
import flash.events.ProgressEvent;
import flash.text.TextField;
import flash.text.TextFormat;
import flash.utils.getDefinitionByName;

public class PreloaderNSPlay extends MovieClip 
{
	public function PreloaderNSPlay()
	{
		_mainClassName = 'NSPlay';
		stage.scaleMode = StageScaleMode.NO_SCALE;
		stage.align = StageAlign.TOP_LEFT;
		stage.showDefaultContextMenu = false;
		_tf = new TextField();
		_tf.defaultTextFormat = new TextFormat(null,12,0,null,null,null,null,null,"center");
		_tf.mouseEnabled = false;
		_tf.height = 20;
		_tf.x = (stage.stageWidth-_tf.width)*.5;
		_tf.y = stage.stageHeight*.5;
		this.addChild(_tf);

		this.loaderInfo.addEventListener(ProgressEvent.PROGRESS,progress);
		this.loaderInfo.addEventListener(Event.COMPLETE,complete);
	}

	protected var _tf:TextField;
	protected var _mainClassName:String;
	
	private function progress(e:ProgressEvent):void
	{
		_tf.text = int(e.bytesLoaded/e.bytesTotal*100)+"% 载入中……";
	}

	private function complete(e:Event):void
	{
		gotoAndStop(2);
		var mainClass:Class = Class(getDefinitionByName(_mainClassName));
		stage.addChild(new mainClass() as DisplayObject);
		destroy();
	}

	private function destroy():void
	{
		this.loaderInfo.removeEventListener(ProgressEvent.PROGRESS,progress);
		this.loaderInfo.removeEventListener(Event.COMPLETE,complete);
		//将预加载类从舞台移除(parent.removeChild也一样，因为parent就是舞台），就会导致Flash Player崩溃
		stage.removeChild(this);
		//parent.removeChild(this);

		//如果只移除显示进度的文本，或者只将自身隐藏而不移除，就不会出现这个Bug
		//this.removeChild(_tf);
		//this.visible = false;
	}
}
}
