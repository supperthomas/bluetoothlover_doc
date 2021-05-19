# rt-thread 移植BSP驱动 uart篇

## 简介

uart驱动作为常用外设之一，对rt-thread的msh组件使用和一些外接uart模块来说必不可少，这篇文章将介绍如何基于rt-thread的serial框架来编写drv_uart.c和drv_uart.h文件，直到最后一步步实现msh组件的使用。

阅读本篇文章前，确定你已经熟悉了[rt-thread的使用](https://docs.rt-thread.org/#/rt-thread-version/rt-thread-standard/README)以及在一个stm32或者其他移植过BSP的开发板上跑起来了rt-thread，并且你已经熟悉了[UART](https://www.rt-thread.org/document/site/programming-manual/device/uart/uart/)设备驱动框架的使用方法。

uart作为一种常用的外设，一般情况下只使用两根线 ： tx rx ；在使用时主设备的tx接从设备的rx， 主设备的rx接从设备的tx。 一般情况下作为异步方式使用，即tx和rx互不相干，如果想做半双工通讯，可以只接tx或者rx。当然uart还有许多扩展的通讯方式，比如硬件流控和时钟同步等等，但是一般情况下都不用，这里不做讨论。

## 移植

### 准备模板文件

首先准备一个模板文件，drv_uart.c和drv_uart.h。这两个文件里面只有函数体，并没有函数实现，将这两个文件加入到工程中，一般情况下都是可以编译通过的。

drv_uart.c

```c
/*
 * Copyright (C) 2020, Huada Semiconductor Co., Ltd.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2020-05-18     xph          first version
 */

/*******************************************************************************
 * Include files
 ******************************************************************************/
#include <rtdevice.h>
#include <rthw.h>

#include "drv_usart.h"
#include "board_config.h"

#ifdef RT_USING_SERIAL

#if !defined(BSP_USING_UART1) && !defined(BSP_USING_UART2) && !defined(BSP_USING_UART3) && \
    !defined(BSP_USING_UART4) && !defined(BSP_USING_UART5) && !defined(BSP_USING_UART6) && \
    !defined(BSP_USING_UART7) && !defined(BSP_USING_UART8) && !defined(BSP_USING_UART9) && \
    !defined(BSP_USING_UART10)
#error "Please define at least one BSP_USING_UARTx"
/* UART instance can be selected at menuconfig -> Hardware Drivers Config -> On-chip Peripheral Drivers -> Enable UART */
#endif



static rt_err_t hc32_configure(struct rt_serial_device *serial,
                                struct serial_configure *cfg)
{


    return RT_EOK;
}

static rt_err_t hc32_control(struct rt_serial_device *serial, int cmd, void *arg)
{
    struct hc32_uart *uart;
 

    return RT_EOK;
}

static int hc32_putc(struct rt_serial_device *serial, char c)
{


    return 1;
}

static int hc32_getc(struct rt_serial_device *serial)
{
    int ch= -1;
    return ch;
}



static const struct rt_uart_ops hc32_uart_ops =
{
    .configure = hc32_configure,
    .control = hc32_control,
    .putc = hc32_putc,
    .getc = hc32_getc,
    .dma_transmit = RT_NULL
};

int hc32_hw_uart_init(void)
{
    rt_err_t result = RT_EOK;

    return result;
}

INIT_BOARD_EXPORT(hc32_hw_uart_init);

#endif /* RT_USING_SERIAL */

/*******************************************************************************
 * EOF (not truncated)
 ******************************************************************************/

```

drv_uart.h

```c
/*
 * Copyright (C) 2020, Huada Semiconductor Co., Ltd.
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date           Author       Notes
 * 2020-05-18     xph          first version
 */
 

#ifndef __DRV_USART_H__
#define __DRV_USART_H__

/*******************************************************************************
 * Include files
 ******************************************************************************/
#include <rtthread.h>
#include "rtdevice.h"

#include "uart.h"


/* C binding of definitions if building with C++ compiler */
#ifdef __cplusplus
extern "C"
{
#endif

/*******************************************************************************
 * Global type definitions ('typedef')
 ******************************************************************************/

/*******************************************************************************
 * Global pre-processor symbols/macros ('#define')
 ******************************************************************************/

/*******************************************************************************
 * Global variable definitions ('extern')
 ******************************************************************************/

/*******************************************************************************
 * Global function prototypes (definition in C source)
 ******************************************************************************/
int rt_hw_uart_init(void);

#ifdef __cplusplus
}
#endif

#endif /* __DRV_USART_H__ */

/*******************************************************************************
 * EOF (not truncated)
 ******************************************************************************/

```

将这两个文件加入到你的工程中，然后保证编译通过，如果编译出错，把能删除的都删除，只保留函数就行了。

```c
".\output\release\rt-thread.axf" - 0 Error(s), 0 Warning(s).
```



### 添加函数体

然后重头戏来了，我们要分别实现每个函数的函数体。这些函数体的实现和你目标MCU的uart驱动有关系，大致思想就是将目标MCU的uart驱动给移植过来。这里我分析一下我的移植思路。

根据rt-thread的设计思想，我们一般情况下分析驱动文件是从drv_xxx.c的最后一行开始分析。这里就是

`INIT_BOARD_EXPORT(hc32_hw_uart_init);`

然后，找到这个函数，这个函数就是将uart设备注册到serial驱动框架中的，主要是就是将设备的driver层和device层联系起来，当上层调用rt_device_find的时候，就会跟着执行drv_xxx.c里面的硬件配置函数，函数实现看下面代码注释。

```c
int hc32_hw_uart_init(void)
{
    rt_err_t result = RT_EOK;
    /* 当前一共用了多少个串口设备， 在rtconfig.h中的 BSP_USING_UARTx 宏来决定用了多少个串口*/
    rt_size_t obj_num = sizeof(uart_obj) / sizeof(struct hc32_uart_t); 
	/* 串口默认配置参数  主要是配置波特率 数据位 停止位 奇偶校验位等等 */
    struct serial_configure config = RT_SERIAL_CONFIG_DEFAULT;
	/* 将这些配置参数放在uart 管理结果体里，同时像device层注册uart设备 */
    for (int i = 0; i < obj_num; i++)
    {
        uart_obj[i].config = &uart_config[i];
        uart_obj[i].serial.ops = &hc32_uart_ops; // 上层操作函数最终会进入到drv层来操作具体的硬件 所以实现drv的ops就是移植的重点
        uart_obj[i].serial.config = config;

        /* register UART device */
        result = rt_hw_serial_register(&uart_obj[i].serial, uart_obj[i].config->name,
                                       RT_DEVICE_FLAG_RDWR | RT_DEVICE_FLAG_INT_RX | RT_DEVICE_FLAG_INT_TX, NULL);
        RT_ASSERT(result == RT_EOK);
    }
    return result;
}
```

然后就要实现各个ops函数了，这个是我们移植的重点和难点。ops操作函数的每个意义如下：

```c
static const struct rt_uart_ops hc32_uart_ops =
    {
        .configure = hc32_configure,   // 配置和初始化函数 
        .control = hc32_control,	  // 重新配置串口操作函数 常用的就是更改波特率
        .putc = hc32_putc,		      // 串口发送一个字节
        .getc = hc32_getc,			 // 串口接收一个字节
        .dma_transmit = RT_NULL       // dma传输 这个一开始可以不实现
    };
```

首先，重点介绍两个比较重要的结构体

```c
struct hc32_uart_config
{
    const char *name;                 // 串口的名字
    M0P_UART_TypeDef *Instance;       // 对应的串口硬件接口
    IRQn_Type irq_type;               // 中断类型

};

struct hc32_uart_t
{
    stc_uart_cfg_t stcCfg;                   // 和具体的MCU有关，配置结构体
    struct hc32_uart_config *config;         // 串口通用配置
    struct rt_serial_device serial;          // 对接uart device 必要

};
```

接着实现config函数，这个函数的两个入参，一个是对接设备驱动框架的serial，通过serial我们能找到当前操作的是哪个串口，另一个就是配置cfg，这个cfg里的参数就是我们上面注册serial设备时的默认初始化参数 *RT_SERIAL_CONFIG_DEFAULT*。函数的具体实现逻辑我在函数体中做了注释。

```c
static rt_err_t hc32_configure(struct rt_serial_device *serial,
                               struct serial_configure *cfg)
{
    struct hc32_uart_t *uart;
    RT_ASSERT(serial != RT_NULL);
    RT_ASSERT(cfg != RT_NULL);
    uart = rt_container_of(serial, struct hc32_uart_t, serial);   // 通过serial来找到uart 然后操作这个uart
    /* 这里通过interface接口来确定具体操作哪个串口 实现方式和各个MCU有关系 可以参考MCU的SDK里给的simple */
    if (uart->config->Instance == M0P_UART1) 
    {
        stc_gpio_cfg_t stcGpioCfg;
        DDL_ZERO_STRUCT(stcGpioCfg);
		/* 使能时钟 */
        Sysctrl_SetPeripheralGate(SysctrlPeripheralUart1, TRUE); ///<使能uart1模块时钟
        Sysctrl_SetPeripheralGate(SysctrlPeripheralGpio, TRUE);  //使能GPIO模块时钟
		/* 初始化IO */
        ///<TX
        stcGpioCfg.enDir = GpioDirOut;
        Gpio_Init(GpioPortA, GpioPin2, &stcGpioCfg);
        Gpio_SetAfMode(GpioPortA, GpioPin2, GpioAf1); //配置PA02 端口为URART1_TX

        ///<RX
        stcGpioCfg.enDir = GpioDirIn;
        Gpio_Init(GpioPortA, GpioPin3, &stcGpioCfg);
        Gpio_SetAfMode(GpioPortA, GpioPin3, GpioAf1); //配置PA03 端口为URART1_RX
		/* 具体的串口参数配置 各个MCU厂家各不相同 */
        uart->stcCfg.enRunMode = UartMskMode3; ///<模式3
        uart->stcCfg.stcBaud.u32Baud = cfg->baud_rate;
        uart->stcCfg.stcBaud.enClkDiv = UartMsk8Or16Div;      ///<通道采样分频配置
        uart->stcCfg.stcBaud.u32Pclk = Sysctrl_GetPClkFreq(); ///<获得外设时钟（PCLK）频率值

        switch (cfg->stop_bits)
        {
        case STOP_BITS_1:
            uart->stcCfg.enStopBit = UartMsk1bit;
            break;
        case STOP_BITS_2:
            uart->stcCfg.enStopBit = UartMsk2bit;
            break;
        default:
            uart->stcCfg.enStopBit = UartMsk1_5bit;
            break;
        }

        switch (cfg->parity)
        {
        case PARITY_NONE:
            uart->stcCfg.enMmdorCk = UartMskDataOrAddr;
            break;
        case PARITY_ODD:
            uart->stcCfg.enMmdorCk = UartMskOdd;
            break;
        case PARITY_EVEN:
            uart->stcCfg.enMmdorCk = UartMskEven;
            break;
        default:
            uart->stcCfg.enMmdorCk = UartMskDataOrAddr;
            break;
        }
    }
    Uart_Init(uart->config->Instance, &(uart->stcCfg)); ///<串口初始化

    ///<UART中断使能
    Uart_ClrStatus(uart->config->Instance,UartRC);                ///<清接收请求
    Uart_EnableIrq(uart->config->Instance,UartRxIrq);             ///<使能串口接收中断   
    EnableNvic(uart->config->irq_type, IrqLevel3, TRUE);       ///<系统中断使能


    return RT_EOK;
}
```

接下来实现的putc和getc就好办了，比较简单

```c
static int hc32_putc(struct rt_serial_device *serial, char c)
{
    struct hc32_uart_t *uart;
    RT_ASSERT(serial != RT_NULL);
    uart = rt_container_of(serial, struct hc32_uart_t, serial);
    Uart_SendDataPoll(uart->config->Instance, c);
    return 1;
}

static int hc32_getc(struct rt_serial_device *serial)
{
    int ch = -1;
    struct hc32_uart_t *uart;
    RT_ASSERT(serial != RT_NULL);
    uart = rt_container_of(serial, struct hc32_uart_t, serial);
    if (Uart_GetStatus(uart->config->Instance, UartRC)) //UART1数据接收
    {
        Uart_ClrStatus(uart->config->Instance, UartRC);     // 清中断状态位
        ch = Uart_ReceiveData(uart->config->Instance);      // 接收数据字节
    }
    return ch;
}
```

最后，我们再分析一下，串口的中断接收。

根据MCU的SDK里的串口中断接收simple，首先找到中断服务函数放在drv_uart.c里，如下：

```c
#if defined(BSP_USING_UART1) || defined(BSP_USING_UART3)
//UART1中断函数
void UART1_3_IRQHandler(void)
{
    /* enter interrupt */
    rt_interrupt_enter();
#if (INT_CALLBACK_ON == INT_CALLBACK_UART1)  
    uart_isr(&(uart_obj[UART1_INDEX].serial));
#endif
    /* leave interrupt */
    rt_interrupt_leave();
}

#endif
```

然后在中断服务函数里调用uart_isr函数，这个函数也是我们需要实现的函数，如下：

```c
/**
 * Uart common interrupt process. This need add to uart ISR.
 *
 * @param serial serial device
 */
static void uart_isr(struct rt_serial_device *serial)
{
    struct hc32_uart_t *uart;
    RT_ASSERT(serial != RT_NULL);
    uart = rt_container_of(serial, struct hc32_uart_t, serial);

    /* UART in mode Receiver -------------------------------------------------*/
    if(Uart_GetStatus(uart->config->Instance , UartRC))         //UART1数据接收
    {
        rt_hw_serial_isr(serial, RT_SERIAL_EVENT_RX_IND);      // 在getc里清除中断
    }
    if(Uart_GetStatus(uart->config->Instance, UartTC))         //UART1数据发送
    {
        Uart_ClrStatus(uart->config->Instance, UartTC);        //清中断状态位
    }
}
```

在这个函数里，我们要分析当前发生的是什么中断，并处理对应的中断，常见的中断有接收中断、发送中断以及DMA中断等等。这里，我们只处理接收中断，在接收中断中，调用`rt_hw_serial_isr`函数来通知serial框架有中断发生，并告知中断类型，然后`rt_hw_serial_isr`会调用我们驱动中实现的getc函数来接收一个字符，在getc中要注意，**接收完成一个字符后，要清除中断标志位。**

这些操作都完成后，串口驱动应该就能跑起来了。



```c
 \ | /
- RT -     Thread Operating System
 / | \     4.0.3 build May 19 2021
 2006 - 2021 Copyright by rt-thread team
Os is Start!!! 
msh >
msh >
msh >
msh >

```



当然，如有要更改串口波特率或者校验位 数据位等串口配置参数，就要实现control函数了。这里就不过多介绍了。



## 问题&总结

- 串口驱动实现的重点是要挂接串口驱动函数到serial设备框架，然后再实现每个函数
- 我们在做串口驱动的时候，应该先熟悉目标开发板的SDK里面的串口相关驱动函数，然后在此基础上再做移植
- 遇到问题应该单步调试一下，主要是看 `uart = rt_container_of(serial, struct hc32_uart_t, serial);` 这里有没有获取到正确的uart
- 对于同系列的MCU要考虑兼容性，但是先实现的时候以实现目标为准，然后再考虑重构和优化







