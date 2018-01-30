title: CentOS上部署Hexo的方法
description: 
date: 2015-7-28
layout: post
comments: ture
categories:
- 笔记
tags: 
- hexo
- centos
- 博客
---

{% pullquote %}
这两天刚一直在折腾Hexo，做个笔记备用吧。
{% endpullquote %}


<!--more-->


## 写在前面

[Hexo](https://hexo.io)很灵活，玩法比较多，
我之所以选择将Hexo直接部署在服务器上是因为移动上的需求。

Hexo有一个功能，就是一直检测存放文章的目录中的变更，自动生成静态页，所以部署在服务器上，使用起来也挺方便（当然了，肯定不如git同步的方式敲个命令来得快）

不太熟悉linux，遇到了各种问题，鼓捣了一整天才弄好。

这里假设系统中已经配置好http、php环境。（网上教程很多，或者直接使用现成的lamp一键安装包也可）

---

## 部署Hexo

Hexo是台湾人写的，所以官网hexo.io的文档也是中文的，照着步骤安装和配置就行。

这里还是列一下命令吧。

### 安装git
```
$ sudo yum install git-core
```

### 安装nvm
nvm = nodejs version manager
npm = nodejs package manager
前者用于切换版本，后者用于模块安装和管理

nvm的其他使用方法参照: https://github.com/cnpm/nvm
```
$ cd
$ git clone https://github.com/cnpm/nvm.git
$ cd nvm
$ ./install.sh
$ source /root/nvm/nvm.sh
```

### 安装node.js
接着上一步的最后一条命令，启动nvm之后，才能使用nvm（系统重启之后，还得再次启动它）
```
$ nvm install 0.10
$ nvm use 0.10
```

### 安装Hexo
`-g`的意思是，将hexo安装在全局目录下。（npm root -g 可以查看全局目录具体位置）
```
$ npm install hexo -g  
```

### 创建Hexo的文件夹
创建出来的文件夹里，将包含存放内容、生成的静态页的文件夹（的默认位置）、主题、插件之类的存放位置。
这里以`/home/hexo`为例
```
$ hexo init /home/hexo
```

### 配置Hexo
官方写的很清楚了。
主要就是设置好源的目录和输出的目录。我将输出目录指向我之前配置好的网站的根目录。

### 尝试Hexo
然后试着添加一篇文章(参考官方文档-写作)后`hexo g`吧。
配置正确的话，网页就应该成功生成了。

## 服务器配置
至此，hexo已经能正常使用，但是我们的目标是：
> 脱离shell环境、文件变更后自动生成、服务器重启后功能依旧有效。

### 启动后自动加载hexo 在后台监视文件变更
linux在系统启动后，会执行rc.local。

> $ nano /etc/rc.local 

我们在里边添加：
```
source /root/nvm/nvm.sh
nvm use 0.10
cd /home/hexo
nohup hexo generate -w > /dev/null 2>&1 &
```
-w参数会一直监视hexo源文件夹中的变更，nohup会将这个命令挂在后台。（你可以`ps -aux |more`找到它的存在）

### 用户登入后自动加载nvm
~/.bash_profile 中添加
```
source /root/nvm/nvm.sh
nvm use 0.10
```

### 选择一种上传文件的方式
#### SCP
懒得配置的话，可以使用，在win下可以用WinSCP方便地传文件
#### SVN
如果平时只用一台机子的话，部署一个SVN是不错的选择，用海龟SVN之类的还是挺方便的。
#### 网页
我选择php下的文件管理器，好处显而易见。
这里推荐一个https://github.com/kalcaddle/KODExplorer
这玩意自带一个和本地程序基本无异的编辑器，还能拖拽上传，用着挺爽。

{% img /i/note_hexo/edit.jpg 400 %} 

## 写在后面
用了Hexo，感觉自己有动力多写点东西了，这就是纯文本书写的魅力吧。
如果把Hexo部署在本地的话会非常简单，唔不过即使是部署在服务器上，其实还是挺简单的，只是咱对linux不熟，折腾了半天。
部署结束，只是折腾的开始吧，这玩意可玩性太高。
爽。
