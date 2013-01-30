[在ANE插件中启动AIR开发的Android应用](http://zengrong.net/post/1663.htm)

在Android原生应用开发中，启动一个应用非常容易：

<pre lang="JAVA">
Intent __intent = new Intent(this, YourAppActivity.class);
startActivity(__intent); 
</pre>

但在ANE插件开发中，要启动AIR开发的Android应用，就不那么容易了。

因为我并不知道AIR应用的Activicy类名是什么，无法设置Indent。

ANE包含在AIR应用中，我或许可以在ANE中得到AIR应用的Activity类名，但我尝试了下面的方法，不顶用：<!--more-->

<pre lang="JAVA">
public class SetAlarmFun implements FREFunction
{
	public static final String TAG = "org.zengrong.ane.funs.SetAlarmFun";
	
	/**
	 * 保存上下文
	 */
	private FREContext _context;
	
	@Override
	public FREObject call(FREContext $context, FREObject[] $args)
	{
		_context = $context;
		Log.i(TAG, _context.getActivity().getApplicationInfo().className);
		//null
	}
}
</pre>

ANE和AIR应用应该是运行在不同的线程中的，这或许是无法得到类名的原因。

最后，下面的代码可以在ANE中启动AIR开发的Android应用。当然，在Android原生应用中，也可以用这种方法启动AIR应用。

我的AIR应用的包名为`org.zengrong.ane.test`。但是AIR会自动为包名加入`air`前缀。如果是调试版的AIR应用，还会被自动加上`debug`后缀。

因此，这个AIR应用的id实际上变成了`air.org.zengrong.ane.test.debug`。真够长的……

<pre lang="JAVA">
public FREObject call(FREContext $context, FREObject[] $args)
{
	_context = $context;
	Intent __activityIntent = _context.getActivity().getPackageManager().getLaunchIntentForPackage("air.org.zengrong.ane.test.debug");
	startActivity(__activityIntent);
}
</pre>

**这个技巧有什么用？**

例如有个AIR开发的游戏希望在自己没有打开的时候提醒玩家上线，那么它就可以在后台使用ANE悄悄放一个Service，这个Service可以在合适的时候弹出Notification提醒玩家上线。玩家看到消息后，直接单击消息提示，自动打开游戏。

如果我上面说的应用环境你没有看懂，那么就当我没说好了。
