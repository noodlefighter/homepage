
Scons交叉编译

老早就想把nono盘开源了，但代码太丑了就中途放弃了，现在打算把源码整理下，构建方式改为Scons+GCC，所以就有了这篇文章。

参考：
Scons 简单入门
https://www.jianshu.com/p/e4bd3ab9e5d6

http://leng521.top/posts/79065537/
http://leng521.top/posts/66615451/

https://blog.csdn.net/arag2009/article/details/17392653


https://stackoverflow.com/questions/23898584/how-can-i-use-a-cross-compiler-with-scons

https://stackoverflow.com/questions/13161690/how-to-tell-scons-to-use-mingw-instead-of-msvc

## 简单多层用例

关于基本用法的资料很多，加上[Scons手册](https://scons.org/doc/HTML/scons-user/)里已经说得很清楚了。

这里弄个编译多个文件的例子：



``

```
files = ['a.c', 'b.c']
```