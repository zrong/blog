"=========== Meta ============
"StrID : 1695
"Title : 生成Google Play需要的p12自签名数字证书
"Cats  : 技术
"Status: draft
"Preview: http://zengrong.net/?p=1695&preview=true
"Tags  : AIR, Android, google
"========== Content ==========
[生成Google Play需要的p12自签名数字证书](http://zengrong.net/post/1695.htm)
Google Play的比App Store的要求松太多，可以制作一个自签名证书来对自己的应用进行签名。

有许多工具可以生成这个自签名证书。下面讲讲在使用AIR发布Google Play应用的时候，如何生成需要的证书。

<h2>使用AIR ADT工具生成p12证书</h2>

AIR SDK中包含的ADT工具提供了方法让我们创建一个自签名的p12证书。

下面的代码生成一个所有者为zengrong.net的证书，密码为123456，保存在当前目录下，文件名为zrong.p12。

<pre>
adt -certificate -cn zengrong.net 1024-RSA zrong.p12 123456
</pre>

使用Flash Builder的”导出发行版”功能，也可以基于图形界面生成一个p12证书，用于给AIR程序签名。

关于使用ADT签名的详细信息，可以看下面两篇文章：

<ul>
	<li><a href="http://help.adobe.com/zh_CN/air/build/WS5b3ccc516d4fbf351e63e3d118666ade46-7f72.html">ADT 代码签名选项</a></li>
	<li><a href="http://help.adobe.com/zh_CN/air/build/WS5b3ccc516d4fbf351e63e3d118666ade46-7f74.html">使用 ADT 创建自签名证书</a></li>
</ul>

但是，这样得到的证书打包出的Android应用程序，并不能提交到Google Play上。

这是因为Google Play要求对应用程序进行签名的证书，过期日期必须在2033年10月22日之后。而ADT生成的数字证书，只有5年有效期。

我们可以用JDK提供的keytool工具来查看刚才生成的证书的具体信息：

<pre>
keytool -list -keystore zrong.p12 -storetype pkcs12 -v

输入密钥库口令:

密钥库类型: PKCS12
密钥库提供方: SunJSSE

您的密钥库包含 1 个条目

别名: 1
创建日期: 2012-9-27
条目类型: PrivateKeyEntry
证书链长度: 1
证书[1]:
所有者: CN=zengrong.net
发布者: CN=zengrong.net
序列号: 2d35623566386132633a31336130373138653863333a2d38303030
有效期开始日期: Wed Sep 26 17:40:04 CST 2012, 截止日期: Wed Sep 27 17:40:04 CST 2017
证书指纹:
         MD5: 6C:EB:0D:73:1A:15:C9:12:5E:DE:69:BA:C7:C2:0F:23
         SHA1: 3E:2C:38:0A:CA:D5:D0:5B:67:80:92:50:46:36:99:82:1D:41:C9:25
         SHA256: 83:C4:F8:4F:7C:97:CB:EC:51:64:BC:B2:D0:DA:E8:97:48:C1:FD:BF:A1:8F:45:A5:75:39:81:E9:6A:51:7C:FB
         签名算法名称: SHA1withRSA
         版本: 3
</pre>

从该证书的截至日期，可以看出这个证书在2017年9月27日过期。

如果使用这个证书来对Android程序进行签名，在网上提供给别人下载是可以的，提交野鸡市场也是可以的。但如果提交到Google Play，Google就会提示你证书的时间有问题，并拒绝提交。

<h2>使用JDK keytool工具生成p12证书</h2>

keytool工具包含在JDK中，如果没有JDK，<a href="http://www.oracle.com/technetwork/java/javase/downloads/index.html">猛击下载</a>。

keytool支持交互的方式提供证书信息。要生成一个p12证书，必须了解这样几个参数：

<ul>
	<li>-genkeypair 生成证书</li>
	<li>-keystore 生成证书的路径和文件名</li>
	<li>-storetype 生成的证书类型，使用pkcs12指定p12格式证书</li>
	<li>-validity 有效期的天数，用一个足够大的值跳转到2034年</li>
</ul>

下面是一个例子：

<pre>
keytool -genkeypair -keystore zrong2.p12 -storetype pkcs12 -validity 8050
输入密钥库口令:
再次输入新口令:
您的名字与姓氏是什么?
  [Unknown]:  zengrong.net
您的组织单位名称是什么?
  [Unknown]:  zengrong.net
您的组织名称是什么?
  [Unknown]:  zengrong.net
您所在的城市或区域名称是什么?
  [Unknown]:  WUHAN
您所在的省/市/自治区名称是什么?
  [Unknown]:  HUBEI
该单位的双字母国家/地区代码是什么?
  [Unknown]:  CN
CN=zengrong.net, OU=zengrong.net, O=zengrong.net, L=WUHAN, ST=HUBEI, C=CN是否正确?
  [否]:  y
</pre>

还是用上面的方法验证一下证书的有效期：

<pre>
keytool -list -keystore zrong2.p12 -storetype pkcs12 -v
输入密钥库口令:

密钥库类型: PKCS12
密钥库提供方: SunJSSE

您的密钥库包含 1 个条目

别名: mykey
创建日期: 2012-9-27
条目类型: PrivateKeyEntry
证书链长度: 1
证书[1]:
所有者: CN=zengrong.net, OU=zengrong.net, O=zengrong.net, L=WUHAN, ST=HUBEI, C=CN
发布者: CN=zengrong.net, OU=zengrong.net, O=zengrong.net, L=WUHAN, ST=HUBEI, C=CN
序列号: 1faa29fb
有效期开始日期: Thu Sep 27 18:23:31 CST 2012, 截止日期: Thu Oct 12 18:23:31 CST 2034
证书指纹:
         MD5: F8:00:9C:3B:7B:4F:F2:9D:A3:B6:3F:E9:78:2D:9A:46
         SHA1: 10:21:FF:B3:DE:3F:D4:0D:44:F7:D1:07:6A:3F:09:D8:36:B9:D1:21
         SHA256: AB:8A:09:5B:69:1F:95:A5:94:F7:60:F6:D0:81:8A:1D:23:42:94:3C:96:D3:04:AD:C9:59:05:14:2E:B6:6D:79
         签名算法名称: SHA1withDSA
         版本: 3
</pre>

使用这个证书，重新对AIR程序进行打包，就可以提交Google Play了。

<strong>参考文章：</strong>

<ul>
	<li>
		<a href="http://blog.csdn.net/kmyhy/article/details/6431609">http://blog.csdn.net/kmyhy/article/details/6431609</a>
	</li>
	<li>
		<a href="http://5aijava.iteye.com/blog/123269">http://5aijava.iteye.com/blog/123269</a>
	</li>
	<li>
		<a href="http://www.android123.com.cn/androidkaifa/173.html">http://www.android123.com.cn/androidkaifa/173.html</a>
	</li>
</ul>
