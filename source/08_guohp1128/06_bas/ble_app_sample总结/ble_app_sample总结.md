# ble_app_sample总结



## 1 ble_app_sample是什么

​		ble_app_sample是nordic nrf5x系列芯片从设备（Slave）的蓝牙服务例程，例如电池服务、心率服务等。该例程包含在RT-Thread的nrf5x_sdk软件包中，可以很方便的加载到RTT工程中运行。该例程使用的蓝牙协议栈是Nordic softdevice s140。

## 2 ble_app_sample如何使用

​		一般直接使用nrf5x的RT-Thread工程模板。

​		工程中加载例程可以使用RTT的ENV工具，也可以使用RT-Thread Studio配置工程。配置完后例程会自动加载到工程之中。

​		下面以ENV工具配置ble_app_blinky服务为例说明。

### 2.1 试验板

​		以nrf52840开发板试验。如下图：

![](image/20201011183341.jpg)

### 2.2 程序配置设置

- 下载RT-Thread的nrf52840 BSP工程模板，下载地址是 https://github.com/RT-Thread/rt-thread

- 下载并安装RT-Thread 开发辅助工具Env。参考RTT安装介绍，下载地址 https://www.rt-thread.org/page/download.html

- 进入nrf52840工程文件夹

  \rt-thread\bsp\nrf5x\nrf52840

  ![](image/1602414008006.png)

  

- 打开env配置工具

  在工程中右击选择ConEmu Here

  ![1602414635016](image/1602414635016.png)

  

- 然后弹出如下界面

   ![1602414731322](image/1602414731322.png)

  

- 输入menuconfig弹出如下界面

    ![1602414840083](image/1602414840083.png)

  

- 使用方向键选择配置UART和GPIO

   ![1602415188693](image/1602415188693.png)



​		![1602415356435](image/1602415356435.png)



![1602416377390](image/1602416377390.png)



在Enable UART中可以选择UART0或者UART1，可以配置rx和tx的引脚编号。此开发板选择默认。

![1602415971201](image/1602415971201.png)



- 配置ble协议栈

    ![1602416110142](image/1602416110142.png)



![1602416513402](image/1602416513402.png)



- 配置nrfx和nrf5x_sdk软件包

   ![1602416646372](image/1602416646372.png)



​		![1602416691268](image/1602416691268.png)



![1602416784531](image/1602416784531.png)



在nrf5x_sdk中选择ble_app_blinky应用例程

![1602417315424](image/1602417315424.png)

ble_app_blinky例程中可以配置应用使用的引脚编号（要与开发板对应），此开发板选择默认值。引脚编号是rtt驱动层drv_gpio.c对nrf5x芯片定义的引脚编号。从1-47依次对应gpio端口0的32个引脚和gpio端口1的16个引脚。

### 2.3 配置编译

按Esc退到该界面

![1602416971612](image/1602416971612.png)



选择yes保存，出现如下界面

![1602417099315](image/1602417099315.png)

输入scons --target=mdk5回车编译工程，因为使用mdk5开发环境，也可以根据具体环境选择mdk4或者iar等。

编译需要一段时间，完成后退出env工具。

### 2.4 编译下载程序

打开项目中的工程文件

![](image/1602513252474.png)



编译工程

![](image/1602513620018.png)



连接开发板，选择softdevice，下载程序

![](image/1602513747416.png)



选择rtthread，下载程序

![](image/1602513851980.png)



打开串口调试助手，首次启动运行出现如下信息

![1602514582172](image/1602514582172.png)



输入help，按压回车，出现如下信息

![1602514666270](image/1602514666270.png)



输入ble_app_blinky，启动ble_app_blinky应用例程。开发板的广播指示灯亮。

![1602514860424](image/1602514860424.png)



### 2.5 手机连接验证

手机端下载nRF Connect工具。下载地址是



https://www.nordicsemi.com/Software-and-tools/Development-Tools/nRF-Connect-for-mobile

![1602515417544](image/1602515417544.png)



打开手机蓝牙功能，打开该app，搜索到Nordic_Blinky。

![1602515696197](image/1602515696197.png)



点击CONNECT，连接并打开按钮和LED服务

![1602516049884](image/1602516049884.png)



按照下面操作，可蓝牙无线控制开发板。

![1602516464739](image/1602516464739.png)



## 3 添加新的ble_app_sample

​		ble_app_bas是电池服务例程，下面以ble_app_bas为例介绍添加过程。

### 3.1 编写ble_app_bas.c源文件

​		在软件包nrf5x_sdk中创建ble_app_bas.c文件，保存路径是\nrf5x_sdk\rtt_adapter。如下图：

![1606623889936](image/1606623889936.png)

​		

​		ble_app_bas.c是例程的主体文件。主要实现的内容包括：

- 创建RTT任务（例程是单独的一个任务）
- 相关芯片外设的初始化
- 蓝牙协议栈初始化
- GAP初始化
- GATT初始化
- 服务初始化（服务实现例程的功能）
- 连接参数初始化
- 广播功能初始化，并启动广播



## 3.2 添加工程配置的Kconfig

​		nrf5x_sdk软件包是依靠RTT的env工具配置（RT-Thread Studio最终也是依赖env），所以需要在env对应的包配置Kconfig文件中添加配置语句。方法看RTT文档中Kconfig基本语法。

​		Kconfig文件的路径是env\packages\peripherals\nrf5x_sdk。配置语句内容如下：

![1606657568831](image/1606657568831.png)

​		语句层级关系属于if PKG_USING_NRF5X_SDK下一级，又choice的下一级。



### 3.3 添加文件加载的脚本

​		生成工程的时候，该脚本将依赖的.c文件、.h文件加载到工程中。脚本位置是\nrf5x_sdk中的Sconscript。如图：

![1606626624105](image/1606626624105.png)

​		

​		脚本中需要添加ble_app_bas.c主体文件下载路径。还有电池服务依赖的ble_bas.c文件下载路径、头文件ble_bas.h的路径。代码如下：

![1606626847968](image/1606626847968.png)



### 3.4 向github仓库提交写好的例程

- 把例程主体文件ble_app_bas.c和加载的脚本Sconscript文件提交到nrf5x_sdk软件包的GitHub仓库。

  仓库地址是https://github.com/supperthomas/nrf5x_sdk

- 把Kconfig文件提交到env软件包配置仓库。

  仓库地址是https://github.com/RT-Thread/packages








