# BLE Privacy分析

Privacy是BLE里面一个非常重要的概念，尤其是当目前手机默认开启了Privacy功能后，大家就不得不深入的了解这个机制的原理和使用场景了。



## CORE SPEC阅读

个人觉得要如何掌握一个知识点，一定要去看最原始的资料，其他人提供的资料多少带有个人理解。就像你想学一个工具一样，如果一直看别人写的教程（其实大多数也是别人翻译的东西），很难深入理解，初学者可以多看看母语的东西，后面有机会还是得看原著的资料（如果你要从事蓝牙行业的话）。

BLE Privacy的说明在蓝牙Core Spec里面都有，并不需要看其他Host的Profile。直接到官网[Core Specification 5.3 – Bluetooth® Technology Website](https://www.bluetooth.com/specifications/specs/core-specification-5-3/)下载即可。

截止到写文档的时间点，Core Spec最新版本是v5.3。

![image-20220818092510055](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818092510055.png)



Spec里面包含BR/EDR(经典蓝牙)和BLE的内容。到目前Spec已经到3085页了，其实Core Spec4.0就有Privacy相关的概念，但是还不是很完善。

从Core Spec 5.3中的《Vol0 Part C  REVISION HISTORY AND ACKNOWLEDGMENTS》-《Page，101 / 3085》看改动记录可以看到在4.1和4.2都有相关完善，基本到4.2版本开始，Privacy已经比较成熟了。

Core Spec相关章节可以通过搜索**privacy**关键字来看相关内容，当然后续会简单和大家说一下需要哪些部分，各个部分的简要说明。

![image-20220818094647715](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818094647715.png)

![image-20220818094736389](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818094736389.png)

### Architecture

在Spec的《Vol 1, Part A  Architecture》《Page - 275 / 3085》章节中，讲了下LE Privacy是干什么，以及一些关键的概念，没多少字，建议详细看完。相关原文也贴在下图中，下面对一些重点概念进行简要说明。

Privacy的主要目的就是去Track 周期更新的BLE设备地址。BLE为了安全考虑，会一段时间更新一次自身的设备地址，根据是否需要满足**reconnect**需要，可以用resolvable或者non-resolvable地址。

同时也说明了在Privacy中有两种方式，分别是**Host**实现方式和**Controller+Host**实现方式。4.2之后才支持**Controller+Host**模式，通常Host的能力强一些，而Controller的Resolvable List的能力比较有限，基本还得靠Host来做，虽然这样会导致功耗更高。

此外在Privacy中也定义了两种模式，分别是**device privacy mode**和**network privacy  mode**，默认情况下都是**network privacy  mode**，当然可以通过HCI命令《HCI_LE_Set_Privacy_Mode-0x204F》通知Controller特定的Peer Address使用**device privacy mode**。详细描述见Spec原文。（这个模式是Spec5.0才引入的概念，一般用默认模式就行）

同时Spec也说明了Privacy基本都是伴随着Filter（通常也叫White List）来使用的，合理使用这个机制，可以有效减少Controller上报Adv Event的数量，从而降低功耗。

![image-20220818101339682](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818101339682.png)

![image-20220818102347940](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818102347940.png)

![image-20220818101913660](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818101913660.png)



### Generic Access Profile(GAP)

在Spec的《Vol 3, Part C  Generic Access Profile》《Page - 1351 / 3085》章节中，讲了下LE Privacy如何使用，并对Architecture中的描述做进一步的解释说明，建议详细看完。

看完以后对如何使用Privacy会有一个更清晰的认识。

![image-20220818104248224](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818104248224.png)

![image-20220818104400563](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818104400563.png)



![image-20220818103549662](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818103549662.png)



### Link Layer Specification(LL)

在Spec的《Vol 6, Part B  Link Layer Specification》章节中，对LE的link layer具体实现有详细说明。需要重点看以下几个部分：

- 《4.3 LINK LAYER DEVICE FILTERING》-《Page - 2743 / 3085》，因为Privacy基本和Filter同时使用的，所以需要看这个部分。
- 《4.7 RESOLVING LIST》-《Page - 2837 / 3085》，Resovling List部分。
- 《6 PRIVACY》-《Page - 2883 / 3085》，Privacy详细说明部分。

在Spec的《Vol 6, Part D  Message Sequence Charts》章节中，重点看带有Privacy实现的部分，有重点说明如何使用HCI Command控制Controller来实现Privacy的策略。



## Address

要讲明白Privacy，需要对BLE的Address定义有一个清晰的认识。

Address可以理解为IP地址或者MAC地址，是设备的唯一身份。其是6个字节，共48bits组成。

对于BLE来讲，如果不涉及到Privacy你只需要关心自己的地址是Public地址还是Random地址就行。

刚开始接触蓝牙时，很多人会对BLE定义的各种地址一脸蒙，简单分为Public Address和Random Address不就好了么？如果考虑可解析，Random Address全部用RPA Address不就行了。这样Public Address是设备的真实身份，Random Address是设备的伪装身份不就OK了，这样理解起来也省事，为什么要搞这么多地址。要解释这个问题，就得深入理解Privacy的机制了。

BLE地址分两大类，分别是Public Address和Random Address，然后Random Address又分为Static Address和Private Address，Private Address又分为Non-Resolvable private address和Resolvable private address。一共4种地址类型。

- **Public Address**

- Random Address

  - **Static Address**

  - Private Address

    - **Non-Resolvable private address**

    - **Resolvable private address**

为什么要分这么多层呢，直接划分为4个不就好了么。这就涉及到：

- Public Address是原本就有的概念，48个bits都有特定的概念，那要区分不同的设备类型必须加入额外的bit位才能做到。而且Public Address不能变，其定义48bits都可以配置，这会导致其可能和Random Address相同，所以必须通过额外bit区分开来。
- 如果要分成4个类型的话要区分需要2个bit才能做到。只用1个bit的话可以省不少（个人理解），通过1个bit来区分Public Address和Random Address。而Random Address留2个bits来区分这三种设备地址类型，剩余46个bits根据要求随机产生。
- 通过1个bit来区分的话，Advertising PDU的Header才能将地址类型发送出去，不然就超过了，产生不必要的浪费。
- Filter List中也是1个bit来区分设备地址类型，这样就算只知道设备的Non-Resolvable地址，也可以用这个地址过滤出来。

![image-20220818111458495](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818111458495.png)

在经典蓝牙中，只有一个Public Address的概念，虽然别的行为复杂一些，baseband的逻辑也比较复杂，但是很多行为好理解，毕竟一个设备一个地址就好了，不容易搞混。

而BLE为了**Privacy**的需要引入了一堆地址的概念，反而让问题更复杂一些了，虽然能解决蛮多实际问题，但是多少让大家学习成本大大增加。

### Public Address

这个和经典蓝牙公用的地址，使用需要找sig购买，UAP/NAP是购买时确定的，只有LAP厂商才可以自己使用（部分LAP要留给经典蓝牙使用，经典蓝牙的Inquiry跳频机制-1个GIAC和63个DIACs，都是直接使用LAP来产生的，如果设备地址用这些地址，会导致Inquiry和Page大家，所以不能随便用），也就是只有3个字节可选，总共也就16,777,215个。实际购买据我了解可以只买一个地址区间（几千个买一买），具体多少价格不记得了，大家只要记住是需要付钱购买的。

蓝牙芯片厂商一般会买一些地址段，但是并不会每一个蓝牙芯片生产出来就买一个，只有实际生产出产品，客户有需要才买，目前芯片厂的模式基本都是由方案商根据需要自行购买地址段，蓝牙芯片厂并不提供。

此外，标准Sig HCI协议中并没有可以设置Public Address的接口，基本上一个Controller芯片只有唯一一个蓝牙地址，Host不可以自己修改，当然一般蓝牙芯片厂商都会提供自家的Vendor Command来重新设置Public Address，以便后续方案商自行使用。

实际情况是，基本没谁购买，除非一些特殊项目，不然都是随便使用。通过Vendor Command，各个方案商自行设定了没有在Sig购买的地址，但是方案商很多规模都比较小，Sig基本也没办法去找方案商收费了。（其实按照现状，其实Sig把设置public address接口留出来算了，省得每家方案商都要设置一套接口了，做通用蓝牙Stack都比较麻烦。）

![image-20220814121417589](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220814121417589.png)



### Random Address

Random地址都是通过Address[47:46]这两个bits来区分的。剩余的46bits按照特定规则生成。

![image-20220818112117592](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818112117592.png)

#### Static Address

地址格式如下：

![image-20220818112249984](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818112249984.png)

随机部分的生成规则如下：

![image-20220818112332090](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818112332090.png)

一般来讲，每次上电可以重新指定一个Static Address，但是由于Static Address一般也用于Identity Address，这会导致reconnect失败。

所以实际操作时，当设备没有Public Address时，设备第一次上电会指定一个，之后只要记录没删除，基本不会重新指定，以便其他配对过的设备回连本设备。

#### Private Address

Privacy中说的一直换的地址就是Private Address，而这里的地址一个是**Non-Resolvable private address**，另外一个是**Resolvable private address（RPA）**。

平常手机每隔一段时间修改的地址就是**Resolvable private address（RPA）**，因为手机要满足reconnect需要，所以基本不会使用**Non-Resolvable private address**。

##### Non-resolvable Private Address

地址格式如下：

![image-20220818112946056](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818112946056.png)

随机部分的生成规则如下：

![image-20220818113005413](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818113005413.png)

Non-resolvable private address通常被用于不需要reconnect的场景下，其他时候用的基本上都是Resolvable private address。



##### Resolvable Private Address

地址格式如下：

![image-20220818113221405](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818113221405.png)

24bits随机部分的生成规则如下：

![image-20220818113202403](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818113202403.png)

其中24bits的hash部分是通过IRK生成的。

![image-20220818113324677](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818113324677.png)

Resolvable private address字面意思，可以解析。通过IRK可以找到与之对应的Identity Address，从而知道设备的真实身份，更新地址并不会影响设备的reconnect，所以基本上可以隔一段时间就修改一次，以满足特定安全功能需要。







## Identity Address

在Privacy中有个概念是Identity Address，可以理解为设备的真实身份。平时设备使用的是Private Address，而且Privacy规定一定时间（15分钟）就会换一个地址，那么如果设备修改完地址之后，之前配对过的设备需要再和这个设备连接的时候，需要一套机制让两者之间知道对方的真实身份。

那么为什么要定义成Identity Address呢？直接用Public Address不就可以了么。那是因为Public Address是要在Bluetooth Sig那购买的，而如果不想购买怎么办呢？毕竟BLE是低成本方案，买个Public Address也要花钱，也不利于推广。（个人猜测，但是确实符合实际场景需要，能自圆其说）

所以Identity Address也可以是Random Address中的**Static Address**。

如下加粗字体就是Identity Address。

- **Public Address**

- Random Address

  - **Static Address**

  - Private Address

    - Non-Resolvable private address

    - Resolvable private address

那么问题来了，建立连接之前需要通过ADV/SCAN来发现设备，而这时用的是Private Address，这样就存在3个问题：

- 两个开启Privacy功能的设备，在第一次连接时，什么时候交互**Identity Address**和**IRK**呢？
- 开启Privacy功能后，应该如何使用RPA。
- 已经交互过一次的设备，如何通过Private Address来得知其Identity Address呢？

### 交互Identity Address

要交互**Identity Address**和**IRK**需要通过**SMP**流程，在加密完成后（安全考虑），通过SMP交互流程来交互这两个信息，实际根据设备是否启动Privacy功能，来决定是否需要发送。

![image-20220818115422135](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818115422135.png)

**Identity Information**来发送IRK

![image-20220818114917671](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818114917671.png)

**Identity Address Information**来发送BD_ADDR和AddrType，因为Identity Address可以是Random Static Address也可以是Public Address，所以必须区分开来。

![image-20220818115041548](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818115041548.png)



### 如何使用Private Address

上面讲得是如何对接收到的Privacy Address进行解析，并识别成Identity Address。本节具体讲一下如何使用RPA。


#### Host-Only的实现方式

这个模式下，不需要Controller参与，其实控制逻辑还是比较简单的，还是按照几个业务来说明。

##### ADV模式

Host控制设备进入发送广播状态，先发送《HCI_LE_Set_Random_Address-0x2005》，配置好RPA，而后在发送的《HCI_LE_Set_Advertising_Parameters-0x2006》参数中，设置Own_Address_Type为0x01，就可以使所发送的AdvA为RPA了。

![image-20220818150858815](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818150858815.png)

##### Scan模式

Host控制设备进入扫描状态，先发送《HCI_LE_Set_Random_Address-0x2005》，配置好RPA，而后在发送的《HCI_LE_Set_Scan_Parameters-0x200B》参数中，设置Own_Address_Type为0x01，就可以使所发送的Scan Request中的ScanA为RPA了。

![image-20220818151354001](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818151354001.png)

##### Initial模式

Host控制设备进入扫描状态，先发送《HCI_LE_Set_Random_Address-0x2005》，配置好RPA，而后在发送的《HCI_LE_Create_Connection-0x200D》参数中，设置Own_Address_Type为0x01，就可以使所发送的Connection Request中的InitA为RPA了。

![image-20220818151534899](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818151534899.png)



#### Host+Controller的实现方式

上述描述可以发现，都是需要通过Host设置随机地址来控制实现，基本上满足需要。当然也可以通过Host配置Controller来实现。

##### ADV模式

Host控制设备进入发送广播状态，先发送《HCI_LE_Add_Device_To_Resolving_List-0x2027》，配置好Local IRK，而后通过《HCI_LE_Set_Address_Resolution_Enable-0x202D》使能Resolvable List功能，最后在发送的《HCI_LE_Set_Advertising_Parameters-0x2006》参数中，设置Own_Address_Type为0x02或者0x03，Controller自己就会根据IRK生成RPA，并且发送的AdvA就是RPA了。

**注意**，如果Own_Address_Type为0x03，最好要先设置《HCI_LE_Set_Random_Address-0x2005》以便没有resolvable list时使用Random Address。

##### Scan模式

Host控制设备进入发送广播状态，先发送《HCI_LE_Add_Device_To_Resolving_List-0x2027》，配置好Local IRK，而后通过《HCI_LE_Set_Address_Resolution_Enable-0x202D》使能Resolvable List功能，最后在发送的《HCI_LE_Set_Scan_Parameters-0x200B》参数中，设置Own_Address_Type为0x02或者0x03，Controller自己就会根据IRK生成RPA，并且发送的ScanA就是RPA了。

**注意**，如果Own_Address_Type为0x03，最好要先设置《HCI_LE_Set_Random_Address-0x2005》以便没有resolvable list时使用Random Address。

##### Initial模式

Host控制设备进入发送广播状态，先发送《HCI_LE_Add_Device_To_Resolving_List-0x2027》，配置好Local IRK，而后通过《HCI_LE_Set_Address_Resolution_Enable-0x202D》使能Resolvable List功能，最后在发送的《HCI_LE_Create_Connection-0x200D》参数中，设置Own_Address_Type为0x02或者0x03，Controller自己就会根据IRK生成RPA，并且发送的ScanA就是RPA了。

**注意**，如果Own_Address_Type为0x03，最好要先设置《HCI_LE_Set_Random_Address-0x2005》以便没有resolvable list时使用Random Address。






### 如何识别Private Address

因为在建立连接之前，ADV/SCAN交互的地址都是可能变化的。按照之前GAP的描述，如果设备满足**reconnect**的需要，使用的是**Resolvable Private Address**，那就可以识别出来。

按照GAP描述的实现方式，可以分为Host-Only的实现方式和Host+Controller的实现方式。

#### Host-Only的实现方式

这个模式下，不需要Controller参与，其实控制逻辑还是比较简单的，按照几个业务来说明。

##### ADV模式

Host控制设备进入发送广播状态，按照LL的定义（暂时只对Legacy Adv进行说明），根据广播类型，可以被**Scan Request**控制回复Scan Response；根据广播类型，可以被**Connection Request**连接进行Connection State。而这些行为Host都无法介入，所以基本没什么办法。

##### Scan模式

Host控制设备进入扫描状态，Controller会将收到的ADV通过ADV Report Event上报给Host，Event中包含设备类型和设备地址。Host如果发现是**Resolvable Private Address**就会和自身的Resolvable List进行匹配，看List中哪个IRK能把RPA解析出来，能解析的那个就将上报给APP层的Event中的Address给替换成之前记录的Identity Address。

上述过程就将一个随机地址解析成Identity Address，就可以进行下一步的**Reconnect**业务了。

##### Initial模式

之前已经知道了设备的Identity Address，又知道了设备目前正在使用的RPA，那就直接用对方的RPA地址和对方发起连接即可。

##### 总结

可以发现Host-Only模式下，可操作性非常有限，由于不知道对方目前最新的RPA是什么，这个信息只有Host知道，而Controller并不清楚，所以在ADV模式下无法用Filter规则限制是否回复Scan Response，和限制接收Connection Request进入连接状态。



#### Host+Controller的实现方式

上述描述可以发现，单用Host实现，能操作的行为还是非常有限的，远远达不到对Privacy的功能需要，为此需要考虑Host+Controller共同实现。依然按照各个模式来分析。

##### ADV模式

设备进入发送广播状态后，根据广播类型，可以被**Scan Request**控制回复Scan Response；根据广播类型，可以被**Connection Request**连接进行Connection State。

- 如果不开启**Filter**功能，其效果就和Host-Only实现方式一样。

- 如果开启了**Filter**功能，Controller就可以根据**Filter策略**和**Filter Accept List**能决定是否响应决定是否回复Scan Response和是否和响应Connection Request进入Connection State了。

**注意**，这时候存在Filter Accept List中的Address应该是Identity Address。收到ADV后，会先将AdvA解析成Identity Address后，再按照Filter策略和Filter Accept List进行地址匹配。

**注意**，Controller一般功能有限，Resolvable List的解析功能通常是配合Filter Accept List来使用，要求在T_IFS(150us)内完成对Privacy地址识别，并通过Filter Accept List匹配来决定是否回复对端的Scan Response，再考虑RF通路延迟和PLL锁定时延，时间更为有限，单纯匹配地址所需时间还好，要进行Resolvable Private Address的解析所需的时间会很长，基于这一现实情况，一般Controller的Resolvable List的大小都比较小，实际使用通常只会用一个，或者说会一定小于Host所记录的总个数。

##### Scan模式

设备进入扫描状态，Controller收到的ADV时。

- 如果不开启**Filter**功能，那Controller只会用Resolvable List解析收到的设备地址，找到符合条件的IRK后，将设备的Identity Address通过ADV Report Event上报给Host。

- 如果开启了**Filter**功能，Controller就可以根据**Filter策略**和**Filter Accept List**能决定是否上报收到的ADV已经是否发起Scan Request。

和ADV模式同样的原因，由于Controller的Resolvable List个数有限，Host收到ADV Report Event后，如果发现是RPA，还是会进行解析，找到后替换成Identity Address上报给APP层。

Spec在MSC中描述了两边同时开启RPA情况下的交互流程（未开启Filter功能模式）。

可以看出两边通过《HCI_LE_Add_Device_To_Resolving_List-0x2027》，配置好Local IRK和Peer IRK后，而后通过《HCI_LE_Set_Address_Resolution_Enable-0x202D》使能Resolvable List功能。

B发送ADV_IND中的AdvA就是RPA，A在150us内对收到的AdvA进行解析，并根据需要上报LE Advertising Report Event，而后生成ScanA的RPA发送SCAN_REQ；B收到后先检查AdvA是否是自身的RPA，并解析ScanA的RPA，条件通过后回复SCAN_REP；A收到后上报LE Advertising Report Event。

![image-20220818152957580](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818152957580.png)

##### Initial模式

这里就存在2个情况，一个是Controller知道其Identity Address和RPA，一个是Host知道，这会影响后续发起连接时的行为。

- 如果是Host解析的情况，那就按照上述流程，Create Connection的时候就用记录的RPA发起连接。

- 如果是Controller解析，Host用Identity Address发起连接，Controller发现Identity Address在Resolvable List中，收到ADV后，会对AdvA进行解析，如果Identity Address匹配就和设备进行连接。这样就算这段时间设备的RPA变化了，Controller也可以准确和设备进行连接了。

Spec在MSC中描述了两边同时开启RPA情况下的交互流程（未开启Filter功能模式）。

可以看出两边通过《HCI_LE_Add_Device_To_Resolving_List-0x2027》，配置好Local IRK和Peer IRK后，而后通过《HCI_LE_Set_Address_Resolution_Enable-0x202D》使能Resolvable List功能。

B发送ADV_IND中的AdvA就是RPA，A在150us内对收到的AdvA进行解析，而后生成InitA的RPA发送CONNECT_IND，并上报LE Enhanced Connection Complete Event；B收到后先检查AdvA是否是自身的RPA，并解析InitA的RPA，条件通过后并上报LE Enhanced Connection Complete Event。之后两个设备就可以进行交互了，需要注意的是，上报的Event中，Address使用Identity Address。

![image-20220818153712843](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818153712843.png)

##### 总结

可以发现Host+Controller模式下，配合Filter功能，可以实现各种灵活的功能配置，也能最终达到Privacy的功能需要。虽然让这个行为变得非常复杂，但是为了满足功能需要，还是非常有必要的。












## Resolving List控制

通过上述分析可以知道，在Host+Controller实现方式下，需要Host配置Resolvable List，以便Controller来实现对Privacy的功能实现。

Resolving List的结构如下，每个item是由Local IRK，Peer IRK，Peer Device Identity，Address Address Type组成。

![image-20220818154259723](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818154259723.png)

Spec定义了如下的Hci Command来实现对Resolving List的管理。

![image-20220818150241351](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818150241351.png)

操作流程一般是先读Size，再Clear，再Add。要开启时再Enable。

![image-20220818155600205](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818155600205.png)

![image-20220818154536508](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818154536508.png)



## Filter Accept List控制

通过上述分析可以知道，在Host+Controller实现方式下，如果开启Filter开关，需要Host配置Filter策略和Filter Accept List，以便Controller来实现对Filter的功能实现。

Filter策略基本都是在各个业务开启时设定的，各个Policy如何使用在spec有详细描述《Vol 6, Part B  Link Layer Specification》章节中《4.3 LINK LAYER DEVICE FILTERING》-《Page - 2743 / 3085》有详细描述，这里就不具体展开了：

- ADV是《HCI_LE_Set_Advertising_Parameters-0x2006》
- SCAN是《HCI_LE_Set_Scan_Parameters-0x200B》
- Initial是《HCI_LE_Create_Connection-0x200D》

Filter Accept List结构如下图，每个Item是有Device Identity Address和Address Type组成，这里当然也可以直接设置为RPA，但是并没有多少意义就是了。

![image-20220818154502147](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818154502147.png)

Spec定义了如下的Hci Command来实现对Filter Accept List的管理。

![image-20220818155400324](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818155400324.png)

操作流程一般是先读Size，再Clear，再Add。

![image-20220818155516556](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220818155516556.png)





## 总结

BLE Privacy为了安全，会不断改变设备地址。但是为了**reconnect**的需要，设计了RPA地址，既然有动态Random Address，自然有代表其真实身份的Identity Address。

所有上报到APP层的都是Identity Address，然后围绕这些东西设计了一系列的逻辑，本文主要围绕于使用需求来说明，详细的说明还是得看Core Spec的说明。

但是不管怎么说，理解了需求后，才能理解所谓Core Spec设定的一系列限制。上述说明并没有保护Extended Adv，Extended Adv只是换一个方式用，后续有时间再完善。









