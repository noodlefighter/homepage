title: UML状态图（层次状态图）入门
description: 
date: 2018-10-21
updated: 2018-10-21
layout: post
comments: ture
categories:
- 嵌入式软件
tags: 
- UML
- 状态机
---

两年前写的一篇教程，原本是某本书的一部分，被嫌弃不易懂没被采用，整理一下贴出来。

其实自己还参考QP-Nano做了个层次状态机框架，比QP的寻径算法的时间效率更高点，本来想屯着等有空发篇期刊的，一直也只是处于构想阶段，想想还是整理下发出来吧。

(working...)

<!--more-->
---

## 什么是状态机？
状态机是对某种事物在它的生存周期内各个阶段的描述：有什么事情会对它产生影响；在它的某个阶段，那些会对它产生影响的事情发生时，它会如何应对；什么因素会改变它当前所处的阶段等等。

## 什么是UML？

UML（Unified Model Language）又称为标准建模语言，用于软件系统建模，使用它能以图表的形式描述系统的功能、结构、内部行为。而UML状态图（UML Statechart Diagram）是UML图中的一种，用于描述系统内的对象的内部状态，能提供对象的行为、对象行为如何根据状态而变化、状态之间如何转换等信息。
UML状态图是状态机的表示方法，我们把能用UML状态图描述的状态机叫做UML状态机。

## 我们为什么要使用UML状态机进行程序开发？

嵌入式系统通常都有接收外界输入并进行响应的需求：用户按下了一个按钮，系统执行相应功能；数模转换器触发了中断，系统在中断服务程序中取回数据；收到了一个网络数据包，系统需要对它解包并根据其内容并采取相应操作，可能是一条用户登入信息，需要记录登入状态，也可能是一个用于保持通讯的数据包，需要回传一条信息告诉对方自身还处于在线状态。

系统并不只根据输入的不同而作出不同的响应，很多时候，响应还取决于系统自身当前的状态，比如用户需要先登入才能对设备进行各种操作，那么“用户是否已登入”便是一个系统的一个状态。一个状态可能意味着程序代码中的一个标志变量，系统当前的状态是这些标志变量的各种值的组合。

通常程序在开发的初期，只有一个模糊的目标，一开始需要实现的功能不会太多，而在迭代开发过程中，随着需求逐渐清晰，功能被慢慢丰富，此时的程序会比初期复杂得多。随着程序特性的增加，表示系统状态的标志变量的数量只增不减，而为系统增加一种特定状态下的特性，便意味着一句对那些标志变量进行判断的if语句，有时候还需要多个分支来应对各种可能的情况，这些语句复杂而难理解，追踪程序运行情况的难度随着标志变量的增加而增加。更糟糕的是，这些标志变量可能在程序的各个角落中被修改，编程人员必须小心地保证这些修改操作的一致性。当程序复杂到难以增加新的功能或者修复程序错误需要的时间太多时，便需要大费周章地重构程序了。

将状态机思想用于程序设计，可以大量减少程序中的分支语句，使运行中的程序以一定规则在预先设计好的状态间转换，降低程序调试难度。


## 状态机基础

### 状态、事件、监护条件、动作、转换

让我们从一张描述防盗门状态的状态图开始，如图 1.1，当“转动钥匙”且满足“钥匙匹配”的条件时，门的状态从“门关”转换到“门开”，同时执行“开门”动作。

图中的“门关”、“门开”，是两种状态（State），状态以圆角矩形框表示，将状态名写在框内；当状态框中需要包含除名称外的更多信息（如内部转换动作列表、嵌套的状态，下文会详细说明）时，可在状态框顶部绘制一条水平线，把状态名标在水平线的上方。图 1.1展示了状态的两种表示方法。
图中的箭头表示从“门关”到“门开”的状态变化，状态变化的过程叫做转换（Transition），以一个从源状态指向目标状态的箭头表示。
转换符号旁标注着“转动钥匙[钥匙匹配] / 开门”，这是对转换行为的说明，斜杠前说明该转换由于何种原因触发，斜杠后说明转换发生时执行什么操作。这个转换的具体含义为：“‘转动钥匙’时，如果‘钥匙匹配’，则执行‘开门’操作，状态从‘门关’转换到‘门开’”。这句标注需以一定的格式书写：

```
触发事件[监护条件] / 转换动作
```

其中，事件（Event）指的是能引起系统状态变化的事情，触发事件是引起这个转换的事件。
监护条件（Guard Condition）描述了转换的前提条件，。
动作（Action）指的是某种操作，转换动作是发生转换时执行的动作，在UML状态图中，它可以是一些描述性文字也可以是一小段程序代码。
触发事件、监护条件、转换动作可以同时或单独存在，若一个转换没有触发条件和监护条件，则该转换为无条件转换。

### 初态、终态、初始转换

初始状态（Initial State）简称初态，以实心圆点表示，表示状态机生命周期的开始；最终状态（Final State）简称终态，用牛眼符号（外包圆框的实心圆点）表示，它表示状态机生命周期的结束如图 1.4。

始于初态的无条件转换称为初始转换，这个转换决定了状态机初始化后所处的状态，初始转换执行意味着状态机开始工作。如图 1.5。

### 进入动作、退出动作、内部转换和自转换

以图 1.4展示的服务器状态图进行说明。

每个状态都可以有自己的进入动作、退出动作，分别在进入状态、退出状态时被执行。UML状态图中，进入动作、退出动作列表分别跟在保留字“entry”、“exit”后，写在状态框中。
图 1.5中，服务器状态机初始转换，进入“服务器”状态的同时，进入动作“服务器启动”被执行；“关闭命令”事件触发，状态退出，退出动作“服务器停止”被执行。
转换有内部转换（Internal Transition）和自转换(Self-transition)两种特殊情形。
内部转换，顾名思义，指的是“在内部的转换”，内部转换不会改变当前状态，只执行相应的操作。在状态图中以文字的形式表示在状态中。
图 1.6中展示了3种内部转换，“entry”、“exit”分别表示进入、退出状态时产生的事件，事件发生时分别会执行对应的进入、退出动作；“event / action”表示由于事件“event”引起的内部转换，即执行“action”动作而不改变状态机当前状态。
自转换指的是因事件触发而向当前状态转换，源状态和目标状态均为同一状态。如图 1.7所示，处于状态state时，传入event事件会触发状态state的自转换。
内部转换和自转换是两个容易混淆的概念，自转换退出当前状态后再次进入，状态的退出动作和进入动作会被依次执行。以图 1.8所示服务器状态图为例，“重启命令”事件触发了自转换，“服务器停止”、“服务器启动”动作被执行，“服务器”重新进入而使状态初始化；而“请求数据”事件触发的内部转换，只会使“回传数据”动作执行。

## 有限状态机（Finite State Machine）

假设存在这样的电梯自动门，当控制系统向它发送“开门”指令时自动门打开，向它发送“关门”指令时自动门关闭。图 1.9是用于表示上述电梯门的状态机图。
读图可知，状态机有“门关”（door_closed）、“门开”（door_open）两种状态，“开门命令”（command_open）和“关门命令”（command_close）事件对状态机产生影响。当电梯门处于“门关”状态时，“开门命令”可以使当前状态转换至“门开”状态；反之，当电梯门处于“门开”状态时， “关门命令”可以使当前状态转换至“门关”状态。（状态转换表）
这个状态图描述的是一个简单的有限状态机，有限状态机的思想广泛应用于硬件电路设计领域，同时它也是程序设计中常用的一种编程思想。有限状态机的定义是：对象在生存周期中，拥有不同运行情况的各个互不重叠的状态，对象在同一时刻只能处于一种状态下；对象能接收来自外界的输入，不同的状态下的对象，对输入可以有不同的响应并转换对象当前的状态，这样的对象叫做有限状态机。

## 扩展有限状态机（Enhanced Finite State Machine）

试想一下，有一只气球，每次充入1毫升气体，当气球内气体超过2000毫升时气球破裂，如果用有限状态机描述该气球，需要多少个状态呢，答案是2002个，如图 1.10，状态“unaerated”表示未充气，“cubage_n”表示气球内气体的体积为n毫升，“broken”状态表示气球损坏，“inflate”则为充气事件。
管理这样多的状态显然不符合我们的期望，这时便需要用到扩展有限状态机（EFSM）了。EFSM在FSM的基础上，允许状态机拥有扩展状态变量，转换可以带有布尔表达式作为监护条件，即状态转换的前提是监护条件的计算结果为真。
图 1.11为该气球的EFSM状态图，“inflate”表示“充气”事件，“unaerated”表示“未充气”状态，“bulging”表示“膨胀”状态，“broken”表示“损坏”状态。状态机在一开始处于“未充气”状态，“充气”事件发生时执行动作“cubage = 1;”的同时转换至“膨胀”状态；“膨胀”状态中，“充气”事件发生时执行动作“cubage++;”，满足条件“cubage > 2000”时转换至“损坏”状态；“损坏”状态进入动作 “cubage = 0;”，不处理事件。
可以发现，即使再增加气球的体积上限，也不会导致状态的增加。可以这样理解——EFSM允许在状态机中加入的变量，适合表示那些改变时不一定引起状态转换的量。

## UML状态机对有限状态机扩展的特性

之前介绍的有限状态机，很适合描述简单的状态转换关系，但面对一些复杂问题就力不从心了。在有限状态机中，如果要增加一个所有状态中都响应的事件，那就必须明确地在所有状态中处理这个事件，这是吃力不讨好的。面对比较复杂的问题时，我们可以使用UML状态机对有限状态机扩展的特性。

### 状态的嵌套
如图 1.12，UML状态图中，一个状态可以有一个父状态（Super State）和若干子状态（Sub-state）。存在状态嵌套的状态机，被称为层次状态机（Hierarchical State Machine）。
在层次状态机中，当一个事件传入，它由当前状态处理，如果当前状态不处理这个事件，事件将交给当前状态的父状态处理，若当前状态的父状态不处理该事件，则交由父状态的父状态处理，以此类推直到事件被处理；如果直到顶层状态（也就是没有父状态的状态）事件也未被处理，则忽略这个事件。
层次状态机的事件分发方式，意味着子状态“继承”了父状态对事件的处理方式，需要改变父状态对某事件的处理方式，只需在子状态中处理该事件。
要进入一个状态就必须先进入它的父状态，要退出一个状态就必须先退出它的子状态，进入、退出动作很像面向对象程序设计中的构造和析构——总是先执行父类的构造函数、子类的析构函数，所以它们很适合用于初始化、销毁操作。对于一个状态而言，进入它时的源状态、退出它时的目标状态也可以是多种多样的，所以在每个转换中都要小心地管理那些状态中需要使用的对象的初始化和销毁操作是个艰巨的任务(不通顺)。如同母亲叮嘱你“外出记得锁门”，出门上课、购物都会顺手把门锁上，而当你的朋友邀你到公园踢球的时候却很容易忘记锁门（即忘了把锁门操作的代码填上），如图 1.13；若使用了退出动作，出门时（退出“家中”状态时）锁门操作会随着自动执行，如图 1.14。
状态嵌套带来的这些特性，使得层次状态机能够避免过多的状态和状态转换，减少了重复的处理。

### 2．	层次状态机中的状态转换

事件进入状态机引起转换，状态转换的大致过程如图 1.15所示：
（1）如果事件在当前状态的父状态中被处理，则先从当前状态退出至处理事件的状态，依次执行退出动作（对应图中的退出动作a1）；
（2）转换到目标状态，按退出和进入路径依次执行退出、与转换相关联的动作、进入动作（对应图中的退出动作a2、转换相关联的动作a3、进入动作a4、a5）；
（3）执行目标状态的初始化，依次进入子状态，执行子状态的进入动作（对应图中的进入动作a6）、初始化，直到状态初始化时不再转换到子状态。

由于层次状态机中的状态转换过程比较复杂，所以在这里单独以实例说明，图 1.16是一个状态转换图，图中的状态均有进入和退出动作。

	状态机初始转换至S0，执行S0-entry动作，S0初始转换至S00，执行S00-entry动作，S00初始转换至S000，执行动作S000-entry，S000初始化；
	当前状态S000，此时事件D传入，S000无法处理，事件在S00中被处理，执行动作action_d（注意这是一次内部转换，只执行了动作action_d）；
	当前状态S000，此时事件A传入，S000、S00无法处理，事件在S0中处理，自转换，依次执行动作S000-exit、S00-exit、S0-exit、S0-entry，S0初始转换至S00，执行动作S00-entry，S00初始转换至S000，执行动作S000-entry，S000初始化；
	当前状态S000，此时事件C传入，转换至S001，依次执行动作S000-exit、S001-entry，S001初始化；
	当前状态S001，此时事件A传入，转换至S1，依次执行动作S001-exit、S00-exit、S0-exit、S1-entry，S1初始化；
	当前状态S1，此时事件B传入，转换至S000，依次执行动作S1-exit、S0-entry、S00-entry、S000-entry，S000初始化；
	当前状态S000，此时事件B传入，S000无法处理，事件在S00中被处理，依次执行动作S000-exit、S00-exit、S0-exit、S1-entry。

###	历史伪状态
历史状态是一种伪状态，用于表示某状态退出前最后的活动状态。伪状态在UML状态图中用于表示转换节点，初始状态、最终状态也属于伪状态。
历史状态分为两种：深历史伪状态、浅历史伪状态。深历史伪状态记录状态退出前完整的状态情况，以圆形内标注H*表示；浅历史伪状态只记录状态退出前的直接子状态，以圆形内标注H表示。
这里以洗衣机的洗衣流程状态图为例，介绍历史伪状态，图 1.17为洗衣流程状态图，洗衣流程中，设计了断电恢复功能：当“断电”事件发生，系统停止洗衣流程并切换到“断电中”状态，等待“恢复供电”事件；当“恢复供电”事件发生，状态转换至“洗衣流程”的深历史伪状态。

假设“断电”事件发生时系统处于“漂洗”状态。洗衣流程例子使用了深历史伪状态，“恢复供电”时，转入深历史伪状态可以让洗衣流程回到“漂洗状态”，因为深历史伪状态记录了退出前完整的状态情况；假如将例子中的历史伪状态为浅历史伪状态，则“恢复供电”时只能帮我们回到“洗衣”状态，因为状态退出前只记录了最后的直接子状态信息。

### UML状态机设计例子

我们试着在图 1.9电梯门状态图例子的基础上扩展出电梯状态图，增加一个在任意状态下均可由报警命令触发的报警功能，并为电梯门的开启关闭增加约束条件：在电梯处于运动状态时不允许开关门操作，以及电梯门关闭后电梯才允许升降。
实现电梯运动状态下不允许开关门的限制，我们的第一反应可能是为状态机增加表示电梯运动状态的布尔类型变量，并为开关门转换增加监护条件。没错，这样的实现也能满足要求，但是监护条件对应的代码就是分支语句if-else，过多的分支语句会让程序难以维护，而减少分支语句是使用状态机编程的初衷之一。我们不妨增加两个状态——“电梯静止”“电梯移动”，并把“门开”、“门关”两个状态作为“电梯静止”的子状态，这样一来，状态机只有进入“电梯静止”状态后才能响应开关门操作了，我们无需为此新增判断语句，约束被自然地包含在了的状态间的层次关系之中。以此为基础，可以很自然地实现“电梯门关闭时才允许升降”的约束条件：增加从“门关”到“电梯移动”、从“电梯移动”到“电梯静止”的转换。加入启停约束后，状态图如图 1.18。
如果没有状态嵌套这强力的工具，那么要实现“随时可用的报警按钮”，我们就必须在每个状态中对“报警按钮被按下”这个事件进行处理，但是在层次状态机中，要做的仅仅是在顶层的状态中处理这个事件：为当前所有状态增加一个“elevator”顶层状态，在此状态中处理“command_alarm”事件。如图 1.19。例如当前状态为“door_open”，事件“command_alarm”传入，事件的处理过程为：door_open状态无法处理、elevator_stop状态无法处理、事件被elevator状态处理并执行action_alarm()。

