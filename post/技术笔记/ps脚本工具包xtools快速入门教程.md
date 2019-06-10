
date: 2015-09-20
tags: 
- Photoshop
- Photoshop Script
- xtools
- ps脚本图形界面
---


制作[LabelPlus](http://noodlefighter.com/label_plus)的让我接触了ps脚本
后来了解到有xtools这一系列工具和函数库 不禁感叹作者的用心
前人铺好了路 然而国内找不到相关资料
所以摸索起来也花了半天时间
现在边摸索边写个快速入门教程 以供参考

<!--more-->

以下为我使用xtools的界面库 为LabelPlus做的ps导入工具的截图
{% img /i/note_ps_script_xtools/pic.jpg 600 %}
---

## 从ps脚本说起
PS脚本(Photoshop Script)给我们一个使ps自动操作的方法 
能做到动作(Action)无法实现的 流程控制、参数设定
所以脚本要灵活得多 但是制作起来比动作更麻烦

## 要xtools有何用

`xtools is a JavaScript toolkit that facilitates scripting Adobe Photoshop.`
xtools是一个帮助编写Adobe Photoshop JS脚本的工具集
`xtools is intended for script writers.`
xtools为脚本编写者而生

大概列举一下它带给我们什么好处：
* 实用函数集(Stdlib) 给脚本编写提供便利
* 通用界面库(GenericUI) 提供简单的图形化界面框架
* 一些工具脚本(Toolkit Scripts) 比如调试工具jsh 混合工具FlattenJS
* 相当于大量ps脚本学习例程

以下是发布页，自备梯子
http://ps-scripts.sourceforge.net/xtools.html
或者直接墙内度盘(xtools-2_2b1.zip):
http://pan.baidu.com/s/1pJoY1SJ

值得一提的是xtools是以LGPL协议发布的
所以基于它开发的脚本是可以用于私人用途的

---

## 目录结构
|        目录       |     说明      |
|-------------------|---------------|
|/xtools/           |安装程序       |
|/xtools/xapps      |依赖库的程序   |
|/xtools/apps       |已脱离库的程序 |
|/xtools/xlib       |xtools库       |
|/xtools/docs       |文档           |
|/xtools/etc        |...            |

---

## 安装
执行`Install.jsx`
功能是把xtools拷贝到ps安装目录，并更改文件中一些引用路径
为依赖xtools函数的脚本提供运行环境

---

## 如何开始使用xtools
`/xapps`和`/apps`文件夹中有大量例子、工具
可以在发布页以及`/xapps/README`文件的帮助下测试、阅读脚本

`/docs/`文件夹中的文档可以起参考作用

建议通过阅他的各种Demo来熟悉xtools

---

## 实用函数集(Stdlib)
用户手册：`/docs/Stdlib.pdf`

提供一段测试程序：获取本地`C:\`下的文件列表

```
//@includepath "/d/Adobe Photoshop CS5 Extended 12.0.3.0/xtools"
//@include "xlib/stdlib.js"

function main() {
  var fs = Stdlib.getFiles("/c/", "*");
  var text = "";
  var textUI = "";
  
  for(var i=0; i<fs.length; i++) {
    text += "\r" + fs[i];   
    textUI += "\r" + fs[i].toUIString();   
  }
  
  text = "text:" + text;
  textUI = "textUI:" + textUI;
  
  alert(text);
  alert(textUI);  
};

main();
```

`//@includepath` 引用文件路径
`//@include` 引用的文件
这些注释是为了需要发布时，能使用`Flatten.js`把文件合并起来
(详见见本文文末 “发布自己的脚本”)

---

## 通用界面库(GenericUI)
{% img /i/note_ps_script_xtools/sampleui.jpg 400 %}
以上为SampleUI.jsx的运行结果 
界面库可以做出这样的界面
`创建界面-处理-执行`
用户可以继承GenericUI，然后编写这三部分的程序 
从而完成自己所需要的功能

`/docs/GenericUI Tutorial.rtf`是一个快速入门手册 请先阅读 并测试程序

### 参考文档
`/docs/GenericUI.pdf`提供了`GenericUI类`的信息
GenericUI未提供完整的用户文档 使用控件时需要参考`GenericUI.jsx`内代码

---

## 通用界面库.简单例子
看本篇之前建议阅读`/docs/GenericUI Tutorial.rtf`
这里以`/apps/SimpleUI.jsx`为例进行梳理

### SimpleUI函数的功能
```
SimpleUIOptions = function(obj)     //配置一些默认值
SimpleUI = function()       //用户编写的GenericUI子类

/* 三个回调函数 由GenericUI.exec()调用 */
SimpleUI.prototype.createPanel = function(pnl, ini) //用于创建界面元素
SimpleUI.prototype.validatePanel = function(pnl, ini) //用于预处理 返回值作为process(opts, doc)的参数
SimpleUI.prototype.process = function(opts, doc)    //用于执行程序功能 用户程序主要写在里面

SimpleUI.main = function()  //入口函数 创建GenericUI类实例 并执行其exec()成员函数
```

### 程序入口
创建SimpleUI实例，并使用exec()成员函数显示窗口。
```
SimpleUI.main = function() {
  var ui = new SimpleUI();      //SimpleUI为GenericUI的子类
  var opts = {}; // {noUI: true};   //初始化参数
  var doc = (app.documents.length > 0) ? app.activeDocument : undefined;    //传入活动文档

  ui.exec(opts, doc);   //该函数内部将使用回调函数实现用户功能
  ui.updateIniFile({ uiX: ui.winX, uiY: ui.winY }); //将信息存入配置文件
};

SimpleUI.main();
```

### 界面元素常用用法

#### button为例
```
pnl.sourceBrowse = pnl.add('button', [xx,yy,xx+30,yy+20], '...');
alert(pnl.sourceBrowse.text);
```

第一个参数为界面元素的类型 
第二个参数为控件的尺寸/位置：[x坐标,y坐标,宽度,高度]
第三个参数,不同类型的界面元素有不同意义
比如这里的'...'实际上是赋给了text
具体要参考
```
GenericUI._widgetMap = {
  button: 'text',
  checkbox: 'value',
  dropdownlist: 'selection',
  edittext: 'text',
  iconbutton: 'icon',
  image: 'icon',
  listbox: 'selection',
  panel: 'text',
  progressbar: 'value',
  radiobutton: 'value',
  scrollbar: 'value',
  slider:  'value',
  statictext: 'text',
};
```

#### listBox例子
```
  var arr1 = ["a", "b", "c"];
  var arr2 = ["d", "e", "f"];
  pnl.myListBox = pnl.add('listbox', [xx,yy,xx+150,yy+235], arr1 ,{multiselect:true});
  for(var i=0; i<arr2.length; i++){
    pnl.myListBox[arr2.length] = pnl.myListBox.add('item', arr2[i]);
  }
```

---

## 工具脚本(Toolkit Scripts)
发布页、`/xapps/README`和`/docs`中已经对这些工具有足够的说明了
这里只简单介绍我自己常用的

### jsh.jsx
辅助编写js脚本的工具
可以直接在解释器环境中执行脚本
P.S.有个bug 不能在输入框按Enter 要用Ctrl+Enter来代替

### ActionToJavascript.jsx
把动作转换成js脚本
很便利

---

## 发布自己的脚本
使用`Flatten.js`可以将依赖xtools库的程序(比如`/xapps`中的)
通过处理脱离依赖


```
//@include "stdlib.js"
```
其实就是把类似这样的注释替换成对应文件


```
Flatten.js - PS7,CS,CS2,CS3
        This script is great as part of packaging scripts for deployment. This
        will flatten the include file hierarchy of an application script so
        that you end up with one huge file, instead of several smaller ones.
```
以上为`/xapps/README`中内容

要注意 无论自己的源脚本用什么编码 经过处理后均会变成ANSI编码

---

## 感谢

xtools版本2.2b1 是2014年底上传的
可见这个工程还在继续维护
在这里感谢xtools作者xbytor...为我们节省了大量开发时间.
