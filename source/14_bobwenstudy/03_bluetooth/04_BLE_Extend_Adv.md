# 蓝牙Extend Adv说明

在蓝牙5.0 Spec之后引入了Extend Adv的一整套控制行为，相比以前简单清晰的BLE Adv，空口交互行为复杂很多，HCI Command也引入新的Command，参数也多了很多。本文重点对Extend Adv进行说明，关于LE Audio和AoA/AoD的概念暂不展开。

本文更多是概述性的讲解，让大家对Extend ADV有个总体认识。更详细的基本概念请大家看[Core Specification | Bluetooth® Technology Website](https://www.bluetooth.com/specifications/specs/core-specification-5-4/)，也可以看一些中文博主的讲解：如：[BLE_爱洋葱的博客-CSDN博客](https://blog.csdn.net/zhoutaopower/category_9083143.html)。

本文大多数图片截取自[蓝牙5.4-Core Spec](https://www.bluetooth.com/specifications/specs/core-specification-5-4/)。

## 优缺点概述

要理解Extend Adv，主要从需求来分析，其解决了Legacy ADV的一些痛点问题，大致如下：

| 痛点                   | Legacy                                                       | Extend                                                       |
| ---------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 广播长度               | 单笔包最大只能支持31字节，加上scan response也只有31+31=62字节 | 单笔包最大255字节，更多包可以通过AUX_CHAIN_IND连接。同时支持Scan Response机制 |
| 多广播                 | 同一时间只能支持一组ADV+SCAN_RSP的设置，要实现Mesh的多广播需求只能不断地开关广播 | 引入Advertising SID概念，可以同时开启多组不同配置的广播参数  |
| 发送功率配置           | 不支持独立配置广播发送功率                                   | 不同Advertising SID配置不同的发送功率                        |
| Sync通道               | 不支持                                                       | 支持periodic ADV（AUX_SYNC_IND），为LE Audio提供支持         |
| 独立Random Address配置 | 不支持                                                       | 可以独立生成Random Address                                   |
| Coded PHY              | 不支持                                                       | 支持特殊长距离需求，进入连接也是Coded PHY                    |
| Connect Req握手        | 不支持（容易Initial进入了，ADV未进入）                       | 需要回复Connect Res才进入，可靠性高一些                      |
| AoA/AoD                | 不支持                                                       | 支持CIS等特别字段                                            |
| 支持channel选择        | 只能37/38/39                                                 | primary是37/38/39是短数据，second channel可以选择data channel |
| 同广播更新数据区分     | 手机开启duplicate后更新数据无法上报                          | 可以通过Advertising DID更新                                  |

当然解决一些问题同时也引入了一些问题

| 引入问题              | Legacy                                              | Extend                                                       |
| --------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| 功耗更高              | 1. 只用37/38/39就行；2. 发完3个包就可以进deep sleep | 1. 37/38/39并不带数据包，需要再second channel才发有效数据；2. 一般需要等second channel发完后才进Deep Sleep |
| 业务逻辑复杂          | 简单清晰                                            | 复杂，一堆状态                                               |
| RAM/Code Size需求更多 | 广播总共31+31就可以了，代码也少                     | 单包最长255，还支持aux包，还有多ADV，RAM和Code Size需求倍增  |

由于其功耗更高，业务更复杂，大多数场景下还是用Legacy，Mesh场景用Extend也是使用其多Advertising Set的功能。









## 包类型

### HCI层定义的包类型

#### Legacy

可以通过**HCI_LE_Set_Advertising_Parameters**这个Command的Advertising_Type来定义。这个Command只支持定义Legacy的广播。

![image-20230729102719325](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729102719325.png)

![image-20230729102815505](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729102815505.png)

![image-20230729102846829](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729102846829.png)



#### Extend

可以通过**HCI_LE_Set_Extended_Advertising_Parameters[v1]**和**HCI_LE_Set_Extended_Advertising_Parameters[v2]**这两个Command来设置，通过**Advertising_Event_Properties**来设置广播类型。

![image-20230729103053285](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729103053285.png)

![image-20230729103251953](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729103251953.png)

![image-20230729103311130](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729103311130.png)



### LL层定义的包类型

空口交互的类型只有4bit，在**PDU Type**中定义。

![image-20230729101405638](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729101405638.png)

蓝牙5.0把广播信道抽象为两类，一种叫主广播信道(**Primary**)，工作在**37**,**38**,**39**三个信道中，蓝牙4.0的广播使用的都是主广播信道，另一种叫第二广播信道（**Secondary**），工作在**0–36**的Data信道中，这是蓝牙5.0新增的。

其实可以看出为了兼容考虑，在相同的主广播信道(**Primary**)，由于原本定义有限，Extend在主广播信道(**Primary**)的PDU Type使用了**ADV_EXT_IND**。

为考虑兼容性，在相同PDU Type下通过所在信道区分和具体行为来分。

需要注意的是，Extend实际通过**Common Extended Advertising Payload Format**来实现对应HCI Command包类型定义。

![image-20230729101835483](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729101835483.png)

![image-20230729101914552](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729101914552.png)



### 广播包定义和Event定义

#### Event定义

按照是否可以Scan、Connect和Direct，Spec定义了如下Advertising Event类型。

![image-20230729110957945](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729110957945.png)

这些事件类型对应的PDU Type和可交互的PDU如下图所示。

![image-20230729110859369](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729110859369.png)



#### Legacy ADV

这里按照**HCI_LE_Set_Extended_Advertising_Parameters** Command的**Advertising_Event_Properties**参数来划分各个包类型。

| Event                                        | PDU             | Connect-able | Scan-able | Direct | High Duty | legacy | Omit Addr | TxPower | Data |
| -------------------------------------------- | --------------- | ------------ | --------- | ------ | --------- | ------ | --------- | ------- | ---- |
| Connectable and Scannable Undirected         | ADV_IND         | ✓            | ✓         | -      | -         | ✓      | -         | -       | ✓    |
| Connectable Undirected                       | -               | -            | -         | -      | -         | -      | -         | -       | -    |
| Connectable Directed                         | ADV_DIRECT_IND  | ✓            | -         | ✓      | ※         | ✓      | -         | -       | -    |
| Non-Connectable and Non-Scannable Undirected | ADV_NONCONN_IND | -            | -         | -      | -         | ✓      | -         | -       | ✓    |
| Non-Connectable and Non-Scannable Directed   | -               | -            | -         | -      | -         | -      | -         | -       | -    |
| Scannable Undirected                         | ADV_SCAN_IND    | -            | ✓         | -      | -         | ✓      | -         | -       | ✓    |
| Scannable Directed                           | -               | -            | -         | -      | -         | -      | -         | -       | -    |

##### ADV_IND定义

![image-20230729113147515](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113147515.png)

##### ADV_DIRECT_IND定义

![image-20230729113157956](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113157956.png)

##### ADV_NONCONN_IND定义

![image-20230729113249399](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113249399.png)

##### ADV_SCAN_IND定义

![image-20230729113313529](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113313529.png)









#### Extend ADV

从上述描述可以看出，Extend ADV只用了主广播信道(**Primary**)的PDU Type使用了**ADV_EXT_IND**，具体是通过**Common Extended Advertising Payload Format**来实现对应HCI Command包类型定义。Extend ADV引入了Event的概念，通过**AdvMode**和**Extended**
**Header Flags**定义来划分不同Event。

Spec定义的如下，其实就是定义了一系列的Event Type，再根据HCI Command中定义的参数来区分，需要注意的是**ADV_EXT_IND**本身不带Adv Data，如果HCI Command中定义了Adv Data必须设置**ADI**和**Aux Ptr**，说明在第二广播信道（**Secondary**）会发送**AUX_ADV_IND**，数据会在这个包里发送。

**注意**，**ADV_EXT_IND**本身不带Adv Data！！！

| Event                                        | PDU                     | Connect-able | Scan-able | Direct | High Duty | legacy | Omit Addr | TxPower | Data |
| -------------------------------------------- | ----------------------- | ------------ | --------- | ------ | --------- | ------ | --------- | ------- | ---- |
| Connectable and Scannable Undirected         | -                       | -            | -         | -      | -         | -      | -         | -       | -    |
| Connectable Undirected                       | ADV_EXT_IND AUX_ADV_IND | ✓            | -         | -      | -         | -      | -         | -       | ※    |
| Connectable Directed                         | ADV_EXT_IND AUX_ADV_IND | ✓            | -         | ✓      | -         | -      | -         | -       | ※    |
| Non-Connectable and Non-Scannable Undirected | ADV_EXT_IND AUX_ADV_IND | -            | -         | -      | -         | -      | -         | -       | ※    |
| Non-Connectable and Non-Scannable Directed   | ADV_EXT_IND AUX_ADV_IND | -            | -         | ✓      | -         | -      | -         | -       | ※    |
| Scannable Undirected                         | ADV_EXT_IND AUX_ADV_IND | -            | ✓         | -      | -         | -      | -         | -       | -    |
| Scannable Directed                           | ADV_EXT_IND AUX_ADV_IND | -            | ✓         | ✓      | -         | -      | -         | -       | -    |







##### ADV_EXT_IND定义

![image-20230729105339358](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729105339358.png)



##### AUX_ADV_IND定义

![image-20230729110140966](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729110140966.png)

![image-20230729110158323](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729110158323.png)



#### Common Extended Advertising Payload Format定义

所有Extend ADV都是用该格式。也就是下面这些包类型。

![image-20230729113525367](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113525367.png)

帧格式如下所示。

![image-20230729113419405](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113419405.png)

##### AdvMode

其实就是connectable和scannable的排列组合，由于Extend不支持Connectionable and Scannable所以预留了1个值。

![image-20230729113700136](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729113700136.png)

##### Extend Header

只有**Extended Header Flags**定义了对应bit位，后续的对应的数据才会存在，数据顺序不变。

![image-20230729114140683](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729114140683.png)

###### Extended Header Flags

对应位设置，相应数据才会存在。

![image-20230729114321593](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729114321593.png)

###### AdvA field

自身的广播地址，地址类型在**TxAddr**中定义。

![image-20230729114419960](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729114419960.png)



###### TargetA field

目标的地址，地址类型在**RxAddr**中定义。

![image-20230729114545666](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729114545666.png)

###### CTEInfo field

AoA/AoD的东西。



###### AdvDataInfo field

最主要的SID，支持多广播设置。DID用于当前广播需要更新Data的场景（常用于传感器之类的广播数据更新，不然手机一般打开了duplicate）。

![image-20230729115122523](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729115122523.png)





###### AuxPtr field

可以配置Aux包的交互信道由**Channel Index**决定；交互时间点由 **Offset Units**和**AUX Offset**共同决定；交互的PHY由**AUX PHY**决定；**CA**用于定义时钟精度，便于长时间的时候不确定窗口开多大。

![image-20230729115907889](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729115907889.png)



![image-20230729120223359](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729120223359.png)





###### SyncInfo field

用于Periodic Adv场景，定义了AUX_SYNC_IND PDUs or AUX_SYNC_SUBEVENT_IND PDUs的信息。

![image-20230729120454042](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729120454042.png)

![image-20230729123559751](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729123559751.png)





###### TxPower field

指示当前包实际的发送功率，beacon之类定位需要，Controller会填入真实的发送功率。

![image-20230729123253990](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729123253990.png)







###### ACAD field

是变长的，根据Header Length减去其他存在数据后的剩余长度指定。有特殊的用途，暂没用过。



























## 业务模型

### Legacy ADV业务模型

#### 基本业务

在设定的advInterval基础上会加入随机的advDelay，以便有相同advInterval的设备不会一直在同一时间发送数据包，导致设备一直冲突。

![image-20230728224210968](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728224210968.png)



#### Event行为

##### Connectable and scannable undirected-ADV_IND

只有Legacy才有，可以被connect和scan，最常用的包类型。

只有广播包的场景。

![image-20230728225455781](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728225455781.png)

被Scan的场景，中间被scan并不会结束Event。

![image-20230728225519732](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728225519732.png)

![image-20230729125523179](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729125523179.png)



被Connect的场景，收到CONNECT_IND后立即结束广播。

![image-20230728230008804](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728230008804.png)

##### Connectable directed-ADV_DIRECT_IND

Low Duty场景

![image-20230729125855482](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729125855482.png)

收到CONNECT_IND后立即结束。

![image-20230729125938651](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729125938651.png)

Higi Duty场景。

![image-20230729130018445](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130018445.png)



##### Scannable undirected-ADV_SCAN_IND

不可被连接，收到SCAN_REQUEST后回复SCAN_RSP，并不会结束Event。

![image-20230729130125340](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130125340.png)

![image-20230729130135588](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130135588.png)

![image-20230729130149611](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130149611.png)

##### Non-connectable and non-scannable undirected-ADV_NONCONN_IND

只管发广播就行，可以不开Scan Window。

![image-20230729130418598](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130418598.png)











### Extend ADV业务模型

#### 基本业务

##### 常规事件

多个Advertising Event也有Random的T_advEvent和advDelay的概念，多个Advertising Event可以共享一个AUX_ADV_IND。

照理说多个Advertising Event共享一个**AUX_ADV_IND**，功耗应该更低才对，但是实际业内大多数做法是一个Advertising Event对应一个**AUX_ADV_IND**，然后再睡眠，所以功耗高。

![image-20230728224330134](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728224330134.png)



带有**AUX_CHAIN_IND**的场景，这个场景下如下图所示。

![image-20230728224351438](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728224351438.png)



##### Periodic业务

在**AUX_ADV_IND**中会指向一个**AUX_SYNC_IND**，两个**AUX_SYNC_IND**之间是固定的**Periodic Advertising Interval**。

![image-20230728224828973](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230728224828973.png)



下面是一些Subevent和Response Slot的一些定义。

![image-20230729130632388](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130632388.png)

![image-20230729130717035](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729130717035.png)



#### Event行为

##### Connectable directed event

能接收**AUX_CONNECT_REQ**后回复**AUX_CONNECT_RSP**，之后就进入Connection State。

![image-20230729131102137](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131102137.png)

![image-20230729131119641](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131119641.png)



##### Scannable undirected event

能接收**AUX_SCAN_REQ**后回复**AUX_SCAN_RSP**，之后继续发广播。

![image-20230729131356818](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131356818.png)



![image-20230729131418608](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131418608.png)



##### Non-connectable and non-scannable undirected event

不会接收SCAN和CONNECT请求。

![image-20230729131526297](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131526297.png)

![image-20230729131548885](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131548885.png)



##### Connectable undirected event

能接收**AUX_CONNECT_REQ**后回复**AUX_CONNECT_RSP**，之后就进入Connection State。

![image-20230729131640134](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131640134.png)



![image-20230729131703973](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131703973.png)





##### Scannable directed event

和**Scannable undirected event**行为基本一样，但是这个AUX_ADV_IND会带TargetA，并且收到AUX_SCAN_REQ会检查其TxAddr信息是否匹配。



![image-20230729131418608](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131418608.png)



##### Non-connectable and non-scannable directed event

和**Non-connectable and non-scannable undirected event**行为基本一致，只是会带TargetA信息，接收端需要过滤不是发给自己的数据。

![image-20230729131548885](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729131548885.png)







## MSC(MESSAGE SEQUENCE CHARTS)

### Legacy

可以用Extend发，当然也可以用以前的命令发。

![image-20230729134026679](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729134026679.png)



![image-20230729134107708](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729134107708.png)





### Extend

必须用**LE_Set_Extended_Advertising_Parameters**、**LE_Set_Extended_Advertising_Data**、**LE_Set_Extended_Scan_Response_Data**和**LE_Set_Extended_Advertising_Enable**来发送。

![image-20230729134154641](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729134154641.png)

![image-20230729134420870](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729134420870.png)



### PERIODIC

注意PERIODIC广播和Extend广播走的命令不同。必须用**LE_Set_Extended_Advertising_Parameters**、**LE_Set_Periodic_Advertising_Data**、**LE_Set_Periodic_Advertising_Enable**和**LE_Set_Extended_Advertising_Enable**来发送。



![image-20230729134525919](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20230729134525919.png)

