[AIR 3.7 Bug:You uploaded an unsigned APK](http://zengrong.net/post/1838.htm)

将一个需要更新的APK上传到Google Play的时候，Google Play提示我这样的错误：

>Uploaded failed
>You uploaded an unsigned APK. You need to create a signed APK.

截图如下：

<img src="/wp-content/uploads/2013/04/upload_apk.png" alt="upload_apk_error" width="612" height="281" class="aligncenter size-full wp-image-1839" />

这个提示无疑是 **错误** 的。我并没有修改过任何编译参数，也从来没有修改过打包使用的证书。在程序编译正常的情况下去修改编译参数和证书？我不是吃饱了撑的么。

这个APK在Android设备上是可以正常安装和运行的，因此程序本身没有什么问题。

我怀疑了许多地方，比如是否有ANE需要签名，或者是否有某些Android权限比较特殊，都没有找到什么线索。
<!--more-->
突然想起昨天曾经把 `AIR 3.6 SDK` 更新成了 `AIR 3.7 SDK` ，是否是这个原因呢？于是我将SDK切换回 3.6版本，果然一切正常了。使用 `AIR 3.6 SDK` 编译的APK包，Google Play上传和更新正常。

但是，这并没有解决问题。对于 AIR 这个 **被Adobe寄予厚望的、BUG重重的、快速更新的** 平台，我不可能永远不更新它。我必须找到真正的原因。

终于，在编译了几十个测试包之后，我终于找到了真正原因。

原来导致APK签名错误的罪魁祸首，是图标！

APK的图标是在 **应用程序描述符文件** `app-xml` 中设置的，这是我原来的设置：

<pre lang="XML">
<!-- 此内容是AIR 的应用程序描述符文件的一部分 -->
<icon>
	<image16x16>assets/icon/16.png</image16x16>
	<image32x32>assets/icon/32.png</image32x32>
	<image36x36>assets/icon/36.png</image36x36>
	<image48x48>assets/icon/48.png</image48x48>
	<image57x57>assets/icon/57.png</image57x57>
	<image72x72>assets/icon/72.png</image72x72>
	<image114x114>assets/icon/114.png</image114x114>
	<image128x128>assets/icon/128.png</image128x128>
	<image144x144>assets/icon/144.png</image144x144>
</icon>
</pre>

我知道这样设置的图标有点多。其实Android不需要这么多图标。但iOS那个变态需要。早期写编译脚本的时候，对于iOS和Android使用的是同一个app-xml文件，需要在XML中包含Android和iOS支持的所有图标尺寸。现在虽然已经分开了，但旧的app-xml就一直保存了下来。

直到AIR 3.6 SDK，这样写都是没有问题的，打包出APK可以正常安装运行，也可以正常上传到Google Play。

可是到了AIR 3.7 SDK，这样写就不行了，这会导致我上面阐述的问题。可是纠结的地方就在于打包出来的APK是可以正常使用的，而且打包过程中，也没有任何的提示或者错误信息。

算了，多的话不说了，浪费的时间和精力那都是浮云。现在说解决方案。

<pre lang="XML">
<icon>
	<image36x36>assets/icon/36.png</image36x36>
	<image48x48>assets/icon/48.png</image48x48>
	<image72x72>assets/icon/72.png</image72x72>
</icon>
</pre>

对于Android来说，只需要3个图标就可以了，分别对应Android系统的低密度、中密度、高密度设备。

更详细的描述，可以在这里找到：[Application icons](http://help.adobe.com/en_US/air/build/WS901d38e593cd1bac1e63e3d129907d2886-8000.html)

重新打包，搞定。

要查看我发现的更多Adobe产品Bug，可以看这里：[AdobeBug](http://zengrong.net/post/tag/AdobeBug)
