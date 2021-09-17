# I2S总线介绍

## I2S基本介绍

I2S(Inter-IC Sound Bus)，又称集成电路内置音频总线，是飞利浦公司为数字音频设备之间的音频数据传输而制定的一种总线标准。该总线专门用于音频设备之间的数据传输，广泛应用于各种多媒体系统，在飞利浦公司的I2S标准中，既规定了硬件接口规范，也规定了数字音频数据的格式。

I2S 特点：

- 支持全双工，半双工模式

  > 全双工：同一时刻，允许数据在两个方向上同时传输
  >
  > 半双工：同一时刻，只允许数据在某一个方向上传输数据
  >
  > 单工：同一时刻，只有一方能接受或者放松数据
  >
  > ![image-20210915094816217](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039439.png)

- 支持主从模式

  > 一般主从模式的区别是谁提供时钟，谁就是master角色

- I2S仅支持立体声通道（左右两个声道数据）

## I2S协议细节

I2S一般有3个主要信号，BCLK, WS, SDATA， 有时，为了使系统间能更好地同步，还需要另外传输一个信号MCLK，称为主时钟，也叫系统时钟，这里暂时先说明如下三个主要信号。

### BCLK

位时钟，也称为SCK， SCLK等，串行时钟，对应数字音频的每一个bit数据，SCLK都有一个脉冲

### WS

- 用于切换左右声道的数据。**WS的频率＝采样频率**。
- 命令选择线， 0和1表明了正在被传输的声道为左声道还是右声道（可配置）。

- 也叫帧时钟LRCK（左右时钟）

### SDATA

串行数据，就是用二进制补码，表示音频数据， **I2S格式的信号**无论有多少位有效数据，数据的最高位总是被最先传输(在WS变化(也就是一帧开始)后的第2个SCK脉冲处)，因此最高位拥有固定的位置，而最低位的位置则是依赖于数据的**有效位数**。也就使得接收端与发送端的有效位数可以不同。如果接收端能处理的有效位数少于发送端，可以放弃数据帧中多余的低位数据；如果接收端能处理的有效位数多于发送端，可以自行补足剩余的位(常补足为零)。这种同步机制使得数字音频设备的互连更加方便，而且不会造成数据错位。为了保证数字音频信号的正确传输，**发送端和接收端应该采用相同的数据格式和长度**。当然，对I2S格式来说数据长度可以不同。

> 这里的I2S格式的信号，有效位数，都是可配置的

### I2S系统接口

对于系统而言，产生SCK和WS的信号端就是主设备，用MASTER表示，简单系统示意图如图1所示

![image-20210915125127642](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039806.png)

### I2S数据格式

#### 左对齐模式

SDATA 的MSB在BCLK的第一个上升获得根据LRCK的传输。

![image-20210915133922031](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039105.png)

#### 右对齐模式

![image-20210915134530110](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039138.png)

#### I2S模式

![image-20210915134600263](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039378.png)

## I2S 抓包分析

### 逻辑分析仪

我这边使用的是如下逻辑分析仪，大概1000元人民币

[购买链接](https://dreamsourcelab.cn/shop/logic-analyzer/dslogic-plus/)

![image-20210917104543127](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171045431.png)

### 抓包软件

[DSView 软件 软件](https://dreamsourcelab.cn/download/)

![image-20210917104215829](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171042786.png)

### 抓包配置

I2S解码器配置如下图所示

![image-20210908131107499](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039921.png)

### 配置部分说明

#### WS Polarity

![image-20210908131958067](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039841.png)

- WS polarity: 即下图中的DACLRC/ADCLRC一栏，用来选择左声道还是右声道数据的，比如WS为低时（下图Left channel位置），表示左声道数据，WS为高时，表示右声道数据，当然WS为高，还是为低表示的是左声道还是右声道，这个也是可配置的，**不过需要I2S master和 I2S salve端，配置相同**

  ![image-20210908131152058](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039810.png)

- 选择left-high 表示 WS为高时，表示的是左声道的数据

- 选择left-low  表示WS为低时，表示的是左声道的数据

- WS的频率，也表示着I2S的采样频率，如下图所示，是可配置的采样率范围, I2S的采样频率，结合上面的这张图，怎么理解呢？比如48K的采样率，1秒钟，可以采样到48000个音频数据(左声道+右声道数据， I2S只有立体声数据，无单通道数据)

#### SCK active edge

标志着I2S的数据在SCK（BCLK）的上升沿，还是下降沿，有效，一般情况下都是上升沿有效

![image-20210908162848104](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039447.png)

## 抓包协议分析

![image-20210908171930602](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171039509.png)

![image-20210908171947234](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora02/202109171040030.png)

## 参考文档

[1] [I2SBUS.pdf](https://web.archive.org/web/20070102004400/http://www.nxp.com/acrobat_download/various/I2SBUS.pdf)
[2] [I2S协议](https://www.cnblogs.com/linhaostudy/p/7700287.html)
[3] [音频总线I2S协议](https://cloud.tencent.com/developer/article/1529022)
