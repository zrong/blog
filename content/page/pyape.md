+++
title = "PYAPE"
postid = 2788
date = 2022-10-02T15:56:39+08:00
isCJKLanguage = true
toc = true
type = "page"
slug = "pyape"
url = "/pyape/"
description = "a Application Programming Environment of Python."
draft = false
thumbnail = "/uploads/2022/10/pyape.png"
codeMaxLines = 10
codeLineNumbers = true
figurePositionShow = true
category = [ "technology" ]
tag = ["python", "flask", "sqlalchemy"]
+++

PYAPE ``[paɪp]`` = a Application Programming Environment of Python.

<!--more-->

Pyape 是我在开发 Flask 应用程序过程中积累的一个开发框架。准确的说，这不算一个框架，而是一组集合。
我将开发 Web 以及 API 应用程序过程中积累的一些好用的工具和常用功能进行了简单的封装，整合在一起，
方便快速启动一个新项目。

PYAPE 的完整文档： <https://pyape.rtfd.io/>

PYAPE 的 github 主页： <https://github.com/zrong/pyape>

PYAPE 我的博客上的页面： <https://blog.zengrong.net/pyape/>

**Pyape 的特点如下：**

## 集成命令行

通过对 [Fabric][fabric] 的集成，使用统一的命令行工具来实现如下功能：

1. 生成配置文件
2. 将程序部署到远程服务器
3. 控制远程服务器的运行

详细说明请阅读：[命令行][command]。

## 多开发环境支持

可配置多套开发环境，方便同时支持本地开发、局域网开发、互联网测试和正式服部署。

在开发环境配置中提供的配置，将被 合并 进入默认的配置。 合并规则如下：

- 开发环境配置会 覆盖 默认配置中的同名参数。
- 开发环境中的新配置，会 增加 到默认配置中。
- 若希望在开发环境中 删除 某个默认配置，可以将开发环境中的同名变量设置为空值。

详细说明请阅读： [多开发环境支持][multi_env]

## 模版支持与配置合并

pyape 的命令行工具支持多级配置合并，方便在多个配置中共用数据，不必重复输入配置。

pyape 允许自定义配置生成模版。

## 环境变量替换支持

pyape 的配置文件模版机制支持从环境变量中获取实际值，这样可以避免将敏感信息写入配置文件提交到 CVS 造成安全隐患。

详细说明请阅读：[替换变量][pyape_toml_substitution]

## SQLAlchemy 支持

Pyape 集成了 [SQLAlchemy][sqlalchemy] 支持。与 [Flask-SQLAlchemy][flask-sqlalchemy] 不同，Pyape 直接使用标准的 SQLAlchemy 语法。

这更加方便升级到未来的 SQLAlchemy 2.0 版本。

[Use Flask and SQLalchemy, not Flask-SQLAlchemy](https://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4?gi=dd7c37dae9bf)

这篇文章的观点，我也是赞同的。

## Redis 支持

基于 [flask-redis](https://github.com/underyx/flask-redis) 修改，使其支持多个 Redis 数据库。

## Logging 集成

支持 ZeroMQHandler、RedisHandler，提供 `get_logger` 和 `get_logging_handler` 方便从配置中直接生成 Logger 和 Handler 对象。

关于 logging，我在博客上讨论过多次，详见： [TAG: logging](https://blog.zengrong.net/tag/logging/)。

详情参见 [pyape.logging][pyape_logging] 包。

## 与 PYAPE 相关

下面这些文章与开发 PYAPE 相关。有些是灵感，有些是实现。

- [TAG: flask](https://blog.zengrong.net/tag/flask/)
- [TAG: uwsgi](https://blog.zengrong.net/tag/uwsgi/)
- [TAG: sqlalchemy](https://blog.zengrong.net/tag/sqlalchemy/)
- [TAG: server](https://blog.zengrong.net/tag/server/)
- [TAG: python](https://blog.zengrong.net/tag/python/)
- [部署Flask + uWSGI + Nginx][2568]
- [在 Python+uWSGI 应用中使用缓存][2659]
- [uWSGI+rsyslog 实现 rotating logging][2631]
- [Flask+uWSGI 的 Logging 支持][2660]
- [Flask+uWSGI Logging rotate：重要补充][2690]
- [pyzog：uWSGI logging rotate 的终极方案][2691]
- [uWSGI 的 log 参数详解][2692]

{{< label 全文完 >}}

[fabric]: https://www.fabfile.org/
[command]: https://pyape.readthedocs.io/zh_CN/latest/command.html
[multi_env]: https://pyape.readthedocs.io/zh_CN/latest/configuration.html#multi-env
[pyape_toml_substitution]: https://pyape.readthedocs.io/zh_CN/latest/configuration.html#pyape-toml-substitution
[sqlalchemy]:  https://www.sqlalchemy.org/
[flask-sqlalchemy]: https://flask-sqlalchemy.palletsprojects.com/
[pyape_logging]: https://pyape.readthedocs.io/zh_CN/latest/reference.html#pyape-logging

[2568]: {{<relref "2568.md">}}
[2630]: {{<relref "2630.md">}}
[2650]: {{<relref "2650.md">}}
[2659]: {{<relref "2659.md">}}
[2631]: {{<relref "2631.md">}}
[2660]: {{<relref "2660.md">}}
[2690]: {{<relref "2690.md">}}
[2691]: {{<relref "2691.md">}}
[2692]: {{<relref "2692.md">}}
