date: 2021-07-10
tags: 

- 输入法

---

[声笔系列码](http://sbxlm.github.io/)是一系列顶功输入法，基于 RIME 输入法框架开发，为了实现顶功和aeiou键选重的特性，对 [librime](https://github.com/rime/librime) 进行了大量魔改，要想在 Linux 上用起，需要自己重新编译安装[魔改后的 librime](https://github.com/sbxlmdsl/librime)。

这篇文章会简单走一遍安装配置流程，如果你想在 Linux 下使用声笔系列码，应该会对你有帮助。

![img](_assets/Linux下使用声笔系列码/show.gif)

<!--more-->

---



请先阅读：

**文章假设你有一定的 Linux 使用基础、知道自己在做什么、能够对自己敲的命令负责，如果不能评估风险，请不要盲目操作。**



## 安装 fcitx5-rime

推荐的输入法框架是 fcitx5，先前在 ibus 框架下尝试过，会有各种奇怪的小毛病（比如设置为“所有程序共享输入法”时，切换窗口会出现“Invalid UTF-8”这样的提示；HOME、END 键工作不正常 ... 等等），而 fcitx5 下目前体验完美。

fcitx5-rime 是 fcitx5 的插件，用以支持RIME框架；大多数发行版都自带 fcitx5 的包，资料应该很多这里不再重复。

***如果你使用 Arch系 Linux (如 Manjaro, Archlinux)***:

```
$ sudo pacman -S fcitx5-rime
```

***如果你使用其他 Linux 发行版***:(未经实机测试实际效果，仅供参考)

目前（2021-07-10），`fcitx5-rime`在 [ubuntu 21.04 中已经可用](https://packages.ubuntu.com/hirsute/fcitx5-rime)，可以考虑升级系统后，直接使用 apt 安装。

## 通过源码编译安装 librime

为了实现顶功和aeiou键选重的特性，声笔系列码对 [librime](https://github.com/rime/librime) 进行了大量魔改，要想在 Linux 上用起，由于目前没有二进制版本，需要自己重新编译安装[魔改后的 librime](https://github.com/sbxlmdsl/librime)。

***如果你使用 Arch系 Linux (如 Manjaro, Archlinux)***:

我已经尝试在 Manjaro 下成功编译，并将构建脚本上传至 AUR 的 [librime-sbxlm-git](https://aur.archlinux.org/packages/librime-sbxlm-git/)，所以只需要用命令简单安装，覆盖原先的 librime 包：

```
$ sudo pacman -S yay
$ yay -S librime-sbxlm-git
```

***如果你使用其他 Linux 发行版***:(未经实机测试实际效果，仅供参考)

那就需要自己从源码编译 librime，编译过程可以参考 [AUR包 librime-sbxlm-git](https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=librime-sbxlm-git)的PKGBUILD脚本。这里以 ubuntu 为例，记录一次成功编译、安装过程：

```
$ sudo apt update
$ sudo apt install -y libboost-all-dev capnproto libgoogle-glog-dev libleveldb-dev librime-data liblua5.1-0-dev libmarisa-dev libopencc-dev libyaml-cpp-dev cmake git libgtest-dev ninja-build wget gcc g++

$ mkdir mybuild && cd mybuild
$ git clone https://github.com/sbxlmdsl/librime
$ wget https://aur.archlinux.org/cgit/aur.git/plain/0001-fix-opencc-1.1.0-failed.patch?h=librime-sbxlm-git -O 0001-fix-opencc-1.1.0-failed.patch
$ _octagramcommit=f92e083052b9983ee3cbddcda5ed60bb3c068e24
$ _luacommit=d45a41af2f9d731e3c1516a191cc3160e3cb8377
$ wget https://github.com/lotem/librime-octagram/archive/$_octagramcommit/librime-octagram-$_octagramcommit.tar.gz
$ wget https://github.com/hchunhui/librime-lua/archive/$_luacommit/librime-lua-$_luacommit.tar.gz
$ tar -xf librime-lua-$_luacommit.tar.gz && tar -xf librime-octagram-$_octagramcommit.tar.gz

$ srcdir=$PWD
$ cd librime
$ patch -p1 < ../0001-fix-opencc-1.1.0-failed.patch
$ cd plugins/
$ ln -sf "$srcdir"/librime-octagram-$_octagramcommit librime-octagram
$ ln -sf "$srcdir"/librime-lua-$_luacommit librime-lua

$ cd $srcdir/librime
$ export CXXFLAGS="$CXXFLAGS -DNDEBUG"
$ cmake . -GNinja -Bbuild -DCMAKE_INSTALL_PREFIX=/usr -DBUILD_MERGED_PLUGINS=Off -DENABLE_EXTERNAL_PLUGINS=On
$ cmake --build build
$ sudo make install
```

## 

## 配置

重新启动 fcitx5 使新编译的 librime 生效，将声笔输入法的配置文件复制到`fcitx5-rime`的RIME配置文件路径下（`$HOME/.local/share/fcitx5/rime/`）。

> 关于配置文件获取、扩展包的细节请参考[官方安装说明](https://sbxlm.gitee.io/vzpz/)

复制好配置文件后，重新部署 RIME 即可，两种方式均可：

- RIME输入法 applet icon 上点击鼠标左键 - 部署
- `rime_deployer --build $HOME/.local/share/fcitx5/rime/`

至此，声笔输入法应该可以正常使用了。