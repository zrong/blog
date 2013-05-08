[在ANE中连接Socket服务器的注意事项](http://zengrong.net/post/1667.htm)

##前戏

也许你会奇怪，既然AS提供了Socket实现，为什么还要用ANE来实现Socket连接？

在[在ANE插件中启动AIR开发的Android应用](http://zengrong.net/post/1663.htm)一文的最后，我提到了一个应用案例，我现在将这个案例明确的说明一下。

对于游戏开发者来说，我们希望能推送给用户一些消息。如果使用常规的手段，只能在用户打开游戏的时候，才能和服务器通信，收到这些消息。

如果用户几天不上线，那么可能会错过这些消息，导致游戏中的公告、奖励不能及时到达。

要解决这个问题，我们可以在Android系统中注册一个Service。这个Service长期保持与服务器的连接，或者隔段时间连接一次服务器，收到消息后马上推送给用户。

这种Service，使用AIR是无法实现的，必须用ANE来解决。因此，我们不可能使用AS的Socket来连接服务器，必须用Android SDK提供的Socket连接方法。

##阻力

在JAVA中实现Socket客户端的方法很简单，这里提供一些简单(且不完整)的代码：<!--more-->

<pre lang="JAVA">
private void connectSocket() throws UnknownHostException, IOException
{
	Socket __socket = new Socket();
	//超时10秒
	__socket.connect(new InetSocketAddress("192.168.18.30", 30000), 10000);
	InputStream __input = __socket.getInputStream();
	OutputStream __output = __socket.getOutputStream();
	if(__socket.isConnected()) Log.i(TAG, "连接成功");
	byte[] __sendByte = getSenderData();
	Log.i(TAG, "发送数据的长度:"+__sendByte.length);
	__output.write(__sendByte);
	while(true)
	{
		if(__input.available()>0)
		{
			byte[] __bytes = new byte[__input.available()];
			__input.read(__bytes);
			Log.i(TAG, "收到的数据长度："+__bytes.length);
			break;
		}
	}
	Log.i(TAG, "关于连接");
	__socket.close();
}
</pre>

上面的代码是阻塞式的，没有使用nio是因为我觉得ANE本来就运行在单独的线程中，不用考虑阻塞对UI的影响。

上面的代码在3台Android 2.3设备上运行良好。但当我在Android 4.0设备上测试的时候，问题出现了。

在连接Socket服务器的时候，ANE进程会崩溃并报错，虽然它不影响AIR主进程，但用户可以看到Android系统推送的错误提示。

我测试了3台Android 4.0设备，其中包括2部手机和一部平板电脑，均有同样的问题出现。

##高潮

为什么会如此？

从stackoverflow上找到的说法是，从Honeycomb（蜂巢，Android 3.0）开始，Andorid就不允许在主进程中进行网络IO的调用。应该使用后台线程或者非阻塞式的API来进行网络通信。如果强插，Android会抛出[NetworkOnMainThreadException](http://developer.android.com/reference/android/os/NetworkOnMainThreadException.html)异常。

于是，我把connectServer方法丢到一个线程中去执行，在3台Android 4.0设备上，测试全部正常。

<pre lang="JAVA">
try
{
	Thread __socketThread = new Thread(
			new Runnable()
			{
				
				@Override
				public void run()
				{
					try
					{
						connectServer();
					}
					catch(Exception $e)
					{
						Log.e(TAG, $e.getMessage());
					}
					
				}
			}
			);
	__socketThread.start();
}
catch (Exception e)
{
	Log.e(TAG, e.getMessage());
}
</pre>


##尾声

虽然问题解决了，但疑问依然存在。

**疑问1**

ANE线程难道不就是后台线程么？本身ANE是没有可视界面的，与UI也无关，应该符合上面的条件啊。

**疑问2**

我随后使用Android SDK开发写了一个应用，就在主UI进程中使用阻塞式IO访问Socket服务器，且在Android 4.0系统上测试，却没有发现任何问题。所有的网络通信都正常。

谁能解答这两个问题么？

参考：

* <http://stackoverflow.com/questions/10530451/android-4-0-socket-problems>
* <http://stackoverflow.com/questions/10313377/tcp-socket-on-android-4-0-3>
