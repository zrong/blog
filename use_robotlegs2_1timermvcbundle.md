Robotlegs2中文教程-1使用MVCBundle

## 目的

本章使用Robotlegs2自带的MVCBundle实现一个简单的MVC实例。

Robotlegs2在架构设计上，框架仅实现了生命周期管理、Logger、消息调度、插件管理器、配置管理器等核心功能，其他功能全部使用插件实现。而MVCBundle，就是Robotlegs2提供的一个插件和配置集合，这个集合包含所有MVC需要的插件和功能。

本章不会研究Robotlegs2在结构上的设计，而是从最终用户的角度来使用MVCBundle。若希望了解Robotlegs2的架构，请关注本系列后续文章。

本章也不会详细介绍MVCBundle的所有用法，那样会导致本文篇幅过长。下一章会进行详细介绍。

## Timer-MVCBundle-Sample概述

Timer-MVCBundle-Sample是本章的实例名称。这个实例实现了一个简单的定时器。看看定时器的3个状态：

1. 初始状态，设置时、分，类名为TimerSetView。按Start按钮开始倒计时。
![TimerSetView][i1]

2. 倒计时状态，类名为TimerActionView。按Cancel按钮取消倒计时，回到初始状态。
![TimerActionView][i2]

3. 倒计时时间到，类名为AlertView。按Dismiss按钮回到初始状态。
![AlertView][i3]

## 项目依赖

本项目依赖 [minimalcomps][u1] 组件库和 [robotlegs 2.0.0b6][u5]。

## 项目结构

这里简单介绍一下项目中的包分类，以及各个部分的作用。介绍按照MVC分块进行。如果你性急，也可以跳过这部分直接看后面的项目详解。

### View + Mediator

刚才看到的后缀为View的类，我叫它们“视图类”，所有的视图类，都位于 `view` 包中，并实现 `ITimerView` 接口。 `ITimerView` 中并没有包含任何方法签名。实现这个接口，是为了方便进行类型匹配。

视图类用于我们能看到的定时器的3个状态，每个状态对应一个视图。定时器运行的过程中所显示的状态，在这3个视图之间切换。上节 `Timer-MCBundle-Sample` 已经介绍了这3个状态以及对应的类名。

视图类都是显示对象的子类，3个视图也就是3个显示对象。在一个视图显示的时候，它会被加到舞台上，其他的视图则移出舞台。

在这个项目中，我使用了[MinialComps](http://www.minimalcomps.com/)组件。视图类继承其中的VBox或者HBox。3个视图类如下图：
![View][i4]

每个视图类都有一个带有Mediator后缀的类，这是视图类的中介类。中介类负责管理视图事件，接收和传递系统事件等等。所有的中介类都继承 Robotlegs2 提供的 `Mediator` 类。如下图：
![Mediator][i5]

### Model

此项目有2个Model：`TimerModel` 和 `ViewModel`。

`TimerModel` 实现 `ITimerModel` 接口。由于项目过于简单，`ITimerModel` 中不包含任何需要具体实现的方法，但是这种编程习惯是Robotlegs所推荐的。它既方便了在Robotlegs中替换Model（例如你可以在开发和发布的时候使用不同的Model），也符合中的针对接口编程的OO原则。

`TimerModel` 中包含了一个 `flash.util.Timer` 实例，用它来实现定时器的核心功能。同时它还会发布定时器 工作的事件，并暴露一些方法来停止和启动定时器。

`ViewModel` 保存上面提到的3个视图类的实例，以此实现对视图实例的重用。同时它还提供一个 `getView()` 方法根据类或者类名来获取一个新的/重用的实例。你可以把 `ViewModel` 理解成一个对象池，虽然它并不是对象池。如下图：
![Model][i6]

### Command + Event

此项目有3个Commnd： `ChangeStateCmd` 、 `TimerStartCmd` 和 `TimerStopCmd` 。

`ChangeStateCmd` 负责切换视图状态。它收到切换的命令，然后移除掉当前舞台上的视图实例，再从 `ViewModel` 中获取一个视图实例，将它加到舞台上。

`TimerStartCmd` 负责用户主动开始定时器运行的事件。它只是简单的更新 `TimerModel` 中的定时器流逝时间，然后开启定时器。

`TimerStopCmd` 负责用户主动停止定时器运行的事件。它停止 `TimerModel` 中的定时器，然后将视图切换到 `TimerSetView`。

`TEvent` 是此项目中使用的系统事件类型。上面的几个Command均使用这个类型代表的事件来触发。如下图：
![Command and Event][i7]

## 项目详解

### 初始化Robotlegs

先来看看主类的全部内容（省略了package和import）：

<pre lang="ActionScript">
[SWF(width=200,height=200)]
public class Robotlegs2TimerExample extends Sprite
{
	public function Robotlegs2TimerExample() 
	{
		Style.embedFonts = true;
		Style.fontSize = 8;
		Component.initStage(this.stage);
		init();
	}
	
	private var _context:IContext;
	
	private function init():void
	{
		_context = new Context()
		.install(MVCSBundle)
		.configure(AppConfig)
		.configure(new ContextView(this));
		
		_context.logLevel = LogLevel.DEBUG;
		trace("init done");
		
		//这里通过内置的事件框架来实现View的启动
		(_context.injector.getInstance(IEventDispatcher) as IEventDispatcher).dispatchEvent(new TEvent(TEvent.CHANGE_STATE, TimerSetView));
	}
}
</pre>

Style和Component都是 [minimalcomps][u1] 中的类，具体用法可参考该[组件源码][u2]。需要注意的是，如果需要显示中文，那么需要将 `Style.embedFonts` 设置为 `false`，具体原因可参考 [MinimalComps简介－一个超轻量级的纯AS组件库][u3]。

让我们来看 `init` 方法的具体内容。`Context` 类是Robotlegs初始化的核心。在本项目的初始化当中，我们使用了 `Context` 的 `install` 和 `configuare` 方法。这两个方法都会返回 `Context` 自身，因此我们可以进行链式调用。

链式调用是JAVA和JavaScript中常用的调用方式，能减少代码量，让代码看起来更干净。当然，如果你不愿意用它，依然可以使用旧的方式。例如，上面的链式调用可以改成这样：

<pre lang="ActionScript">
_context = new Context();
_content.install(MVCSBundle);
_content.configure(AppConfig);
_content.configure(new ContextView(this));
</pre>

`install()` 的作用是安装一个 `IExtension` 或者 `IBundle`。前者是一个扩展，后者是一个/一堆扩展和配置的集合。Robotlegs2根据我们的调用对 `IExtension` 和 `IBundle` 进行按需安装，这样可以节省资源。`install()` 支持无限参数，如果有多个 `IBundle`，可以使用链式调用进行单个安装，也可以使用一个 `install()` 多个参数进行安装。

**注意**

>为了描述的统一性和准确性，后文将不对 `IExtension` 和 `IBundle` 进行翻译，而直接使用接口名。

`MVCBundle` 是一个包含许多 `IExtension` 的 `IBundle`，它包含了MVC框架中的所有 `IExtension`。除此以外，它还包含一些Logger系统等核心功能。在这个项目中，我们不需要其他的 `IExtension` ，一包足矣。

`configuare()` 的作用是对项目进行配置，通常将各种映射放在这里。与 `install()` 只能接收 `IBundle` 和 `IExtension` 不同， `configuare()` 可以接受任何类型的对象作为参数。同时，它也接受多个参数。例如上面的 `configuare()` 相关代码可以写成这样：

<pre lang="ActionScript">
_content.configure(AppConfig, new ContextView(this));
</pre>

需要注意的是，对于ContextView的配置，必须放在所有配置的最后。具体原因，请关注本系列后续文章。

`ContextView` 保存根显示对象的引用。我们可以将它注入到需要的地方，方便访问它。

### AppConfig

让我们看看 `AppConfig` 的内容（同样省略了package和import）。

<pre lang="ActionScript">
public class AppConfig implements IConfig 
{
	[Inject]
	public var injector:Injector;
	
	[Inject]
	public var mediatorMap:IMediatorMap;
	
	[Inject]
	public var commandMap:IEventCommandMap;
	
	[Inject]
	public var logger:ILogger;
	
	public function configure():void
	{
		models();
		mediators();
		commands();
		logger.info("logger in AppConfig");
	}
	
	private function models():void
	{
		injector.map(ITimerModel).toSingleton(TimerModel);
		injector.map(ViewModel).asSingleton();
	}
	
	private function mediators():void
	{
		mediatorMap.map(TimerSetView).toMediator(TimerSetMediator);
		mediatorMap.map(TimerActionView).toMediator(TimerActionMediator);
		mediatorMap.map(AlertView).toMediator(AlertViewMediator);
	}
	
	private function commands():void
	{
		commandMap.map(TEvent.TIMER_START, TEvent).toCommand(TimerStartCmd);
		commandMap.map(TEvent.TIMER_STOP, TEvent).toCommand(TimerStopCmd);
		commandMap.map(TEvent.CHANGE_STATE, TEvent).toCommand(ChangeStateCmd);
	}
}
</pre>

我们来仔细看看这个类中注入的4个对象。

injector是SwiftSuspenders提供的注入器。Robotlegs使用这个注入器来实现注入。最终用户可以使用它来进行单例注入，例如映射Model。

mediatorMap用来实现视图类和Mediator的映射。如果你用过Robotlegs1，你会发现mediatorMap的映射语法改变了不少。mediatorMap抛弃了原来使用参数来映射的方式，改用链式调用，在我看来，这样的改动让语法更加简洁，且容易记忆。

例如，在Robotlegs1中，实现 `TimerSetView` 与 `TimerSetMediator` 的映射，需要这样调用：

<pre lang="ActionScript">
mediatorMap.mapView(TimerActionView, TimerActionMediator);
</pre>

**注意**

>本系列文章在必要的时候会对Robotlegs1和2进行比较，这是为了方便使用过Robotlegs1的读者进行更深入的理解。如果你以前没有使用过Robotlegs1，可以跳过这些内容。

commandMap用来实现事件与Command的映射。在Robotlegs1中，要实现 `TEvent.TIMER_START` 与 `TimerStartCmd` 的映射，需要这样调用：

<pre lang="ActionScript">
commandMap.mapEvent(TEvent.TIMER_START, TimerStartCmd);
</pre>

logger提供一个全局的日志分析器，默认使用tarce实现。logger不但可以像上面的代码一样，直接输出文字，也可以方便的实现文本替换。例如：

<pre lang="Actionscript">
logger.info("logger in {0}, {1}", [this, "done"]);
//输出内容
//638 INFO Context-0-9f [class AppConfig] logger in [object AppConfig], done
</pre>

如果你用过Robotlegs1，那么你会发现它和原来的Context很相似。


[i1]: image/use_robotlegs2/timer_mvcbundle1.png
[i2]: image/use_robotlegs2/timer_mvcbundle2.png
[i3]: image/use_robotlegs2/timer_mvcbundle3.png
[i4]: image/use_robotlegs2/timer_mvcbundle4_view.png
[i5]: image/use_robotlegs2/timer_mvcbundle5_mediator.png
[i6]: image/use_robotlegs2/timer_mvcbundle6_model.png
[i7]: image/use_robotlegs2/timer_mvcbundle7_cmd.png

[u1]: http://www.minimalcomps.com/
[u2]: https://github.com/minimalcomps/minimalcomps
[u3]: http://zengrong.net/post/1142.htm
[u4]: http://www.robotlegs.org/
[u5]: https://github.com/robotlegs/robotlegs-framework/tree/v2.0.0b6
