# InterruptIn

[InterruptIn 官方文档](https://os.mbed.com/docs/mbed-os/v6.5/apis/interruptin.html)

InterruptIn 接口用于当输入引脚的电平变化时触发事件，可以选择在上升沿或下降沿触发中断。

## 构造函数

- [InterruptIn](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a11bbae310fba686d598e0791fd762ceb) (PinName pin) ，创建一个连接到特定引脚的 InterruptIn 。
- [InterruptIn](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a3f121c2c34eb44477a84e94d1bc419f3) (PinName pin, PinMode [mode](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a12ffae4af877bdcd41ad2fc6a0a444ad)) ，创建一个连接到特定引脚的 InterruptIn ，同时指定引脚模式，上拉、下拉或浮空。

## 读引脚电平

- int [read](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#aaab5dab5b969a87f538242e524431637) () ，返回读到的引脚电平（0或1）。
- [operator int](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a4f4ea421e40bda08a2deca657f640fea) () ，`read()` 操作符的简写，可以将对象隐式转化为 int 类型数据，代表引脚电平。

例如：

```C++
InterruptIn button1(SW1, PullUp);
int value = button1;		//读取 button1 关联引脚的电平
```

## 绑定中断回调函数

- void [rise](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a594ade00110428761db64ae163bef34e) ([Callback](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_callback.html)< void()> func) ，绑定上升沿回调函数，参数为 Callback<void()> 对象。
- void [fall](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a19c8712f45eed30a9a041c4b092c03da) ([Callback](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_callback.html)< void()> func) ，绑定下降沿回调函数，参数为 Callback<void()> 对象。

## 使能/失能中断

- void [enable_irq](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#af0810e0eb56d5504c46a89d1e86c045b) () ，使能中断。
- void [disable_irq](https://os.mbed.com/docs/mbed-os/v6.5/mbed-os-api-doxy/classmbed_1_1_interrupt_in.html#a4650511f35a59994b637169e8cca64f6) () ，失能中断。

## 注意事项

- 在中断回调函数里不要写可能导致阻塞的代码：避免延时，无限 while 循环和调用阻塞函数。
- 不要再中断回调函数里使用 `printf`，`malloc`和`new`：避免对一些特别庞大的库函数的调用，尤其是那些不可重入的库函数（如 printf、malloc 和 new）。

## 例程

```C++
/*
 * Copyright (c) 2017-2020 Arm Limited and affiliates.
 * SPDX-License-Identifier: Apache-2.0
 */

#include "mbed.h"

class Counter {
public:
    Counter(PinName pin) : _interrupt(pin)          // create the InterruptIn on the pin specified to Counter
    {
        _interrupt.rise(callback(this, &Counter::increment)); // attach increment function of this counter instance
    }

    void increment()
    {
        _count++;
    }

    int read()
    {
        return _count;
    }

private:
    InterruptIn _interrupt;
    volatile int _count;
};

Counter counter(SW2);

int main()
{
    while (1) {
        printf("Count so far: %d\n", counter.read());
        ThisThread::sleep_for(2000);
    }
}
```



