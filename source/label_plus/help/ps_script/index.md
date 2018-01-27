title: LabelPlus - Easy comic translation tool
description: 
date: 2015-10-09
layout: page_label_plus

---

# 使用说明

---

## Ps文本导入脚本进阶使用

作为`嵌字人员`, 了解LabelPlus的文本导入脚本的功能, 能避免一些重复劳动.

### ps脚本基本使用方法
请参考基础篇__[从实战开始!](/label_plus/help/practice)__

### 导入图片、分组选择说明

![img](/label_plus/help/ps_script/1.jpg)

加载LabelPlus文本后，列表框中将出现项目
脚本可以有选择性的导入__某图片的文本__和__某组文本__.
使用Shift、Ctrl键，可对项目连续选择、单项选择.


### 文本替换

![img](/label_plus/help/ps_script/2.jpg)

导入文字之前将文本做__替换预处理__
替换文本串需要根据需要自行编写
将"A"替换为"B"格式为"A->B"，多项时以"|"隔开

__例1__
```
，->,|。->.
```
全角逗号/句号替换成半角逗号/句号

__例2__
```
！？->|。->
```
删除所有"！？"和"。"

---

### 存取配置文件

![img](/label_plus/help/ps_script/3.jpg)

利用存取配置文件，可以保存多组设置参数
例如对不同分辨率的图源，配置不同默认字体大小参数等
![img](/label_plus/help/ps_script/4.jpg)

---

### 导入文本后，执行以分组命名的动作

该功能常用于给文本设置样式, 是一个LabelPlus的重要功能.
请阅读__[利用分组设置格式](/label_plus/help/group_action)__


__[返回使用说明](/label_plus/help)__
