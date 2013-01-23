[NetworkInfo for iOS](http://zengrong.net/post/1644.htm)
我在Android上使用[flash.net.NetworkInfo](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/net/NetworkInfo.html)实现了socket连接在网络状态改变时的自动重连机制，但却发现在iOS设备上不支持flash.net.NetworkInfo。

Adobe的[API文档](http://help.adobe.com/en_US/FlashPlatform/reference/actionscript/3/flash/net/NetworkInfo.html)中说，NetworkInfo需要[AIR Profile Support](http://help.adobe.com/en_US/air/build/WS144092a96ffef7cc16ddeea2126bb46b82f-8000.html)支持，我在该文档中找到mobileDevice Profile，发现NetworkInfo一栏的值为Check，也就是说，必须由开发者使用NetworkInfo.isSupported来检测设备是否支持NetworkInfo。

悲催的是，iOS设备的NetworkInfo.isSupported是false！这就意味着，不能使用flash.net.NetworkInfo来获取iOS设备的网络状态。

[Adobe AIR Developer Center](http://www.adobe.com/devnet/air.html)中提供了一个iOS的原生插件[NetworkInfo native extension sample](http://www.adobe.com/devnet/air/native-extensions-for-air/extensions/networkinfo.html)来实现获取iOS设备中的网络状态。该文章中直接提供了ANE包的下载，可以直接在Windows环境下使用。

该插件实现了三个类：

<pre>
com.adobe.nativeExtensions.Networkinfo.InterfaceAddress; 
com.adobe.nativeExtensions.Networkinfo.NetworkInfo; 
com.adobe.nativeExtensions.Networkinfo.NetworkInterface; 
</pre>

名称与flash.net下的类相同，但包不同，因此使用的时候要注意包的区别。

这个插件的功能并不完整。因为flash.net.NetworkInfo支持网络状态变更通知(flash.events.Event.NETWORK_CHANGE)，但该插件不支持。

如果希望在一个项目中同时兼容Android和iOS的网络状态，这篇文章提供了一些思路：[Getting NetworkInfo from both Android and iOS](http://cookbooks.adobe.com/post_Getting_NetworkInfo_from_both_Android_and_iOS-19473.html)
