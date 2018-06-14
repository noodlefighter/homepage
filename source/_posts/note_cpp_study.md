title: C++深入学习笔记
description: 
date: 2018-6-14
updated: 2018-6-14
layout: post
comments: ture
categories:
- 笔记
tags: 
- 笔记
- cpp
- 设计模式
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

### 简单工厂

一个函数（类），根据用户需求构建产品，返回对象。

```c++
Product* Factory::createProduct(string proname)
{
    if ( "A" == proname )
    {
        return new ConcreteProductA();
    }
    else if("B" == proname)
    {
        return new ConcreteProductB();
    }
    return  NULL;
}
```

### 工厂方法

factory类为抽象类，每新建一个产品，都需要添加对应的factory子类构建对应产品。

“图说设计模式”中提到一个日志记录器的例子：使用者并不用关心自己调用的是个数据库log或是文件log，通过这个创建模式就能让Factory的子类返回正确的log对象。

### 抽象工厂

以上两种工厂都只适用于同类产品的构建：比如“食品工厂”可以返回牛排、柠檬水，但我现在需要个“外卖打包工厂”，能为牛排配上刀叉、为柠檬水配上吸管，这时候就需要抽象工厂。

```
class 外卖打包工厂
{
    virtual 食品 获取食品();
    virtual 餐具 获取餐具();
}

class 牛排打包工厂 : 外卖打包工厂
{

}

class 柠檬水打包工厂 : 外卖打包工厂
{

}
```

有了“外卖打包工厂”，调用者无需关心什么配什么，只管调用抽象接口。

### 建造者

角色：

```none
Builder：抽象建造者
ConcreteBuilder：具体建造者
Director：指挥者
Product：多个产品角色
```

具体建造者实现了一系列构建产品的步骤：

{% plantuml %}
@startuml
hide footbox

actor Foo
collections Director

create ConcreteBuilder
Foo -> ConcreteBuilder : 1.0 <<create>>

Foo -> Director : 1.1 setBuilder(Builder*)
activate Director
deactivate Director

Foo -> Director : 1.2 construct():Product*
activate Director
Director -> ConcreteBuilder : 1.3 buildPartA()
activate ConcreteBuilder
deactivate ConcreteBuilder
Director -> ConcreteBuilder : 1.4 buildPartB()
activate ConcreteBuilder
deactivate ConcreteBuilder
Director -> ConcreteBuilder : 1.5 buildPartC()
activate ConcreteBuilder
deactivate ConcreteBuilder
Director -> ConcreteBuilder : 1.6 buildPartD()
activate ConcreteBuilder
deactivate ConcreteBuilder
deactivate Director
@enduml
{% endplantuml %}


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
