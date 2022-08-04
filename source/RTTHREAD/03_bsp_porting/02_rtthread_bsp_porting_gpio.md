# RTTHREAD移植BSP驱动 GPIO篇

## 简介

本文介绍pin设备驱动，drv_gpio.c如何编写的。

本文参考RTTHREAD官方文档[PIN 设备](https://www.rt-thread.org/document/site/programming-manual/device/pin/pin/)

## 移植前准备

先要熟悉官方的GPIO的demo如何运行的。

先准备一个drv_gpio.c 这边提供一个模板，基本第一次稍微修改就可以编译通过，license大家可以改成自己的，这个随意。

```
/*
 * Copyright (c) 2006-2020, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2021-02-11     supperthomas first version
 *
 */

#include "drv_gpio.h"
#include <stdbool.h>

#ifdef RT_USING_PIN

#define DBG_LEVEL   DBG_LOG
#include <rtdbg.h>
#define LOG_TAG                "drv.gpio"
#define PIN_PORT_OFFSET 4


#define PIN_NUM(port, no) ((((((port) & 0xFu) << PIN_PORT_OFFSET) | ((no) & 0xFu)))
#define PIN_PORT(pin) ((uint8_t)(((pin) >> PIN_PORT_OFFSET) & 0xFu))
#define PIN_NO(pin) ((uint8_t)((pin) & 0xFu))

#ifdef SOC_MAX32660
#define PIN_MCU_PORT(pin)  PIN_PORT(pin)
#define PIN_MCU_PIN(pin)   ((uint32_t)(1u << PIN_NO(pin)))
#endif

static void mcu_pin_write(rt_device_t dev, rt_base_t pin, rt_base_t value)
{
      /*TODO:set gpio out put mode */
}

static int mcu_pin_read(rt_device_t dev, rt_base_t pin)
{
    int value;
      /*TODO:set gpio out put mode */
    return value;
}

static void mcu_pin_mode(rt_device_t dev, rt_base_t pin, rt_base_t mode)
{
      /*TODO:set gpio out put mode */
}


static rt_err_t mcu_pin_attach_irq(struct rt_device *device, rt_int32_t pin,
                                   rt_uint32_t irq_mode, void (*hdr)(void *args), void *args)
{
    /*TODO: start irq handle */
    return RT_EOK;
}

static rt_err_t mcu_pin_dettach_irq(struct rt_device *device, rt_int32_t pin)
{
    /*TODO:disable gpio irq handle */
    return RT_EOK;
}

static rt_err_t mcu_pin_irq_enable(struct rt_device *device, rt_base_t pin,
                                   rt_uint32_t enabled)
{
     /*TODO:start irq handle */
    return RT_EOK;
}

const static struct rt_pin_ops _mcu_pin_ops =
{
    mcu_pin_mode,
    mcu_pin_write,
    mcu_pin_read,
    mcu_pin_attach_irq,
    mcu_pin_dettach_irq,
    mcu_pin_irq_enable,
    NULL,
};

int rt_hw_pin_init(void)
{
    /*TODO: INIT THE GPIO CLOCK AND OTHER */
    return rt_device_pin_register("pin", &_mcu_pin_ops, RT_NULL);
}
INIT_BOARD_EXPORT(rt_hw_pin_init);

//irq handle
void GPIO0_IRQHandler(void)
{
   
}

#endif /* RT_USING_PIN */

```

再加一个drv_gpio.h即可

```
/*
 * Copyright (c) 2006-2020, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2021-02-11     supperthomas first version
 *
 */

#ifndef __DRV_GPIO_H__
#define __DRV_GPIO_H__

#include <board.h>
#include <rtdevice.h>

int rt_hw_pin_init(void);

#endif /* __DRV_GPIO_H__ */

```

gpio驱动主要是要提交这两个，还需要添加Kconfig

```
    config BSP_USING_GPIO
        bool "Enable GPIO"
        select RT_USING_PIN
        default y
```

这边主要添加`RT_USING_PIN` 和`BSP_USING_GPIO`宏定义。

## PIN引脚

关于引脚，通常引脚分为PORT和PIN脚两个部分

通过宏定义，我们可以port和pin合成一个uint32 的数字，这样直接控制引脚即可，

32bit中，低4位是pin脚，高位为port口，可以修改OFFSET改pin脚个数，4bit就是0~15引脚，大家也可以根据自己的mcu特性来改。用其他定义也可以，总之一个原则就是尽量用一个数字来代表一个PIN脚。

```
#define PIN_PORT_OFFSET 4

#define PIN_NUM(port, no) ((((((port) & 0xFu) << PIN_PORT_OFFSET) | ((no) & 0xFu)))
#define PIN_PORT(pin) ((uint8_t)(((pin) >> PIN_PORT_OFFSET) & 0xFu))
#define PIN_NO(pin) ((uint8_t)((pin) & 0xFu))


#define PIN_MCU_PORT(pin)  PIN_PORT(pin)
#define PIN_MCU_PIN(pin) ((uint32_t)(1u << PIN_NO(pin)))
```

## 添加led_sample

一般GPIO有两块，一块是输出，仅只有控制LED灯的情况，还有一种就是带有GPIO中断的情况，就是带有BUTTON的情况。

默认一般开发板都会至少有一个按键和一个LED灯，

这边为了方便快速验证，可以先来验证LED灯，即GPIO口输出功能。

led_sample

```
#define GPIO_LED_PIN  13

static void led_sample_thread_entry(void *parameter)
{
    int count = 1;
    rt_pin_mode(GPIO_LED_PIN, PIN_MODE_OUTPUT);
    while (count++)
    {
        rt_pin_write(GPIO_LED_PIN, PIN_HIGH);
        rt_thread_mdelay(500);

        rt_pin_write(GPIO_LED_PIN, PIN_LOW);
        rt_thread_mdelay(500);
    }
}

void led_sample(void)
{
    rt_thread_t tid;

    tid = rt_thread_create("led_sample", led_sample_thread_entry, RT_NULL,
                           512, 11, 20);
    RT_ASSERT(tid != RT_NULL);
    if (tid != RT_NULL)
    {
        rt_thread_startup(tid);
    }
}
MSH_CMD_EXPORT(led_sample, led sample);
```

这个sample随便放到main.c里面随便放到哪里都可以，

测试的时候在console里面输入led_sample即可。这边要注意GPIO脚要做修改，引脚选择LED。

改下引脚配置即可。

这边测试sample里面调用函数关系

```
rt_pin_mode  --> mcu_pin_mode
rt_pin_write --> mcu_pin_write
rt_hw_pin_init

```

### 开始实现代码

这边根据一般厂商的LED GPIO sample来

### rt_hw_pin_init

这边先开时钟什么的时钟准备，一些GPIO初始化可以在这个函数里面

### mcu_pin_mode

这个函数需要配置好GPIO引脚模式，通常为设置引脚为输出还是输入

sample code，需要根据mode的值来判断，这边定义了几种常见的值

给出sample code，

```
static void mcu_pin_mode(rt_device_t dev, rt_base_t pin, rt_base_t mode)
{
    gpio_cfg_t tmp_gpio_cfg;
    int ret = 0;
    tmp_gpio_cfg.port = PIN_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);

    switch (mode)
    {
    case PIN_MODE_OUTPUT:
        tmp_gpio_cfg.func = GPIO_FUNC_OUT;
        tmp_gpio_cfg.pad = GPIO_PAD_NONE;
        break;
    case PIN_MODE_INPUT:
        tmp_gpio_cfg.func = GPIO_FUNC_IN;
        tmp_gpio_cfg.pad = GPIO_PAD_NONE;
        break;
    case PIN_MODE_INPUT_PULLUP:
        tmp_gpio_cfg.func = GPIO_FUNC_IN;
        tmp_gpio_cfg.pad = GPIO_PAD_PULL_UP;
        break;
    case PIN_MODE_INPUT_PULLDOWN:
        tmp_gpio_cfg.func = GPIO_FUNC_IN;
        tmp_gpio_cfg.pad = GPIO_PAD_PULL_DOWN;
        break;
    case PIN_MODE_OUTPUT_OD:
        //not support
        LOG_E("NOT SUPPORT");
        break;
    }
    ret = GPIO_Config(&tmp_gpio_cfg);
    if (E_NO_ERROR != ret)
    {
        LOG_E("GPIO_Config error :%d", ret);
    }
}
```

###  mcu_pin_write

这个是用来设置引脚高低电平的

sample code 根据value值来判断高电平还是低电平

```
static void mcu_pin_write(rt_device_t dev, rt_base_t pin, rt_base_t value)
{
    gpio_cfg_t tmp_gpio_cfg;
    tmp_gpio_cfg.port = PIN_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);
    if (value)
    {
        GPIO_OutSet(&tmp_gpio_cfg);
    }
    else
    {
        GPIO_OutClr(&tmp_gpio_cfg);
    }

}
```

这几个函数实现了，就可以跑亮灯程序了。目标是小灯一闪一闪的即可

## 添加gpio_sample

小灯亮了之后，完成一大半了，一些输出的驱动就可以跑了，不过还有一种输入设备是不能跑的，比如button等设备。

这个时候，输入另外一个sample

```
#define GPIO_LED_PIN  13
#define GPIO_BUTTON_PIN  12

static void button_callback(void *args)
{
    static int flag1 = 0;
    if (flag1 == 0)
    {
        flag1 = 1;
        rt_pin_write(GPIO_LED_PIN, PIN_LOW);
    }
    else
    {
        flag1 = 0;
        rt_pin_write(GPIO_LED_PIN, PIN_HIGH);
    }
}
static void gpio_sample_thread_entry(void *parameter)
{
    int count = 1;
    while (count++)
    {
        rt_thread_mdelay(1000);
        rt_kprintf("Current LED STATUS:%d\r\n ", rt_pin_read(GPIO_LED_PIN));
    }
}
void gpio_sample(void)
{
    rt_thread_t tid;

    rt_pin_mode(GPIO_LED_PIN, PIN_MODE_OUTPUT);

    rt_pin_write(GPIO_LED_PIN, PIN_HIGH);

    rt_pin_attach_irq(GPIO_BUTTON_PIN, PIN_IRQ_MODE_FALLING,
                      button_callback, (void *) true);
    rt_pin_irq_enable(GPIO_BUTTON_PIN, PIN_IRQ_ENABLE);

    tid = rt_thread_create("gpio_sample", gpio_sample_thread_entry, RT_NULL,
                           512, 11, 20);
    if (tid != RT_NULL)
    {
        rt_thread_startup(tid);
    }
}
MSH_CMD_EXPORT(gpio_sample, gpio sample);
```

### 开始实现代码

这个sample主要调用以下接口

```
rt_pin_read  ---> mcu_pin_read
rt_pin_attach_irq --> mcu_pin_attach_irq
rt_pin_irq_enable --> mcu_pin_irq_enable

```

### mcu_pin_read

这个函数直接获取GPIO 脚的高低电平返回0 或者1即可

sample code

 ```
static int mcu_pin_read(rt_device_t dev, rt_base_t pin)
{
    int value;
    gpio_cfg_t tmp_gpio_cfg;
    tmp_gpio_cfg.port = PIN_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);

    if (GPIO_InGet(&tmp_gpio_cfg))
    {
        value = 1;
    }
    else
    {
        value = 0;
    }

    return value;
}
 ```

### mcu_pin_attach_irq

这个稍微复杂一些，这个会根据irq_mode来设置上升沿触发还是下降沿触发callback函数

sample code

```
static rt_err_t mcu_pin_attach_irq(struct rt_device *device, rt_int32_t pin,
                                   rt_uint32_t irq_mode, void (*hdr)(void *args), void *args)
{
    gpio_cfg_t tmp_gpio_cfg;
    tmp_gpio_cfg.port = PIN_MCU_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);


    tmp_gpio_cfg.pad = GPIO_PAD_PULL_UP;
    tmp_gpio_cfg.func = GPIO_FUNC_IN;
    GPIO_Config(&tmp_gpio_cfg);
    GPIO_RegisterCallback(&tmp_gpio_cfg, hdr, args);

    gpio_int_mode_t mcu_mode;
    gpio_int_pol_t mcu_pol;

    switch (irq_mode)
    {
    case PIN_IRQ_MODE_RISING:
        mcu_mode = GPIO_INT_EDGE;
        mcu_pol = GPIO_INT_RISING;
        break;
    case PIN_IRQ_MODE_FALLING:
        mcu_mode = GPIO_INT_EDGE;
        mcu_pol = GPIO_INT_FALLING;
        break;
    case PIN_IRQ_MODE_RISING_FALLING:
        mcu_mode = GPIO_INT_EDGE;
        mcu_pol = GPIO_INT_BOTH;
        break;
    case PIN_IRQ_MODE_HIGH_LEVEL:
        mcu_mode = GPIO_INT_LEVEL;
        mcu_pol = GPIO_INT_HIGH;
        break;
    case PIN_IRQ_MODE_LOW_LEVEL:
        mcu_mode = GPIO_INT_LEVEL;
        mcu_pol = GPIO_INT_LOW;
        break;
    }

    GPIO_IntConfig(&tmp_gpio_cfg, mcu_mode, mcu_pol);


    return RT_EOK;
}

```

### mcu_pin_irq_enable

这个就是开触发中断

```
static rt_err_t mcu_pin_irq_enable(struct rt_device *device, rt_base_t pin,
                                   rt_uint32_t enabled)
{
    gpio_cfg_t tmp_gpio_cfg;
    tmp_gpio_cfg.port = PIN_MCU_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);
    if (enabled)
    {
        GPIO_IntEnable(&tmp_gpio_cfg);
        NVIC_EnableIRQ((IRQn_Type)MXC_GPIO_GET_IRQ(PIN_MCU_PORT(pin)));
    }
    else
    {
        GPIO_IntDisable(&tmp_gpio_cfg);
        NVIC_DisableIRQ((IRQn_Type)MXC_GPIO_GET_IRQ(PIN_MCU_PORT(pin)));
    }
    return RT_EOK;
}
```

### mcu_pin_dettach_irq

这个函数就是关中断和关callback等一系列操作，

这个sample中没有调用，

```
static rt_err_t mcu_pin_dettach_irq(struct rt_device *device, rt_int32_t pin)
{
    gpio_cfg_t tmp_gpio_cfg;
    tmp_gpio_cfg.port = PIN_MCU_PORT(pin);
    tmp_gpio_cfg.mask = PIN_MCU_PIN(pin);
    tmp_gpio_cfg.pad = GPIO_PAD_PULL_UP;
    tmp_gpio_cfg.func = GPIO_FUNC_IN;
    GPIO_Config(&tmp_gpio_cfg);
    GPIO_IntDisable(&tmp_gpio_cfg);
    GPIO_RegisterCallback(&tmp_gpio_cfg, NULL, NULL);
    return RT_EOK;
}
```

### 中断处理函数

中断处理函数负责调callback回调函数，当触发某种中断的时候，能调到callback即可。

基本完成这些就能快速porting完成了。

最后gpio_sample的现象就是按button按钮，对应的LED小灯会切换灯的状态。

=============================

drv_gpio 需要的文件

pin.c

pin.h

RT_USING_HEAP

这个是要和pip.c和

#if defined(RT_USING_HEAP)

```
    printf("\r\n=====%s===%d==== \r\n ",__func__,__LINE__);
```

