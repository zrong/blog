[升级Flash Builder 4.6中的AIR SDK](http://zengrong.net/post/1767.htm)

原文地址：<http://helpx.adobe.com/flash-builder/kb/overlay-air-sdk-flash-builder.html>
本文并没有“忠于”原文翻译。
<hr>

Flash Builder 4.7自带AIR SDK 3.4版本。如果你希望使用更新版本的AIR SDK，下载并覆盖软件自带的AIR SDK版本就行了。下面是步骤：

1. 下载对应你操作系统版本的[AIR SDK](http://labs.adobe.com/downloads/asc2.html)（其实也就2个版本而已……）。这个版本包含AIR SDK、AS编译器和其他必要的组件和文件；
2. 退出Flash Builder；
3. 备份AIR SDK  
这是可选步骤，AIR SDK默认位于下面这些目录：
	* Windows 7(32位):   
	C:\Program Files (x86)\Adobe\Adobe Flash Builder 4.7\eclipse\plugins\com.adobe.flash.compiler_4.7.0.349722
	* Windows 7(64位):   
	C:\Program Files\Adobe\Adobe Flash Builder 4.7 (64 Bit)\eclipse\plugins\com.adobe.flash.compiler_4.7.0.349722
	* Mac OS:   
	/Applications/Adobe Flash Builder 4.7/eclipse/plugins/com.adobe.flash.compiler_4.7.0.349722
	* Linux：  
	null（这个我是骗你的，AIR的Linux版被Adobe谋杀了）
4. 备份完毕后，删除 `AIRSDK` 目录中的所有文件。
5. 解压缩下载的 `AIR SDK` 压缩包到已经被删除所有内容的 `AIRSDK` 空目录中。
