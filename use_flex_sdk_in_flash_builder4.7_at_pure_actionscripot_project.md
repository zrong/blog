[在Flash Builder 4.7的纯AS项目中使用Flex SDK](http://zengrong.net/post/1768.htm)

## 现象

将Flash Builder升级到4.7版本后，我发现以前建立的 ActionScript 项目会默认使用 `AIR SDK`，而不是使用 `Flex SDK`。这导致我以前的项目无法使用。因为某些类依赖Flex SDK中提供的 [TLF](http://zengrong.net/post/tag/tlf) 框架，或者只有Flex SDK才有的 SpriteAssets 等Class。

<img src="/wp-content/uploads/2012/12/old_project.png" alt="old_project" width="239" height="285" class="aligncenter size-full wp-image-1771" />

查看项目属性，会发现编译器默认为AIR SDK 3.4，且无法修改：

<img src="/wp-content/uploads/2012/12/air_sdk_compiler.png" alt="air_sdk_compiler" width="521" height="304" class="aligncenter size-full wp-image-1769" />

## 解决方案

用文本编辑器打开项目文件中的 `.actionScriptProperties`，搜索 `useFlashSDK`，将其值替换成 `false`。

<img src="/wp-content/uploads/2012/12/use_flash_sdk.png" alt="use_flash_sdk" width="781" height="230" class="aligncenter size-full wp-image-1772" />

刷新一次项目，再次查看项目属性，发现编译器已经改成了 `Flex SDK`。

<img src="/wp-content/uploads/2012/12/flex_sdk_compiler.png" alt="flex_sdk_compiler" width="530" height="372" class="aligncenter size-full wp-image-1770" />
