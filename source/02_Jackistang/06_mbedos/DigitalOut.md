# DigitalOut

[DigitalOut 官方文档](https://os.mbed.com/docs/mbed-os/v6.5/apis/digitalout.html)

使用 DigitalOut 接口可以配置引脚的高低电平。

## 构造函数

- [DigitalOut](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#ab89d7345362cf8a18c535531cd05cbe6) (PinName pin) ，利用引脚编号构造一个 DigitalOut 。
- [DigitalOut](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#a4ff3198805136b5bab272a9e80505cfc) (PinName pin, int value)，利用引脚编号构造一个 DigitalOut，并指定了引脚初始电平 value 。

## 读写操作

- void [write](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#a25d1931bc29d014446294ab8dc470f2a) (int value) ，设置引脚电平（0或1）。
- int [read](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#aaab5dab5b969a87f538242e524431637) ()，读引脚电平（0或1）。

为了方便使用，DigitalOut 类还定义了 `=` 操作符的重载，以及对象转化为 int 的隐式类型转换。

- [DigitalOut](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html) & [operator=](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#aa70702790381d867e4975764d4caeacd) (int value) 

可以使用 `=` 直接设置引脚电平高低，例如：

```C++
DigitalOut led1(LED1);
led1 = 1;	//设置引脚高电平
led1 = 0;	//设置引脚低电平
```

- [operator int](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_digital_out.html#a4f4ea421e40bda08a2deca657f640fea) ()

可以直接读取引脚高低电平，例如：

```C++
DigitalOut led1(LED1);
int ledValue;
ledValue = led1;	//ledValue 保存引脚的高低电平（0或1）
```

## 例程

```C++
/*
 * Copyright (c) 2006-2020 Arm Limited and affiliates.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

DigitalOut myled(LED1);

int main()
{
    // check that myled object is initialized and connected to a pin
    if (myled.is_connected()) {
        printf("myled is initialized and connected!\n\r");
    }

    // Blink LED
    while (1) {
        myled = 1;          // set LED1 pin to high
        printf("myled = %d \n\r", (uint8_t)myled);
        ThisThread::sleep_for(500);

        myled.write(0);     // set LED1 pin to low
        printf("myled = %d \n\r", myled.read());
        ThisThread::sleep_for(500);
    }
}
```

