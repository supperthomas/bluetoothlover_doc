# 局域网部署共享文档



​	网上有很多关于Sphinx+GitHub+Read the Docs的文档管理方法（如果需要学习和了解此方法的可参考“[Read the Docs 从懵逼到入门]([(50条消息) Read the Docs 从懵逼到入门_阿基米东的博客-CSDN博客_readthedoc](https://blog.csdn.net/lu_embedded/article/details/109006380?utm_source=app))”这篇文章），其原理是先用 Sphinx 生成文档，然后用 GitHub 托管文档，再导入到 Read the Docs 生成在线文档。

​	此方法的内容是需要公开的，对于在公司想搭建内部文档分享是不合适的，因此本文章主要介绍一种通过个人电脑或服务器+局域网就能分享的内部文档。

------

## 搭建IIS Web服务器

本文主要基于windows10上实现（其他的自行按照意思部署），借助微软的IIS协议服务来搭建局域网网络

### 安装IIS

这里介绍win10的设置步骤；

1. 打开控制面板，点击“程序”
2. 点击“程序与功能”
3. 点击左侧“启用或关闭Windows功能”
4. 在弹出的对话框勾选“Internet Information Services”
5. 展开“Internet Information Services”下的内容也全部勾选

操作如下图：

![iis_installer](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimgiis_installer.gif)

### 配置IIS Web服务

如果成功安装了IIS，接下来可进行如下操作：

1. 打开“开始”菜单
2. 选择“Windows管理工具”
3. 在展开的选项里点击"Internet Infomation Services(IIS)管理器“（如果成功安装了会有这个选项）

如图所示：	

​	![Services](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimgServices.png)

在弹出的"Internet Infomation Services(IIS)管理器“软件页面里进行如下操作：

1. 展开左侧选项右键”网站“点击添加网站；
2. ”网站名称“随便设置，”应用程序池“默认即可；
3. ”物理路径“这个需要指定到自己的.html文件夹下；
4. ”传递身份验证“默认即可；
5. ”IP地址“可打开CMD，输入ipconfig查看，”端口“这个可设置成8082(为了防止和其他的冲突)；
6. ”主机名称“不设置；

操作示意图：

![ServicesSet](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgimgServicesSet.gif)

至此已经完成了网站的部署，但还需进行端口的出入站规则设置

## 入站规则设置

1. 打开”网络和Internet设置“；
2. 点击”windows防火墙“；
3. 点击”高级设置“
4. 点击”入站规则“，右键”新建规则“；
5. 在弹出的对话框中”规则类型“选择”端口“，然后下一步；
6. ”协议和端口“勾选”TCP".勾选“特定本地端口”，填入8000-8090（这个设置只要包含之前设置的端口8082即可），然后下一步；
7. ”操作“直接下一步；
8. ”配置文件“也下一步；
9. 名称填入wiki_8000-8090方便记忆即可，然后点击完成；

操作如下图：

![web_set](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgweb_set.gif)

至此已经完成配置！！！

### 访问网站

接下来我们访问网站观看下效果：

![web_watch](https://markdown-1315172582.cos.ap-shanghai.myqcloud.com/imgweb_watch.gif)

**如果出现无法访问的情况下，需关闭防火墙在进行设置！**！！

