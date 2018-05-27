title: 模板&测试
description: 模板和测试
date: 2015-7-27
layout: post
comments: ture
categories:
- 笔记
tags: 
- 模板
---
记录一些常用的标签
<!--more-->
摘要是这之前

```
title: 
description: 
date: 
layout: post
comments: ture
categories:
- Others
tags: 
- model
- 模板
---
```


# Markdown测试
## 二级标题
### 三级标题
#### 四级标题
这里是正文

---

### emoji 

https://github.com/crimx/hexo-filter-github-emojis

https://www.webpagefx.com/tools/emoji-cheat-sheet/

:cn:sometext:sparkles: :bus: :one: :one: :four: :five: :one: :four:

---

### uml

https://github.com/oohcoder/hexo-tag-plantuml


说明
http://plantuml.com/

在线
http://www.plantuml.com/plantuml/uml/


{% plantuml %}
    Bob->Alice : hello
{% endplantuml %}

{% plantuml %}
participant Bob
actor Alice
 
Bob -> Alice : hello
Alice -> Bob : Is it ok?
{% endplantuml %}

---

### hexo-spoiler

https://github.com/unnamed42/hexo-spoiler

```
{% spoiler sometext %} 
```

{% spoiler sometext %} 

---

### 图片标签

```
![image](/note_model/Amae_Koromo.jpg)
```

![image](/note_model/Amae_Koromo.jpg)

---

### Image标签

```
{% img 试试 /note_model/Amae_Koromo.jpg 400 图片说明 %}
```

{% img 试试 /note_model/Amae_Koromo.jpg 400 图片说明 %}

---

### 另一种代码块
```
{% codeblock lang:c %}
[rectangle setX: 10 y: 10 width: 20 height: 20];
{% endcodeblock %}
```

{% codeblock lang:c %}
void (*pfn_dead_fun)(char n) { }
{% endcodeblock %}

---

### 插入引用
```
{% pullquote heheheh %}
这里是某人的名言哦
{% endpullquote %}
```
{% pullquote hehehe %}
这里是某人的名言哦
{% endpullquote %}

---
### 着重符号
```
*测试*
**测试**
***测试***
_测试_
__测试__
___测试___
```
*测试*
**测试**
***测试***
_测试_
__测试__
___测试___

---
### 表格
```
表头1|表头2
---|---|---
内容|内容内容内容内容内容内容
哈哈|呵呵呵呵
1|2
3|4
```
表头1|表头2
---|---|---
内容|内容内容内容内容内容内容
哈哈|呵呵呵呵
1|2
3|4

---
### iframe
```
{% iframe http://noodlefighter.com/ 400 400 %}
```

{% iframe http://noodlefighter.com/ 400 400 %}

---

### 引用文章资源
自动管理资源功能
比如`_post/note_model.md`,对应的的资源文件夹为`_post/note_model/`
```
{% asset_path test.gif %}
{% asset_img test.gif 图片标题 %}
{% asset_link test.gif 链接标题 %}

{% img test.gif 100 %}
{% img \test.gif 100 %}

![image](test.gif)
![image](\test.gif)

![img](test.gif)
![img](\test.gif)

{% img {% asset_path test.gif %} 100 %}

```
{% asset_path test.gif %}
{% asset_img test.gif 图片标题 %}
{% asset_link test.gif 链接标题 %}

{% img test.gif 100 %}
{% img \test.gif 100 %}

![image](test.gif)
![image](\test.gif)

![img](test.gif)
![img](\test.gif)

{% img {% asset_path test.gif %} 100 %}  


---

### 绝对路径
```
[测试](http://noodlefighter.com)
```

[测试](http://noodlefighter.com)

---
### 相对路径
```
[测试](\hehe)
```

[测试](\hehe)

---
### 外部链接

```
{% link 链到焦了家 http://loli.la/ 提示文本 %}
```
{% link 链到焦了家 http://loli.la/ 提示文本 %}

---

### 内部文章链接

```
{% post_link model 自定的标题 %}
```
{% post_link note_model 自定的标题 %}


