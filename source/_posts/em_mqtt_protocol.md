title: MQTT协议快速入门（手册导读，学习笔记）
description: 
date: 2018-02-21
layout: post
comments: ture
categories:
- 嵌入式软件
tags: 
- 笔记
- MQTT
---

`MQTT是个machine-to-machine (M2M)/"Internet of Things"连接协议，非常轻量的订阅/分发传输方式。` by [MQTT.org](http://mqtt.org/)
侧重对应用开发有帮助的信息，写篇学习笔记。
(Working)

<!--more-->

请注意，由于本文使用[MQTT协议中文版by mcxiaoke](https://github.com/mcxiaoke/mqtt)的中的部分素材，以[姓名標示-非商業性-相同方式分享 4.0 國際 (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/legalcode)许可协议发布。

---

## 协议手册导读

http://docs.oasis-open.org/mqtt/mqtt/v3.1.1/os/mqtt-v3.1.1-os.html

中文翻译：
https://mcxiaoke.gitbooks.io/mqtt-cn/content/

手册内容很少，只有80来页，这里抽出重要的部分帮助快速熟悉。

## 摘要 

MQTT是种客户端服务端订阅/分发式的传输协议。它轻量、开放、简单，并设计得易于实现。这些特性使它适合许多应用场景，例如Machine to Machine(M2M)、物联网(IoT)的小代码空间、窄带宽场合。
协议运行在TCP/IP或者其他提供有序的（ordered）、可靠的（lossless）、双向连接（bi-directional）的网络上。特性：

* 使用订阅/分发的消息模式，提供一对多的信息分发及应用的解耦；
* 透明传输（信息的传输与承载的内容无关）
* 信息传输有三种服务质量等级：
    * “最多一次”，允许丢失（如温度传感器）；
    * “最少一次”，保证送达但可能重复；
    * “恰好一次”，保证送达且不允许重复（如订单系统）；
* 协议的开销小，减少网络流量；
* 发生异常断开时，通知相关方的机制。

## 摘要给我们提供的信息

从摘要能得知MQTT提供的功能，就是实现了消息的订阅/分发，有点像控制反转“好莱坞模式”，别联系我，我来联系你。

比如，读者A想看杂志社B的杂志，读者A只需要去邮局C通过“邮发代号”就能订阅到杂志，而无需与杂志社B直接联系，杂志社B也无需有谁订阅了杂志，只管发刊时通知邮局C就行了，由邮局把杂志送到读者A的家里，而像读者A这样的人可以有很多个：

{% plantuml %}
top to bottom direction
(邮局C)
left to right direction
:读者A: ---> (邮局C) : 1.订阅
:杂志社B: ---> (邮局C): 2.发布
(邮局C) ---> :读者A:: 3.分发
{% endplantuml %}

读者A和杂志社B不知道彼此的存在，仅在邮局C通过一个“邮发代号”建立起了联系，也就是“解耦了”，A、B就像客户端，C就像管理订阅和分发的服务端：

{% plantuml %}
top to bottom direction
(服务器C)
left to right direction
:客户端A1: ---> (服务器C) : 1.订阅
:客户端A2: ---> (服务器C) : 1.订阅
:客户端A3: ---> (服务器C) : 1.订阅

:客户端B: ---> (服务器C): 2.发布消息

(服务器C) ---> :客户端A1:: 3.分发消息
(服务器C) ---> :客户端A2:: 3.分发消息
(服务器C) ---> :客户端A3:: 3.分发消息
{% endplantuml %}

服务端的角色就像是一个中介，收到客户端发来的信息后，分发给订阅了该信息的客户端。

## 从目录读出本分细节

可以从目录中看出整体脉络。

* Chapter 1 - Introduction 介绍
    * 1.1 Organization of MQTT MQTT的组织结构
    * 1.2 Terminology 术语
    * 1.3 Normative references 规范参考
    * 1.4 Non normative references 非规范参考
    * 1.5 Data representations 数据表示
* Chapter 2 - MQTT Control Packet format 控制包的格式
* __Chapter 3 - MQTT Control Packets__ 控制包
    * 3.1 CONNECT – Client requests a connection to a Server 连接到服务端
    * 3.2 CONNACK – Acknowledge connection request 确认连接请求
    * 3.3 PUBLISH – Publish message 发布信息
    * 3.4 PUBACK – Publish acknowledgement 发布信息确认(QoS 1)
    * 3.5 PUBREC – Publish received (QoS 2 publish received, part 1) 发布收到
    * 3.6 PUBREL – Publish release (QoS 2 publish received, part 2) 发布释放
    * 3.7 PUBCOMP – Publish complete (QoS 2 publish received, part 3) 发布完成
    * 3.8 SUBSCRIBE - Subscribe to topics 订阅主题
    * 3.9 SUBACK – Subscribe acknowledgement 订阅确认
    * 3.10 UNSUBSCRIBE – Unsubscribe from topics 取消订阅
    * 3.11 UNSUBACK – Unsubscribe acknowledgement 取消订阅确认
    * 3.12 PINGREQ – PING request PING请求
    * 3.13 PINGRESP – PING response PING回应
    * 3.14 DISCONNECT – Disconnect notification 断开连接
* __Chapter 4 - Operational behavior__ 操作行为
    * 4.1 Storing state 储存状态
    * 4.2 Network Connections 网络连接
    * 4.3 Quality of Service levels and protocol flows 服务质量（QoS）和协议流程
    * 4.4 Message delivery retry 信息分发重试
    * 4.5 Message receipt 信息收到
    * 4.6 Message ordering 信息顺序
    * 4.7 Topic Names and Topic Filters 主题名称和主题过滤器
    * 4.8 Handling errors 错误处理
* Chapter 5 - Security 信息安全
    * 5.1 Introduction 介绍
    * 5.2 MQTT solutions: security and certification MQTT解决方案：安全和认证
    * 5.3 Lightweight cryptography and constrained devices 轻量加密和受限设备
    * 5.4 Implementation notes 实现时需注意的细节
* Chapter 6 - Using WebSocket as a network transport 基于WebSocket传输
* Chapter 7 - Conformance Targets 一致性目标

第三章目录中的二级标题提示了实现细节，它列举了MQTT数据包类型，连接、发布和订阅信息、实现不同QoS（服务质量）等级的通信等操作由这些数据包。

第四章“操作行为”，可以猜到这章会描述协议中各个角色的行为，也就是如何把第三章中不同格式的数据包用起来。

第五六七章就是次要的内容了。

可见，如果想以自顶向下的思路了解协议，就应该从一、四章开始着手。

## 第一章简介

第一章中重要的是“1.2术语”。

### 网络连接 Network Connection
MQTT使用的底层传输协议基础设施。
客户端使用它连接服务端。
它提供有序的、可靠的、双向字节流传输。
例子见4.2节。

应用消息 Application Message MQTT协议通过网络传输应用数据。应用消息通过MQTT传输时，它们有关联的服务质量（QoS）和主题（Topic）。

### 客户端 Client
使用MQTT的程序或设备。客户端总是通过网络连接到服务端。它可以
发布应用消息给其它相关的客户端。
订阅以请求接受相关的应用消息。
取消订阅以移除接受应用消息的请求。
从服务端断开连接。

### 服务端 Server
一个程序或设备，作为发送消息的客户端和请求订阅的客户端之间的中介。服务端
接受来自客户端的网络连接。
接受客户端发布的应用消息。
处理客户端的订阅和取消订阅请求。
转发应用消息给符合条件的已订阅客户端。

### 订阅 Subscription
订阅包含一个主题过滤器（Topic Filter）和一个最大的服务质量（QoS）等级。订阅与单个会话（Session）关联。会话可以包含多于一个的订阅。会话的每个订阅都有一个不同的主题过滤器。

### 主题名 Topic Name
附加在应用消息上的一个标签，服务端已知且与订阅匹配。服务端发送应用消息的一个副本给每一个匹配的客户端订阅。

### 主题过滤器 Topic Filter
订阅中包含的一个表达式，用于表示相关的一个或多个主题。主题过滤器可以使用通配符。

### 会话 Session
客户端和服务端之间的有状态的交互。一些会话只在网络连接的情况下保持，而另一些可以跨越多个客户端、服务端间的网络连接。

### 控制报文 MQTT Control Packet
通过网络连接发送的信息数据包。MQTT规范定义了十四种不同类型的控制报文，其中一个（PUBLISH报文）用于传输应用消息。


## 第四章行为

### 储存状态

```none
It is necessary for the Client and Server to store Session state in order to provide Quality of Service guarantees. 

The Client and Server MUST store Session state for the entire duration of the Session.

A Session MUST last at least as long it has an active Network Connection.
```

“会话状态Session state”指的是什么呢？抱着疑问阅读第三章，todo：

### 网络连接

MQTT协议要求基础传输层能够提供有序的、可靠的、双向传输（从客户端到服务端 和从服务端到客户端）的字节流。

无连接的网络传输协议如UDP是不支持的，因为他们可能会丢失数据包或对数据包重排序。

    非规范评注
    MQTT 3.1使用的传输层协议是 [RFC793] 定义的TCP/IP协议。下面的协议也支持：
    TLS协议 [RFC5246]
    WebSocket协议 [RFC6455]
    TCP端口8883和1883已在IANA注册，分别用于MQTT的TLS和非TLS通信。
    

### 服务质量等级(QoS)和协议流程

