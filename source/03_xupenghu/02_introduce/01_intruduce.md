# STM32WB 硬件介绍
## 1 系统和存储
### 1.1 系统总览
STM32使用双核架构，一个cortex-m4核负责app程序开发，一个cortex-m0核负责射频协议栈，还有一个radio子系统负责RF部分。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930104503435.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 1.2 STM32WB总线架构
如下图所示，基本的外设都被CPU1域，也就是cortex-m4内核访问，CPU1和CPU2通过SRAM2通讯。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930104700362.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 1.3 总线矩阵
![](https://img-blog.csdnimg.cn/20200930105113141.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 1.4 存储分布
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930105157465.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 1.5 STM32WB闪存特点
- 共享
	- 闪存的一部分是为RF射频子系统CPU2保护的，为了安全区域，主机CPU1无法访问。
- 使用ART加速
	- 同时执行代码CM4和CM0+对MIPS的影响约为0%，在单独的AHB总线上，它有自己的时钟分频器。
- 3级保护
	- 级别0（无保护）至级别2（最大保护）
- 限制
	- 在射频活跃期间，flash擦除或存储不应该被启动。因为射频活跃期间cpu1会频繁读写flash。
## 2 RF射频简介
### 2.1 RF参数简介
- 模拟前端
	- 最大输出功率
		- 集成巴伦，6dbm发射功率，具有1dbm步进调节
		- 专用引脚驱动外部PA，可以获得最大20dbm的输出功率
	- 接收灵敏度
		- BLE：1Mbps @-96dbm， 2Mbps @-94dbm（250kbps和125kbps不支持）
		- 802.15.4：250kbps @ -100dbm
	- 功耗@3.3V
		- TX：@0dbm：5.2mA
		- RX:4.5mA
		- stop2 with radio in standy (accurate clock LS12):1.8uA
- 调制解调器
	- 通过硬件格式化BLE包（对软件完全开放射频）支持1和2Mbps速率
	- IEEE 802.15.4 ：硬件模式支持250Kbps通信速率
### 2.2 STM32WB典型外围电路
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930110652529.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 2.3 STM32WB RF输入/输出匹配网络
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930110754104.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
一个Π型滤波网络加50Ω阻抗匹配。
## 3 电源管理
### 3.1 供电方案框图
如下图所示，各个电源阈单独供电，在供电选择上有很大的灵活性。
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930111004948.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 3.2 内部SMPS
- SMPS用于降低VDD电源
- SMPS为数字核心和射频LDO供电
- 当VDD电源高于BOR[1..4]阈值时，使用SMPS模式
	- 低于此阈值使用旁路模式，支持及时切换
	- 通过HW机制执行关闭，通过SW重新开启
- SMPS降遵循社保操作模式
	- 在Run和stop0模式下为On
	- 在stop1 2 待机standby和关机shutdown模式下，SMPS自动处于开放模式，唤醒时自动恢复进入前使用模式
### 3.3 电源配置
- 高性能使用SMPS
	- 通过添加外部电容和线圈，SMPS用于降低功耗
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930112611960.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
- 低成本今适用于LDO
	- 通过短接SMPS输入。LDO直接由VDD提供节省电容和电感成本，但是功耗会增加。
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930112744994.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
### 3.4 SMPS原理图
![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930112824925.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)

## 4 核间通信和安全管理
### 4.1 HSEM
STM32WB集成硬件信号量模块，该模块用于同步进程和管理共享资源访问权限。具体如下。

- 管理和访问权限和同步
	- 运行于同一个cpu上的不同进程
	- 不同的cpu
- 32个硬件信号量
- 两种锁定机制
	- 2-step write， read back lock
	- 1-step read lock
- 信号量释放产生中断
- 应用优势
	- 防止共享资源访问冲突
	- 确保进程之间的同步
	- 无阻塞信号量处理

#### 4.1.1 HSEM框图
HSEM模块位于AHB总线上，由AHB接口和中断管理构成，每个CPU都有一个专用中断，并且都有自己的使能、状态、掩码和清除寄存器。每个信号量由两个寄存器组成，一个读写寄存器，用于在两步锁过程中对信号量进行写操作并读取信号量状态，它也可以释放信号量；另一个是读寄存器，它用于一步锁过程中的读取锁。
![框图](https://img-blog.csdnimg.cn/20200930141938212.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
<center>HSEM框图</center>

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930142349269.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
<center>2步 写-回读锁机制</center>

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930142506381.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
<center>1步 锁机制</center>

#### 4.1.2 信号量使用 - 共享资源
两个CPU可以同时访问的所有外设都受硬件信号量保护，在访问此类外设之前，应首先获取相关的信号量并在使用完之后释放。

Semaphore     | Purpose
-------- | -----
sem0  | RNG-All registers
sem1  | PKA-all registers
sem2  | Flash - All registers
sem3|  RCC_CR RCC_CRRCR RCC_EXTCFGR RCC_CFGR

#### 4.1.3 信号量 - 闪存写入和擦除
- 要在闪存种写入，应用程序应该
	* 获取Sem2
	* 写入闪存
	* 释放sem2

- 擦除扇区，应用程序应该
	- 获取Sem2
	- 发送SHCI_C2_FLASH_Erase_Actiity(erase_activity_ON)命令给CPU2
	- 擦除一个或多个扇区
	- 释放Sem2
	- 发送SHCI_C2_FLASH_Erase_Activity( erase_activity_OFF ) 命令给 CPU2

### 4.2 IPCC
IPCC是核间通讯控制模块，它可以提供中断信令，允许微控制器以非阻塞的方式交换信息。

- 为通信信道管理提供非阻塞信令
	- 消息可用性中断
	- 流量开启中断通知
- 通讯方式
	- 单工：每个方向的专用通道
	- 半双工：单个共享双向通道
- 最多6个双向通道
	- 通道数据存储在共享ram中
- 应用优势
	- 非阻塞信息交换
	- 通道流量控制
	- 支持CPU sleep和stop模式
	
	![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930145138448.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)

### 4.3 安全管理
- BLE外设可以安全使用以下外设
	- AES1（仅限IP加密密钥）用于应用程序的加密引擎
	- AES2（Full IP）用于IEEE802.15.4的加密引擎
	- PKA（Full IP）用于加密密钥的生成
	- True RNG（Full IP）用于加密密钥的生成
- 对安全IP的访问由HSEM管理
	- HSEM x,y,z用于管理共享安全外围设备访问
- BLE堆栈提供以下加密密钥功能
	- 密钥存储
	- 密钥更新
	- 密钥删除
	- 密钥加载（在AES1中）

### 4.4 Cortex-M0+安全性
- 闪存的上半部分只能由cortex-m0+访问
	- 由安全选项字SFD和SFSA定义
- 全局安全使能
	- 允许通过安全选项字SBRD和SBRSA来添加SRAM2a上的部分安全性
	- 允许通过安全选项字SNBRD和SNBRSA来添加SRAM2b闪的部分安全性
	- 运行通过SYSCFG使能外设的安全性

![在这里插入图片描述](https://img-blog.csdnimg.cn/20200930150204374.png?x-oss-process=image/watermark,type_ZmFuZ3poZW5naGVpdGk,shadow_10,text_aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3UwMTQ0MjE1MjA=,size_16,color_FFFFFF,t_70#pic_center)
