# 微信小程序OTA升级及NRF_DFU协议搭建

介绍：

- OTA空中升级是进行设备固件更新的重要途径之一，其中升级平台多种多样

- 大部分都是有自有的APP和设备进行通讯升级；用户需要下载其对应的APP，使用起来相对比较麻烦

- 市面上的OTA升级大部分是通过蓝牙升级，其中有的传输走的经典蓝牙SPP，有的传输走的低功耗蓝牙BLE；两者各有其优势，经典蓝牙SPP传输速率较快，相对的升级等待体验较好，BLE传输升级速率相对较慢，不过使用简单方便

- 本文主要介绍通过微信小程序进行OTA升级，使用微信的BLE蓝牙进行通信传输（因为现如今微信已成为手机必备APP，用户无需再另外安装APP，用户使用便捷体验比较好，所以采用微信平台是比较好的选择，微信官方公布以后也会支持经典蓝牙，目前支持BLE）设备端则用nrf52832，通过NRF DFU协议实现固件升级。同时介绍NRF的升级模式

  

## 搭建自己的微信蓝牙小程序

关于搭建微信小程序环境官网有详细的搭建步骤可[点击连接](https://developers.weixin.qq.com/miniprogram/dev/framework/quickstart/getstart.html#申请账号)

如下：![image-20231104141206754](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104141206754.png)

### 使用官方提供的蓝牙例程

在注册完小程序账号以及下载完微信开发者平台后可以直接跳到**连接硬件能力**这个标题介绍：

如下：

![image-20231104142221249](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104142221249.png)

里面有关于蓝牙方面的基础简单介绍，拉到最下底部有**示例代码**，可点击[在开发者工具中预览效果](https://developers.weixin.qq.com/s/OF4Y9Gme6rZ4)：会调出微信开发者平台，里面有Beacon的示例代码，不过本文使用的例程是Central角色，因此可以跳到API选项中唤起Central例程的选项

如下：

![image-20231104150927833](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104150927833.png)

唤起微信开发者平台如下：

![image-20231104151056577](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104151056577.png)

使用此例程需要一些BLE蓝牙基础知识：此例程可发现周围设备并且连接它

至此我们已经可以通过此例程开发我们的蓝牙OTA小程序了

## NRF DFU

DFU(Device Firmware Update)是设备固件升级的英文解释，升级传输的方式有许多种比如USB、SD卡，SPI、串UART以及通过无线传输，

无线传输升级统称OTA （Over the Air)DFU,为了方便起见我们用OTA来指代固件空中升级。OTA的传输媒介也有许多种，例如蓝牙和无线电等，其中常用的蓝牙、又可用传统蓝牙SPP和低功耗蓝牙BLE

### NRF DFU原理介绍

NRF的DFU分为两种模式分别是dual bank和single bank模式，

#### 升级流程

- Dual bank

dual bank是升级时系统先进入bootloader ，把新固件下载下来，校验成功后再把老固件升级新系统，dual bank在空间剩余多的情况下使用起来方便许多，提供比较好的升级体验

- Single bank

Single bank升级时也是先进入bootloader，然后把老系统的空间擦除，将接收到的数据写入进去，相对比较dual bank，single bank使用的空间更少，适合APP应用程序比较大的时候使用，但是缺点就是一旦传输过程中出现失败，则老的APP程序无法使用，只能待在bootloader中

如下图所示：

- Dual bank APP应用程序升级方式

  ![image-20231104172127367](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104172127367.png)

- Single bank APP应用程序升级方式

  ![image-20231104172303362](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104172303362.png)

值得注意的时以上是升级用户程序的APP的方式，有时还需要升级SoftDevice和bootloader（SoftDevice是协议栈部分，bootloader为引导APP程序）

- Dual bank 升级SoftDevice和bootloader方式

![image-20231104173118805](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104173118805.png)

可以看出升级SoftDevice和bootloader时是需要擦除用户程序的

参考官方介绍[点击链接]([Nordic Semiconductor Infocenter](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fstruct_nrf52%2Fstruct%2Fnrf52.html&cp=5))

#### Bank擦写流程

- 第一步：升级前应用程序放在Bank0而Bank1的空间为空的，如下图所示：

  ![image-20231104174007355](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104174007355.png)

- 第二步：当bootloader 进入DFU模式时会先擦除Bank1清空用于存放需要更新的应用程序，如下图所示：

  ![image-20231104174502424](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104174502424.png)

- 第三步：开始将接收到的新应用程序逐步写入Bank1，如下图所示：

![image-20231104174652735](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104174652735.png)

- 第四步：将完整的通过校验的新应用程序都接收完成并写入Bank1后，此时存在新旧两份完整的应用程序，旧的程序仍可以运行，如下图所示：

  ![image-20231104175111617](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104175111617.png)

- 第五步：开始擦除旧的应用程序也就是Bank0，如下图所示：

  ![image-20231104175251678](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104175251678.png)

- 第六步：开始将Bank1的应用程序写入到Bank0中，此时如果产生失败则开机会一直待在bootload DFU中直至将Bank 1写入到Bank0中。如下图所示：

  ![image-20231104175712542](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104175712542.png)

- 第七步：当彻底将bank1写入到bank0后，bank1中的数据不会擦除，等下次升级进入bootdoad DFU 模式时才将其擦除

  

![image-20231104180609281](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimage-20231104180609281.png)

### NRF OTA DFU Profile介绍

上面介绍了关于DFU的原理，那么如果想要微信和nrf设备进行通信交互，还需要相关的OTA通信协议

#### **BLE DFU Service**

设备端进行描述服务的内容

[参考链接]([Nordic Semiconductor Infocenter](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fcom.nordic.infocenter.sdk5.v11.0.0%2Fbledfu_transport_bleservice.html))

#### BLE DFU Profile

[参考链接]([Nordic Semiconductor Infocenter](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fstruct_nrf52%2Fstruct%2Fnrf52.html&cp=5))

#### 协议参考

[参考链接](https://github.com/dmlls/InfiniTime/blob/54d58dbc46a357334bf5825973e2d817ac855954/bootloader/ota-dfu-python/ble_secure_dfu_controller.py)