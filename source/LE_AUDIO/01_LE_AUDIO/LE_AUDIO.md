# LE AUDIO Call

[TOC]

## 简介

Note:这篇文章主要涉及到LE AUDIO 的unicast的传输，不涉及到broadcast传输。

### 什么是LE AUDIO?

![image-20241207175347124](figure/LE_AUDIO/image-20241207175347124.png)

LE Audio（Low Energy Audio）是新一代蓝牙音频技术标准，它基于低功耗蓝牙（Bluetooth Low Energy, BLE）无线通信技术，旨在提升蓝牙音频的性能，并引入新的音频应用场景。以下是LE Audio的一些关键特点：

1. **全新架构**：LE Audio为支持音频应用的蓝牙技术引入了全新的架构，为未来20年的无线音频创新奠定基础。
2. **超低功耗**：LE Audio利用BLE的优势，特别适用于需要低功耗的音频设备，如助听器等。
3. **高音质、低功耗音频解码器LC3**：LE Audio包含一个新的音频编解码器LC3（Low Complexity Communications Codec），它在低比特率下提供高质量的音频，同时降低功耗。
4. **LE同步通道（LE Isochronous Channels）**：LE Audio支持同步音频流，这对于减少延迟和提高音质非常重要。
5. **多重串流音频（Multi-Stream Audio）**：LE Audio支持多个音频流的传输，允许多个设备共享同一音频源。
6. **广播音频技术（Broadcast Audio）**：LE Audio引入了Auracast™广播音频功能，允许单个音频源向无限数量的接收设备广播音频流。
7. **助听器支持**：LE Audio增强了对助听器的支持，使得助听器用户可以更便捷地使用蓝牙音频。
8. **兼容性**：LE Audio产品可以支持Classic Audio和LE Audio，但不是所有Classic Audio设备都能与LE Audio源设备兼容。
9. **灵活性**：LC3编解码器为开发者提供了在音质和功耗之间做出更好权衡的灵活性。

LE Audio通过这些特点，为用户提供了享受和分享无线音频的新方式，并有望再次改变我们体验音频和与周围世界连接的方式.

### LE AUDIO 有哪些优势

LE AUDIO 主打低功耗和超低的延时， 目前主流的TWS耳机延时普遍在200ms左右，只有几家高端的私有协议可以做到比较低的100ms的延时，还是能让用户感知到，而且之前的A2DP设计上并没有支持TWS这种模式的SPEC。所以对于多重串流的播放 各家标准不一致。目前LE AUDIO的普遍延时可以做到50ms，几乎用户感知不到延时，有的可以做到比线控还要低的20ms延时（加DONGLE)。

### 哪些手机支持le audio

标称LC3解码和Auracast的，都是可以支持LE AUDIO的。

三星flip5以上系列，三星 s24系列，三星 a55系列

 google pixel 7 以上系列

#### REDMI K80 PRO & K70 系列

https://www.mi.com/prod/redmi-k80/specs

![image-20241207181637204](figure/LE_AUDIO/image-20241207181637204.png)

#### XIAOMI 15旗舰

![image-20241207181800154](figure/LE_AUDIO/image-20241207181800154.png)

### 哪些耳机支持LE AUDIO

##### REDMI BUDS 6 PRO & redmi buds 5 pro

https://www.mi.com/prod/redmi-buds-6-pro

![image-20241207182243459](figure/LE_AUDIO/image-20241207182243459.png)

三星galaxy buds3 https://item.jd.com/100127183384.html 支持LE AUDIO
vivoTWS 4 Hi-Fi https://item.jd.com/100104242270.html#crumb-wrap 支持LE AUDIO

索尼（SONY）INZONE Buds https://item.jd.com/100070911747.html 

![image-20241207182934620](figure/LE_AUDIO/image-20241207182934620.png)

### 什么是LE AUDIO call？

LE AUDIO call是指使用低功耗蓝牙（Bluetooth Low Energy，简称LE）技术进行的音频通话。LE AUDIO是蓝牙技术联盟（Bluetooth SIG）提出的一种新的蓝牙音频标准，旨在提供更高质量的音频体验，并且支持更复杂的音频场景，比如多人音频会议、助听器支持等。

在LE AUDIO call中，涉及到的关键技术和服务包括：

1. **BAP（Basic Audio Profile）**：基本音频配置文件，定义了如何使用低功耗蓝牙进行音频分发和接收。
2. **PACS（Published Audio Capabilities Service）**：发布音频功能服务，公开服务器音频功能和音频可用性，允许客户端进行发现。
3. **ASCS（Audio Stream Control Service）**：音频流控制服务，为音频流端点（ASE）提供接口，使客户端能够发现、配置、建立和控制ASE及其相关的单播音频流。
4. **CCP（Call Control Profile）**：电话控制配置文件，定义了用于与实现通用电话承载服务（GTBS）以及可选的和附加的电话承载服务（TBS）的远程设备交互的角色和过程。
5. **TBS（Telephone Bearer Service）**：电话承载服务，为可以拨打和接听电话的设备上的承载者提供电话呼叫控制接口和电话呼叫控制状态。
6. **MCP（Media Control Profile）**：媒体控制配置文件，使客户端能够控制服务端设备上的媒体播放器并与之交互。
7. **TMAP（Telephony and Media Audio Profile）**：电话和媒体音频配置文件，定义了一组蓝牙功能，通过指定较低级别音频服务和配置文件的可互操作配置来启用这些功能。

LE AUDIO call通过这些服务和配置文件，使得蓝牙设备能够进行音频通话，同时保持低功耗和高质量的音频传输。

本文主要针对LE AUDIO的profile和service，将打电话的整个流程讲下，将需要用到的profile和service串讲起来。

涉及到的Profile是： TMAP, CAP,BAP,MCP, CCP, CSIP, VCP

涉及到的service是： PACS, ASCS, MCS, TBS, CSIS, VSC, VOCS, AICS

![image-20241207175159217](figure/LE_AUDIO/image-20241207175159217.png)

**不包含ASCS的，不支持单播；**

**不包含BASS的，不支持广播；**

 **不包含BAP和PACS的，根本没法用！**

### 前提知识

PACS、ASCS等Service均是基于Bluetooth Core中的GATT协议。GATT定义两个 BLE 设备通过叫做 Service 和 Characteristic 的东西进行通信。GATT起作用前，需要两个蓝牙设备先建立连接。作为GATT-Server的设备中会存在相应的Service，作为GATT-Client的设备可以通过Service中的定义特征与行为对Server设备中的数据进行修改。

后缀为S的是service，同时会对应拥有对应后缀为P的就是Profile。

BAP、MCP、CCP、CSIP、MICP、VCP等配置文件定义了如何使用相关Service实现一些基础功能，如：单纯的音频数据传输功能、单纯的媒体控制功能等。

Service的pdf里面定义了service的表，Profile里面定义了如何操作这些service中的Characteristic.

CAP定义了如何将这些功能结合起来实现基础场景。

TMAP、HAP定义了如何结合这些功能实现一些具体用例。例如：TMAP可以将BAP与CCP等结合起来，实现通话场景；CCP定义了如何拨打电话、接听电话、挂断电话等；BAP定义了如何发送音频数据、接收音频数据等；TMAP定义首先通过CCP的定义拨打电话，接通后，再通过BAP的定义发送和接收音频数据，完成一个完整的用例。

**Service**：服务是完成特定功能或特性的数据和相关行为的集合。在GATT中，服务是由其服务定义来定义的。服务定义可能包含的服务、强制特征和可选特征。例如，电量信息服务、系统信息服务等，每个service中又包含多个characteristic特征值。

每个具体的characteristic特征值才是BLE通信的主题。比如当前的电量是80%，所以会通过电量的characteristic特征值存在从机的profile里，这样主机就可以通过这个characteristic来读取80%这个数据。

**Profile**：规范是蓝牙对应于每一个具体的应用场景以及每一种应用的不同的协议栈，也就是说它其实是实现某种功能对应的自下而上的协议的组合。类似于对于横向协议的纵向组合。例如，BAP（基本音频配置文件）定义了PACS(发布音频功能服务)和ASCS(音频流控制服务)如何组合使用实现单播功能；以及PACS(发布音频功能服务)和BASS(广播音频扫描服务)如何组合使用实现广播功能。

### 角色定义

#### BAP单播角色定义如下：



| **角色**       | **中文名称** | **功能**                                                     |
| -------------- | ------------ | ------------------------------------------------------------ |
| Unicast Server | 单播服务端   | 1. 发送一种广播使单播客户端可以发现服务端并建立连接。2.暴露一些属性使单播客户端可以知道服务端支持的音频能力3.暴露一些属性使客户端可以配置和控制服务端上的ASE4.暴露当前接收和传送的音频流的可行性5.支持建立CIG,CIS来传输音频流 |
| Unicase Client | 单播客户端   | 1.扫描服务端相关的广播2.发现服务端相关能力                   |

#### 广播角色定义如下：

| **角色**            | **中文名称** | **功能**                                                     |
| ------------------- | ------------ | ------------------------------------------------------------ |
| Broadcast Source    | 广播源       | 1.建立BIG,BIS等传输广播音频流2.发送描述广播音频流配置的数据3.发送能让其他设备发现和接收广播音频流的数据 |
| Broadcast Sink      | 广播接收者   | 1.发现Source发送的相关数据2.暴露音频相关能力                 |
| Broadcast Assistant | 广播助手     | 1.发现Sink音频相关能力2. 发现Source发送的相关数据3.与Scan Delegator相连接，帮助其扫描广播源，将扫描到的信息传输给Delegator，对Delegator发送执行同步音频流等命令 |
| Scan Delegator      | 扫描委托者   | 1.委托Assistant协助扫描                                      |

![image-20241207180328526](figure/LE_AUDIO/image-20241207180328526.png)

#### MCP角色定义如下：

| **角色**             | **中文名称**   | **功能**                                                     |
| -------------------- | -------------- | ------------------------------------------------------------ |
| Media Control Server | 媒体控制服务端 | 暴露媒体控制服务与媒体控制客户端交互以管理媒体，并将各种状态和设置传送到媒体控制客户端 |
| Media Control Client | 媒体控制客户端 | 启动播放和暂停，确定播放顺序等，并收集搜索来自媒体控制服务器的结果。 |

![image-20241207180432629](figure/LE_AUDIO/image-20241207180432629.png)

####  CCP角色定义如下：

| **角色**            | **中文名称**   | **功能**                                                     |
| ------------------- | -------------- | ------------------------------------------------------------ |
| Call Control Server | 电话控制服务端 | 位于可以处理一个或多个电话呼叫承载器上的呼叫的设备（如手机或平板电脑）上 |
| Call Control Client | 电话控制客户端 | 可以向服务器发出请求以拨打、接听和管理呼叫支持呼叫控制客户端的设备包括带有麦克风的耳机和扬声器，或手表等可能没有扬声器或麦克风但可以管理电话呼叫的设备。 |

![image-20241207180559826](figure/LE_AUDIO/image-20241207180559826.png)

#### CSIP角色定义如下：

| **角色**        | **中文名称** | **功能**                                                     | **举例**                                                     |
| --------------- | ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Set Member      | 协调组成员   | 作为协调组的一部分，和其他成员作为一个组、集合成员角色共享公共集合标识信息并参与协作 | 一对耳机可以作为一个协调组（Coordinated Set），每个耳机都作为协调组成员定义了相关数据能说明为一个协调组 |
| Set Coordinator | 协调组协调者 | 发现协调集合及其集合成员的，可以被授予对集合成员的独占访问权 | 手机连接到一只耳机后，可以通过相关数据发现属于同一协调组的另一只耳机 |



#### MICP角色定义如下：

| **角色**              | **中文名称** | **功能**       | **举例** |
| --------------------- | ------------ | -------------- | -------- |
| Microphone Device     | 麦克风设备   | 公开麦克风控件 | 耳机     |
| Microphone Controller | 麦克风控制者 | 可以控制麦克风 | 手机     |

 

#### VCP角色定义如下：

| **角色**          | **中文名称** | **功能**                                   |
| ----------------- | ------------ | ------------------------------------------ |
| Volume Renderer   | 音量变化者   | 接收一个或多个音频输入并显示对音频输出控制 |
| Volume Controller | 音量控制者   | 控制音频音量和相关状态                     |

 

#### CAP角色定义如下：

| **角色**  | **中文名称** | **功能**                                                     | **举例**                                                     |
| --------- | ------------ | ------------------------------------------------------------ | ------------------------------------------------------------ |
| Acceptor  | 接收者       | 1.BAP单播服务端的功能或者广播接受者和扫描委托者的功能2.VCP音量变化者的功能3.MICP麦克风设备的功能4.CSIP协调组成员的功能 | 耳机、助听器、麦克风、扬声器等                               |
| Initiator | 发起者       | 1.BAP单播客户端的功能或者广播源的功能，可选广播助手功能2.CCP电话控制服务端3.MCP媒体控制服务端4.CSIP协调组协调员的功能 | 手机、电脑、媒体播放器、电视等                               |
| Commander | 指挥官       | 1.CSIP协调组协调员的功能2.BAP广播助手或者扫描委托者或者3.VCP音量控制者4.CSIP协调组协调员 | 独立设备：用于调节助听器声音的遥控器等 同时作为发起者：用于调节助听器声音时的手机 |

#### TMAP角色定义如下：

| **角色**                      | **中文名称**   | **功能**                                                  | **举例**                       |
| ----------------------------- | -------------- | --------------------------------------------------------- | ------------------------------ |
| Call Gateway(CG)              | 电话网关       | 与电话网络设施相关CAP发起者、指挥者                       | 手机、电脑等                   |
| Call Terminal(CT)             | 电话终端       | CAP接收者                                                 | 耳机、扬声器、麦克风等         |
| Unicast Media Sender(UMS)     | 单播媒体发送端 | 在一个或多个单播音频流中发送媒体音频内容CAP发起者、指挥者 | 手机、电视、电脑、媒体播放器等 |
| Unicast Media Receiver(UMR)   | 单播媒体接收端 | 接收单播媒体音频数据CAP接收者                             | 耳机、扬声器、等               |
| Broadcast Media Sender(BMS)   | 广播媒体发送端 | 向无限数量的接收设备发送媒体音频内容CAP发起者、指挥者     | 手机、电视、电脑、媒体播放器等 |
| Broadcast Media Receiver(BMR) | 广播媒体接收端 | 接收广播媒体音频数据CAP接收者                             | 耳机、扬声器、手机等           |

实例：实现一次通话的过程可以是：

1. 手机CG（作为CallControl Server）自己接通电话/耳机CT（作为Call Control Client）通过手机上的TBS服务命令手机接通电话；

   这个时候耳机可以控制和知道在打电话

2. 手机CG（作为UnicastClient）对耳机CT（作为Unicast Server）通过耳机上的PACS、ASCS等服务进行音频流控制操作，控制耳机接收或传输音频数据；

   这个时候耳机不知道是否在打电话

3. 手机CG（作为CallControl Server）自己挂断电话/耳机CT（作为Call Control Client）通过手机上的TBS服务命令手机挂断电话。

   这个时候耳机可以知道在打电话

## 空口包分析

### GATT服务发现协议

GATT 服务发现阶段，可以看出手机和耳机各有哪些服务。

这边抓取了手机和耳机的HCI包和ellisys包。

 [ellisys_explain.btt](ref\ellisys_explain.btt) 

 [redmiK70_tws.btt](ref\redmiK70_tws.btt) 

 [BT_HCI_2024_1108_134415.cfa](ref\BT_HCI_2024_1108_134415.cfa) 

#### 耳机端重要的 characteristic

首先是手机搜寻耳机的ATT服务，根据这些数据可以整理出耳机的service如下：



![image-20241207183414668](figure/LE_AUDIO/image-20241207183414668.png)

primary service和second service

![image-20241113113543917](figure/LE_AUDIO/image-20241113113543917.png)

这里可以看到PACS, ASES, VCP, AICS, VOCS, CSIS, CAS, TMAS.

同时我们根据搜到的characristic，整理出对应的characristic

首先是PACS和ASE 服务，这里的charactristic

PACS: 代表audio的能力一些参数

ASE: 代表的是音频流，类似于经典蓝牙的A2DP

![image-20241113114028145](figure/LE_AUDIO/image-20241113114028145.png)

然后是VCS和CSIS和CAS

VCS: 音量控制

CSIS: 这个是用来组队使用的协调集

![image-20241113113903213](figure/LE_AUDIO/image-20241113113903213.png)

接下来是TMAS和额外的服务secondary service： AICS和VOSS

AISC: 是音频输入控制

VOSS: 是音量偏移控制



![image-20241113114239496](figure/LE_AUDIO/image-20241113114239496.png)

这里主要的几个服务

PACS: 这个代表该音响有哪些能力

ASCS: 这个是音响或者耳机的主要的音频流控制接口，开启音频流主要用该服务.



#### 手机端重要的characteristic

耳机也要搜索手机的服务，手机的服务主要有以下所示，重要的有MCS和TBS.

![image-20241113150311429](figure/LE_AUDIO/image-20241113150311429.png)

#### MCP- MCS

Media State和Media Control Point， 这两个是主要的

![image-20241113150422141](figure/LE_AUDIO/image-20241113150422141.png)

播放音乐之前，会发个playing的notification过来。

![image-20241113150557544](figure/LE_AUDIO/image-20241113150557544.png)

![image-20241113151318174](figure/LE_AUDIO/image-20241113151318174.png)

Media Control Point 是由耳机来控制的，主要在MCS中有介绍

![image-20241113151423586](figure/LE_AUDIO/image-20241113151423586.png)

status和opcode组队还有如下图的状态机。

![image-20241113151602403](figure/LE_AUDIO/image-20241113151602403.png)

#### CCP-TBS

同样的GTBS中两个重要的属性，Call State和Call control Point。

![image-20241113152739254](figure/LE_AUDIO/image-20241113152739254.png)

 TBS中有定义：

![image-20241113153116765](figure/LE_AUDIO/image-20241113153116765.png)



![image-20241113152947619](figure/LE_AUDIO/image-20241113152947619.png)

![image-20241113153109466](figure/LE_AUDIO/image-20241113153109466.png)

![image-20241113153139841](figure/LE_AUDIO/image-20241113153139841.png)

Call control Point

![image-20241113153207068](figure/LE_AUDIO/image-20241113153207068.png)

## 手机和耳机服务和角色

根据每个profile中的角色：

BAP:

![image-20241113161213302](figure/LE_AUDIO/image-20241113161213302.png)

MCP:

![image-20241113161232942](figure/LE_AUDIO/image-20241113161232942.png)

VCP:

![image-20241113161255324](figure/LE_AUDIO/image-20241113161255324.png)

![image-20241113161316385](figure/LE_AUDIO/image-20241113161316385.png)

![image-20241113161338800](figure/LE_AUDIO/image-20241113161338800.png)

![image-20241113161401982](figure/LE_AUDIO/image-20241113161401982.png)

![image-20241113161501967](figure/LE_AUDIO/image-20241113161501967.png)

![image-20241113161110962](figure/LE_AUDIO/image-20241113161110962.png)



## 流程分析

### 播放音乐流程

打电话和播放音乐的流程本质上是一样的，都是开流。

要理解开流，就要看BAP协议。

看看BAP中主要内容。

![image-20241113153434696](figure/LE_AUDIO/image-20241113153434696.png)

我们这次主要涉及的是单播，所以流程在BAP的第五章中。

LE AUDIO book中有一张图：

![image-20241113153742802](figure/LE_AUDIO/image-20241113153742802.png)



Control Point的opcode如下：

![image-20241113154119425](figure/LE_AUDIO/image-20241113154119425.png)

sate状态如下：



![image-20241113154111210](figure/LE_AUDIO/image-20241113154111210.png)

source 状态机

![image-20241113154208092](figure/LE_AUDIO/image-20241113154208092.png)

Sink 状态机

![image-20241113154213629](figure/LE_AUDIO/image-20241113154213629.png)

首先手机播放音乐的时候，手机回了一个Media State： Playing：

![image-20241113154322869](figure/LE_AUDIO/image-20241113154322869.png)

之后，手机来控制ASE control Point

1. Media State： Playing：
2. 手机配置ASE control Point 配置各种LC3参数，这里操作是config codec
3. 耳机返回success，并且Sink ASE 返回codec configured状态
4. 手机接着配置Qos, 操作码是Config Qos
5. 耳机返回success， Sink ASE返回状态Qos Configured
6. 手机接着配置Enable，操作，
7. 耳机返回succes， Sink ASE返回状态Enabling
8. 然后建立CIS链路
9. 然后耳机返回Receiver Start Ready opcode
10. 耳机返回状态处于Streaming状态。



![image-20241113155143446](figure/LE_AUDIO/image-20241113155143446.png)

![image-20241113155532750](figure/LE_AUDIO/image-20241113155532750.png)

![image-20241113155513668](figure/LE_AUDIO/image-20241113155513668.png)

![image-20241113155434409](figure/LE_AUDIO/image-20241113155434409.png)

### 打电话流程

打电话流程和播放音乐流程一样：

触发事件是call state 的alerting事件。

![image-20241113155634801](figure/LE_AUDIO/image-20241113155634801.png)

之后开始开流，这里开了两个流，一个是Sink ASE，另外一个是Source ASE。

![image-20241113155843402](figure/LE_AUDIO/image-20241113155843402.png)

这里的CIG ID是1， CIS ID是0

#### Codec configured



 ![image-20241113160447403](figure/LE_AUDIO/image-20241113160447403.png)

#### Qos

![image-20241113160640586](figure/LE_AUDIO/image-20241113160640586.png)

#### Enabling ASE and Setting up CISes

![image-20241113160714026](figure/LE_AUDIO/image-20241113160714026.png)

#### Starting streaming

![image-20241113160805889](figure/LE_AUDIO/image-20241113160805889.png)

#### Ending streaming



![image-20241113160933648](figure/LE_AUDIO/image-20241113160933648.png)

参考引用：

> 【科普】一文读懂LE Audio和LC3
> https://mp.weixin.qq.com/s/QavJvKNhwWjYv5eVWKlbtA

完整LC3规格下载地址：

https://www.bluetooth.com/specifications/le-audio/ 

> Introducing-Bluetooth-LE-Audio-book.pdf

史上最全LE Audio专业术语名词解释
https://mp.weixin.qq.com/s/p_ktcks6EGJ76siRrcazKQ

