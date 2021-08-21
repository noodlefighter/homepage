
date: 2016-08-17
---

## 介绍
[Unity](https://github.com/ThrowTheSwitch/Unity)是一个C下的单元测试框架（Unity Test Framework），MIT开源协议。
初衷就是为嵌入式程序单元测试编写提供便利。

<!--more-->

## 单元测试
单元测试是软件开发过程中的一种减少bug、提高代码质量的手段
简单的说就是 编写程序的人员 逐个对最小单元（函数）编写对应的测试代码，以此验证它的输出是否符合自己的预期
比如当输入信息正确时，返回值是否正确；当输入信息错误时，是否产生了相应的错误信息。

它除了作为一种自测减少bug，还能带来一些好处：

1. _减少集成测试工作量_
项目前期编写的程序通常位于下层 项目后期时上层程序对下层调用路径错综复杂
若在后期修改底层程序（如） 则将牵一发而动全身（修改一处就要重新进行集成测试 是代价很高的）
单元测试即可为这样的修改提供保障 若因一次改动产生了错误 能快速定位出错的代码

2. _是一份最新的文档_
测试用例本身就是一份例程，可以为其他开发者提供参考（而且能确保是正确的）。

3. _提升设计质量_
编写代码时，为了使代码便于测试，会自然而然地对程序解耦。

## Unity的风格

执行测试代码
```
static
void __test_id_get(void)
{
    TEST_ASSERT(0 != sensor_id_get("sensor-name"));  /* 正确的输入 输出不为0时正确 */
    TEST_ASSERT(0 == sensor_id_get("000abc1234"));   /* 错误的输入 输出为0时正确 */
    TEST_ASSERT(0 == sensor_id_get(""));             /* 错误的输入 输出为0时正确 */
}

void tset_run(void)
{
    UnityBegin(__FILE__);
    RUN_TEST(__test_id_get);
    RUN_TEST(__test_channel);
    RUN_TEST(__test_attribute);
    UnityEnd();
}
```

Unity输出的调试信息
```
../user_code/test_code/test_sensor_general.c:179:__test_id_get:PASS
../user_code/test_code/test_sensor_general.c:180:__test_channel:PASS
../user_code/test_code/test_sensor_general.c:181:__test_attribute:PASS
--------------------
3 Tests 0 Failures 0 Ignored
OK
```

## Unity使用方法

Unity Project的src文件夹里只有3个文件
```
unity.h
unity.c
unity_internals.h
```
使用时只需`#include "unity.h"`即可
需要注意的是Unity是单实例程序 没法一次开多个task来跑单元测试

