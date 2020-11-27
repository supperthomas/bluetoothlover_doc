# nRF5x_BSP I2C 移植指南

作者[毛工]

- ## 目标：使用RT-Thread标准化接口驱动nRF5x的I2C硬件

  了解RT-Thread标准化接口 [文档](https://www.rt-thread.org/document/site/programming-manual/device/i2c/i2c/)

  通过示例整理外部接口

```c
/* 查找I2C总线设备，获取I2C总线设备句柄 */
i2c_bus = (struct rt_i2c_bus_device *)rt_device_find(name);

/* 调用I2C设备接口传输数据 */
(rt_i2c_transfer(bus, &msgs, 1) == 1)
```



数据流：标准化接口 > **接口封装** > 硬件层

- ## 了解**接口封装**   *通过头文件*

  ENV 开启 RT_USING_I2C 添加了

  ```
  #include "drivers/i2c.h"
  #include "drivers/i2c_dev.h"
  ```

- 底层接口调用流程 以及核心函数

  ```c
  rt_err_t rt_i2c_bus_device_register(struct rt_i2c_bus_device *bus,
                                      const char               *bus_name)
      
  rt_size_t rt_i2c_transfer()  >>   bus->ops->master_xfer(bus, msgs, num);
  ```

  

- rt_i2c_bus_device 结构体

  ```c
  /*for i2c bus driver*/
  struct rt_i2c_bus_device
  {
      struct rt_device parent;
      const struct rt_i2c_bus_device_ops *ops;
      rt_uint16_t  flags;
      rt_uint16_t  addr;
      struct rt_mutex lock;
      rt_uint32_t  timeout;
      rt_uint32_t  retries;
      void *priv;
  };
  ```

- OPS接口  

  ```c
  struct rt_i2c_bus_device_ops
  {
      rt_size_t (*master_xfer)(struct rt_i2c_bus_device *bus,
                               struct rt_i2c_msg msgs[],
                               rt_uint32_t num);
      rt_size_t (*slave_xfer)(struct rt_i2c_bus_device *bus,
                              struct rt_i2c_msg msgs[],
                              rt_uint32_t num);
      rt_err_t (*i2c_bus_control)(struct rt_i2c_bus_device *bus,
                                  rt_uint32_t,
                                  rt_uint32_t);
  };
  ```

  slave_xfer 和 i2c_bus_control 其实没有任何用处，只能支持Master设备

  在registe之前需要自己初始化硬件，初始化完成后 不能通过标准化接口更改I2C硬件参数

  不支持 rx_indicate 和 tx_complete  回调函数

  

  

  在整理下思路 > **仅需要实现 master_xfer 这个底层接口即可**



### 了解nRF5x的I2C（TWI）驱动层

TWIME

先跑起来示例 

```c
examples\peripheral\twi_sensor 
```

drv_xxx  : 历史遗漏层   文档
twi_xxx  ：被遗弃的外设驱动 主要是为了代码兼容而保留
twim_xxx ：EasyDMA 

EasyDMA和PPI

IO中断 -》 PPI -》 I2C read

传感器 带FiFo， I2C接口的 FIFO满了 会触发一个IO上升沿

如果没有PPI 

接受到IO中断，CPU去触发I2C read 可能是DMA 读取完成再触发读取完成的中断

如果有PPI 

接收到IO上升沿  产生了一个io event

PPI 接收到io event后 直接触发 i2c read tasks（固化 发送的内存的地址） 存到固定的位置

读取完成后 再触发read finsh event 这个时候才会有**中断** CPU才退出低功耗模式 假设只能省10uA 

CR2032 220mAH  

DMA  CPU不用参与

PPI  主要解决的问题是 外设之间的触发 不涉及内存



