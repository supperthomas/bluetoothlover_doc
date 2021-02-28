# Callback

## 函数指针理解

在 C++ 里，函数指针分为两种：

- 普通函数指针：与 C 语言函数指针类似，静态的类成员函数指针也是该类型。
- 类成员函数指针（非静态）。

普通函数指针的使用与 C 语言里的函数指针使用一致，直接调用即可，例如：

```C++
typedef void (*func)(void);
func f;
f();
```

但是类成员函数指针（非静态）则不同了，区别在于该函数指针指向一个类成员函数，而该函数属于一个具体的类对象，需要在该对象的状态下调用该成员函数。

对于类成员函数的指针使用包含以下几个步骤：

**声明：** 指向类的成员函数的指针需要在指针前面加上类的类型，格式为：

```C++
typedef 返回值 (类名::*指针类型名)(参数列表);
```

**赋值：** 需要用类的成员函数地址赋值，格式为：

```C++
指针类型名  指针名 = &类名::成员函数名;
```

*注意：这里的这个&符号是比较重要的：不加&，编译器会认为是在这里调用成员函数，所以需要给出参数列表，否则会报错；加了&，才认为是要获取函数指针。这是C++专门做了区别对待。*

**调用：** 针对调用的对象是对象还是指针，分别用 `.` 和 `->`进行调用，格式为：

```C++
(类对象.*指针名)(参数列表);

(类指针->*指针名)(参数列表);
```

*注意：这里的前面一对括号是很重要的，因为()的优先级高于成员操作符指针的优先级。*

可以通过一个例程来理解：

```C++
class Calculation
{
public:
    int add(int a,int b){ //非静态函数
        return  a + b;
    }
};

typedef int (Calculation::*FuncCal)(int,int);

int main()
{
    FuncCal funAdd = &Calculation::add;
    Calculation * calPtr = new Calculation;
    int ret = (calPtr->*funAdd)(1,2);  //通过指针调用

    Calculation cal;
    int ret2 = (cal.*funAdd)(3,4);  //通过对象调用

    cout << "ret = " << ret << endl;
    cout << "ret2 = " << ret2 << endl;
    return 0;
}

```

## Callback 引入

目前我对 Callback 的理解是：

mbed os 为了解决在给 API 传入类成员函数指针（非静态）时，API 无法知道该函数指针属于哪一个对象，因此就无法调用它。引入 Callback 模板类之后，就可以给 API 传入 Callback 对象，由 Callback 来管理类成员函数指针和它所属的对象，这样方便了 API 的设计。

例如：

```C++
_event_queue.call(Callback<void(bool)>(_button_service, &ButtonService::updateButtonState), true);
```

该语句指明了在 _button_service 对象里调用 updateButtonState 函数，即调用 ` _button_service.updateButtonState(true);`

## Callback 使用

TODO