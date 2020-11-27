date: 2020-11-27
tags:

- 应用笔记

---


<!--more-->

需要硬件：

- Jetson Nano本体
- 能支持5V/3A的QC快充电源适配器、USB-TYPEA转TYPEC电源线
- 一张至少32GB的TF卡（推荐64GB）、读卡器

必要的基础知识和经验：

- 解决国内糟糕网络问题的代理经验
- 一些unix命令行使用经验

在[官方的视频教程](https://www.youtube.com/watch?v=QXIwdsyK7Rw&list=PL5B692fm6--uQRRDTPsJDp4o0xbzkoyf8&index=9)里有详细说明，

## 环境布置

开箱后，烧TF卡、桌面环境配置参考[手册](https://developer.nvidia.com/embedded/learn/jetson-nano-2gb-devkit-user-guide)，玩过树莓派的朋友估计很熟悉这流程了，开机，接HDMI之后就可以开始拖仓库了：

```
$ git clone --recursive https://github.com/dusty-nv/jetson-inference
```

这里有两种选择，使用Docker或者

### Fork1. 使用Docker作为开发环境

相关文档：https://github.com/dusty-nv/jetson-inference/blob/master/docs/aux-docker.md

使用Docker环境的好处是无需配置太多环境，官方帮你准备好了，但感觉不是太灵活。

进入docker环境：

```
$ cd jetson-inference
$ ./docker/run.sh
```

这里会让你选需要下载的预训练模型，下载一堆东西。


### Fork2. 直接编译到当前环境

```
$ cd jetson-inference
$ mkdir build && cd build
$ cmake ..
```

## 跑个测试DEMO

要用到摄像头，这里在一台Android手机上安装了`RTSP Camera Server`当视频源，测试：

```
$ cd build/aarch64/bin
$ ./video-viewer rtsp://192.168.99.100:5554/camera display://0 --input-codec h264
```

跑目标检测网络：

```
$ ./detectnet rtsp://192.168.99.100:5554/camera display://0 --input-codec h264
```