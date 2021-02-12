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
| [samples](https://github.com/RT-Thread/packages/tree/master/misc/samples) | SAMPLE   |              | [filesystem-sample](https://github.com/RT-Thread-packages/filesystem-sample)、[kernel-sample](https://github.com/RT-Thread-packages/kernel-sample)、[network-sample](https://github.com/RT-Thread-packages/network-sample)  、[peripheral-sample](https://github.com/RT-Thread-packages/peripheral-sample) |
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

| 包名                                                         | 技术标签   | 依赖平台                                         | 备注                                                         |
| ------------------------------------------------------------ | ---------- | ------------------------------------------------ | ------------------------------------------------------------ |
| [LedBlink](https://github.com/aeo123/LedBlink)               | LED        | GPIO                                             | 简单易用led闪烁控制软件包                                    |
| [MotionDriver2RTT](https://github.com/greedyhao/MotionDriver2RTT) | Motion     | MPU-6050                                         | 移植 MotionDriver 到 RTT 的包                                |
| [paj7620](https://github.com/orange2348/paj7620)             |            | PAJ7620                                          | 手势传感器PAJ7620的驱动包                                    |
| [SignalLed](https://github.com/WKJay/SignalLed)              | GPIO       | LED                                              | 信号灯软件包，支持自定义闪烁方式、周期，支持随时开启、关闭   |
| [rt-ad7746](https://github.com/wuhanstudio/rt-ad7746)        |            | AD7746                                           | AD7746 高精度电容测量芯片在 RT-Thread 移植库                 |
| [agile_button](https://github.com/loogg/agile_button)        | GPIO       | BUTTON                                           | 一个灵活的button软件包                                       |
| [agile_console](https://github.com/loogg/agile_console)      | CONSOLE    | UART                                             | 一个灵活的console设备软件包                                  |
| [agile_led](https://github.com/loogg/agile_led)              | GPIO       | LED                                              | 一个灵活的led软件包。                                        |
| [as608](https://github.com/greedyhao/as608)                  |            | AS608                                            | AS608 指纹模块的驱动                                         |
| [as7341](https://github.com/RiceChen/as7341)                 | I2C        | AS7341                                           | AS7341可见光传感器，可测量8个波长的可见光                    |
| [at24cxx](https://github.com/XiaojieFan/at24cxx)             | eeprom     | at24c02,                                         | eeprom at24cxx 的驱动库。                                    |
| [ rtt-pkgs-beep](https://github.com/Sunwancn/rtt-pkgs-beep)  | PIN,PWM    |                                                  | 基于 rt-thread 的 pin 和 pwm 驱动的蜂鸣器控制软件包，可以容易地驱动有源蜂鸣器或无源蜂鸣器，产生各种间隔长短的鸣叫声。 |
| [rtpkg_button](https://github.com/jiejieTop/rtpkg_button)    | GPIO       | BUTTON                                           | C 实现的按键驱动，支持单击和双击，长按，长按释放"            |
| [rt_can_ymodem](https://github.com/redocCheng/rt_can_ymodem) | YMODEM     | CAN                                              | 连接can设备和ymodem的驱动包                                  |
| [dm9051](https://github.com/aozima/dm9051)                   |            | DM9051                                           | DM9051 SPI 接口以太网芯片驱动                                |
| [rtt-pkgs-easyblink](https://github.com/Sunwancn/rtt-pkgs-easyblink) | GPIO       | LED                                              | 小巧轻便的 LED 控制软件包，可以容易地控制 LED 开、关、反转和各种间隔闪烁，占用 RAM 少，支持 RT-Thread 标准版和 Nano 版。 |
| [embarc_bsp](https://github.com/foss-for-synopsys-dwc-arc-processors/embarc_bsp) | SDK        | Synopsys                                         | Synopsys ARC 处理器 板级支持包                               |
| [rt-i2c-tools](https://github.com/wuhanstudio/rt-i2c-tools)  | I2C        |                                                  | I2C 调试时可以使用的小工具，可以扫描设备，读写寄存器         |
| [icm20608](https://github.com/RT-Thread-packages/icm20608)   | I2C        | icm20608                                         | 三轴加速度与三轴陀螺仪 icm20608 的传感器驱动库               |
| [infrared_framework](https://github.com/RT-Thread-packages/infrared_framework) | PIN PWM    | 红外                                             | 基于 rt-thread 的 pin,pwm 和 hwtimer 驱动的红外框架          |
| [kendryte_sdk](https://github.com/RT-Thread-packages/kendryte_sdk) | SDK        | K210                                             | 勘智 K210 处理器对应的外设驱动包                             |
| [ ld3320](https://github.com/xqyjlj/ld3320)                  | PIN \|SPI  | LD3320                                           | LD3320语音识别芯片                                           |
| [rtt-littled](https://github.com/luhuadong/rtt-littled)      | PIN        | LED                                              | littled软件包: Littled LED Daemon 服务线程                   |
| [lkdGui](https://github.com/guoweilkd/lkdGui)                | GUI        |                                                  | lkdGui是一款为单色显示屏制作的图形化界面，用于设计简单漂亮的图形界面。 |
| [lora-radio-driver](https://github.com/Forest-Rain/lora-radio-driver) | LORA       | SX126x                                           | lora芯片(SX126x\\SX127x)驱动包                               |
| [ly68l6400](https://github.com/Ghazigq/ly68l6400)            | SPI RAM    | ly68l6400                                        | ly68l6400芯片的驱动                                          |
| [MAX17048](https://github.com/aeo123/MAX17048)               | I2C        | MAX17048                                         | 电池监测芯片                                                 |
| [max7219](https://github.com/redocCheng/max7219)             | SPI        | MAX7219                                          | 本软件包是在数码管上应用 MAX7219 的驱动包                    |
| [multi-rtimer](https://github.com/Forest-Rain/multi-rtimer)  | 低功耗     |                                                  | 一个实时、低功耗软件定时器模块                               |
| [nes](https://gitee.com/Ghazi_gq/nes)                        | GAME       | GUI                                              | nes模拟器c库                                                 |
| [nrf24l01](https://github.com/sogwms/nrf24l01)               | 2.4G       | nRF24L01                                         | 单芯片 2.4GHz 无线收发器                                     |
| [nrf5x_sdk](https://github.com/supperthomas/nrf5x_sdk)       | VENDOR     | nordic                                           | Nordic SDK软件开发包nRF5_SDK_16                              |
| [nrfx](https://github.com/xckhmf/nrfx)                       | VENDOR     | nordic                                           | Nordic SOC的独立外设驱动库                                   |
| [nuclei-sdk](https://github.com/Nuclei-Software/nuclei-sdk)  | VENDOR     | Nuclei SDK                                       | 芯来科技RISC-V处理器软件开发包                               |
| [pca9685](https://github.com/greedyhao/pca9685)              | I2C        | PCA9685                                          | 通过I2C总线控制的16路PWM控制器                               |
| [pcf8574](https://github.com/RT-Thread-packages/pcf8574)     | I2C        | pcf8574                                          | 针对 I2C 并行口扩展 8 位 I/O 软件包                          |
| [pms_series](https://github.com/MrpYoung/pms_series)         | uart       | pms_series                                       | pms 数字式通用颗粒物浓度传感器驱动库                         |
| [rt-thread-qkey](https://github.com/qiyongzhong0/rt-thread-qkey) | GPIO       | BUTTON                                           | 一个快捷易用的按键驱动包                                     |
| [rt-thread-qled](https://github.com/qiyongzhong0/rt-thread-qled) | GPIO       | LED                                              | 一个快捷易用的led驱动包                                      |
| [rc522_rtt](https://github.com/greedyhao/rc522_rtt)          | SPI        | RC522                                            | rc522 rfid 模块驱动                                          |
| [realtek_ameba](https://github.com/flyingcys/realtek_ameba)  | VENDOR     | AMEBA                                            | realtek 的 ameba 软件包在 RT-Thread 上的移植                 |
| [rt-rosserial](https://github.com/wuhanstudio/rt-rosserial)  | UART;TCP   | ROS                                              | 机器人操作系统(ROS) 软件包 rosserial 在 RT-Thread 的移植库   |
| [rplidar](https://github.com/wuhanstudio/rplidar)            | uart       | 激光雷达                                         | RPLIDAR: 适用于机器人室内建图的低成本激光雷达                |
| [rt-thread-rs485](https://github.com/qiyongzhong0/rt-thread-rs485) | serial pin | RS485                                            | rs485驱动包                                                  |
| rtc                                                          | RTC        | [rtt-rx8900](https://github.com/Prry/rtt-rx8900) | 外置RTC驱动，支持实时时钟和闹钟功能 [rtt-ds3231](https://github.com/Prry/rtt-ds3231) |
| [SENSOR](https://github.com/RT-Thread/packages/tree/master/peripherals/sensors)  ********** | ********** | **********                                       | sensor大框架                                                 |
| [tt-sgm706](https://github.com/Prry/rtt-sgm706)              | WDG        | sgm706                                           | SGM706独立看门狗驱动软件包                                   |
| [sht2x](https://github.com/RT-Thread-packages/sht2x)         | I2C        | sh2x                                             | 数字湿度和温度传感器 sht2x 驱动软件包[sht3x](https://github.com/donghao2nanjing/sht3x) |
| [stm32_sdio](https://github.com/RT-Thread-packages/stm32_sdio) | SDIO       | STM32L4                                          | 这是一个STM32平台 SDIO控制器驱动包                           |
| [rtt-ssd1306](https://github.com/luhuadong/rtt-ssd1306)      | OLED       | SSD1309                                          | 基于 SSD1306、SH1106、SH1107 和 SSD1309 的 OLED 驱动，支持 I2C 和 SPI |
| [sx12xx](https://github.com/XiaojieFan/sx12xx)               | LORA       | SX12XX                                           | Semtech LoRa RF 芯片驱动库                                   |
| [TOUCH](https://github.com/RT-Thread/packages/tree/master/peripherals/touch)  ********** | ********** | **********                                       | TOUCH 驱动                                                   |
| [rt-u8g2](https://github.com/wuhanstudio/rt-u8g2)            | **         | u8g2                                             | U8g2 不同种类单色屏驱动在 RT-Thread 移植库                   |
| [vdevice](https://github.com/RT-Thread-packages/vdevice)     | GPIO/LCD   | VIRTUAL                                          | 适配于rt-thread device框架下的虚拟IO设备                     |
| [vsensor](https://github.com/RT-Thread-packages/vsensor)     | SENSOR     | VIRTUAL                                          | 虚拟传感器设备                                               |
| [wk2124](https://github.com/MrMichael/wk2124)                | SPI        | wk2124                                           | wk2124 spi转四串口芯片的驱动库。                             |
| [rtpkg-wm_libraries](https://github.com/WinnerMicro/rtpkg-wm_libraries) | WIFI       | W60X                                             | WinnerMicro 芯片软件支持包                                   |
| [rt_ws2812b](https://github.com/maplerian/rt_ws2812b)        | SPI + DMA  | ws2812b                                          | 用于 RT-Thread 的 ws2812b 软件驱动包，使用 SPI + DMA 方式驱动。 |
|                                                              |            |                                                  |                                                              |



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

| 包名                                                         | 技术标签   | 依赖平台   | 备注                                                         |
| ------------------------------------------------------------ | ---------- | ---------- | ------------------------------------------------------------ |
| [CMSIS](https://github.com/RT-Thread-packages/CMSIS)         | CMSIS      | ARM        | CMSIS 软件包在 RT-Thread 上的移植                            |
| [EV](https://github.com/sogwms/EV)                           |            | vehicles   | 效开发 vehicles(包括无人机) 的框架                           |
| [FlashDB](https://github.com/armink/FlashDB)                 | FLASH      | ALL        | 一款支持 KV 数据和时序数据的轻量级数据库                     |
| [LittlevGL2RTT](https://github.com/liu2guang/LittlevGL2RTT)  | GUI        | LITTVGL    | Littlevgl 是基于 RT-Thread 的图形库软件包                    |
| [UCOS](https://github.com/RT-Thread/packages/tree/master/system/Micrium) | UCOS       |            | UCOS组件大包                                                 |
| [Ppool](https://github.com/mysterywolf/Ppool)                | POOL       | ALL        | 基于pthread的线程池库                                        |
| [Qfplib-M0-full](https://github.com/mysterywolf/Qfplib-M0-full) |            |            | Cortex-M0浮点运算汇编加速库(full版) [Qfplib-M3](https://github.com/mysterywolf/Qfplib-M3) |
| [cairo](https://github.com/RT-Thread-packages/cairo)         | GUI        | LCD        | 适用于多平台的 2D 图形软件包                                 |
| [fal](https://github.com/RT-Thread-packages/fal)             | FLASH      | ALL        | Flash 抽象层的实现，负责管理 Flash 设备和 Flash 分区         |
| [gui_engine](https://github.com/RT-Thread-packages/gui_engine) |            |            | 来自 RT-Thread 官方的 GUI 引擎                               |
| [littlefs](https://github.com/geniusgogo/littlefs)           | littlefs   |            | 为微控制器设计的一个小型的且掉电安全的文件系统               |
| [lwext4](https://github.com/Michael0066/lwext4)              | fs         |            | 适合微控制器的 ext2 / 3/4文件系统的实现                      |
| [minIni](https://github.com/hichard/minIni)                  | INI        | 配置       | minIni 在 RT-Thread 上移植的软件包，用于读取和写入“ .INI”文件 |
| [openamp](https://github.com/bigmagic123/openamp)            | AMP        | 非堆成多核 | RT-Thread OpenAMP软件包                                      |
| [partition](https://github.com/RT-Thread-packages/partition) |            |            | 一个基于块设备的分区管理软件包                               |
| [persimmon](https://github.com/RT-Thread-packages/persimmon) | UI         | 柿饼       | RT-Thread 的柿饼 UI                                          |
| [pixman](https://github.com/RT-Thread-packages/pixman)       | pix        |            | 提供低等级像素控制的库                                       |
| [plccore](https://github.com/hyafz/plccore)                  | PLC        | IEC61131   | plccore 在 RT-Thread 上移植的软件包                          |
| [rt-thread-qboot](https://github.com/qiyongzhong0/rt-thread-qboot) | BootLoader | boot       | qboot ：一个用于快速制作bootloader的组件                     |
| [ramdisk](https://github.com/majianjia/ramdisk)              | 文件系统   | RAM        | ramdisk除了能被文件系统格式化，还能当一般的块设备来存储数据。 |
| [rt-robot](https://github.com/RT-Thread-packages/rt-robot)   |            |            | RT-Thread 机器人平台                                         |
| [rt_memcpy_cm](https://github.com/mysterywolf/rt_memcpy_cm)  | memcpy     |            | rt_memcpy函数的Cortex-M内核汇编加速版                        |
| [rt_printf](https://github.com/mysterywolf/rt_printf)        | printf     |            | 线程安全版本的rt_kprintf                                     |
| [rti](https://github.com/RT-Thread-packages/rti)             |            |            | RT-Thread 展示系统内部运行信息的组件，能够帮助分析系统内部情况 |
| [SQLite](https://github.com/RT-Thread-packages/SQLite)       | SQLITE     | SQL        | SQLite 是一个完备、高度可靠、嵌入型、全功能、公共领域的 SQL 数据库引擎", |
| [sys_load_monitor](https://github.com/armink-rtt-pkgs/sys_load_monitor) | MONITOR    |            | 一款轻量级的系统负荷监视器                                   |
| [rt-thread-syswatch](https://github.com/qiyongzhong0/rt-thread-syswatch) | SYSWATCH   |            | 系统看守：一个用于保障系统长期正常运行的组件                 |
| [thread_pool](https://github.com/armink-rtt-pkgs/thread_pool) | pool       |            | 基于 RT-Thread 的线程池实现"                                 |
| [yaffs2_rtt_port](https://github.com/heyuanjie87/yaffs2_rtt_port) | 文件系统   | yaffs      | yaffs2 移植到RT-Thread                                       |
|                                                              |            |            |                                                              |
|                                                              |            |            |                                                              |



## tools

| 包名                                                         | 技术标签    | 依赖平台 | 备注                                                         |
| ------------------------------------------------------------ | ----------- | -------- | ------------------------------------------------------------ |
| [Chinese_font_library](https://github.com/lxzzzzzxl/Chinese_font_library) | FONT        | FAL      | rt-thread中文字库软件包                                      |
| [CmBacktrace](https://github.com/armink-rtt-pkgs/CmBacktrace) | DEBUG       | ARM      | ARM Cortex-M 系列 MCU 错误追踪库                             |
| [coremark](https://github.com/wuhanstudio/coremark)          | Coremark    |          | EEMBC 的单片机性能测试小工具 [跑分排名](https://www.eembc.org/coremark/scores.php) |
| [dhrystone](https://github.com/wuhanstudio/dhrystone)        |             |          | Dhrystone 单片机性能测试小工具                               |
| [EasyFlash](https://github.com/armink-rtt-pkgs/EasyFlash)    |             |          | 轻量级嵌入式 Flash 存储器库KV 数据库                         |
| [EasyLogger](https://github.com/armink-rtt-pkgs/EasyLogger)  | LOG         |          | 一款超轻量级(ROM<1.6K, RAM<0.3k)、高性能的 C/C++ 日志库      |
| [MemoryPerf](https://github.com/SummerLife/MemoryPerf)       | performance |          | ARM CPU 内存性能测试。                                       |
| [SEGGER_SystemView](https://github.com/RT-Thread-packages/SEGGER_SystemView) | RTT         | SEGGER   | SEGGER 的 SystemView 移植                                    |
| [UrlEncode](https://github.com/jch12138/UrlEncode)           | URL         |          | 一个简单易用的Url编解码工具                                  |
| [adbd](https://github.com/heyuanjie87/adbd)                  | ADB         |          | 在 RT-Thread 上实现的 Android ADB daemon                     |
| [bs8116a](https://github.com/illusionlee/bs8116a)            |             | bs8116a  | 合泰的bs8116a-3的触摸按键芯片                                |
| [cpu_usage](https://github.com/enkiller/cpu_usage)           | CPU         |          | CPUU: CPU 使用率统计小工具。                                 |
| [gbk2utf8](https://gitee.com/Ghazi_gq/gbk2utf8)              | FONT        |          | GBK与UTF8编码之间的转换                                      |
| [gps_rmc](https://github.com/maplerian/gps_rmc)              | GPS         |          | 用于解析GPS模块的 $XXRMC 类型数据                            |
| [kdb](https://github.com/RT-Thread-packages/kdb)             | DEBUG       | ALL      | 内核检测漏洞工具                                             |
| [logmgr](https://github.com/RT-Thread-packages/logmgr)       | LOG         |          | logmgr: 日志管理系统功能支持                                 |
| [lunar_calendar](https://github.com/illusionlee/lunar_calendar) | 日历        |          | 将阳历日期转换为阴历的工具。                                 |
| [lwrb2rtt](https://github.com/Jackistang/lwrb2rtt)           |             |          | 轻量级的 FIFO 环形缓冲区                                     |
| [rttpkg-mbedtls_bench](https://github.com/xfan1024/rttpkg-mbedtls_bench) | mbedtls     |          | mbedtls 性能测试                                             |
| [nr_micro_shell](https://github.com/Nrusher/nr_micro_shell)  | SHELL       |          | 轻量的命令行交互工具。                                       |
| [qrcode](https://github.com/RT-Thread-packages/qrcode)       | QR          |          | 一个用于将字符串生成二维码的软件包                           |
| [rdb](https://github.com/RT-Thread-packages/rdb)             |             |          | 基于 USB/TCP等可靠通信协议的远程调试桥。                     |
| [uMCN](https://github.com/JcZou/uMCN)                        | MQTT        | ALL      | uMCN是一个基于发布者/订阅者模式的轻量级且功能强大的跨进程通信库。 |
| [ulog_easyflash](https://github.com/armink-rtt-pkgs/ulog_easyflash) | LOG         | ALL      | 基于 EasyFlash 的 ulog 插件                                  |
| [ulog_file](https://github.com/RT-Thread-packages/ulog_file) | LOG         |          | ulog_file: 基于文件系统的 ulog 后端插件。                    |
| [vconsole](https://github.com/enkiller/vconsole)             | VCONSOLE    | ALL      | 一个虚拟控制台软件包。                                       |
| [wasm-micro-runtime](https://github.com/bytecodealliance/wasm-micro-runtime) |             |          | WebAssembly微型运行时（WAMR）是占地面积小的独立WebAssembly（WASM） |



###  game

https://github.com/RT-Thread/packages/tree/master/misc/games

### sample

https://github.com/RT-Thread/packages/tree/master/misc/samples





TODO LIST

- licence 确认
- 软件包是否可以用确认



## 软件包分类

### 平台完全无关性

该软件包完全不依赖任何硬件，只要rtthread跑起来就可以跑

### 文件系统相关性软件包

该软件包需要依赖文件系统才可以运行

### 简单GPIO LED 依赖性软件包

该软件包需要依赖GPIO小灯或者BUTTON来运行的软件包

### I2C依赖性软件包

该软件包需要依赖I2C

### SPI 依赖性软件包

该软件包需要依赖SPI

### 完全硬件相关性软件包

该软件包必须要特定硬件支持

### AI 相关的软件包





### LOG



### 文件系统



