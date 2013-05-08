[如何知道某个Activity是否在前台？](http://zengrong.net/post/1680.htm)

有一个Android应用包含包含一个后台程序，该程序会定期连接服务器来实现自定义信息的推送。但是，当这个应用处于前台的时候，后台程序就没有必要连接服务器了。这样可以节省网络资源，也更省电。

用什么方法知道该应用是否处于前台呢？

网上搜到的方法大多数都是使用下面的代码：
<pre lang="JAVA">
ActivityManager am = (ActivityManager) this.getSystemService(ACTIVITY_SERVICE);
//获得task列表
List<ActivityManager.RunningTaskInfo > taskInfo = am.getRunningTasks(1); 
Log.d("topActivity", "CURRENT Activity ::"+ taskInfo.get(0).topActivity.getClassName());
ComponentName componentInfo = taskInfo.get(0).topActivity;
componentInfo.getPackageName();
</pre>

但是查阅[Android文档](http://developer.android.com/reference/android/app/ActivityManager.html#getRunningTasks(int))后发现，google并不推荐使用这个方法：

>This should never be used for core logic in an application, such as deciding between different behaviors based on the information found here. Such uses are not supported, and will likely break in the future. For example, if multiple applications can be actively running at the same time, assumptions made about the meaning of the data here for purposes of control flow will be incorrect.

而且，这个方法还要求设置`android.permission.GET_TASKS`权限。

因此，我必须寻找更加合适的方法来做这件事。最终，我找到这个方法[getRunningAppProcesses()](http://developer.android.com/reference/android/app/ActivityManager.html#getRunningAppProcesses())，它并不需要增加特殊的权限。

下面是范例代码：

<pre lang="JAVA">
/**
 * 返回当前的应用是否处于前台显示状态
 * @param $packageName
 * @return
 */
private boolean isTopActivity(String $packageName) 
{
	//_context是一个保存的上下文
	ActivityManager __am = (ActivityManager) _context.getApplicationContext().getSystemService(Context.ACTIVITY_SERVICE);
	List<ActivityManager.RunningAppProcessInfo> __list = __am.getRunningAppProcesses();
	if(__list.size() == 0) return false;
	for(ActivityManager.RunningAppProcessInfo __process:__list)
	{
		Log.d(getTAG(),Integer.toString(__process.importance));
		Log.d(getTAG(),__process.processName);
		if(__process.importance == ActivityManager.RunningAppProcessInfo.IMPORTANCE_FOREGROUND &&
				__process.processName.equals($packageName))
		{
			return true;
		}
	}
	return false;
}
</pre>
