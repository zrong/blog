[quick-cocos2d-x的热更新机制实现](http://zengrong.net/post/2131.htm)

Hot update in quick-cocos2d-x

# 0. 依赖

这里说的热更新，指的是客户端的更新。

大致的流程是，客户端在启动后访问更新api，根据更新api的反馈，下载更新资源，然后使用新的资源启动客户端，或者直接使用新资源不重启客户端。

这种方式可以跳过AppStore的审核，避免了用户频繁下载、安装、覆盖产品包。

我们一般使用这种方式快速修复产品BUG和增加新功能。

本文基于 [quick-cocos2d-x zrong 修改版][5] 。 <!--more-->

# 1. 前言

在实现这个机制之前，我研究了这两篇文章：

* [quick-cocos2d-x基于源码加密打包功能的更新策略][1] by SunLightJuly
* [看到有同学在研究在线更新，希望我能帮到你一些][2] by Henry

另外，我也查看了 [AssetsManager][3] 的源码和 [sample][4] 。

不幸的是，这几个方案我都不能直接拿来用。因此思考再三，还是自己写了一套方案。

我并不打算实现一套通用的机制。因为热更新有许多的必要条件，每个产品的需求可能都不太想同。

例如 [AssetsManager][3] 那套机制就太死板，在真实的产品中不修改很难使用。

在这里，我尽量详细地阐述我的思路和做法，抛砖引玉吧。

# 2. 特色

基本的热更新功能就不说了大家都有。我这套机制还有如下几个特色：

## 2.1 可以更新 frameworks_precompiled.zip 模块

frameworks 模块是 quick 的核心模块，在quick 生成的项目中，它直接在 AppDelegate.cpp 中载入 `main.lua` 之前进行载入。如下：

<pre lang="c++">
bool AppDelegate::applicationDidFinishLaunching()
{
    // initialize director
    CCDirector *pDirector = CCDirector::sharedDirector();
    pDirector->setOpenGLView(CCEGLView::sharedOpenGLView());
    pDirector->setProjection(kCCDirectorProjection2D);

    // set FPS. the default value is 1.0/60 if you don't call this
    pDirector->setAnimationInterval(1.0 / 60);

    // register lua engine
    CCLuaEngine *pEngine = CCLuaEngine::defaultEngine();
    CCScriptEngineManager::sharedManager()->setScriptEngine(pEngine);

    CCLuaStack *pStack = pEngine->getLuaStack();

#if (CC_TARGET_PLATFORM == CC_PLATFORM_IOS || CC_TARGET_PLATFORM == CC_PLATFORM_ANDROID)
    // load framework
    pStack->loadChunksFromZIP("res/framework_precompiled.zip");

    // set script path
    string path = CCFileUtils::sharedFileUtils()->fullPathForFilename("scripts/main.lua");
	......
</pre>

这可以说明这个核心模块对quick的重要性。正因为它重要，所以必须要能更新它。

## 2.2 可以更新 update 模块自身

更新功能是客户端启动后载入的第一个lua模块，它负责载入更新资源，以及启动主项目。一般情况下，这个模块是不需要改动的。对它进行改动，既不科学，也不安全（安全啊……）。

但是万一呢？大家知道策划和运营同学都是二班的，或许哪天就有二班同学找你说：改改怕什么？又不会怀孕…… 所以这个必须有。

## 2.3 纯lua实现

把这个拿出来说纯粹是撑数的。不凑个三大特色怎么好意思？

上面SunLightJuly和Henry同学的方案当然也是纯lua的。用quick你不搞纯lua好意思出来混？小心廖大一眼瞪死你。

当然，我这个不是纯lua的，我基于 [AssetsManager(C++)][3] 的代码实现了一个 Updater 模块。

而且，我还改了 AppDelegate 中的启动代码。

所以，你看，我不仅是撑数，还是忽悠。

# 3. Updater(C++)

[AssetsManager][3] 中提供了下载资源，访问更新列表，解压zip包，删除临时文件，设置搜索路径等等一系列的功能。但它的使用方式相当死板，我只能传递一个获取版本号的地址，一个zip包的地址，一个临时文件夹路径，然后就干等着。期间啥也干不了。

当然，我可以通过 quick-cocos2d-x 为其增加的 registerScriptHandler 方法让lua得知下载进度和网络状态等等。但下载进度的数字居然以事件名的方式通过字符串传过来的！这个就有点太匪夷所思了点。

于是，我对这个 AssetsManager 进行了修改。因为修改的东西实在太多，改完后就不好意思再叫这个名字了（其实主要是现在的名字比较短 XD）。我们只需要记住这个 Updater 是使用 AssetsManager 修改的即可。

在上面SunLightJuly和Henry同学的方法中，使用的是 CCHTTPRequest 来获取网络资源的。CCHTTPRequest 封装了cURL 操作。而在 Updater 中，是直接封装的 cURL 操作。

在我的设计中，逻辑应该尽量放在lua中，C++部分应该尽量提供功能供lua调用。因为lua可以进行热更新，而C++部分则只能整包更新。

[Updater][6] 主要实现的内容如下：

## 3.1 删除了get和set相关的一堆方法，new对象的时候不必传递参数；

## 3.2 使用 `getUpdateInfo` 方法通过HTTP协议获取升级列表数据，获取到的数据直接返回，C++并不做处理；

## 3.3 使用 `update` 方法通过HTTP协议下载升级包，需要提供四个参数：

1. zip文件的url；
2. zip文件的保存位置；
3. zip 文件的解压临时目录；
4. 解压之前是否需要清空临时目录。

## 3.4 把传递给lua的事件分成了四种类型：

**3.4.1 `UPDATER_MESSAGE_UPDATE_SUCCEED` **

事件名为 success，代表更新成功，zip文件下载并解压完毕；

**3.4.2 `UPDATER_MESSAGE_STATE`  **

事件名为 state，更新过程中的状态（下载开始、结束，解压开始、结束）也传递给了lua。这个方法是这样实现的：

<pre lang="c++">
void Updater::Helper::handlerState(Message *msg)
{
    StateMessage* stateMsg = (StateMessage*)msg->obj;
    if(stateMsg->manager->_delegate)
    {
        stateMsg->manager->_delegate->onState(stateMsg->code);
    }
    if (stateMsg->manager->_scriptHandler)
    {
        std::string stateMessage;
        switch ((StateCode)stateMsg->code)
        {
            case kDownStart:
                stateMessage = "downloadStart";
                break;
                
            case kDownDone:
                stateMessage = "downloadDone";
                break;
                
            case kUncompressStart:
                stateMessage = "uncompressStart";
                break;
            case kUncompressDone:
                stateMessage = "uncompressDone";
                break;
                
            default:
                stateMessage = "stateUnknown";
        }
        
        CCScriptEngineManager::sharedManager()
            ->getScriptEngine()
            ->executeEvent(
                           stateMsg->manager->_scriptHandler,
                           "state",
                           CCString::create(stateMessage.c_str()),
                           "CCString");
    }
    
    delete ((StateMessage*)msg->obj);
}
</pre>
	
**3.4.3 `UPDATER_MESSAGE_PROGRESS`  **

事件名为 progress，传递的对象为一个 CCInteger ，代表进度。详细的实现可以看[源码][6]。

**3.4.4 `UPDATER_MESSAGE_ERROR`  **

事件名为 error，传递的对象是一个 CCString，值有这样几个：

* errorCreateFile
* errorNetwork
* errorNoNewVersion
* errorUncompress
* errorUnknown
	
方法的实现和上面的 `UPDATER_MESSAGE_STATE` 类似，这里就不贴了。详细的实现可以看[源码][6]。

Updater(C++) 部分只做了这些苦力工作，而具体的分析逻辑（分析getUserInfo返回的数据决定是否升级、如何升级和升级什么），下载命令的发出（调用update方法），解压成功之后的操作（比如合并新文件到就文件中，更新文件索引列表等等），全部需要lua来做。下面是一个处理Updater(C++)事件的lua函数的例子。

<pre lang="lua">
function us._updateHandler(event, value)
	updater.state = event
	if event == "success" then
		updater.stateValue = value:getCString()
		-- 成功之后更新资源列表，合并新资源
		updater.updateFinalResInfo()
		-- 调用成功后的处理函数
		if us._succHandler then
			us._succHandler()
		end
	elseif event == "error" then
		updater.stateValue = value:getCString()
	elseif event == "progress" then
		updater.stateValue = tostring(value:getValue())
	elseif event == "state" then
		updater.stateValue = value:getCString()
	end
	-- us._label 是一个CCLabelTTF，用来显示进度和状态
	us._label:setString(updater.stateValue)
	assert(event ~= "error", 
		string.format("Update error: %s !", updater.stateValue))
end

updater:registerScriptHandler(us._updateHandler)
</pre>

# 4. update包（lua）

update包是整个项目的入口包，quick会首先载入这个包，甚至在 framework 之前。

## 4.1 为update包所做的项目修改

我修改了quick项目文件 AppDelegate.cpp 中的 `applicationDidFinishLaunching` 方法，使其变成这样：

<pre lang="c++">
bool AppDelegate::applicationDidFinishLaunching()
{
    // initialize director
    CCDirector *pDirector = CCDirector::sharedDirector();
    pDirector->setOpenGLView(CCEGLView::sharedOpenGLView());
    pDirector->setProjection(kCCDirectorProjection2D);

    // set FPS. the default value is 1.0/60 if you don't call this
    pDirector->setAnimationInterval(1.0 / 60);

    // register lua engine
    CCLuaEngine *pEngine = CCLuaEngine::defaultEngine();
    CCScriptEngineManager::sharedManager()->setScriptEngine(pEngine);

    CCLuaStack *pStack = pEngine->getLuaStack();
    
    string gtrackback = "\
    function __G__TRACKBACK__(errorMessage) \
    print(\"----------------------------------------\") \
    print(\"LUA ERROR: \" .. tostring(errorMessage) .. \"\\n\") \
    print(debug.traceback(\"\", 2)) \
    print(\"----------------------------------------\") \
    end";
    pEngine->executeString(gtrackback.c_str());
    
    // load update framework
    pStack->loadChunksFromZIP("res/lib/update.zip");
    
    string start_path = "require(\"update.UpdateApp\").new(\"update\"):run(true)";
    CCLOG("------------------------------------------------");
    CCLOG("EXECUTE LUA STRING: %s", start_path.c_str());
    CCLOG("------------------------------------------------");
    pEngine->executeString(start_path.c_str());
    
    return true;
}
</pre>

原来位于 main.lua 中的 `__G_TRACKBACK__` 函数（用于输出lua报错信息）直接包含在C++代码中了。那么现在 `main.lua` 就不再需要了。

同样的，第一个载入的模块变成了 `res/lib/update.zip`，当然这个zip也可以放在quick能找到的其它路径中，使用上面的路径只是我的个人习惯。

最后，LuaStack直接执行了下面这句代码启动了 `update.UpdateApp` 模块：

<pre lang="lua">
require("update.UpdateApp").new("update"):run(true); 
</pre>

## 4.2 update包中的模块

update包有三个子模块，每个模块是一个lua文件，分别为：

* update.UpdateApp
* update.updater
* update.updateScene

对于不同的大小写，是因为在我的命名规则中，类用大写开头，对象是小写开头。

**4.2.1 update.UpdateApp**

下面是入口模块 UpdateApp 的内容：

<pre lang="lua">
local UpdateApp = {}

UpdateApp.__cname = "UpdateApp"
UpdateApp.__index = UpdateApp
UpdateApp.__ctype = 2

local sharedDirector = CCDirector:sharedDirector()
local sharedFileUtils = CCFileUtils:sharedFileUtils()
local updater = require("update.updater")

function UpdateApp.new(...)
	local instance = setmetatable({}, UpdateApp)
	instance.class = UpdateApp
	instance:ctor(...)
	return instance
end

function UpdateApp:ctor(appName, packageRoot)
    self.name = appName
    self.packageRoot = packageRoot or appName

	print(string.format("UpdateApp.ctor, appName:%s, packageRoot:%s", appName, packageRoot))

    -- set global app
    _G[self.name] = self
end

function UpdateApp:run(checkNewUpdatePackage)
	--print("I am new update package")
	local newUpdatePackage = updater.hasNewUpdatePackage()
	print(string.format("UpdateApp.run(%s), newUpdatePackage:%s", 
		checkNewUpdatePackage, newUpdatePackage))
	if  checkNewUpdatePackage and newUpdatePackage then
		self:updateSelf(newUpdatePackage)
	elseif updater.checkUpdate() then
		self:runUpdateScene(function()
			_G["finalRes"] = updater.getResCopy()
			self:runRootScene()
		end)
	else
		_G["finalRes"] = updater.getResCopy()
		self:runRootScene()
	end
end

-- Remove update package, load new update package and run it.
function UpdateApp:updateSelf(newUpdatePackage)
	print("UpdateApp.updateSelf ", newUpdatePackage)
	local updatePackage = {
		"update.UpdateApp",
		"update.updater",
		"update.updateScene",
	}
	self:_printPackages("--before clean")
	for __,v in ipairs(updatePackage) do
		package.preload[v] = nil
		package.loaded[v] = nil
	end
	self:_printPackages("--after clean")
	_G["update"] = nil
	CCLuaLoadChunksFromZIP(newUpdatePackage)
	self:_printPackages("--after CCLuaLoadChunksForZIP")
    require("update.UpdateApp").new("update"):run(false)
	self:_printPackages("--after require and run")
end

-- Show a scene for update.
function UpdateApp:runUpdateScene(handler)
	self:enterScene(require("update.updateScene").addListener(handler))
end

-- Load all of packages(except update package, it is not in finalRes.lib)
-- and run root app.
function UpdateApp:runRootScene()
	for __, v in pairs(finalRes.lib) do
		print("runRootScene:CCLuaLoadChunksFromZip",__, v)
		CCLuaLoadChunksFromZIP(v)
	end
	
	require("root.Finger").new("root"):run()
end

function UpdateApp:_printPackages(label)
	label = label or ""
	print("\npring packages "..label.."------------------")
	for __k, __v in pairs(package.preload) do
		print("package.preload:", __k, __v)
	end
	for __k, __v in pairs(package.loaded) do
		print("package.loaded:", __k, __v)
	end
	print("print packages "..label.."------------------\n")
end


function UpdateApp:exit()
    sharedDirector:endToLua()
    os.exit()
end

function UpdateApp:enterScene(__scene)
    if sharedDirector:getRunningScene() then
        sharedDirector:replaceScene(__scene)
    else
        sharedDirector:runWithScene(__scene)
    end
end

return UpdateApp
</pre>

我来说几个重点。

**没有framework**

由于没有加载 framework，class当然是不能用的。所有quick framework 提供的方法都不能使用。

我借用class中的一些代码来实现 UpdateApp 的继承。其实我觉得这个UpdateApp也可以不必写成class的。

**入口函数run**

run 是入口函数，同时接受一个参数，这个参数用于判断是否要检测本地有新的 update.zip 模块。

-- 未完待续 --

[1]: http://my.oschina.net/SunLightJuly/blog/180639
[2]: https://groups.google.com/forum/#!topic/quick-x/ni6Nf50jzfo
[3]: https://github.com/cocos2d/cocos2d-x/tree/v2/extensions/AssetsManage
[4]: https://github.com/cocos2d/cocos2d-x/tree/v2/samples/Cpp/AssetsManagerTest
[5]: https://github.com/zrong/quick-cocos2d-x
[6]: https://github.com/zrong/quick-cocos2d-x/tree/zrong/lib/cocos2d-x/extensions/updater
