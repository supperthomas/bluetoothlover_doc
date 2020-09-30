# WIKI FAQ

### 1. 如何修改markdown

如果只是修改markdown的里面的文字的话，推荐使用github里面自带的编译器来编辑，直接保存就可以提交commit了。

![image-20200930175422098](./picture/image-20200930175422098.png)

然后直接点击

![image-20200930175728780](./picture/image-20200930175728780.png)

### 2. 如何在本地新建文件以及如何验证

如果不是特别必要，请最好不要操作这些步骤，直接使用上述用github直接编辑的方式比较好。

本地新建文件需要添加索引路径到index.rst上面，可以参考其他文件夹的添加方法：

![image-20200930180336439](./picture/image-20200930180336439.png)

新建文件夹和文件要注意以下几点：

- 文件夹和文件名不能有中文

- 文件夹和文件名不能有空格

- 文件夹要和index.rst里面完全匹配

- 图片路径尽量用左斜杠`/`

  新建和改好自己的文件一定要本地验证一下再上传提交PR

**如何验证**

- 找一个linux的环境，比如ubuntu虚拟机

- 安装Sphinx，命令安装对应的包: 

  ```
  pip install sphinx
  pip install sphinx-autobuild
  pip install sphinx_rtd_theme
  pip install recommonmark
  ```

- git clone所有文件

- 在有Makefile文件的目录下面敲命令 `make html`

![image-20200930180956861](./picture/image-20200930180956861.png)

- 最后看下编译有没有自己新建文件的相关的error，没有error说明没有问题，有error请检查下error
- 然后打开根目录下面的`build/html/index.html`   打开之后查看下自己添加的页面是否可以正常显示。
- 提交的时候一定要把添加的所有文件一起提交。