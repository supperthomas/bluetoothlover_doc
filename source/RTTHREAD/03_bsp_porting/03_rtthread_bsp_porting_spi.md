# RTTHREAD移植BSP驱动 SPI篇

## 简介

本文介绍SPI设备驱动，drv_spi.c如何编写的，SPI驱动稍微复杂一些。

本文参考RTTHREAD官方文档[SPI 设备](https://www.rt-thread.org/document/site/programming-manual/device/spi/spi/)

一些基本知识，官方文档已经写的很详细了，大家如果不是很了解可以仔细看下官方文档，这边简单讲解下移植的时候遇到的一些问题，以及如何能快速上手的解决方案。

##  SPI简介

4根线，MOSI ,MISO , SCLK  CS



## 移植前准备

先要熟悉官方的SPI的demo如何运行的。

先准备一个drv_spi.c 这边提供一个模板，基本第一次稍微修改就可以编译通过，license大家可以改成自己的，这个随意。

```
/*
 * Copyright (c) 2006-2018, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date             Author          Notes
 * 2021-02-14       supperthomas    first version
 */

#include <stdint.h>
#include <string.h>
#include "board.h"
#include "drv_spi.h"

#define DBG_LEVEL   DBG_LOG
#include <rtdbg.h>
#define LOG_TAG                "drv.spi"

#ifdef BSP_USING_SPI

#if defined(BSP_USING_SPI0) || defined(BSP_USING_SPI1) || defined(BSP_USING_SPI2)
static struct mcu_drv_spi_config spi_config[] =
{
#ifdef BSP_USING_SPI0
    MCU_SPI0_CONFIG,
#endif
#ifdef BSP_USING_SPI1
    MCU_SPI1_CONFIG,
#endif

};

static struct mcu_drv_spi spi_bus_obj[sizeof(spi_config) / sizeof(spi_config[0])];


static rt_err_t spi_configure(struct rt_spi_device *device,
                              struct rt_spi_configuration *configuration)
{
    //init
    return RT_EOK;
}

static rt_uint32_t spixfer(struct rt_spi_device *device, struct rt_spi_message *message)
{
}

/* spi bus callback function  */
static const struct rt_spi_ops nrfx_spi_ops =
{
    .configure = spi_configure,
    .xfer = spixfer,
};

/*spi bus init*/
static int rt_hw_spi_bus_init(void)
{
    rt_err_t result = RT_ERROR;
    for (int i = 0; i < sizeof(spi_config) / sizeof(spi_config[0]); i++)
    {
        spi_bus_obj[i].spi_instance = spi_config[i].spi_instance;
        spi_bus_obj[i].spi_bus.parent.user_data = &spi_config[i];   //SPI INSTANCE
        result = rt_spi_bus_register(&spi_bus_obj[i].spi_bus, spi_config[i].bus_name, &nrfx_spi_ops);
        RT_ASSERT(result == RT_EOK);
    }
    return result;
}

int rt_hw_spi_init(void)
{
    return rt_hw_spi_bus_init();
}
INIT_BOARD_EXPORT(rt_hw_spi_init);

/**
  * Attach the spi device to SPI bus, this function must be used after initialization.
  */
rt_err_t rt_hw_spi_device_attach(const char *bus_name, const char *device_name, rt_uint32_t cs_pin)
{
    return RT_EOK;
}

#endif /* BSP_USING_SPI0 || BSP_USING_SPI1 || BSP_USING_SPI2 */
#endif /*BSP_USING_SPI*/



```

再加一个drv_spi.h即可

```
/*
 * Copyright (c) 2006-2018, RT-Thread Development Team
 *
 * SPDX-License-Identifier: Apache-2.0
 *
 * Change Logs:
 * Date             Author          Notes
 * 2021-02-14       supperthomas    first version
 */

#include <rtthread.h>
#include <rtdevice.h>
#include <rthw.h>

#include "spi.h"

#ifndef __DRV_SPI_H_
#define __DRV_SPI_H_

rt_err_t rt_hw_spi_device_attach(const char *bus_name, const char *device_name, rt_uint32_t ss_pin);

//SPI bus config
#ifdef BSP_USING_SPI0
#define MCU_SPI0_CONFIG          \
{                                \
    .bus_name = "spi0",          \
    .spi_instance = SPI0A,       \
}
#endif
#ifdef BSP_USING_SPI1
#ifdef BSP_USING_SPI1A  //The SPI1A is conflit with UART1 TX RX P0.10 P0.11
#define MCU_SPI1_CONFIG          \
{                                \
    .bus_name = "spi1",          \
    .spi_instance = SPI1A        \
}
#else
#define MCU_SPI1_CONFIG          \
{                                \
    .bus_name = "spi1",          \
    .spi_instance = SPI1B        \
}
#endif
#endif

struct mcu_drv_spi_config
{
    char *bus_name;
    spi_type spi_instance;
};

struct mcu_drv_spi
{
    spi_type spi_instance;
    spi_req_t spixfer_req;
    struct rt_spi_configuration *cfg;
    struct rt_spi_bus spi_bus;
};

#endif  /*__DRV_SPI_H_*/


```

spi驱动主要是要提交这两个，还需要添加Kconfig

```
    config BSP_USING_SPI
        bool "Enable SPI"
        select RT_USING_SPI
        default n
```

这边主要添加`RT_USING_SPI` 和`BSP_USING_SPI`宏定义。

```

```

## 添加spi_sample

spi_sample 方便测试，先把spi_sample放好，这个sample是将MOSI和MISO对接，采用loopback的方式进行测试，这样的话，可以不依赖硬件来测试SPI，发送数据和接收数据比对能够正确即可。或者收到数据即可。



```
#define SPI_DEVICE_BUS      "spi0"
#define SPI_DEVICE_NAME     "spi01"

#define TEST_LEN        10
uint8_t rx_data[TEST_LEN];
uint8_t tx_data[TEST_LEN];

static void spi_sample(int argc, char *argv[])
{
    struct rt_spi_device *spi_dev;
    char name[RT_NAME_MAX];


    spi_dev = (struct rt_spi_device *)rt_device_find(SPI_DEVICE_NAME);
    if (RT_NULL == spi_dev)
    {
        rt_hw_spi_device_attach(SPI_DEVICE_BUS, SPI_DEVICE_NAME, PIN_0);
        spi_dev = (struct rt_spi_device *)rt_device_find(SPI_DEVICE_NAME);
    }

    struct rt_spi_configuration spi_cfg =
    {
        .mode = 0,
        .data_width = 8,
        .max_hz = 1000000,
    };
    rt_spi_configure(spi_dev, &spi_cfg);

    rt_kprintf("\n************** SPI Loopback Demo ****************\n");
    rt_kprintf("This example configures the SPI to send data between the MISO (P0.4) and\n");
    rt_kprintf("MOSI (P0.5) pins.  Connect these two pins together. \n");

    for (int j = 0; j < TEST_LEN; j++)
    {
        tx_data[j] = j ;
    }
    if (argc == 2)
    {
        rt_strncpy(name, argv[1], RT_NAME_MAX);
    }
    else
    {
        rt_strncpy(name, SPI_DEVICE_NAME, RT_NAME_MAX);
    }

    spi_dev = (struct rt_spi_device *)rt_device_find(name);
    if (!spi_dev)
    {
        rt_kprintf("spi sample run failed! can't find %s device!\n", name);
    }
    else
    {
        rt_spi_transfer(spi_dev, tx_data, rx_data, TEST_LEN);
        for (int i = 0; i < TEST_LEN; i++)
        {
            rt_kprintf(" 0x%02x, ", rx_data[i]);
        }
    }
}
MSH_CMD_EXPORT(spi_sample, spi sample);
```

这个sample随便放到main.c里面随便放到哪里都可以，

测试的时候在console里面输入spi_sample即可。

这边测试sample里面调用函数关系

```
rt_hw_spi_device_attach  --> rt_hw_spi_device_attach
rt_spi_configure --> spi_configure
rt_spi_transfer  --> spixfer

```

### 开始实现代码

这边根据一般厂商的SPI sample来

### rt_hw_spi_init

这个函数主要设置一些和SPI不相干的一些时钟和注册一个spi0的spi bus。

这边需要注意的是：

mcu_drv_spi_config： 这个是配置spi bus的名称和存放一个控制SPI的handle值，这个需要根据厂商的接口来定义

mcu_drv_spi： 这个存放的是结构体，存放当前spi的cfg（速率以及其他）， 存放一个控制SPI的handle值

这边多放了一个传输的结构体，这个根据厂商来，这边是MAX32660的参考例程。

这边完成的内容不多，只要这个device注册上去即可。



### rt_hw_spi_device_attach

这个函数是用来选择CS片选的，SPI是一个通信总线，总线上可以有多个设备，根据SPI协议，一个CS片选对应一个device设备，调用这个设备代表该设备被选中，CS选中，对于一个MASTER而言可以有多个CS。每注册一个设备需要上拉一个cs pin脚。

cs脚可以先不实现，根据应用再实现，最后调rt_spi_bus_attach_device来实现设备的挂载在bus总线上，根据RTTHREAD官方文档，对于总线名称是spi0， 对于设备名称是spi01

所以这边主要添加一个device，需要实现的代码不多，cs可以暂时不实现。

```
rt_err_t rt_hw_spi_device_attach(const char *bus_name, const char *device_name, rt_uint32_t cs_pin)
{
    RT_ASSERT(bus_name != RT_NULL);
    RT_ASSERT(device_name != RT_NULL);
    RT_ASSERT(cs_pin != RT_NULL);

    rt_err_t result;
    struct rt_spi_device *spi_device;
    /* attach the device to spi bus*/
    spi_device = (struct rt_spi_device *)rt_malloc(sizeof(struct rt_spi_device));
    RT_ASSERT(spi_device != RT_NULL);
    /* initialize the cs pin */
    result = rt_spi_bus_attach_device(spi_device, device_name, bus_name, (void *)cs_pin);
    if (result != RT_EOK)
    {
        LOG_E("%s attach to %s faild, %d", device_name, bus_name, result);
        result = RT_ERROR;
    }
    /* TODO: SET THE GPIO */

    RT_ASSERT(result == RT_EOK);
    return result;
}
```

###  rt_spi_configure

这个是用来配置spi bus的速率的，这边比较重要，需要根据configuration->mode的模式进行调整，

前期可以直接将官方的demo的初始化配置放这里，

```
static rt_err_t spi_configure(struct rt_spi_device *device,
                              struct rt_spi_configuration *configuration)
{
    RT_ASSERT(device != RT_NULL);
    RT_ASSERT(device->bus != RT_NULL);
    RT_ASSERT(device->bus->parent.user_data != RT_NULL);
    RT_ASSERT(configuration != RT_NULL);
    struct mcu_drv_spi *tmp_spi;
    tmp_spi = rt_container_of(device->bus, struct mcu_drv_spi, spi_bus);
    int mode;

    ///init

    switch (configuration->mode & RT_SPI_MODE_3)
    {
    case RT_SPI_MODE_0/* RT_SPI_CPOL:0 , RT_SPI_CPHA:0 */:
    case RT_SPI_MODE_1/* RT_SPI_CPOL:0 , RT_SPI_CPHA:1 */:
    case RT_SPI_MODE_2/* RT_SPI_CPOL:1 , RT_SPI_CPHA:0 */:
    case RT_SPI_MODE_3/* RT_SPI_CPOL:1 , RT_SPI_CPHA:1 */:
        mode = configuration->mode & RT_SPI_MODE_3;
        break;
    default:
        LOG_E("spi_configure mode error %x\n", configuration->mode);
        return RT_ERROR;
    }

    tmp_spi->spixfer_req.width = SPI17Y_WIDTH_1;
    tmp_spi->spixfer_req.bits = configuration->data_width;
    tmp_spi->spixfer_req.ssel = 0;
    tmp_spi->spixfer_req.deass = 1;
    tmp_spi->spixfer_req.tx_num = 0;
    tmp_spi->spixfer_req.rx_num = 0;
    tmp_spi->spixfer_req.callback = NULL;
    LOG_D("spi init mode:%d, rate:%d", mode, configuration->max_hz);
    if (SPI_Init(tmp_spi->spi_instance, mode, configuration->max_hz) != 0)
    {
        LOG_E("Error configuring SPI\n");
        while (1) {}
    }
    //init
    return RT_EOK;
}

```

### spixfer

这个函数是主要的传输函数：

这个是主要的传输函数：

参考sample

```
static rt_uint32_t spixfer(struct rt_spi_device *device, struct rt_spi_message *message)
{
    RT_ASSERT(device != RT_NULL);
    RT_ASSERT(device->bus != RT_NULL);
    RT_ASSERT(device->bus->parent.user_data != RT_NULL);

    int ret = 0;
    struct mcu_drv_spi *tmp_spi;
    tmp_spi = rt_container_of(device->bus, struct mcu_drv_spi, spi_bus);


    tmp_spi->spixfer_req.tx_data = message->send_buf;
    tmp_spi->spixfer_req.rx_data = message->recv_buf;
    tmp_spi->spixfer_req.len = message->length;
    ret = SPI_MasterTrans(tmp_spi->spi_instance, &tmp_spi->spixfer_req);
    if (ret == E_NO_ERROR)
    {
        return message->length;
    }
    else
    {
        LOG_E("spixfer faild, ret %d", ret);
        return 0;
    }
}
```

