# RTTHREAD软件包目录自分类

这边统计下RTTHREAD软件包的各项内容

## AI 相关的软件包

| 包名                                                         | 技术标签 | 依赖平台             | 备注                                                         | 分类                 |
| ------------------------------------------------------------ | -------- | -------------------- | ------------------------------------------------------------ | -------------------- |
| [TensorflowLiteMicro](https://github.com/QingChuanWS/TensorflowLiteMicro) | AI       | ART-Pi               | 用于rt-thread操作系统的轻量级深度学习端侧推理框架Tensorflow Lite软件包。" | 太大                 |
| [rt-libann](https://github.com/wuhanstudio/rt-libann)        | AI       | ANY                  | 轻量级 ANN 库，可以训练，保存和导入模型                      | 需要文件系统         |
| [nnom](https://github.com/majianjia/nnom)                    | AI       |                      | NNoM是一个专门为了神经网络在 MCU 上运行的框架                | 没有sample           |
| [onnx-backend](https://github.com/wuhanstudio/onnx-backend)  | AI       | ******************** | 开源神经网络模型 onnx 后端，支持几乎所有主流机器学习模型     | 有个简单的可以学一下 |
| [rt-onnx-parser](https://github.com/wuhanstudio/rt-onnx-parser) | AI       |                      | 开源神经网络模型 onnx 解析库                                 |                      |
|                                                              |          |                      |                                                              |                      |

##  log相关的软件包

| 包名                                                         | 技术标签 | 依赖平台 | 备注                                                    | 分类 |
| ------------------------------------------------------------ | -------- | -------- | ------------------------------------------------------- | ---- |
| [EasyLogger](https://github.com/armink-rtt-pkgs/EasyLogger)  | LOG      |          | 一款超轻量级(ROM<1.6K, RAM<0.3k)、高性能的 C/C++ 日志库 |      |
| [logmgr](https://github.com/RT-Thread-packages/logmgr)       | LOG      |          | logmgr: 日志管理系统功能支持                            |      |
| [ulog_easyflash](https://github.com/armink-rtt-pkgs/ulog_easyflash) | LOG      | ALL      | 基于 EasyFlash 的 ulog 插件                             |      |
| [ulog_file](https://github.com/RT-Thread-packages/ulog_file) | LOG      |          | ulog_file: 基于文件系统的 ulog 后端插件。               |      |

## 文件系统软件包

| 包名                                                         | 技术标签 | 依赖平台 | 备注                                                         | 分类 |
| ------------------------------------------------------------ | -------- | -------- | ------------------------------------------------------------ | ---- |
| [littlefs](https://github.com/geniusgogo/littlefs)           | littlefs |          | 为微控制器设计的一个小型的且掉电安全的文件系统               |      |
| [lwext4](https://github.com/Michael0066/lwext4)              | FLASH    | ALL      | Flash 抽象层的实现，负责管理 Flash 设备和 Flash 分区         |      |
| [fal](https://github.com/RT-Thread-packages/fal)             | **       | u8g2     | U8g2 不同种类单色屏驱动在 RT-Thread 移植库                   |      |
| [ramdisk](https://github.com/majianjia/ramdisk)              | 文件系统 | RAM      | ramdisk除了能被文件系统格式化，还能当一般的块设备来存储数据。 |      |
| [yaffs2_rtt_port](https://github.com/heyuanjie87/yaffs2_rtt_port) | 文件系统 | yaffs    | yaffs2 移植到RT-Thread                                       |      |
|                                                              |          |          |                                                              |      |
|                                                              |          |          |                                                              |      |
|                                                              |          |          |                                                              |      |
|                                                              |          |          |                                                              |      |
|                                                              |          |          |                                                              |      |

## GUI 引擎软件包

| 包名                                                         | 技术标签    | 依赖平台 | 备注                                                         | 分类 |
| ------------------------------------------------------------ | ----------- | -------- | ------------------------------------------------------------ | ---- |
| [STemWin](https://github.com/loogg/STemWin)                  | STemWin,gui | ST       | STemWin在RT-Thread上的移植                                   |      |
| [lkdGui](https://github.com/guoweilkd/lkdGui)                | GUI         |          | lkdGui是一款为单色显示屏制作的图形化界面，用于设计简单漂亮的图形界面。 |      |
| [rt-u8g2](https://github.com/wuhanstudio/rt-u8g2)            | **          | u8g2     | U8g2 不同种类单色屏驱动在 RT-Thread 移植库                   |      |
| [LittlevGL2RTT](https://github.com/liu2guang/LittlevGL2RTT)  | GUI         | LITTVGL  | Littlevgl 是基于 RT-Thread 的图形库软件包                    |      |
| [cairo](https://github.com/RT-Thread-packages/cairo)         | GUI         | LCD      | 适用于多平台的 2D 图形软件包                                 |      |
| [persimmon](https://github.com/RT-Thread-packages/persimmon) | UI          | 柿饼     | RT-Thread 的柿饼 UI                                          |      |
| [nes](https://gitee.com/Ghazi_gq/nes)                        | GAME        | GUI      | nes模拟器c库                                                 |      |
|                                                              |             |          |                                                              |      |
|                                                              |             |          |                                                              |      |





## 好玩的没有依赖的软件包

| 包名                                          | 技术标签 | 依赖 | 备注                                                         | 验证情况 | 分类 |
| --------------------------------------------- | -------- | ---- | ------------------------------------------------------------ | -------- | ---- |
| [vt100](https://github.com/wuhanstudio/vt100) | MSH      |      | 串口终端绘图库，可以在 msh 下画图                            | 已验证   | misc |
| games                                         | GAME     | ANY  | [c2048](https://github.com/mysterywolf/c2048)    、[俄罗斯方块](https://github.com/volatile-static/rtt_tetris)  、[贪吃蛇](https://github.com/mysterywolf/snake)、 [threes](https://github.com/mysterywolf/threes) |          | misc |
|                                               |          |      |                                                              |          |      |

## 



## LED BUTTON 软件包



