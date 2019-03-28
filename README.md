# RC_system

[TOC]

## 1.环境配置

### 1.1.🐍Python环境

&emsp;&emsp;本系统开发时使用的Python版本是**Python3.6.3**，由于其中使用的一个人脸识别库dlib目前只支持Python3.6.x，故没有采用最新的Python3.7版本。

&nbsp;&nbsp;本系统开发时使用的Python版本是Python3.6.3，由于其中使用的一个人脸识别库目前只支持Python3.6.x，故没有采用最新的Python3.7版本。

&emsp;&emsp;Python的安装可以在[官网](https://www.python.org/)进行下载Python3.6.x的安装包，然后运行安装程序。也可以使用Anaconda进行安装，Anaconda中会包含很多Python十分常用的库。由于Anaconda官网的下载速度比较缓慢，推荐使用国内[清华镜像源](https://mirrors.tuna.tsinghua.edu.cn/)进行下载安装([Anaconda下载地址windows64位版本](https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/Anaconda3-5.0.1-Windows-x86_64.exe))。

&emsp;&emsp;按照安装引导程序安装完成之后，需要配置Python解释器和包安装工具pip的环境变量，它们的路径分别是：

```shell
Python安装路径/
Python安装路径/Scripts
```

&emsp;&emsp;配置好环境变量之后打开cmd，输入：

```powershell
>>>python
```

&emsp;&emsp;如果可以进入一个交互式的Python Shell，说明安装已经完成了。然后可以试试：

```python
>>>print("Hello world!")
```

&emsp;&emsp;在交互式界面中输入exit()即可退出。接下来检查pip是否已经配置完成，在cmd中输入:

```powershell
>>>pip
```

&emsp;&emsp;如果看到弹出类似如下的信息，说明pip已经可以正常使用了。

```powershell
Usage:
  pip <command> [options]

Commands:
  install                     Install packages.
  download                    Download packages.
  uninstall                   Uninstall packages.
  freeze                      Output installed packages in requirements format.
  list                        List installed packages.
  show                        Show information about installed packages.
  check                       Verify installed packages have compatible dependencies.
  config                      Manage local and global configuration.
  search                      Search PyPI for packages.
  wheel                       Build wheels from your requirements.
  hash                        Compute hashes of package archives.
  completion                  A helper command used for command completion.
  help                        Show help for commands.
```

### 1.2.🍰Pipenv虚拟环境

&emsp;&emsp;上一步中安装的是系统的Python环境，为了使多个项目之间的解释器不互相混淆，这里选用Pipenv作为本项目的包管理工具。使用Pipenv首先需要安装Pipenv包，最简单的安装方式就是通过pip进行安装。打开cmd，输入：

```powershell
>>>pip install -U pipenv
```

&emsp;&emsp;（上面的“-U”可以省略，加上代表若本地已经存在pipenv库，则将其更新到当前最新版本）

&emsp;&emsp;等待进度条走完之后，若没有报错，则说明Pipenv已经安装完成。下一步就是使用Pipenv进行虚拟环境的搭建了。在这之前还需要将项目从[github](https://github.com/)上下载到本地，或者使用git clone命令，关于git工具的安装此处就不赘述了。假设目前项目已经下载到了D盘的project目录下，那么使用如下操作来进行虚拟环境的搭建：

```powershell
>>>d:
>>>cd project/RC_system
>>>pipenv install --skip-lock
```

&emsp;&emsp;输入完成上述命令之后，pipenv将会在当前目录下创建一个虚拟的Python环境。需要注意的是：

&emsp;&emsp;1、使用“--skip-lock”的原因使pipenv提供了一个严格的版本控制(lock)功能，但是lock的过程耗时十分漫长，由于本项目对于库的版本要求并不严格所以建议跳过此过程。

&emsp;&emsp;2、在安装的过程中可能会出现face_recognition库安装失败的情况，具体的解决方案还在测试中。

### 1.3💻MongoDB数据库(相关模块正在编写中)

&emsp;&emsp;可在[官网](https://www.mongodb.com/)下载安装包进行安装，过程十分轻松愉快。推荐一个MongoDB可视化的工具Robo 3T，也可以在它的官网上直接[下载](https://robomongo.org/download)。

&emsp;&emsp;&emsp;&emsp;1、使用“--skip-lock”的原因使pipenv提供了一个严格的版本控制(lock)功能，但是lock的过程耗时十分漫长，由于本项目对于库的版本要求并不严格所以建议跳过此过程。



## 2.代码结构

目前项目的代码结构如下所示:

&emsp;目前项目的代码结构如下所示:

```powershell
RC_system
│  Pipfile
│  Pipfile.lock
│  README.md
│  README.pdf
│  testa.py
│  __init__.py
│
├─core
│  │  face_image_handler.py
│  │  __init__.py
│  │
│  ├─face_comparison
│  │  │  local_comparer.py
│  │  └─ __init__.py
│  │
│  └─face_detection
│     │  local_detector.py
│     └─ __init__.py
│
└─utils
        __init__.py
```

检查是否有文件缺失

### 2.1.core

&emsp;&emsp;core包中封装了人脸检测、人脸比对还有人脸图片处理的类和函数。

### 2.2.utils

&emsp;&emsp;utils包封装各种工具类和函数：

&emsp;&emsp;&emsp;1、文件IO

&emsp;&emsp;&emsp;2、数据库交互

&emsp;&emsp;&emsp;3、装饰器(计时器等)

### 2.3.主要外部依赖库

&emsp;&emsp;1、face_recognition（人脸检测和比对）

&emsp;&emsp;2、pymongo（数据库交互）

&emsp;&emsp;3、opencv-python、dlib（图像处理）

&emsp;&emsp;4、numpy（基础的高性能计算库）



## 3.运行程序

（未完待续）