# PIP 如何添加国内源

## 前言
由于国内的网络环境大家都懂的，但是很多python包服务器都在境外，所以安装的时候各种报错，最好的方案是搭个梯子，但不是人人都有条件，所以找了个折中的方案，使用国内的源来替换默认源，提高下载速度。

## 临时使用
临时使用只针对本次安装包时生效，如果不是经常安装更新包，这种方法是最推荐的，简单省事，用法如下：

```c
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```
`-i` 后面加的是镜像源的地址，空格后面跟的是包名

## 永久修改
这种方法适合经常使用pip安装和更新包的人群，一次配置省去后顾之忧，缺点是替换源失效后还得重新更改默认源地址。
### Linux下
修改 ~/.pip/pip.conf (没有就创建一个文件夹及文件。**文件夹要加“.”**，表示是隐藏文件夹)，文件内容如下：

```c
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host=mirrors.aliyun.com
```
### win下
在user目录中创建一个pip目录，如：C:\Users\xxx\pip，新建文件pip.ini。内容同上。

## 国内源推荐
- https://pypi.tuna.tsinghua.edu.cn/simple (推荐使用)
- http://mirrors.aliyun.com/pypi/simple/
- https://pypi.mirrors.ustc.edu.cn/simple/
- http://pypi.hustunique.com/
- http://pypi.sdutlinux.org/
- http://pypi.douban.com/simple/
