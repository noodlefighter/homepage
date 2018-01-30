title: Funckb工作日志
description: 
date: 2017-12-01
layout: post
comments: ture
categories:
- 工作日志
tags: 
- 键盘
- 嵌入式软件
---

受到[nan-15](https://github.com/trebb/nan-15)启发, 打算做一个相同布局的键盘, 用途为辅助操作的宏键盘.

<!-- more -->

2017-12-01
============

用户最多可以配置32个自定义操作, 对接数个内置功能:
1. Action: 用户脚本
2. Layer操作: 对keymap中各layer的状态进行操作
3. Multi-Key: 实现修饰键+单个按键的组合, 普通/单次按下弹起
4. Serial-Key: 以用户指定的速度敲击一系列按键
5. If-Key: 若"按键A按下(或未按下) 且(And) 按键B按下(或未按下)", 该按键键值为KC1, 否则为KC2. A,B可仅指定其一
