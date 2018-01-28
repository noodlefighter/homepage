title: 解决单片机硬件定时器(Timer)不够用的问题
description: 
date: 2015-4-28
layout: post
comments: ture
categories:
- 嵌入式软件
tags: 
- 单片机
- 嵌入式软件
- timer
---


## 适用情形

硬件Timer功能很多，单片机应用经常用到它

但是它的数量是固定的，少则2个多则5、６个，时常面临不够用的问题

<!--more-->

## 简单类比

若定时器的作用是，定期执行某些程序(比如键盘扫描)，则可以对定时器进行复用

使用“时标”，可以简单的做到分时复用一个TIMER，典型例子如下。

> 一个人，７点吃早餐，１２点吃中餐，１８点吃晚餐
假设该程序第一次运行时０点，每隔一小时运行一次

__则程序可以这么写__
{% codeblock lang:c %}
TIMER(){
    static uint8 time = 0; //定义一个时钟
    switch(time){
        case 7: //７点
            吃早餐();
            break;
        case 12: //１２点
            吃中餐();
            break;
        case 18:    //１８点
            吃晚餐();
            break;            
        default:
            break;
    }
 
    time++;
    if(time >= 24) time = 0;  //到２４点后,时间归零
}
{% endcodeblock %}

---

## 具体实现

我以相同原理，实现了一个以1ms为最小单位的的低速定时器。

可无限制增加执行的子程序（前提是内存足够，运行时间足够）
{% codeblock lang:c %}
/**
 *  file:       fredivider.c
 *  Describe:   可无限量增加的定时器一样的东西,
           设置成功后，定时调用你的子程序。
           该程序以子程序来区分
           需要让子程序耗时尽可能的短.
           需要配置定时器每隔1ms调用一次FREDIVIDER_clk()
 *  Author:      Noodlefighter
 *
 *  EditDate:    2015-04-05
**/
 
/** Includes ------------------------------------------------------------------**/
#include <stdlib.h>
 
//#include "stm32f10x.h"
#include "fredivider.h"
 
/** Private typedef -----------------------------------------------------------**/
/** Private define ------------------------------------------------------------**/
/** Private macro -------------------------------------------------------------**/
/** Private variables ---------------------------------------------------------**/
typedef FREDIVIDER_InitTypeDef ItemSetup;
typedef struct Item{
     ItemSetup          setup;
     uint16_t           timeLable;
     struct Item*   nextItem;
}Item;
 
typedef Item* ItemsCollection;
 
ItemsCollection itemCollecion = NULL;
 
/** Extern variables ----------------------------------------------------------**/
/** Private function prototypes -----------------------------------------------**/
/** Private functions ---------------------------------------------------------**/
 
void FREDIVIDER_init(FREDIVIDER_InitTypeDef* initStruct){
    if(itemCollecion == NULL){
        //初次使用
 
        itemCollecion = (Item*) malloc( sizeof(Item) );
 
        Item* newItemPtr = itemCollecion;
        newItemPtr = (Item*) malloc( sizeof(Item) );
        newItemPtr->setup = *initStruct;
        newItemPtr->timeLable = 0;
        newItemPtr->nextItem = NULL;
        itemCollecion->nextItem = newItemPtr;
    }
    else{
        //先查重
        Item* ptr = itemCollecion;
        do{
            ptr = ptr->nextItem;
            if(ptr->setup.Clk_Function == initStruct->Clk_Function){
                //找到，直接处理
                ptr->setup = *initStruct;
                ptr->timeLable = 0;
                return;
            }
        }while(ptr->nextItem !=NULL);
 
        //未找到,添加新项目
        ptr->nextItem = (Item*) malloc( sizeof(Item) );
        ptr = ptr->nextItem;
        ptr->setup = *initStruct;
        ptr->timeLable = 0;
        ptr->nextItem = NULL;
    }
 
}
 
//1ms
void FREDIVIDER_clk(void){
    if(itemCollecion == NULL) return;
    if(itemCollecion->nextItem == NULL) return;
 
    Item *ptr = itemCollecion;
    do{
        ptr = ptr->nextItem;
        if(ptr->setup.Enable != 0){ //若此项开启
            (ptr->timeLable)++;
            if(ptr->timeLable == ptr->setup.Prescaler){
                ptr->timeLable = 0;
                (*(ptr->setup.Clk_Function)) ();    //执行对应子程序
            }
        }
    }
    while(ptr->nextItem !=NULL);
}
/**END OF FILE**/
{% endcodeblock %}

{% codeblock lang:c %}
/**
 *  file:          fredivider.h
 *  Describe:
 *  Author:      Noodlefighter
 *
 *  EditDate:  2015-04-05
**/
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef _FREDIVIDER_H_
#define _FREDIVIDER_H_
 
/* Includes ------------------------------------------------------------------*/
/* Exported types ------------------------------------------------------------*/
 
#ifndef uint16_t
    #define uint16_t unsigned short
#endif // uint16_t
 
#ifndef uint8_t
    #define uint8_t unsigned char
#endif // uint8_t
 
 
 
typedef void (*Clk_Function)(void);
 
typedef struct{
    Clk_Function    Clk_Function;       //想要定时执行的函数
    uint16_t        Prescaler;          //分频系数
    uint8_t         Enable;             //是否启用
}FREDIVIDER_InitTypeDef;
 
typedef enum {FREDIVIDER_DISABLE = 0, FREDIVIDER_ENABLE = !FREDIVIDER_DISABLE} FREDIVIDER_InitTypeDef_Enable;
 
/* Exported constants --------------------------------------------------------*/
/* Exported macro ------------------------------------------------------------*/
/* Exported variables ------------------------------------------------------- */
 
/* Exported functions ------------------------------------------------------- */
void FREDIVIDER_clk(void);
void FREDIVIDER_init(FREDIVIDER_InitTypeDef* initStruct);
 
#endif
 
/*****END OF FILE****/
 {% endcodeblock %}

---

## 使用例子

__FreDriver，分频器，顾名思义，这里必然是需要提供一个时钟，每1ms需要调用一次FREDIVIDER_clk()__
    
{% codeblock lang:c %}
#include "fredriver.h"
 
void main()
{
     
    TIM3_init();    //初始化 1ms溢出
         
    FREDIVIDER_InitTypeDef FREDIVIDER_InitStruct;    //初始化结构体
    FREDIVIDER_InitStruct.Clk_Function = myprog_clk;  //需要定时执行的函数的函数指针
    FREDIVIDER_InitStruct.Prescaler = 200;              //每200ms执行一次
    FREDIVIDER_InitStruct.Enable = FREDIVIDER_ENABLE;   //使能
    FREDIVIDER_init(&FREDIVIDER_InitStruct);              //执行初始化
     
    while(1){
        if(TIM_GetFlagStatus(TIM3,TIM_FLAG_Update)){
                TIM_ClearFlag(TIM3,TIM_FLAG_Update);
                FREDIVIDER_clk();   
         }
    }
}
 
void myprog_clk(void)    //一定要符合这个参数表和返回值
{
    /*你自己的程序*/
}
 {% endcodeblock %}
