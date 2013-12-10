Cocos2d-x中的事件调用方式汇总

从 AS3 转到 Cocos2d-x 后，最纠结的一点就是，事件怎么调？

在 AS3 中，只要继承一下 EventDispatcher ，就能发事件了。而 C++ 没有这些。所有的轮子，都要自己造。

好在 Cocos2d-x 内部已经造好了一些轮子供我们使用。这些轮子分别是：

1. 回调函数
2. CCNotification
3. Signals
<!--more-->

## 1. Cocos2d-x 中的回调函数

Cocos2d-x 内部大量使用回调函数来进行消息传递（或者说事件调用）。 例如 CCMenu 的事件触发，CCAction 中的结束回调等等。
 
具体实现在 CCObject.h 中，这里包含了菜单、Action和shedule的回调。

<pre lang="CPP">
typedef void (CCObject::*SEL_SCHEDULE)(float);
typedef void (CCObject::*SEL_CallFunc)();
typedef void (CCObject::*SEL_CallFuncN)(CCNode*);
typedef void (CCObject::*SEL_CallFuncND)(CCNode*, void*);
typedef void (CCObject::*SEL_CallFuncO)(CCObject*);
typedef void (CCObject::*SEL_MenuHandler)(CCObject*);
typedef void (CCObject::*SEL_EventHandler)(CCEvent*);
typedef int (CCObject::*SEL_Compare)(CCObject*);

#define schedule_selector(_SELECTOR) (SEL_SCHEDULE)(&_SELECTOR)
#define callfunc_selector(_SELECTOR) (SEL_CallFunc)(&_SELECTOR)
#define callfuncN_selector(_SELECTOR) (SEL_CallFuncN)(&_SELECTOR)
#define callfuncND_selector(_SELECTOR) (SEL_CallFuncND)(&_SELECTOR)
#define callfuncO_selector(_SELECTOR) (SEL_CallFuncO)(&_SELECTOR)
#define menu_selector(_SELECTOR) (SEL_MenuHandler)(&_SELECTOR)
#define event_selector(_SELECTOR) (SEL_EventHandler)(&_SELECTOR)
#define compare_selector(_SELECTOR) (SEL_Compare)(&_SELECTOR) 
</pre>
 
观察上面的代码可以发现，函数指针定义类型定义和定义与所有这些函数原型相匹配的函数指针，比如：
typedef void (SelectorProtocol::*SEL_SCHEDULE)(ccTime);
 
 同时定义进行这种类型转换的宏：
#define schedule_selector(_SELECTOR) (SEL_SCHEDULE)(&_SELECTOR)
 
然后在具体的类里，就可以使用这种回调进行一些事件通知了：
  void CCNode::schedule(SEL_SCHEDULE selector, ccTime interval);
比如上面这个，CNode就可以在有具体事件是，调用selector进行回调通知了。

2）使用方法
   (以上面的CCNode::schedule为例子)
   a.首先要在类里声明与上面列出的某一个触发函数原型一样的函数(返回值，参数要一样，名称可以不一样)，然后做具体触发的实现处理；
void Box2DView::tick(ccTime dt)
{
 m_test->Step(&settings);
}
 
   b.把该函数当成一个变量一样设置到Node的schedule：
schedule( schedule_selector(Box2DView::tick) );
因为大部分数据类都是从CNode里继承过来的，所以可以直接使用schedule()。而schedule_selector是我们前面提到的进行类型转换的宏

CCNotification

Signals

