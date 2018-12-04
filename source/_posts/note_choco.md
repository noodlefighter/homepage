title: windows上的包管理器chocolatey
description: 
date: 2018-10-21
updated: 2018-10-21
layout: post
comments: ture
categories:
- 笔记
tags: 
- windows
---

win给人感觉，装什么都得下个安装程序一路next到底，有了choco这些工作就能自动完成了，舒爽：

```none
C:\>choco install Python3
Chocolatey v0.10.11
Installing the following packages:
Python3
...
Installing 64-bit python3...
python3 has been installed.
...
```

<!--more-->

安装只用copy一串命令到cmd里就能完成：[传送门](https://chocolatey.org/install#installing-chocolatey)

![img](choco_install.png)

安装choco的命令可以嵌到自动化脚本里，再用choco安装其他程序就方便了，这是用choco安装py2的效果:
![img](choco_python2.png)

