# USB

## 目标

学习完本文内容，你对以下内容会有一个大概的了解：

- USB的基础知识
- USB相关资料可以到哪里找
- RT-Thread USB协议栈的实现介绍

## USB 简介

USB(Universal Serial Bus)是一种支持热插拔的通用串行总线。它使用差分信号来传输数据，在 USB 1.0和 USB 1.1 版本中，只支持 1.5Mb/s 的低速（low-speed）模式和 12Mb/s 的全速（full-speed）模式，在 USB 2.0 中，又加入了480Mb/s 的高速模式，USB 3.0(super speed)，传输速率最大5Gbps。

### USB Host

任何USB系统中只有一个主机。 主机系统的USB接口被称为主机控制器。 主机控制器可以以硬件，固件或软件的组合来实现。 根集线器集成在主机系统内以提供一个或多个连接点。

### USB Device

USB Device 可以分为 USB Hub 和 USB Function。

1. USB Hub 提供了一种低成本、低复杂度的  USB接口扩展方法。Hub  的上行端口面向 HOST，下行端口面向设备(Hub 或功能设备)。在下行端口上，Hub 提供了设备连接检测和设备移除检测的能力，并给各下行端口供电。Hub 可以单独使能各下行端口。不同端口可以工作在不同的速度等级(高速/全速/低速)。

2. USB Function 能够通过总线传输或接收数据或控制信息的设备，在 USB2.0 标准中，别称为 Class



## USB 应用

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291106060.png)

## USB 硬件介绍

### 标准接口

标准接口分为PC端和Device端

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291120188.png)



### 硬件接口

一般情况下，USB接口有DP,DM 这两个差分传输线，但是其实还有一个ID线，但有些MCU的USB模块即支持做USB设备又支持做USB主机，此时ID线就起作用了，当做USB设备时，ID接高，当做USB主机时，ID接低

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291134836.png)

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291134201.png)





## USB 拓扑结构

- USB总线基于分层的星状拓扑结构
- 以HUB为中心，连接周围的设备
- 总线上最多可连接127个设备，HUB串联数量最多5个

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291142195.png)



## 协议核心术语

要想理解USB协议栈，必须对一些术语理解，这样我们在看USB协议栈的时候，才能理解代码的流程含义

- USB 传输（transfer）
- USB 事务 （transaction）
- USB 包 （package）
- 配置
- 接口
- 端点 （Endpoint）
- 管道

## USB 抓包器

要想理解USB协议，我们最好能有一个USB抓包器，结合协议文档，以及抓包器的解析，来理解协议，USB抓包工具分为纯软件的和硬件的两种，纯软件usb抓包工具需要在系统能正确枚举usb设备的前提下才能让内核的钩子函数捕抓到数据，而后者在usb不正常时也能捕捉到链路数据（令牌包等），属于更底层的抓包方式。

关于软件抓包起，因为我没有实际用过，大家自行百度尝试，比如[开源硬件USB抓包及协议分析工具分享](https://blog.csdn.net/litao31415/article/details/103925094) 我这边使用的硬件抓包器是

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291242990.png)



## USB抓包分析

所有的USB设备，在插入时，首先进行USB枚举过程，枚举过程其实就是控制传输过程，控制传输是所有的USB必须有的过程，下面我们以获取设备描述符举例，整体截图如下

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400123.png)

- 在一个transfer中，一般会有3个transaction, 一个transaction中，一般会有3个packet

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400012.png)



![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400162.png)

<img src="https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400907.png" alt="image-20210722150818691"  />



HOST某次数据交互分析

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400099.png)

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400474.png)



## USB 资料查找

### 官方网站

[www.usb.org](https://www.usb.org/)

### 搜索文档

https://www.usb.org/documents



比如查找USB2.0相关文档，可以输入usb 2.0



![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400306.png)





![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108301400966.png)





## USB 协议栈介绍

一些相对有名的开源USB协议栈有

- [TeenyUSB](https://github.com/xtoolbox/TeenyUSB)

  TeenyUSB是一个用于STM32芯片的轻量级USB协议栈。这个项目最开始主要目的是为了解决芯片代码空间的不足的问题。用CubeMX生成的代码体积比较大，而选用的芯片资源又十分有限，因此就有了实现一个轻量级USB的想法

- [tinyusb](https://github.com/hathach/tinyusb)

  全静态内存分配，不支持多设备，不支持同一设备上使用多个同类型接口，暂时不支持STM32主机模式。

- [usbx](https://github.com/azure-rtos/usbx)

  A high-performance USB host, device, and on-the-go (OTG) embedded stack, Azure RTOS USBX is fully integrated with Azure RTOS ThreadX and available for all Azure RTOS ThreadX–supported processors. Like Azure RTOS ThreadX, Azure RTOS USBX is designed to have a small footprint and high performance, making it ideal for deeply embedded applications that require an interface with USB devices.

- RT-Thread usb stack

  

- 其他。。。

  

## RT-Thread usb stack

### 简介

RT-Thread usb协议栈支持USB HOST和USB Device，协议栈位置在`components\drivers\usb`

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291322849.png)

### STM32L496 USB CDC适配

[STM32L496 USB CDC适配](https://club.rt-thread.org/ask/article/2959.html)





### 详细介绍

#### USB Device 核心代码

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291334452.png)

#### USB Device 设备类代码

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291334812.png)

#### USB HOST 核心代码

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291335725.png)

#### USB HOST 支持的设备类

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291339119.png)

#### USB 驱动代码

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291339100.png)







#### USB 驱动移植

需要实现的ops

```
const static struct udcd_ops _udc_ops =
{
    _set_address,		// 设置设备地址
    _set_config,		// 
    _ep_set_stall,		// 给USB HOST回复STALL命令
    _ep_clear_stall,	// 清楚设备的STALL状态
    _ep_enable,			// 使能ep端口
    _ep_disable,
    _ep_read_prepare,	// 读取endpoint数据
    _ep_read,
    _ep_write,			// 给USB HOST发送数据
    _ep0_send_status,	// Status stage 发送状态
    _suspend,
    _wakeup,
};
```

### rt-thread协议栈思维脑图

#### 枚举+数据输入输出

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404171.png)



#### 设备类注册

![image-20210802142636619](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404177.png)



## EP0 SETUP 阶段

### 协议文档描述

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404926.png)

### 协议结构体描述

#### setup包的封装

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404698.png)



#### setup包的解析

##### request_type

###### request_type.Direction (D7)

Direction字段表示请求的方向，D7为1表示的是IN包（DEVICE->HOST，device给host发送数据），D7为0表示OUT包（HOST->DEVICE,即host给device发送数据）

Direction字段，其实和setup包中的第二个字节，即bRequest字段，有一些重复，比如当bRequest为`USB_REQ_GET_STATUS`时，Direction字段必然需要为1，即IN包，如果不为IN包，只能说明USBHOST组包时出错了（USB传输过程中如果出错，USB硬件CRC校验失败后，不会将接收到的数据向上传递，即应用层根本不会收到setup包数据），当bRequest为`USB_REQ_SET_FEATURE`时，Direction字段必须为0，即OUT包。

request_type.Direction字段和bRrequest字段通常可以联合起来，校验USBHOST发送过来的数据包是否合法，但是通常认为USBHOST组包发送错误的概率不大，因此，rt-thread中并没有很多联合校验的功能代码，查看代码，只看到了在获取描述符时，加了这样的校验逻辑，（其实按照协议完整性，很多地方需要加上这一校验逻辑）如下所示

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404705.png)



###### request_type.Type（D6~D5）

Type字段表示请求类型： 标准请求，类请求，厂商请求三种

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404073.png)

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404290.png)

###### request_type.Recipient (D4~D0)

- 详细内容请查看文档《USB3.0spec中文译本.pdf》第9.4章节

- Recipient字段，表示HOST该次请求的设定的接受者，可以是： 设备，接口，端点，未定义

- 不同的接受者，setup包中wValue,wIndex等含义也不一样比，如当接受者是端点时，wIndex的低字节表示希望获取哪个端点的信息

- 不同接收者，对相同的bRequest请求，设备的回复的数据含义是不一样的，表示的指定接受者的当前状态

- 当接受者是端点时:CLEAR_FEATURE,GET_STATUS,SET_FEATURE这三个请求需要处理（bmRequestType.Recipient为00010）
- 当接受者是接口时:CLEAR_FEATURE, GET_STATUS,SET_FEATURE这三个请求需要处理（bmRequestType.Recipient为00001）



![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404914.png)

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404691.png)

 ​	![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404473.png)



##### bRequest

不同的请求类型（request_type.Typez字段 标准请求，设备类请求，厂商请求），bRequest可表示的值也不一样

###### 标准设备请求

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404729.png)



###### 设备类请求

- audio mic, audio_speaker 设备

  ```c
  #define USB_REQ_GET_INTERFACE           0x0A
  #define USB_REQ_SET_INTERFACE           0x0B
  ```

- CDC 设备

  ```C
  #define CDC_SET_LINE_CODING             0x20
  #define CDC_GET_LINE_CODING             0x21
  #define CDC_SET_CONTROL_LINE_STATE      0x22
  ....其他并不常用
  ```

- HID 设备

  ```
  #define USB_REQ_GET_DESCRIPTOR      0x06	// 设备类中也可能有标准设备类的一些请求
  #define USB_HID_REQ_GET_REPORT      0x01
  #define USB_HID_REQ_GET_IDLE        0x02
  #define USB_HID_REQ_GET_PROTOCOL    0x03
  #define USB_HID_REQ_SET_REPORT      0x09
  #define USB_HID_REQ_SET_IDLE        0x0a
  #define USB_HID_REQ_SET_PROTOCOL    0x0b
  ```

- STORAGE 存储类设备

  ```c
  #define USBREQ_GET_MAX_LUN              0xfe
  #define USBREQ_MASS_STORAGE_RESET       0xff
  ```

  

- 其他，暂不一一列举



###### 厂商设备请求

目前，从rt-thread usb驱动代码看，bRequest字段需要是字母`A`



## EP0 DATA阶段

如果在SETPUP阶段，请求包的方向为IN方向，即DEVICE->HOST，那么接下来的阶段则为DATA IN阶段，最后是OUT STATUS阶段，反之，如果请求包方向为OUT方向，即HOST->DEVICE,那么接下来的阶段则为DATA OUT阶段，最后为IN STATUS阶段

### DATA IN 阶段

HOST发送了IN方向请求，DEVICE给HOST回复请求的阶段，称之为DATA IN阶段，一般就是解析了请求后，调用`rt_usbd_ep0_write`给PC回复数据。



### DATA OUT 阶段

HOST发送了OUT方向的请求，且OUT的数据内容不存在于SETUP packet中，需要额外使用EP0发送DATA packet，那么就必须有一个DATA OUT阶段，一般调用`rt_usbd_ep0_out_handler`函数进行EP0数据的OUT

注意一下，一般情况下，一个Transfer中有3个Transtraction,但是，如果HOST发送了OUT方向数据请求，且OUT数据的内容，存在于setup的8个字节命令中，那么，第二个阶段的DATA OUT阶段就不存在了，只有IN STATUS阶段，典型的比如set address请求

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202108291404647.png)





## STATUS 阶段

所有PC的请求，都有一个status stage，用来作为最后一个确认的transaction

### OUT STATUS阶段

当第二个transtracion为 IN data 阶段，那么这个status阶段就是out status阶段

## IN STATUS 阶段

当第二个transtracion为 OUT data 阶段，那么这个status阶段就是in status阶段



## EPx数据传输

枚举阶段使用的是EP0端口进行枚举的，当枚举完成后，需要进行数据的传输，则需要使用到EP1,EP2等，当收到`USB_MSG_DATA_NOTIFY`消息时，进行数据的输入输出



## SOF

收到HOST的SOF包请求

## RESET

当device复位时，执行

## 参考资料

- [《USB3.0spec中文译本.pdf》](https://gitee.com/chenyingchun0312/usb-doc)
- [《USB3.0官方协议规格书(英文版).pdf》](https://gitee.com/chenyingchun0312/usb-doc)
- 《rtthread-studio-usb-device.md》
- 《an0046-rtthread-driver-usbh.md》
- [**《USB培训_Part1_协议.pdf》**](https://gitee.com/chenyingchun0312/usb-doc)

