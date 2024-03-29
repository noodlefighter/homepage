date: 2017-11-12
tags:

- 编程
---

"透过现象看本质."


<!--more-->

---

需求描述
========
使用C# + .Net framework 监视一个文件夹里的doc文件 文件被修改时记录文件名

解决方案
========
使用System.IO.FileSystemWatcher类, 类描述
```
侦听文件系统更改通知，并在目录或目录中的文件发生更改时引发事件。
```

着手尝试
========
测试程序
```
FileSystemWatcher watcher = new FileSystemWatcher(path, "*.doc");
watcher.NotifyFilter = NotifyFilters.FileName | NotifyFilters.LastWrite | NotifyFilters.Size;
watcher.Changed += new FileSystemEventHandler(watcher_Changed);
```

尝试测试效果, 方法是用office word打开doc文件, 修改后保存, 看Changed事件有没有被触发, 结果是没有, 于是开始找原因.

解决问题
========
先msdn重新看了遍 用法应该无误 而且测试了Create事件能被正常触发
然后开始到处搜/瞎几把尝试, 无果, 直到翻到Github上.NET Core项目的一个issue: [FileSystemWatcher does not raise events for files that are opened/changed in Visual Studio](https://github.com/dotnet/corefx/issues/9462)
提问者也用了这个类的Changed事件, 在VS中修改一个.json文本并保存, 但是事件并没有触发, 二楼回复:
![1.png](_assets/解决.Net框架中FileSystemWatcher类无法产生Changed事件问题有感/1.png)

看到这里 一下子清醒过来.. 直觉上总觉得Editor在用户编辑期间是把数据暂存在内存中 需要保存的时候整个写回外存储..
可现实是..大文件怎么可能直接丢内存里.. 它们的做法是``建一个临时文件来存放用户编辑中的数据 用户保存时直接删掉原来的文件 然后把临时文件重命名``..

比如这里 打开了一个文件, 修改后保存, 得到的记录如下:
![2.png](_assets/解决.Net框架中FileSystemWatcher类无法产生Changed事件问题有感/2.jpg)

最后, 解决方案是监听Renamed事件, 问题得到解决.
