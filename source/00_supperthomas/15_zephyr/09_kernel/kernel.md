

#



KERNEL sleep 在nordic平台上用的是RTC定时器。

![image-20231117192848409](images/image-20231117192848409.png)

![image-20231117204719793](images/image-20231117204719793.png)







## semaphore 信号量

tests\kernel\semaphore

定义信号量

```
struct k_sem my_sem;
k_sem_init(&my_sem, 0, 1);
```

或者

```
K_SEM_DEFINE(my_sem, 0, 1);
```

这里0是初始化值，1是最大值。这里可以模拟成二进制信号量。1可以设置的最大值为K_SEM_MAX_LIMIT。

给出信号量，通常由中断服务例程来给出信号量

```
void input_data_interrupt_handler(void *arg)
{
    /* notify thread that data is available */
    k_sem_give(&my_sem);

    ...
}
```

等待信号量

```
void consumer_thread(void)
{
    ...

    if (k_sem_take(&my_sem, K_MSEC(50)) != 0) {
        printk("Input data not available!");
    } else {
        /* fetch available data */
        ...
    }
    ...
}
```

这里等待50ms， 如果一直等待采用，

- K_NO_WAIT： 表示不等待
- K_FOREVER： 一直等待
- K_MSEC(50)： 50ms

k_sem_reset： 把count设置成0

k_sem_count_get: 获取count值。

### user mode对应的API

用户模式的API功能一样，命名不一样

SYS_SEM_DEFINE

sys_sem_init

sys_sem_give

sys_sem_take

sys_sem_count_get

### 建议用途

使用信号量来控制多个线程对一组资源的访问。

使用信号量来同步生产和消费线程或 ISR 之间的处理。

## mutex 互斥信号量

### 定义

```
struct k_mutex my_mutex;

k_mutex_init(&my_mutex);
```

或者

```
K_MUTEX_DEFINE(my_mutex);
```

锁互斥量

```
if (k_mutex_lock(&my_mutex, K_MSEC(100)) == 0) {
    /* mutex successfully locked */
} else {
    printf("Cannot lock XYZ display\n");
}
```

解锁互斥量

```
k_mutex_unlock(&my_mutex);
```

### 建议用途

使用互斥体提供对资源（例如物理设备）的独占访问。

## event事件

### 定义

```
struct k_event my_event;
k_event_init(&my_event);
```

或者

```
K_EVENT_DEFINE(my_event);
```



设置事件：

```
void input_available_interrupt_handler(void *arg)
{
    /* notify threads that data is available */

    k_event_set(&my_event, 0x001);

    ...
}
```

发布事件

```
void input_available_interrupt_handler(void *arg)
{
    ...

    /* notify threads that more data is available */

    k_event_post(&my_event, 0x120);

    ...
}
```



![image-20231120160930821](images/image-20231120160930821.png)

k_event_post: 相当于这次就这么多事件

k_event_set: 相当于这次触发这么多事件，但是这个事件可以叠加之前的事件。

等待事件，可以加mask

```
void consumer_thread(void)
{
    uint32_t  events;

    events = k_event_wait(&my_event, 0xFFF, false, K_MSEC(50));
    if (events == 0) {
        printk("No input devices are available!");
    } else {
        /* Access the desired input device(s) */
        ...
    }
    ...
}
```

第三个bool参数，代表是否清除之前的event。

等待所有event

```
void consumer_thread(void)
{
    uint32_t  events;

    events = k_event_wait_all(&my_event, 0x121, false, K_MSEC(50));
    if (events == 0) {
        printk("At least one input device is not available!");
    } else {
        /* Access the desired input devices */
        ...
    }
    ...
}
```

### 建议用途

使用事件来指示一组条件已经发生。

使用事件将少量数据一次传递到多个线程。

## 条件变量(比较难理解)

tests\kernel\condvar\condvar_api

可以定义任意数量的条件变量（仅受可用 RAM 的限制）。每个条件变量都由其内存地址引用。

要等待条件变为真，线程可以使用条件变量。

条件变量基本上是一个线程队列，当某些执行状态（即某些条件）不符合预期（通过等待条件）时，线程可以将自己放入该队列中。该函数 [`k_condvar_wait()`](https://docs.zephyrproject.org/latest/kernel/services/synchronization/condvar.html#c.k_condvar_wait)自动执行以下步骤；

1. 释放最后获取的互斥体。
2. 将当前线程放入条件变量队列中。

定义

```
 struct k_condvar my_condvar;
 k_condvar_init(&my_condvar);
```

或者

```
K_CONDVAR_DEFINE(my_condvar);
```

等待条件变量

```
K_MUTEX_DEFINE(mutex);
K_CONDVAR_DEFINE(condvar)

int main(void)
{
    k_mutex_lock(&mutex, K_FOREVER);

    /* block this thread until another thread signals cond. While
     * blocked, the mutex is released, then re-acquired before this
     * thread is woken up and the call returns.
     */
    k_condvar_wait(&condvar, &mutex, K_FOREVER);
    ...
    k_mutex_unlock(&mutex);
}
```

通知条件变量

```
void worker_thread(void)
{
    k_mutex_lock(&mutex, K_FOREVER);

    /*
     * Do some work and fulfill the condition
     */
    ...
    ...
    k_condvar_signal(&condvar);
    k_mutex_unlock(&mutex);
}
```

[`k_condvar_broadcast()`](https://docs.zephyrproject.org/latest/kernel/services/synchronization/condvar.html#c.k_condvar_broadcast)

这个有点像

### 建议用途

使用带有互斥体的条件变量来表示从一个线程到另一线程的状态（条件）变化。条件变量不是条件本身，也不是事件。该条件包含在周围的编程逻辑中。

互斥体本身并不是设计用作通知/同步机制的。它们旨在仅提供对共享资源的互斥访问。

这个和互斥量很接近。

他可以用来等一个条件，并且互斥的访问资源。

并且可以对多个线程进行通知和唤醒。

## 轮询API

轮询有点类似于posix里面的poll机制

定义

```
struct k_poll_event events[2] = {
    K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_SEM_AVAILABLE,
                                    K_POLL_MODE_NOTIFY_ONLY,
                                    &my_sem, 0),
    K_POLL_EVENT_STATIC_INITIALIZER(K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                                    K_POLL_MODE_NOTIFY_ONLY,
                                    &my_fifo, 0),
};
```

或者

```
struct k_poll_event events[2];
void some_init(void)
{
    k_poll_event_init(&events[0],
                      K_POLL_TYPE_SEM_AVAILABLE,
                      K_POLL_MODE_NOTIFY_ONLY,
                      &my_sem);

    k_poll_event_init(&events[1],
                      K_POLL_TYPE_FIFO_DATA_AVAILABLE,
                      K_POLL_MODE_NOTIFY_ONLY,
                      &my_fifo);

    // tags are left uninitialized if unused
}
```

