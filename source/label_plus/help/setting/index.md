title: LabelPlus - Easy comic translation tool
description: 
date: 2015-10-09
layout: page_label_plus

---

# 使用说明

---

## Label进阶设置

修改`labelplus_config.xml`可以修改一些默认设置.

### __如何正确修改默认分组信息__
编辑labelplus_config.xml，GroupDefine中的项目
可更改分组项目的名称和RGB颜色
请确保：存在Name的Group项目连续，且第一个Group项的Name不为空

### __如何正确修改QuickText功能(快速输入)项目__
编辑labelplus_config.xml，QuickText中的项目
Text为文本，Key为快捷键

### __如何修改输入模式下，图片自动跳转功能中标签的位置__
编辑labelplus_config.xml，SetLabelVisualRatio的内容
两个数字分别为x轴、y轴比例，以半角逗号隔开，0<x,y<1
如"0.5,0.4",标签将会出现在中心偏上的位置.

__[返回使用说明](/label_plus/help)__
