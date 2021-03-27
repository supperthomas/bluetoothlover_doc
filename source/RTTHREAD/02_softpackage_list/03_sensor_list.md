
# RT-Thread 传感器软件包归类
## 简介

介绍了目前已经适配了rtthread的sensor框架的软件包，注意：**有些传感器是即支持IIC也支持SPI，但是目前适配sensor框架只用了一种通讯接口。**

## 传感器软件包列表

| 传感器型号                                                   | 类型                     | 通讯接口 | 厂家       | 备注                                                         |
| :----------------------------------------------------------- | ------------------------ | -------- | ---------- | ------------------------------------------------------------ |
| [AHT10](https://github.com/RT-Thread-packages/aht10)         | 温湿度传感器             | IIC      | ASAIR      | SMD封装可用于回流焊，精度一般                                |
| [AP3216C](https://github.com/RT-Thread-packages/ap3216c)     | 接近感应与光照强度传感器 | IIC      | Kingbright | 集成光传感器，距离传感器，红外LED的芯片                      |
| [BH1750](https://github.com/sanjaywu/bh1750_sensor)          | 光照强度传感器           | IIC      | ROHM       | 16位量程                                                     |
| [BMA400](https://github.com/RT-Thread-packages/bma400)       | 三轴加速度传感器         | IIC      | BOSH       |                                                              |
| [BME280](https://github.com/RT-Thread-packages/bme280)       | 温湿度/气压传感器        | IIC      | BOSH       | 温度、湿度、气压三合一传感器                                 |
| [BME680](https://github.com/luhuadong/rtt-bme680)            | VOC 温湿度 气压传感器    | IIC      | BOSH       | 贵                                                           |
| [BMI088](https://github.com/gmyFighting/bmi088)              | 六轴传感器               | IIC      | BOSH       | 3轴陀螺仪和3轴加速度计，可用于无人机和机器人                 |
| [BMI160/BMX160](https://github.com/RT-Thread-packages/bmi160_bmx160) | 六轴/九轴传感器          | IIC      | BOSH       | 超低功耗；BMI：六轴 BMX：九轴                                |
| [BMP180](https://github.com/Prry/rtt-bmp180)                 | 气压/温度传感器          | IIC      | BOSH       | 比较老了                                                     |
| [BMP280](https://github.com/nfsq246/RTT_BMP280)              | 气压/温度传感器          | IIC/SPI  | BOSH       | 应该是要替代BMP280的，支持IIC和SPI两种接口                   |
| [CCS811](https://github.com/luhuadong/rtt-ccs811)            | 气体传感器               | IIC      | AMS        | 用于检测室内低水平的挥发性有机化合物和二氧化碳浓度           |
| [DA270](https://github.com/MiraMEMS-Wonderful/da270-RT-Thread) | 加速度三轴传感器         | IIC      | MiraMEMS   | 超低功耗                                                     |
| [DF220](https://github.com/MiraMEMS-Wonderful/df220-RT-Thread) | 力传感器                 | IIC      | MiraMEMS   | 超低功耗                                                     |
| [DHT11](https://github.com/murphyzhao/dht11_rtt)             | 温湿度传感器             | 单总线   | AOSONG     | 单总线通讯                                                   |
| [DHTxx](https://github.com/luhuadong/rtt-dhtxx)              | DHT家族大集合            | 单总线   | AOSONG     | DHT11、DHT12、DHT21 和 DHT22 等型号                          |
| [DS18B20](https://github.com/willianchanlovegithub/ds18b20)  | 温度传感器               | 单总线   | UMW        | 单总线温度传感器                                             |
| [GP2Y10](https://github.com/luhuadong/rtt-gp2y10)            | 灰尘检测传感器           | ADC      | SHARP      | 粉尘传感器，模拟电压输出                                     |
| [GY271](https://github.com/jch12138/gy271)                   | 地磁传感器               | IIC      | Honeywell  | 测量范围: ±1.3-8Ga                                           |
| [HDC1000](https://github.com/Forest-Rain/hdc1000)            | 温湿度传感器             | IIC      | TI         | 超低功耗，新设计推荐用HDC2010                                |
| [HMC5883](https://github.com/Forest-Rain/hdc1000.git)        | 三轴磁力计               | IIC      | Honeywell  |                                                              |
| [HSHCAL001](https://github.com/lucaslsh/hshcal001)           | 温湿度传感器             | IIC      | ALPSALPINE | 超低功耗                                                     |
| [HTS221](https://github.com/RT-Thread-packages/hts221)       | 温湿度传感器             | IIC      | ST         |                                                              |
| [INA226](https://github.com/xupenghu/ina226)                 | 功率监视器               | IIC      | TI         | 可监测总线电压、电流和功率                                   |
| [INA260](https://github.com/xupenghu/ina260)                 | 功率监视器               | IIC      | TI         | 自带2mΩ采样电阻，可采样15A连续电流                           |
| [LIS2DH12](https://github.com/StackRyan/lis2dh12)            | 加速度传感器             | SPI      | ST         | 超低功耗                                                     |
| [LPS22HB](https://github.com/RT-Thread-packages/lps22hb)     | 气压传感器               | IIC      | ST         | 测量的气压范围0.26*10^5pa---1.26*10^5pa，且精度能达到10cm    |
| [LSM303AGR](https://github.com/RT-Thread-packages/lsm303agr) | 加速度&磁力计传感器      | IIC      | ST         | 超低功耗，内嵌32级FIFO                                       |
| [LSM605L](https://github.com/RT-Thread-packages/lsm6dsl)     | 加速度&陀螺仪传感器      | IIC      | ST         | 内置计步器                                                   |
| [MAX30102](https://github.com/Jackistang/max30102_rtt)       | 心率&血氧传感器          | IIC      | Maxim      |                                                              |
| [MAX31865](https://github.com/SimpleInit/max31865)           | 温度传感器               | SPI      | Maxim      | 热敏电阻转数字输出转换器，非数字传感器                       |
| [MAX6675](https://github.com/JonasWen/max6675)               | 温度传感器               | SPI      | Maxim      | ±0.25℃精度                                                   |
| [MLX90632]()                                                 | 非接触式温度传感器       | IIC      | Melexis    | 人体温度测量精度高达±0.2 °C                                  |
| [MPU6xxx](https://github.com/RT-Thread-packages/mpu-6xxx)    | 加速度&陀螺仪传感器      | IIC      | InvenSense | 兼容 mpu6000、mpu6050、mpu6500、mpu9250、icm20608 等         |
| [MS5611](https://github.com/sogwms/ms5611)                   | 气压传感器               | IIC&SPI  | MEAS       | 高分辨率气压传感器                                           |
| [MS5805](https://github.com/schuck-wang/RTThread-MS5805)     | 气压传感器               | IIC      | MEAS       | 高分辨率气压传感器                                           |
| [PMSxx](https://github.com/luhuadong/rtt-pmsxx)              | 颗粒物传感器             | UART     | Plantower  | 支持 PMS1003、PMS3003、PMS5003、PMS7003、PMS9003、PMSA003 等多种型号传感器，还没有对接sensor框架。 |
| [RT3020](https://github.com/RichtekTechnology/RT3020)        | 加速度传感器             | IIC      | Richtek    | 低功耗，用于可穿戴设备                                       |
| [SGP30](https://github.com/luhuadong/rtt-sgp30)              | 金属氧化物气体传感器     | IIC      | Sensirion  | 用于检测 TVOC 和 eCO2                                        |
| [SHTC1](https://github.com/nfsq246/RTT_SHTC1)                | 大气压强传感器           | IIC      | SENSIRION  |                                                              |
| [SPL0601](https://github.com/RT-Thread-packages/spl0601)     | 大气压传感器             | IIC      | Goer       | 同时内置温度传感器，低功耗                                   |
| [HC-SR04](https://github.com/alec-shan/hc-sr04)              | 超声波测速               | Timer    | 无         | 淘宝有模块                                                   |
| [TMP1075](https://github.com/Prry/rtt-tmp1075)               | 温度传感器               | IIC      | TI         | 供电范围广、功耗低、精度高                                   |
| [TSL4531](https://github.com/JellyYe/tsl4531pkgs)            | 光照度传感器             | IIC      | AMS        | 量程:3 lux-220k lux 分辨率: 1 lux                            |
| [VL53L0x](https://github.com/Prry/rtt-vl53l0x)               | 红外测距传感器           | IIC      | ST         | 量程: 0-2000mm 分辨率: 1mm                                   |


