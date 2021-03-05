# 掉坑汇总

## ESP32 不断重启

### 硬件环境

- ESP32-DevKitC V4 (模组 ESP32-WROVER-E)
- Micro USB 数据线

### 软件环境

- examples/bluetooth/esp_ble_mesh/ble_mesh_node/onoff_server

### 错误信息

> Brownout detector was triggered，failed to load RF calibration data.

出现上述错误信息后就不断重启，该错误信息产生是因为触发了**断电探测器**。具体含义就是 ESP32 的电平低于某个设定值，导致触发了断电探测器，断电探测器就会使 ESP32 重启。

这里根据错误信息可以知道是 RF 在工作时电压突然降低，导致 ESP32 重启。

有很多原因可能导致这个问题：

- 笔记本的 USB 口供电不稳定。
- ESP32 板卡本身的问题（新的板卡一般不会有这个问题）。
- Micro USB 数据线质量太差。

我先采取禁用了断电探测器的方法，这样可以避免 ESP32 不断重启，输入

```
idf.py menuconfig
```

然后禁用 `component config->ESP32-specific->Hardware brownout detect & reset` 。这样 ESP32 的确不会重启，但出现了新的问题：

我用 `idf.py -p /dev/ttyUSB0 monitor` 监控串口，ESP32 在启动时会自动将串口断开，并报错：

```shell
device reports readiness to read but returned no data (device disconnected or multiple access on port?)
Waiting for the device to reconnect....
```

我换了一种思路，开始怀疑数据线的问题了，毕竟当时为了省钱在某宝买了很多的 3 元一根的 Micro USB 数据线。我这次换成了 10 元的 Micro USB 数据线，问题神奇的解决了！！！一分钱一分货，下次再也不贪小便宜了。

之前出现这个问题的原因应该是数据线质量不好，导致供电不稳定，数据传输也不稳定。

----

参考：

[ESP32 Brownout detector was triggered，failed to load RF calibration data , 错误解决方法](https://blog.csdn.net/qq_31232793/article/details/87889368)