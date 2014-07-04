[在lua中递归删除一个文件夹](http://zengrong.net/post/2129.htm)

rmdir in quick-cocos2d-x with lua.

在使用 quick-cocos2d-x 做项目热更新的时候，我需要建立临时文件夹以保存下载的更新包。在更新完成后，我需要删除这些临时文件和文件夹。

cocos2d-x 和 quick-cocos2d-x 都没有提供删除文件夹功能。我做了如下2个尝试：

## 1. 使用C++

在 cocos2d-x 2.x 中的 [AssetsManager][2] 包中提供了一个 `CreateDirectory` 方法。这个方法可以跨平台支持创建文件夹。在实际项目中运行没有问题。<!--more-->

<pre lang="C++">
bool AssetsManager::createDirectory(const char *path)
{
#if (CC_TARGET_PLATFORM != CC_PLATFORM_WIN32)
    mode_t processMask = umask(0);
    int ret = mkdir(path, S_IRWXU | S_IRWXG | S_IRWXO);
    umask(processMask);
    if (ret != 0 && (errno != EEXIST))
    {
        return false;
    }
    
    return true;
#else
    BOOL ret = CreateDirectoryA(path, NULL);
if (!ret && ERROR_ALREADY_EXISTS != GetLastError())
{
return false;
}
    return true;
#endif
}
</pre>

在 cocos2d-x 2.x 的 [AssetsManager sample][1] 范例中提供了一个 `reset` 方法，这个方法使用系统命令递归删除文件夹。

<pre lang="C++">
void UpdateLayer::reset(cocos2d::CCObject *pSender)
{
    pProgressLabel->setString(" ");
    
    // Remove downloaded files
#if (CC_TARGET_PLATFORM != CC_PLATFORM_WIN32)
    string command = "rm -r ";
    // Path may include space.
    command += "\"" + pathToSave + "\"";
    system(command.c_str());
#else
    string command = "rd /s /q ";
    // Path may include space.
    command += "\"" + pathToSave + "\"";
    system(command.c_str());
#endif
    // Delete recorded version codes.
    getAssetsManager()->deleteVersion();
    
    createDownloadedDir();
}
</pre>

但是，这个 `reset` 在 ios 模拟器中运行的时候，xcode会报这样的warinng：

>The iOS Simulator libSystem was initialized out of order.  This is most often caused by running host executables or inserting host dylibs.  In the future, this will cause an abort.

**因此，我转而考虑另一个方案。**

## 2. 纯lua

纯 lua 其实是个噱头。这里还是要依赖 [lfs(lua file sytem)][3]，好在 quick-cocos2d-x 已经包含了这个库。

`lfs.rmdir` 命令 和 `os.remove` 命令一样，只能删除空文件夹。因此实现类似 `rm -rf` 的功能， 必须要递归删除文件夹中所有的文件和子文件夹。

让我们扩展一下 os 包。

<pre lang="lua">
require("lfs")

function os.exists(path)
	return CCFileUtils:sharedFileUtils():isFileExist(path)
end

function os.mkdir(path)
	if not os.exists(path) then
		return lfs.mkdir(path)
	end
	return true
end

function os.rmdir(path)
	print("os.rmdir:", path)
	if os.exists(path) then
		local function _rmdir(path)
			local iter, dir_obj = lfs.dir(path)
			while true do
				local dir = iter(dir_obj)
				if dir == nil then break end
				if dir ~= "." and dir ~= ".." then
					local curDir = path..dir
					local mode = lfs.attributes(curDir, "mode") 
					if mode == "directory" then
						_rmdir(curDir.."/")
					elseif mode == "file" then
						os.remove(curDir)
					end
				end
			end
			local succ, des = os.remove(path)
			if des then print(des) end
			return succ
		end
		_rmdir(path)
	end
	return true
end
</pre>

上面的代码在 iOS 模拟器和 Android 真机上测试成功。Windows系统、Mac OSX 以及 iOS 真机还没有测试。我测试后会立即更新。

[1]: https://github.com/cocos2d/cocos2d-x/tree/v2/samples/Cpp/AssetsManagerTest
[2]: https://github.com/cocos2d/cocos2d-x/tree/v2/extensions/AssetsManage
[3]: https://github.com/keplerproject/luafilesystem
