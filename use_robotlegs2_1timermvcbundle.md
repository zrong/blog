Robotlegs2中文教程-1使用MVCBundle

## 目的

本章使用Robotlegs2自带的MVCBundle实现一个简单的MVC实例。

Robotlegs2在架构设计上，框架仅实现了生命周期管理、Logger、消息调度、插件管理器、配置管理器等核心功能，其他功能全部使用插件实现。而MVCBundle，就是Robotlegs2提供的一个插件和配置集合，这个集合包含所有MVC需要的插件和功能。

本章不会研究Robotlegs2在结构上的设计，而是从最终用户的角度来使用MVCBundle。若希望了解Robotlegs2的架构，请关注本系列后续文章。

## Timer-MVCBundle-Sample概述

Timer-MVCBundle-Sample是本章的实例名称。这个实例实现了一个简单的定时器。看看定时器的三个状态：

1. 初始状态，设置时、分，类名为TimerSetView。按Start按钮开始倒计时。

2. 倒计时状态，类名为TimerActionView。按Cancel按钮取消倒计时，回到初始状态。

3. 倒计时时间到，类名为AlertView。按Dismiss按钮回到初始状态。

## 项目结构

### View + Mediator

刚才看到的后缀为View的类，我叫它们“视图类”，所有的视图类，都位于 `view` 包中，并实现 `ITimerView` 接口。 `ITimerView` 中并没有包含任何方法签名。实现这个接口，是为了方便进行类型匹配。

视图类用于我们能看到的定时器的三个状态，每个状态对应一个视图。定时器运行的过程中所显示的状态，在这三个视图之间切换。

视图类都是显示对象的子类，三个视图也就是三个显示对象。在一个视图显示的时候，它会被加到舞台上，其他的视图则移出舞台。

在这个项目中，我使用了[MinialComps](http://www.minimalcomps.com/)组件。视图类继承其中的VBox或者HBox。如下图：

每个视图类都有一个带有Mediator后缀的类，这是视图类的中介类。中介类负责管理视图事件，接收和传递系统事件等等。所有的中介类都继承 Robotlegs2 提供的 `Mediator` 类。如下图：

### Model

这个项目中，有2个Model。
