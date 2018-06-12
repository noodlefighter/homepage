title: C++深入学习笔记
description: 
date: 2018-6-10
updated: 2018-6-10
layout: post
comments: ture
categories:
- 笔记
tags: 
- 笔记
- cpp
- 设计模式
- 标准库
---

大学期间听过CPP的课，之后就没怎么写过，顶多是有需要的时候看看别人的代码，这里简单做点记录。

计划系统性的补补：
* C++标准库、STL
* 设计模式
* Boost之类的常见库

(Working...)

<!--more-->

## 设计模式

参考资料：
* [图说设计模式](http://design-patterns.readthedocs.io/zh_CN/latest/index.html)
* 《UML和模式应用（Applying UML and Patterns）》
* 

## C++标准库

## STL

## Boost

## 杂物堆

### 不允许建立栈上对象

[参考](https://blog.csdn.net/yiyele/article/details/77806071)

```cpp
class A  
{  
protected:  
     A(){}  
     ~A(){}  
public:  
     static A* create(){return new A();}  
     void destory(){delete this;}  
};  
```

### 不允许建立自由存储区上的对象

```
class A  
{  
private:  
     void* operator new(size_t t){}            
     void operator delete(void* ptr){}
public:  
     A(){}  
     ~A(){}  
};  
```
