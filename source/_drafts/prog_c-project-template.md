title: C语言CMake工程模板
description: 
date: 2018-02-15
layout: post
comments: ture
categories:
- 编程
tags: 
- C
---

目标：
* 一个简单的命令行入口
* 比较通用的模板，稍做改动就能投入新项目
* 手工编译指定模块的单元测试，方便TDD式编程
* 自动化测试
* 比较少的依赖以方便放到构建服务器上

<!-more->

## 从使用方法开始设计

```sh
usage: 
    ./build.sh [<target_dir> [arg] ... | all ]
    
examples:
./build.sh         # 根目录作为入口构建
./build.sh all     # 搜索"target_"前缀文件夹 分别构建
./build.sh clean   # 清理build目录
./build.sh testall # 搜索test目录下所有子目录 分别构建
```


