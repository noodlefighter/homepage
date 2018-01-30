title: Photoshop Script中给图层分组的方法
description: 
date: 2015-9-9
layout: post
comments: ture
categories:
- 笔记
tags: 
- Photoshop
---

有时候需要给创建的图层分组

<!--more-->

> https://forums.adobe.com/message/4282351

先创建图层组
`var theGroup = app.activeDocument.layerSets.add()`

然后再将图层移入
`myLayer.move(theGroup, ElementPlacement.PLACEATBEGINNING)`


