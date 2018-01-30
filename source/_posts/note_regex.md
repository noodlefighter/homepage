title: 用过的正则表达式记录
date: 2016-09-19
layout: post
comments: ture
categories:
- 笔记
---

笔记

<!--more-->

## 将C99风格双斜杠“//”注释替换成ANSI封闭风格注释
```
搜索： //(.+)
替换： /* \1 */
```
P.S. 在eclipse的搜索替换功能中测试通过
