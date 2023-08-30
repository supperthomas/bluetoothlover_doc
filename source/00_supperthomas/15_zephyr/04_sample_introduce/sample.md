# ZEPHYR example介绍

https://docs.zephyrproject.org/latest/samples/sample_definition_and_criteria.html

## sample_definition_and_criteria

sample 样例的标准和定义

## class Sample

经典样例， 可以运行在任意平台

- [Hello World](https://docs.zephyrproject.org/latest/samples/hello_world/README.html)    最简单的hello world
- [Synchronization Sample](https://docs.zephyrproject.org/latest/samples/synchronization/README.html)    线程同步问题
- [Dining Philosophers](https://docs.zephyrproject.org/latest/samples/philosophers/README.html)    哲学家就餐问题

## basic sample

基本sample

- [Blinky](https://docs.zephyrproject.org/latest/samples/basic/blinky/README.html)   LED 灯闪烁
- [PWM Blinky](https://docs.zephyrproject.org/latest/samples/basic/blinky_pwm/README.html)   用PWM 进行LED灯闪烁
- [Button](https://docs.zephyrproject.org/latest/samples/basic/button/README.html) 一个简单的按钮演示，展示了 GPIO 输入和中断的使用。每次按下按钮时，该示例都会向控制台打印一条消息。
- [GPIO with custom devicetree binding](https://docs.zephyrproject.org/latest/samples/basic/custom_dts_binding/README.html)

在 Zephyr 中，所有特定于硬件的配置都在设备树中描述。

因此，GPIO 引脚也在设备树中进行配置，并使用兼容分配给特定用途。

这与 Arduino 等其他嵌入式环境形成鲜明对比，其中 GPIO 引脚的方向（输入/输出）是在应用程序固件中配置的。

对于 LED 或按钮等典型用例，可以使用现有的[`gpio-leds`](https://docs.zephyrproject.org/latest/build/dts/api/bindings/led/gpio-leds.html#std-dtcompatible-gpio-leds)或 兼容的。[`gpio-keys`](https://docs.zephyrproject.org/latest/build/dts/api/bindings/input/gpio-keys.html#std-dtcompatible-gpio-keys)

此示例演示了如何通过自定义设备树绑定将 GPIO 引脚用于其他目的。

- [Fade LED](https://docs.zephyrproject.org/latest/samples/basic/fade_led/README.html)

LED 开始时会增加其亮度，直到完全或接近完全亮起。然后亮度逐渐降低，直至 LED 关闭，完成淡入淡出循环。每个循环需要 2.5 秒，并且循环会永远重复。PWM 周期取自 Devicetree。它应该足够快以高于闪烁融合阈值。

- [System Hashmap](https://docs.zephyrproject.org/latest/samples/basic/hash_map/README.html)

系统哈希图

这是一个简单的例子，反复

- 插入最多`CONFIG_TEST_LIB_HASH_MAP_MAX_ENTRIES`

- 最多替换先前插入的相同数字

- 删除所有先前插入的键

  

- [Minimal footprint](https://docs.zephyrproject.org/latest/samples/basic/minimal/README.html)

占地面积最小
概述
此示例提供了一个空的main()各种配置文件，可用于测量 Zephyr 在不同配置中的最小 ROM 占用空间。



- [PWM: RGB LED](https://docs.zephyrproject.org/latest/samples/basic/rgb_led/README.html)

  脉宽调制：RGB LED
  概述
  这是一个使用 PWM 驱动 RGB LED 的示例应用程序。

  RGB LED 中有 3 个单色 LED。每个 LED 组件均由 PWM 端口驱动，其中脉冲宽度从零更改为 Devicetree 中指示的周期。该周期应足够快，以高于闪烁融合阈值（LED 被感知为稳定的最小闪烁率）。该示例使每个 LED 组件从黑暗变为最大亮度。三个for循环（每个 LED 组件一个）从 RGB LED 生成一系列逐渐变化的颜色，并且示例将永远重复。

- [Servomotor](https://docs.zephyrproject.org/latest/samples/basic/servo_motor/README.html)

伺服电机
概述
这是一个使用 PWM 驱动伺服电机的示例应用程序。

该示例通过 PWM 控制信号使伺服电机在 180 度范围内来回旋转。

该应用程序针对伺服电机 ROB-09065。0 至 180 度范围内相应的 PWM 脉冲宽度分别为 700 至 2300 微秒。不同的伺服电机可能需要不同的 PWM 脉冲宽度，如果使用不同的伺服电机，您可能需要修改源代码。

- [System heap](https://docs.zephyrproject.org/latest/samples/basic/sys_heap/README.html)

系统堆
概述
一个简单的示例，可与任何支持的板一起使用，并将系统堆使用情况打印到控制台。

- [Basic Thread Example](https://docs.zephyrproject.org/latest/samples/basic/threads/README.html)

基本线程示例
概述
此示例演示了使用 生成多个线程 K_THREAD_DEFINE()。它产生三个线程。然后在编译时使用 K_THREAD_DEFINE 定义每个线程。

前两个分别控制一个 LED。这些 LEDled0和led1具有由单独功能控制的循环控制和定时逻辑。

blink0()控制led0并具有 100ms 的睡眠周期

blink1()控制led1并具有 1000ms 的睡眠周期

当这些线程中的任何一个线程切换其 LED 时，它还会将信息推送到 FIFO中，以识别线程/LED 以及已切换的次数。

第三个线程用于printk()将添加到 FIFO 的信息打印到设备控制台。

## USER SPACE

- [Hello World](https://docs.zephyrproject.org/latest/samples/userspace/hello_world_user/README.html)

你好世界
概述
一个简单的 Hello World 示例，可与任何支持的板一起使用并打印“Hello World from UserSpace!” 到控制台。如果不可用或未配置，则“特权模式下的 Hello World”。而是打印出来。

- [Producer/consumer](https://docs.zephyrproject.org/latest/samples/userspace/prod_consumer/README.html)

生产者/消费者
这是一个练习一些用户模式概念的示例应用程序。

概述
考虑一个“示例驱动程序”，它从某个未知源获取传入数据，并生成带有指向该数据的指针的中断。应用程序需要对此数据执行一些处理，然后将处理后的数据写回驱动程序。

这里的目标是证明：

多个逻辑应用程序，每个应用程序都有自己的内存域

创建 sys_heap 并分配给内存分区

使用k_queue_alloc_append()需要配置线程资源池的API

内核对象和驱动程序的权限管理

显示如何定义特定于应用程序的系统调用

显示 ISR 和应用程序之间的 IPC（使用k_msgq）以及应用程序到应用程序的 IPC（使用k_queue）

展示如何创建特定于应用程序的系统调用

- [Userspace Protected Memory](https://docs.zephyrproject.org/latest/samples/userspace/shared_mem/README.html)

用户空间保护内存
概述
此示例是运行分配有受保护分区的唯一内存域的多个线程的示例。该应用程序使用内存分区和模拟类似谜机的示例算法，但该机器的实现尚未经过验证，不应用于任何实际的安全目的。

要求
该示例依赖于子系统app_memory，并且它不会在不支持该子系统的主板上运行。该示例在以下板子 qemu_x86、frdm_k64、96b_carbon 上进行了测试。

- [Syscall performances](https://docs.zephyrproject.org/latest/samples/userspace/syscall_perf/README.html)

系统调用性能
此示例应用程序的目标是测量与直接调用函数的主管线程相比，用户线程必须经过系统调用时的性能损失。

概述
该应用程序创建一个主管和一个用户线程。然后两个线程都调用 k_current_get() 返回当前线程的引用。用户线程必须经过系统调用。

两个线程都显示调用 k_current_get() 时的核心时钟周期数和执行的指令数。

## subsys

- Controller Area Network (CAN) Bus Samples
  - [ISO-TP library](https://docs.zephyrproject.org/latest/samples/subsys/canbus/isotp/README.html)
- Console Samples
  - [console_getchar() Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/console/getchar/README.html)
  - [console_getline() Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/console/getline/README.html)
- Debug Samples
  - [Debug monitor](https://docs.zephyrproject.org/latest/samples/subsys/debug/debugmon/README.html)
  - [Fuzzing Example](https://docs.zephyrproject.org/latest/samples/subsys/debug/fuzz/README.html)
  - [GDB Debug Sample](https://docs.zephyrproject.org/latest/samples/subsys/debug/gdbstub/README.html)
- Display Samples
  - [Character frame buffer](https://docs.zephyrproject.org/latest/samples/subsys/display/cfb/README.html)
  - [Custom Fonts](https://docs.zephyrproject.org/latest/samples/subsys/display/cfb_custom_font/README.html)
  - [Character Framebuffer Shell Module Sample](https://docs.zephyrproject.org/latest/samples/subsys/display/cfb_shell/README.html)
  - [LVGL Basic Sample](https://docs.zephyrproject.org/latest/samples/subsys/display/lvgl/README.html)
- EDAC Shell Sample
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/edac/README.html#overview)
  - [Building and Running](https://docs.zephyrproject.org/latest/samples/subsys/edac/README.html#building-and-running)
  - [Sample output](https://docs.zephyrproject.org/latest/samples/subsys/edac/README.html#sample-output)
- FS Samples
  - [FS Format Sample](https://docs.zephyrproject.org/latest/samples/subsys/fs/format/README.html)
  - [Filesystems Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/fs/fs_sample/README.html)
  - [littlefs File System Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/fs/littlefs/README.html)
- Input Samples
  - [Input Dump](https://docs.zephyrproject.org/latest/samples/subsys/input/input_dump/README.html)
- IPC Samples
  - [IPC Service - icmsg - Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/ipc/ipc_service/icmsg/README.html)
  - [IPC Service - static vrings - Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/ipc/ipc_service/static_vrings/README.html)
  - [OpenAMP Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/ipc/openamp/README.html)
  - [OpenAMP Sample Application using resource table](https://docs.zephyrproject.org/latest/samples/subsys/ipc/openamp_rsc_table/README.html)
  - [RPMsg Service sample Application](https://docs.zephyrproject.org/latest/samples/subsys/ipc/rpmsg_service/README.html)
- Logging Sample
  - [Logging: BLE Backend](https://docs.zephyrproject.org/latest/samples/subsys/logging/ble_backend/README.html)
  - [Dictionary-based Logging Sample](https://docs.zephyrproject.org/latest/samples/subsys/logging/dictionary/README.html)
  - [Logging](https://docs.zephyrproject.org/latest/samples/subsys/logging/logger/README.html)
  - [MIPI Sys-T Logging Sample](https://docs.zephyrproject.org/latest/samples/subsys/logging/syst/README.html)
- LoRaWAN Samples
  - [LoRaWAN Class A Sample](https://docs.zephyrproject.org/latest/samples/subsys/lorawan/class_a/README.html)
- Management Samples
  - [Hawkbit Direct Device Integration API sample](https://docs.zephyrproject.org/latest/samples/subsys/mgmt/hawkbit/README.html)
  - [SMP Server Sample](https://docs.zephyrproject.org/latest/samples/subsys/mgmt/mcumgr/smp_svr/README.html)
  - [Open Supervised Device Protocol (OSDP)](https://docs.zephyrproject.org/latest/samples/subsys/mgmt/osdp/README.html)
  - [UpdateHub embedded Firmware Over-The-Air (FOTA) sample](https://docs.zephyrproject.org/latest/samples/subsys/mgmt/updatehub/README.html)
- Modbus Samples
  - [Modbus RTU Client Sample](https://docs.zephyrproject.org/latest/samples/subsys/modbus/rtu_client/README.html)
  - [Modbus RTU Server Sample](https://docs.zephyrproject.org/latest/samples/subsys/modbus/rtu_server/README.html)
  - [Modbus TCP to serial line gateway sample](https://docs.zephyrproject.org/latest/samples/subsys/modbus/tcp_gateway/README.html)
  - [Modbus TCP Server Sample](https://docs.zephyrproject.org/latest/samples/subsys/modbus/tcp_server/README.html)
- NVS: Non-Volatile Storage
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/nvs/README.html#overview)
  - [Requirements](https://docs.zephyrproject.org/latest/samples/subsys/nvs/README.html#requirements)
  - [Building and Running](https://docs.zephyrproject.org/latest/samples/subsys/nvs/README.html#building-and-running)
- Portability Samples
  - [Dining Philosophers (CMSIS RTOS V1 APIs)](https://docs.zephyrproject.org/latest/samples/subsys/portability/cmsis_rtos_v1/philosophers/README.html)
  - [Synchronization using CMSIS RTOS V1 APIs](https://docs.zephyrproject.org/latest/samples/subsys/portability/cmsis_rtos_v1/timer_synchronization/README.html)
  - [Dining Philosophers (CMSIS RTOS V2 APIs)](https://docs.zephyrproject.org/latest/samples/subsys/portability/cmsis_rtos_v2/philosophers/README.html)
  - [Synchronization using CMSIS RTOS V2 APIs](https://docs.zephyrproject.org/latest/samples/subsys/portability/cmsis_rtos_v2/timer_synchronization/README.html)
- Sensing Subsystem Samples
  - [Sensing subsystem sample](https://docs.zephyrproject.org/latest/samples/subsys/sensing/simple/README.html)
- Settings sample
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/settings/README.html#overview)
  - [Requirements](https://docs.zephyrproject.org/latest/samples/subsys/settings/README.html#requirements)
  - [Building and Running](https://docs.zephyrproject.org/latest/samples/subsys/settings/README.html#building-and-running)
- Shell System Samples
  - [File system shell example](https://docs.zephyrproject.org/latest/samples/subsys/shell/fs/README.html)
- SiP SVC sample
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/sip_svc/README.html#overview)
  - [Caveats](https://docs.zephyrproject.org/latest/samples/subsys/sip_svc/README.html#caveats)
  - [Building and Running](https://docs.zephyrproject.org/latest/samples/subsys/sip_svc/README.html#building-and-running)
  - [Sample Output](https://docs.zephyrproject.org/latest/samples/subsys/sip_svc/README.html#sample-output)
- Task Watchdog Sample
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/task_wdt/README.html#overview)
  - [Building and Running](https://docs.zephyrproject.org/latest/samples/subsys/task_wdt/README.html#building-and-running)
- Send Tracing Formatted Packet To The Host With Supported Backends
  - [Overview](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#overview)
  - [Requirements](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#requirements)
  - [Usage for UART Tracing Backend](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#usage-for-uart-tracing-backend)
  - [Usage for USB Tracing Backend](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#usage-for-usb-tracing-backend)
  - [Usage for POSIX Tracing Backend](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#usage-for-posix-tracing-backend)
  - [Usage for USER Tracing Backend](https://docs.zephyrproject.org/latest/samples/subsys/tracing/README.html#usage-for-user-tracing-backend)
- USB device support samples
  - [USB Audio Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/audio/headphones_microphone/README.html)
  - [USB Audio Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/audio/headset/README.html)
  - [USB CDC ACM Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/cdc_acm/README.html)
  - [USB CDC ACM Sample Composite Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/cdc_acm_composite/README.html)
  - [Console over CDC ACM UART Sample](https://docs.zephyrproject.org/latest/samples/subsys/usb/console/README.html)
  - [USB DFU Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/dfu/README.html)
  - [USB HID CDC ACM Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/hid-cdc/README.html)
  - [USB HID mouse Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/hid-mouse/README.html)
  - [USB HID Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/hid/README.html)
  - [USB Mass Storage Sample Application](https://docs.zephyrproject.org/latest/samples/subsys/usb/mass/README.html)
  - [USB support shell sample](https://docs.zephyrproject.org/latest/samples/subsys/usb/shell/README.html)
  - [Testusb application sample](https://docs.zephyrproject.org/latest/samples/subsys/usb/testusb/README.html)
  - [WebUSB sample application](https://docs.zephyrproject.org/latest/samples/subsys/usb/webusb/README.html)
- USB-C device support samples
  - [Basic USB-C SINK](https://docs.zephyrproject.org/latest/samples/subsys/usb_c/sink/README.html)
  - [Basic USB-C SOURCE](https://docs.zephyrproject.org/latest/samples/subsys/usb_c/source/README.html)
- Video Samples
  - [Video Capture](https://docs.zephyrproject.org/latest/samples/subsys/video/capture/README.html)
  - [VIDEO TCP SERVER SINK](https://docs.zephyrproject.org/latest/samples/subsys/video/tcpserversink/README.html)
- Zbus Samples
  - [Benchmark sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/benchmark/README.html)
  - [Confirmed channel sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/confirmed_channel/README.html)
  - [Dynamic channel sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/dyn_channel/README.html)
  - [Hello world sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/hello_world/README.html)
  - [Remote mock sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/remote_mock/README.html)
  - [Runtime observer registration sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/runtime_obs_registration/README.html)
  - [UART bridge sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/uart_bridge/README.html)
  - [Workqueue sample](https://docs.zephyrproject.org/latest/samples/subsys/zbus/work_queue/README.html)