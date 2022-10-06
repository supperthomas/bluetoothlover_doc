# USB串口(CDC)协议破解-蓝牙PTS Dongle接口破解

最近在用蓝牙Sig的PTS Dongle进行PTS测试，另外有一个项目是HCI测试Dongle的，之前主要的接口是USB的，BLE这个版本接口是UART的，有时候可以做对比测试用用，所以需要研究下其接口行为。既然PTS上位机能使用这个dongle，走的肯定是HCI协议，看PTS的日志交互也是HCI协议，所以应该直接获取到其USB接口中UART的配置是什么就行。

官网链接在这：[Bluetooth SIG](https://store.bluetooth.com/)

这个设备的datasheet：[CS-PB-BL654-USB_NORDIC_ZEPHYR_v1_0.pdf (connectivity-staging.s3.us-east-2.amazonaws.com)](https://connectivity-staging.s3.us-east-2.amazonaws.com/2019-07/CS-PB-BL654-USB_NORDIC_ZEPHYR_v1_0.pdf)

![image-20220919194444575](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919194444575.png)

## 准备工作

### PTS Dongle

从淘宝搜索`451-00004`，就可以买到。默认情况下，PTS软件默认没有预烧录特殊固件（默认的固件应该也能用，但没研究）。按照PTS软件的手册说明，下载firmware就行。

![image-20220919191112867](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919191112867.png)

![image-20220919191130097](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919191130097.png)

### wireshark+USBPcap

要抓USB的交互，当然要借助工具了，手头暂时没有USB抓包设备，不过wireshark+USBPcap来抓USB的数据包。这个自行安装，可以参考：[使用wireshark抓取USB包_xqhrs232的博客-CSDN博客_wireshark抓usb包](https://blog.csdn.net/xqhrs232/article/details/110387493)

![image-20220919191544589](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919191544589.png)

### SSCOM

串口调试助手，不用多说了，直接用就行，或者其他支持HEX交互的串口工具即可。





## USB串口(CDC)协议破解

既然是串口，只需要知道其串口配置就行，查了下CDC协议[Class definitions for Communication Devices 1.2 | USB-IF](https://www.usb.org/document-library/class-definitions-communication-devices-12)，主要就是通过`SET_LINE_CODING(0x20)`和`SET_CONTROL_LINE_STATE(0x22)`来设置串口的参数。

![image-20220919194121716](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919194121716.png)

![image-20220919192909030](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919192909030.png)



### SET_LINE_CODING(0x20)

这个命令用于设置串口波特率，停止位，奇偶位以及数据位等参数信息。

![image-20220919193034153](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919193034153.png)

![image-20220919193100334](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919193100334.png)

![image-20220919193110208](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919193110208.png)



通过抓取日志可以看到`Data Fragment: 40420f00000008`，解析如下：

- `dwDTERate`-波特率：0x000f4240 = 1Mbit/s
- `bCharFormat`-停止位：0x00, 0-1 Stop bit
- `bParityType`-奇偶位：0x00, None
- `bDataBits`-数据位：0x08, 8

![image-20220919193426401](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919193426401.png)



### SET_CONTROL_LINE_STATE(0x22)

这个主要设置流控这些参数的。也就是`RTS`和`DTR`功能开关。

![image-20220919193931593](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919193931593.png)



抓包后可以看到Value=1，也就是D0=1，开启了`DTR`，没开`RTS`。

![image-20220919194003694](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919194003694.png)



## SSCOM测试

串口参数知道了，直接进行测试，拿熟悉的SSCOM测试即可，按照HCI的H4协议，发送`01 03 0c 00(HCI Reset Command)`，可以看到收到了`04 0e 04 01 03 0c 00(HCI Command Complete Event - Reset)`。

测试通过，之后直接使用即可。

![image-20220919191614929](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220919191614929.png)

