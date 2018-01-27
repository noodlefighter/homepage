title: 代码风格
description: 
date: 2016-3-25
layout: post
comments: ture
categories:
- 笔记
---

记录一下自己的代码风格

---
# C语言下
## 命名
### 变量命名
1. 全局变量带前缀g_
2. 全局静态变量带前缀_
3. 指针变量带前缀p_ 全局指针变量带前缀gp_ 
4. const常量和变量相同规则

#### 全局变量
如viewer模块的数据改变flag
```
/* != 0 when data changed */
bool_t g_viewer_data_changed_flg;
```
#### 全局静态变量
需带上前缀_
```
/* != 0 when data changed */
static bool_t _data_changed_flg;
```
#### 局部变量
```
bool_t data_changed_flg;
```
#### 指针变量和数组
```
/* filename string */
char *gp_viewer_filename;

/* filename string */
char g_viewer_filename[] = "abc";
```

### 枚举项、宏定义命名
模块内部枚举项、宏定义 加前缀_
```
#define _PACKAGE_VERSION_MAJOR       0x01u  /**< \brief 主版本号 */
#define _PACKAGE_VERSION_MINOR       0x01u  /**< \brief 次版本号 */

typedef enum {
    _COMMAND_NONE         = 0x00,
    
    _COMMAND_READ         = 0x01,
    _COMMAND_WRITE        = 0x02,
    _COMMAND_ERASE        = 0X03,
    _COMMAND_CHECK        = 0x04,
    
    _COMMAND_RESTART      = 0xf0,
    
    _COMMAND_RETURN_ERROR = 0xff
} _command_enum_t;
```
### 函数命名
1. 模块内自用函数 如static inline函数 需加前缀_ 
2. 对象主体+动作 如:抓猫 cat_catch ();

#### public函数
```
void viewer_show (void);
```
#### 模块内部函数
```
static inline
void _show_info (void);
```

### 类型命名
1. 类型定义 带后缀_t
2. 枚举类型定义 带后缀_enum_t
3. 模块内部使用的类型加前缀_
```
/** @brief 学生结构体定义 */
typedef struct {
    char *name;   /**< @brief 学生姓名 */
    int   age;    /**< @brief 学生年龄 */
} student_t;

/** @brief USB版本枚举定义 */
typedef enum {
    USB_VER_1_0,  /**< USB 1.0 */
    USB_VER_1_1,  /**< USB 1.1 */
    USB_VER_2_0,  /**< USB 2.0 */
} _usb_ver_enum_t;
```

## 代码格式
### 通用
1. 代码缩进使用4个空格 任何情况都不使用tab
2. 

### 函数体
1. 修饰的关键字放在前一行
2. 大括号顶格写
3. 函数名后加一个空格
```
static inline
void _show_info (void) 
{
    /* ... */
}

void viewer_show (void)
{
    /* ... */
}
```

### 代码块
1. 使用紧凑的格式
2. 代码块 除了case 均强制加双大括号
3. switch需有default
```
if (a == b) {
    /* ... */
} else {
    /* ... */
}

switch(c) {
case 'a':
    /* ... */
    break;
case 'b':
    /* ... */
    break;    
default:
    break;
}
```

## 注释
1. 开源项目使用英文注释 自用程序用中文注释
2. 使用doxygen风格注释
### 函数注释
注释写在.c文件里 函数的前面 
public函数必须详细注释 而private函数可以不写注释或简单文字描述
```
/**
 * @brief 
 * 
 * @details 
 * 
 * @param[in]  var_name  description
 * @param[out] var_name  description
 *
 * @retval    //返回值有限时使用retval罗列
 * @return    //无法使用retval罗列时 使用return说明返回值内容
 * 
 * @note      //函数的注意事项
 */
 
/**
 * @brief 简单版函数注释
 */
```

### 类型定义注释
参考`类型命名`部分

### 常量、枚举注释
必要时使用特殊注释块逐条注释 可以按组来注释
```
#define MY_VERSION 0x01  /**< @brief 版本号 */

/** @brief 版本号 */
#define MY_VERSION 0x01  

/**
 * \name USB version
 * @{
 */
#define USB_VER_1_0   0
#define USB_VER_1_1   1
#define USB_VER_2_0   2
/** @} */
```

## 文件
1. 文件夹结构：头文件放在inc文件夹中, src文件夹可选
2. 

### 源文件
```
/**
 * @file
 * @brief write stm32 flash
 *
 * @internal
 * @par Modification history 
 * - 1.00   2014-08-08 noodlefighter, first implementation
 * @endinternal
 */

/* end of file */

```

### 头文件
```
/**
 * @file
 * @brief write stm32 flash
 *
 * @internal
 * @par Modification history 
 * - 1.00   2014-08-08 noodlefighter, first implementation
 * @endinternal
 */

#ifndef STM32FLASH_H_
#define STM32FLASH_H_

#ifdef __cplusplus
extern "C" {
#endif

extern uint32_t g_stm32flash_xxxx; 
 
void STMFLASH_erase_page(uint32_t addr,uint8_t page_num);

#ifdef __cplusplus
}
#endif

#endif /* STM32FLASH_H_ */

/* end of file */

```
  