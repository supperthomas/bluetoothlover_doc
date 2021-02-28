# 搭建zephyr开发环境

## 完整流程

命令参考官方的[getting-started](https://docs.zephyrproject.org/latest/getting_started/index.html)

1. 其中python PIP的时候速度会比较慢，参考下面的
2. west init时请按照下面的命令说明进行,因为官方的代码是在github上，我吧官方的zephyr用到的所有仓库都export到gitee上了，所以访问速度会提升很多



## 关键命令

其中使用west init时请使用如下命令(从我的gitee仓库clone zephyr工程)

```
west init ~/zephyrproject -m https://gitee.com/AnswerInTheWind/zephyr/ 

cd ~/zephyrproject

west update
```


## 常见问题

### PIP速度慢

解决办法：
在pip 命令后面加上-i https://pypi.tuna.tsinghua.edu.cn/simple

可以从国内的源下载

### west init /west update 慢

解决办法：
修改west init 和west update 从gitee git

其中的连接都是在west init时设置

- west init中-m 参数是设置zephyr仓库的URL

而west update的路径是有**west.yml**文件决定的，我已将zephyr原工程中指向github的连接改为指向我的gitee仓库了，所以使用我的工程的话不需要再修改**west.yml**文件了

## 点亮LED灯

因为zephyr已经支持WB55 nucleo的板子了，所以我们只需参照官方文档，即可点亮LED灯

准备工作：

​	- 将ST-LINK USB口连接至虚拟机

编译、烧写步骤如下

```shell
cd ~/zephyrproject/zephyr

west build -b nucleo_wb55rg samples/basic/blinky

west flash
```

至此，即可看到板上的LED2闪烁了