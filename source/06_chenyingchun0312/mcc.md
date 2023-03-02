# 多核系统

## 参考资料

[1] https://elinux.org/images/3/3b/NOVAK_CERVENKA.pdf

[2] https://github.com/OpenAMP/open-amp/wiki/AMP-Intro

[3] https://github.com/NXPmicro/rpmsg-lite

[4] https://github.com/torvalds/linux/tree/master/drivers/rpmsg

[5] C:\Keil_v5\ARM\PACK\ARM\AMP\1.1.0

## 多核处理器

### 从硬件架构区分

- 同构多核：某一个芯片中的多个CPU的架构是相同的，比如都是CM3
- 异构多核：某一个芯片中的多个CPU的架构是不同的，比如一个是CM3，一个是RISC-V
- 异构多核处理器有：TI的达芬奇平台DM6000系列（ARM9+DSP）、Xilinx的Zynq7000系列（双核Cortex-A9+FPGA）
- 同构多核处理器有：Exynos4412，freescale i.mx6 dual和quad系列、TI的OMAP4460等

### 从运行的软件模式区分

- AMP（非对称多处理）

- SMP（对称多处理）

  


## AMP和SMP介绍

- `AMP`全称`asymmetric Muti-processing`，翻译为`不对称多核处理器`（具体是指什么不对称呢？）

- `SMP`全称`symmetric Muti-processing`，翻译为`对称多核处理器`（具体是指什么对称呢？）

- 一个多核芯片，假设有A核和B核，如果A和B共享很多外设资源，包括内存资源，软件开发的模型，一般使用`SMP`，反之，如果A核和B核具有独立的外设和内存资源，一般使用`AMP`

- `AMP`模式是指，在每个CPU核上单独运行程序，比如，A核上运行了一个`UCOS`操作系统，B核上运行了一个裸机程序

- `SMP`模式是指，在所有CPU核中运行同一套软件，所有CPU的地位相同

- `AMP` 虽然多个核心可以运行不同的系统，但是**需要有一个主要的核心**，需要使用该核心来控制整个系统以及其他的核心。例如：一个核心运行运行实时性较高的任务，另一个核心运行UI界面。

  ![image-20230125125525700](figures/image-20230125125525700.png)



## 开源AMP框架

- [OpenAMP](https://github.com/OpenAMP/open-amp)
- [RPMsg-Lite说明文档](https://nxp-mcuxpresso.github.io/rpmsg-lite/)
- [RPMsg-Lite代码](https://github.com/nxp-mcuxpresso/rpmsg-lite)





## OpenAMP介绍

`OpenAMP`解决了什么问题？

- 在具有多个处理器的系统中，会面临一系列难题，比如
  - 内存怎么分配？
  - 系统资源怎么分配？
  - 处理器之间的数据怎么交换？

![image-20230125165532097](figures/image-20230125165532097.png)



![image-20230126214146617](figures/image-20230126214146617.png)



![image-20230126214533428](figures/image-20230126214533428.png)

## OpenAMP组件

`OpenAMP`为AMP系统开发应用程序提供了三个重要组件： `Virtio`, `RPMsg`和`Remoteproc`



### 虚拟化模块 `Virtio`

`Virtio`是一个管理共享内存的模块，`Virtio`中的`vring`是一个FIFO，FIFO中的每一个元素都是一个数据指针，有两个单向的`vring`，一个专门用于发送数据到远程处理器的消息；另一个`vring`用于保存从远程处理器接收到的消息，两个`vring`组成了一个环形



![image-20230125162321570](figures/image-20230125162321570.png)



### 远程处理器消息传递 `RPMsg`

![image-20230125162359663](figures/image-20230125162359663.png)

- 位于Mailbox框架上层的是`Remoteproc 远程处理框架`
- RPMsg框架基于Virtio的vrings，基于vrings发送和接受消息
- `RPMsg`实际上是一种基于`Virtio`的消息总线，用于实现的是核间消息传递（传递核间数据），可以认为`RPMsg`是一个与远程处理器通信的通道，这个通道，我们也可以称它为RPMsg设备，每个通道都有一个本地源地址和远程处理器的目标地址，消息就可以在源地址和目标地址之间进行传输
- ![image-20230125163225767](figures/image-20230125163225767.png)
- ![image-20230125163316431](figures/image-20230125163316431.png)

### 远程处理 `Remoteproc`

对于非堆成多核处理器的SOC，不同的核心可能跑不通的操作系统，比如，STM32MP157的Cortex-A7运行linux操作系统，Cortex-M4运行RT-Thread或者裸机程序，为了使运行Linux的主处理器与协处理器之间能够轻松通信，在Linux3.4.x版本以后，引入了Remoteproc核间通信框架，该框架由TI公司开发，在此基础上，mentor graphics公司开发了一种软件框架OpenAMP, 在这个框架下，主处理器上的linux操作系统可以对远程处理器及其相关软件环境进行生命周期管理，即启动，或者关闭远程处理器

![image-20230125163814969](figures/image-20230125163814969.png)

![image-20230125163858988](figures/image-20230125163858988.png)

![image-20230125164008631](figures/image-20230125164008631.png)

![image-20230125164234725](figures/image-20230125164234725.png)



## Linux驱动文件介绍

![image-20230125164352349](figures/image-20230125164352349.png)

![image-20230125164822093](figures/image-20230125164822093.png)

![image-20230125164858870](figures/image-20230125164858870.png)

![image-20230125164905825](figures/image-20230125164905825.png)



## OpenAMP源码介绍

![image-20230125165138610](figures/image-20230125165138610.png)

![image-20230125165441405](figures/image-20230125165441405.png)

![image-20230125165450353](figures/image-20230125165450353.png)



## 基于RPMsg实现异核通信



## RPMsg



![image-20230129164205848](figures/image-20230129164205848.png)

![image-20230126220659939](figures/image-20230126220659939.png)



![image-20230130135124554](figures/image-20230130135124554.png)

- 核A调用 `rpmsg_lite_send`接口，将A核应用数据拷贝到共享内存中，再IPI中断通知核B，核B接收它，将共享内存数据直接暴露给应用程序，应用程序负责调用rpmsg_queue_nocopy_free函数来释放接收到的数据。







### RPMsg Channel 

RPMsg组件中的每个远程核心都由RPMsg设备表示，该设备提供了主设备和远程设备之间的通信信道，因此RPMsg设备也被称为信道。RPMsg通道由通道名称和本地（源）和目标地址标识。RPMsg框架使用通道的名称来跟踪通道。



### RPMsg Endpoints

RPMsg端点在RPMsg通道之上提供逻辑连接。它允许用户在同一通道上绑定多个rx回调。每个RPMsg端点都有一个唯一的src地址和关联的回调函数。当应用程序创建具有本地地址的端点时，所有目标地址等于端点的本地地址的进一步入站消息将被路由到该回调函数。每个通道都有一个默认端点，使应用程序能够在不创建新端点的情况下进行通信。

### RPMsg Header

![image-20230126221601510](figures/image-20230126221601510.png)

![image-20230126221546779](figures/image-20230126221546779.png)

#### RPMsg Framework

![image-20230126221847276](figures/image-20230126221847276.png)





## Linux RPMsg

![image-20230128110329934](figures/image-20230128110329934.png)

![image-20230128110320375](figures/image-20230128110320375.png)

![image-20230128110307817](figures/image-20230128110307817.png)

![image-20230128110653148](figures/image-20230128110653148.png)

![image-20230128110739033](figures/image-20230128110739033.png)

![image-20230128110758787](figures/image-20230128110758787.png)

![image-20230128110928257](figures/image-20230128110928257.png)

![image-20230128111105579](figures/image-20230128111105579.png)



## RPMsg-Lite

![image-20230128111218065](figures/image-20230128111218065.png)



![image-20230128111311040](figures/image-20230128111311040.png)







## RPMsg-Lite API



## VIRTIO

[Virtio:一个 I/O 虚拟化框架](https://blog.csdn.net/Rong_Toa/article/details/115266114#t6)



![image-20230129181848430](figures/image-20230129181848430.png)



[图形化解释](https://zhuanlan.zhihu.com/p/68154666)

![image-20230129182625454](figures/image-20230129182625454.png)



[参考文档](https://www.ozlabs.org/~rusty/virtio-spec/virtio-paper.pdf)



![image-20230129184509139](figures/image-20230129184509139.png)

![image-20230129184537052](figures/image-20230129184537052.png)



![image-20230129184839862](figures/image-20230129184839862.png)









![image-20230129191712067](figures/image-20230129191712067.png)

## FreeRTOS AMP

[freertos amp](https://www.freertos.org/zh-cn-cmn-s/2020/02/simple-multicore-core-to-core-communication-using-freertos-message-buffers.html)

