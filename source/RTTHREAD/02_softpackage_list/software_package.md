# RTTHREAD软件包目录

这边统计下RTTHREAD软件包的各项内容



## IOT 

| 包名                                                         | 技术标签            | 依赖平台             | 备注                                                         |
| ------------------------------------------------------------ | ------------------- | -------------------- | ------------------------------------------------------------ |
| [abup_fota](https://github.com/RayShen1018/Abup)             | OTA                 | TCP/UDP              | 本软件包是用于 Abup FOTA 升级的固件下载器                    |
| [agile_jsmn](https://github.com/loogg/agile_jsmn)            | json                | C库                  | jsmn是一个超轻巧，携带方便，单文件，适用于单片机中存储空间有限的环境，简单的可以作为ANSI-C标准的JSON解析器。 |
| [agile_telnet](https://github.com/loogg/agile_telnet)        | ETH                 | TCP                  | 以太网TCP调试。                                              |
| [airkissOpen](https://github.com/heyuanjie87/airkissOpen)    | IOT                 | w600                 | 腾讯 WiFi设备一键配网协议[airkiss]                           |
| [ali-iotkit](https://github.com/RT-Thread-packages/ali-iotkit) | IOT                 | MBEDTLS              | **ali-iotkit** 是 RT-Thread 移植的用于连接**阿里云** IoT 平台的软件包 |
| [atsrv_socket](https://github.com/RT-Thread-packages/atsrv_socket) | AT                  | AT, SAL              | atsrv_socket 是包含了常用 socket 指令的 AT 服务端            |
| [AT device](https://github.com/RT-Thread-packages/at_device) | AT                  |                      | AT device 软件包是由 RT-Thread AT 组件针对不同 AT 设备的移植文件和示例代码组成，目前支持的 AT  设备有：ESP8266、ESP32、M26、MC20、RW007、MW31、SIM800C、W60X 、SIM76XX、A9/A9G、BC26  、AIR720、ME3616、M6315、BC28、EC200X、M5311、L610系列设 |
| [azure-iot-sdk](https://github.com/RT-Thread-packages/azure-iot-sdk) | IOT                 | netutils,MBEDTLS     | **Azure** 是 RT-Thread 移植的用于连接微软 Azure IoT 中心的软件包 |
| [rtt-bc28-mqtt](https://github.com/luhuadong/rtt-bc28-mqtt)  | MQTT                |                      | bc28_mqtt 是基于移远 BC28 模块 AT 固件的 MQTT 软件包         |
| [btstack](https://github.com/supperthomas/RTT_PACKAGE_BTSTACK) | BT,                 | AP6212               | BTstack 软件包是RT-Thread 基于 btstack 开源蓝牙协议栈的适配  |
| [capnp](https://github.com/wuhanstudio/capnp)                | protobuf            |                      | Cap'n 串行化协议，比 protobuf 更高效，更轻量级。比XML高效存储数据 |
| [cJSON](https://github.com/RT-Thread-packages/cJSON)         | JSON                |                      | 超轻量级的 C 语言 json 解析库                                |
| [cmux](https://github.com/RT-Thread-packages/cmux)           |                     |                      | CMUX 软件包常用于蜂窝模块串口复用功能（PPP + AT 模式），以及串口硬件资源受限的设备 |
| [coap](https://github.com/RT-Thread-packages/coap)           | IOT                 | COAP                 | CoAP on RT-Thread                                            |
| [dlt645]()                                                   | DLT645              |                      | 本软件包用于 DL/T 645 协议的采集与数据处理(电表)             |
| [ezXML](https://github.com/RT-Thread-packages/ezXML)         | XML                 |                      | 用来解析XML文件的                                            |
| [freemodbus](https://github.com/RT-Thread-packages/freemodbus) | MODBUS              | RT_Thread UART 设备  | FreeModbus 是一款开源的 Modbus 协议栈                        |
| [GAgent](https://github.com/RT-Thread-packages/GAgent)       | IOT                 | 机智云               | GAgent是**机智云**物联网整体解决方                           |
| [ipmsg](https://github.com/heyuanjie87/ipmsg)                | IP                  |                      | 飞鸽传书，收发文本消息，接收文本                             |
| [jiot-c-sdk](https://github.com/jpush/JIoT-rtthread-package) | IOT                 | 极光                 | 极光 IoT 是极光面向物联网开发者推出的 SaaS 服务平台          |
| [joylink](https://github.com/RT-Thread-packages/joylink)     | IOT                 | 京东云               | joylink 京东小京鱼 IoT 开放平台                              |
| [jsmn](https://github.com/RT-Thread-packages/jsmn)           | JSON                |                      | jsmn是一个超轻巧，携带方便JSON解析器                         |
| [kawaii-mqtt](https://github.com/jiejieTop/kawaii-mqtt)      | MQTT                |                      | 这是一个基于socket API之上的跨平台MQTT客户端                 |
| [libcurl2rtt](https://github.com/liu2guang/libcurl2rtt)      | TCP/IP              |                      | 基于 RT-Thread 移植的 curl 库                                |
| [libmodbus](https://github.com/loogg/libmodbus)              | MODBUS              |                      | libmodbus是一个与使用Modbus协议的设备进行数据发送/接收的库   |
| [librws](https://github.com/RT-Thread-packages/librws)       |                     |                      | 小型、跨平台websocket客户端C库。                             |
| [ljson](https://github.com/qiaoqidui/ljson)                  | JSON                |                      | ANSI-C 标准的 JSON 解析器                                    |
| [lorawan_driver](https://github.com/zyk6271/LoRaWAN_Driver)  | LORA                | SX126X               |                                                              |
| [lorawan_ed_stack](https://github.com/Forest-Rain/lorawan-ed-stack) | LORA                | SX126X               | lorawan_ed_stack是LoRaWAN终端设备协议栈的实现.               |
| [lssdp](https://github.com/RT-Thread-packages/lssdp)         | LSSDP               |                      | 在 RT-Thread 上实现的 lssdp 协议，可以用于局域网设备自动发现 |
| [mongoose](https://github.com/armink-rtt-pkgs/mongoose)      | Web                 |                      | 一款嵌入式 Web 服务器库                                      |
| [mymqtt](https://github.com/hichard/mymqtt)                  | MQTT                |                      | Eclipse 开源的 MQTT                                          |
| [nanopb](https://github.com/RT-Thread-packages/nanopb)       | Protocol Buffers    |                      | Protocol Buffers 解析器在嵌入式上的实现                      |
| [netutils](https://github.com/RT-Thread-packages/netutils)   |                     |                      | RT-Thread 网络网络小工具集                                   |
| [nimble](https://github.com/RT-Thread-packages/nimble)       | BT                  |                      | nimble蓝牙协议栈                                             |
| [nmealib](https://github.com/ShineRoyal/nmealib)             | GPS                 |                      | nmealib库在RT-Thread上的移植                                 |
| [nopoll](https://github.com/RT-Thread-packages/nopoll)       | OpenSource WebSocke |                      | 一款 C 实现的开源 WebSocket 软件包                           |
| [onenet](https://github.com/RT-Thread-packages/onenet)       | IOT                 | 移动云               | 连接中国移动 OneNet 云的软件包                               |
| [onnx-backend](https://github.com/wuhanstudio/onnx-backend)  | AI                  | ******************** | 开源神经网络模型 onnx 后端，支持几乎所有主流机器学习模型     |
| [rt-onnx-parser](https://github.com/wuhanstudio/rt-onnx-parser) | AI                  |                      | 开源神经网络模型 onnx 解析库                                 |
| [ota_downloader](https://github.com/RT-Thread-packages/ota_downloader) | OTA                 | HTTP                 | 基于 RT-Thread OTA 组件的 固件下载器                         |
| [paho-mqtt](https://github.com/RT-Thread-packages/paho-mqtt) | MQTT                |                      | Eclipse 实现的基于 MQTT 协议的客户端                         |
| [pdulib](https://github.com/ShineRoyal/pdulib)               | PDU                 |                      | 一个用于PDU格式的短信文本解析库                              |
| [ppp_device](https://github.com/RT-Thread-packages/ppp_device) | PPP NBIOT           |                      | lwIP PPP 功能针对蜂窝( 2G/3G/4G )模块移植和实现              |
| [protobuf-c](https://github.com/wuhanstudio/protobuf-c)      |                     |                      | Google 的 prototol buffer 一种轻便高效的数据存储格式         |
| [qianxun](https://github.com/RT-Thread-packages/qianxun)     |                     | 千寻                 | qxwz 高精度定位应用本软件包是集成千寻位置差分sdk             |
| [rt_cjson_tools](https://github.com/maplerian/rt_cjson_tools) | JSON                |                      | 用于 RT-Thread 的 cJSON工具库                                |
| [SMTP_CLIENT](https://github.com/WKJay/SMTP_CLIENT)          | SMTP                |                      | SMTP邮件发送软件包，简单易用，支持普通25端口及465/587加密端口 |
| [tcpserver](https://github.com/Guozhanxin/tcpserver)         | tcp                 |                      | 一个支持多客户端的 TCP 服务器                                |
| [umqtt](https://github.com/RT-Thread-packages/umqtt)         | MQTT                |                      | 一个轻量级、功能强大、可定制、易于使用和可嵌入的RT-Thread mqtt客户端 |
| [wayz_iotkit](https://github.com/wayz-iot/wayz_iotkit)       | IOT                 | 机智云               | wayz iot 定位软件包                                          |
| [webclient](https://github.com/RT-Thread-packages/webclient) | HTTPS               |                      | RT-Thread 官方开源的 http/https 协议客户端                   |
| [webnet](https://github.com/RT-Thread-packages/webnet)       | HTTP                | Web 服务器           | RT-Thread 官方开源的、轻量级、可定制嵌入式 Web 服务器        |
| [wiznet](https://github.com/RT-Thread-packages/wiznet)       | WIZnet              | W5500                | WIZNet TCP/IP 芯片（例如： W5500/W5100）的 SAL 框架对接实现  |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |
|                                                              |                     |                      |                                                              |



## language

这个软件包主要是一些支持嵌入式的编程语言的支持，并不依赖特定平台

| 包名                                                         | 技术标签   | 依赖平台 | 备注                                       |
| ------------------------------------------------------------ | ---------- | -------- | ------------------------------------------ |
| [jerryscript](https://github.com/RT-Thread-packages/jerryscript) | JavaScript | ALL      | 轻量级的JavaScript引擎                     |
| [Lua](https://github.com/liu2guang/Lua2RTT)                  | lua        | ALL      | Lua库, 目的是无缝嵌入RTT, 无需开发者去移植 |
| [micropython](https://github.com/RT-Thread-packages/micropython) | python     | ALL      | `MicroPython` 移植                         |



## misc

| 包名                                                         | 技术标签 | 依赖平台     | 备注                                                         |
| ------------------------------------------------------------ | -------- | ------------ | ------------------------------------------------------------ |
| [canfestival-rtt](https://github.com/gbcwbz/canfestival-rtt) | CAN      | CAN  hwtimer | (开源的 CANopen 协议栈)在 RT-Thread 系统上的移植             |
| [DigitalCtrl](https://github.com/xuzhuoyi/DigitalCtrl)       | PID      |              | DigitalCtrl 是一个数字控制算法库                             |
| [FlexibleButton](https://github.com/murphyzhao/FlexibleButton) | GPIO     | Pandora      | 小巧灵活的按键驱动程序                                       |
| [ MultiButton](https://github.com/liu2guang/MultiButton)     | GPIO     | ANY          | 一个小巧易用的事件驱动按钮驱动模块                           |
| [TensorflowLiteMicro](https://github.com/QingChuanWS/TensorflowLiteMicro) | AI       | ART-Pi       | 用于rt-thread操作系统的轻量级深度学习端侧推理框架Tensorflow Lite软件包。" |
| [TinyFrame](https://github.com/XXXXzzzz000/TinyFrame)        | 通信协议 |              | 应用于串口设备（如 UART / RS232)的构建或者解析的库           |
| [armv7m_dwt](https://github.com/sogwms/armv7m_dwt)           | DWT      | TIMER        | armv7m_dwt 高精度计时与延时                                  |
| [crclib](https://github.com/qiyongzhong0/crclib)             | CRC      | ANY          | 一个包含8位、16位、32位CRC校验计算的函数库                   |
| [dstr](https://github.com/RT-Thread-packages/dstr)           | STR      | ANY          | 用 C 编写的动态字符串库                                      |
| [eLapack](https://github.com/wuhanstudio/eLapack)            | MATLAB   | ANY          | 嵌入式线性代数库，兼容 matlab                                |
| [fastlz](https://github.com/RT-Thread-packages/fastlz)       | ZIP      | ANY          | 一款极速的压缩                                               |
| games                                                        | GAME     | ANY          | [c2048](https://github.com/mysterywolf/c2048)    、[俄罗斯方块](https://github.com/volatile-static/rtt_tetris)  、[贪吃蛇](https://github.com/mysterywolf/snake)、 [threes](https://github.com/mysterywolf/threes) |
| [hello](https://github.com/RT-Thread-packages/hello)         | SAMPLE   |              | RT-Thread 软件包示例                                         |
| [kendryte-demo](https://github.com/BernardXiong/kendryte-demo) | K210     | Kendryte     | 配合Kendryte SDK而简单移植的demo软件包                       |
| [ki](https://github.com/mysterywolf/ki)                      | VIM      |              | ki是一个带有语法高亮的终端编辑器，支持C/C++ Python Javascript Go语言语法高亮 |
| [rt-libann](https://github.com/wuhanstudio/rt-libann)        | AI       | ANY          | 轻量级 ANN 库，可以训练，保存和导入模型                      |
| [libcsv](https://github.com/liu2guang/libcsv)                | CSV      |              | libcsv是用纯ANSI C89编写的小型、简单、快速的CSV库，支持读写CSV数据 |
| [lwgps2rtt](https://github.com/orange2348/lwgps2rtt)         | lwgps    | GPS          | 轻量级GPS NEMA协议解析器                                     |
| [lzma](https://github.com/RiceChen/lzma)                     | ZIP      |              | 高压缩率的压缩库                                             |
| [miniLZO](https://github.com/RT-Thread-packages/miniLZO)     | ZIP      |              | LZO 是一个实时数据压缩库，而 miniLZO 是 LZO 压缩库的精简版本 |
| [nnom](https://github.com/majianjia/nnom)                    | AI       |              | NNoM是一个专门为了神经网络在 MCU 上运行的框架                |
| [optparse](https://github.com/liu2guang/optparse)            | CMD      |              | optparse是一个开源, 可移植的, 可重入的和可嵌入的类getopt命令行参数解析器 |
| [quicklz](https://github.com/RT-Thread-packages/quicklz)     | ZIP      |              | 世界上速度最快的压缩库                                       |
| samples                                                      | SAMPLE   |              | [filesystem-sample](https://github.com/RT-Thread-packages/filesystem-sample)、[kernel-sample](https://github.com/RT-Thread-packages/kernel-sample)、[network-sample](https://github.com/RT-Thread-packages/network-sample)  、[peripheral-sample](https://github.com/RT-Thread-packages/peripheral-sample) |
| [state_machine](https://github.com/redocCheng/state_machine) | STATE    |              | 一个用C语言实现功能丰富但简单的有限状态机（FSM）             |
| [uKal](https://github.com/wuhanstudio/uKal)                  |          |              | 微型卡尔曼滤波器库                                           |
| [uLAPack](https://github.com/wuhanstudio/uLAPack)            | MATH     |              | 嵌入式线性代数库                                             |
| [upacker](https://github.com/aeo123/upacker)                 | 通信协议 |              | 用于端对端通讯数据封包、解包，解决各种粘包、分包问题。极简内存占用。 |
| [uparam](https://github.com/aeo123/uparam)                   | OTP      | param        | 系统参数读写管理和持久化                                     |
| [vi](https://github.com/RT-Thread-packages/vi)               | VI       |              | vi 编辑器在 RT-Thread 操作系统上的移植                       |
| [vt100](https://github.com/wuhanstudio/vt100)                | MSH      |              | 串口终端绘图库，可以在 msh 下画图                            |
| [zlib](https://github.com/RT-Thread-packages/zlib)           | ZLIB     |              | Zlib通用数据压缩库                                           |



## multimedia

多媒体库

| 包名                                                         | 技术标签    | 依赖平台        | 备注                         |
| ------------------------------------------------------------ | ----------- | --------------- | ---------------------------- |
| [mupdf](https://github.com/rtoslab/mupdf-rtt)                | pdf         | ALL             | 轻量级PDF，XPS和电子书查看器 |
| [openmv](https://github.com/RT-Thread-packages-by-SummerGift/openmv) | openmv      | openmv          | openmv 在 RT-Thread 上的移植 |
| [STemWin](https://github.com/loogg/STemWin)                  | STemWin,gui | ST              | STemWin在RT-Thread上的移植   |
| [TJpgDec](https://github.com/RT-Thread-packages/TJpgDec)     | jpeg        | all             | jpeg解码库                   |
| [wavplayer](https://github.com/RT-Thread-packages/wavplayer) | WAV media   | RT-Thread Audio | 格式的音乐播放器             |



## peripherals

## security

这个类是存放一些加密库

| 包名                                                         | 技术标签  | 依赖平台 | 备注                                         |
| ------------------------------------------------------------ | --------- | -------- | -------------------------------------------- |
| [libsodium](https://github.com/RT-Thread-packages/libsodium) | crypto    | ALL      | 一个现代的、易用的加密库                     |
| [mbedtls](https://github.com/RT-Thread-packages/mbedtls)     | ARMmbed   | ALL      | 一个由 ARM 公司开源和维护的 SSL/TLS 算法库。 |
| [tinycrypt](https://github.com/RT-Thread-packages/tinycrypt) | tinycrypt | ALL      | 一个简小并且可配置的加解密软件包             |
| [trusted-firmware-m](https://github.com/RT-Thread-packages/trusted-firmware-m) | trusted   | Cortex M | Cortex M系列架构安全固件                     |
| [yd_crypto](https://github.com/china-hai/yd_crypto)          | yd_crypto | ALL      | 软件加密库                                   |



## system



## tools







## 有趣的软件包

###  game

https://github.com/RT-Thread/packages/tree/master/misc/games

### sample

https://github.com/RT-Thread/packages/tree/master/misc/samples