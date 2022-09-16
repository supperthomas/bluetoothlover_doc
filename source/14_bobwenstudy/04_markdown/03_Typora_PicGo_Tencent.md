# Typora+图床（PicGo+腾讯云）

## 引言

最近想开始在网上公开一些自己的想法/知识，以前一直都是从别人身上吸取知识（Ctrl+C\Ctrl+V），也工作这么多年了，也该为大家贡献一些自己的想法/知识。

知识要传播就需要载体，之前自己记录一些知识都是通过《有道云笔记》来弄的，非常方便。但是传播知识就可能面对需要将其传播给各大平台了，单单只发布一个平台很容易就受限了。

作为一个开发人员，做一件事情多少要明确好自己的**需求**，不一定要这个东西好，满足自己需要的才是最好的。所需的编辑器需要满足如下需求：

1. 能在各大平台发布，不受限于平台的文档格式。知识是我自己创造的，平台只是提供一个传播渠道。
2. 对code预览需要很好的支持，如代码高亮等。毕竟是个程序员，分享的知识主要和代码相关。
3. 能在github等开源平台上，关联readme之类。
4. 能支持图片上传，不需要支持视频之类的在线预览（传个gif就行）。
5. 能在Windows、MacOS、linux上使用，毕竟程序员啥平台都有。

综上所述，markdown能够满足我所有需求。markdown是很适合做文档记录的文档格式，市面上有很多markdown编辑器，总体来说我更喜欢Typora（[Typora — a markdown editor, markdown reader.](https://www.typora.io/)）。

说到markdown不得不面对一个问题，就是图片上传的问题。markdown本身是一个文本文件，并不像word那么强大（同样它也不像word那么“重”），可以内部嵌入图片或者视频等。所以如何让文本文件携带图片信息呢？

一个办法是相对路径，本地放一个文件夹，图片放在这里，但是这样文档发布到网上的时候就无法显示图片了。

另一个办法是图床，现在介绍图床的方法比较多，就不再赘述了，其结合Typora能完美达到所需要的功能。之前一直用腾讯云，所以就继续用腾讯云了。

## Typora安装

官网是：[Typora — a markdown editor, markdown reader.](https://www.typora.io/)。下载路径是：[Typora — macOS release channel](https://www.typora.io/releases/all)。

![image-20220725210152746](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725210152746.png)

现在需要收费了，**14.99**美金，支持3台终端，目前查下来的资料是只需要这个钱，能支持就支持下，毕竟只有这样行业才能有更多好用的软件可以用。

上手还提供15天免费，可以15天试用下，好用就用，反正我个人觉得不错（写这个文档的时候也是用的试用版本）。

当然也可以下载Dev/Beta版本，这些还是**免费**的。



![image-20220725205545697](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725205545697.png)





## 腾讯云COS（新人免费1年）

### 免费的打开方式

大家如果是刚开始注册，新人是可以免费使用1年的，别傻乎乎的付钱。

![image-20220725213246464](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213246464.png)



进去后，直接点击这里。新人开通先给了半年的免费使用（50GB的额度），之后有需要可以买1元的秒杀活动，直接1年的使用权。

![image-20220725213424469](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213424469.png)

![image-20220725213629108](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213629108.png)



### 千万别一开始进这个页面付费

千万别一开始就傻乎乎的在这个页面付钱了。



![image-20220725213651695](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213651695.png)

![image-20220725213721561](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213721561.png)



### 创建储存桶

注意红框选中的配置。

![image-20220725213926616](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213926616.png)

![image-20220725213953179](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213953179.png)



![image-20220725214011959](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725214011959.png)













## PicGo安装&配置

安装完Typora之后，直接运行，选择**偏好设置**，到**图像**选项卡，安装图片操作即可，下面对一些重点步骤进行说明。

![image-20220725210725966](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725210725966.png)



### PicGo-Core(command line)

选择command line模式，可以直接用Typora来安装PicGo-Core，app那个好像是要先下载PicGo-Core，为了省事，我们直接通过Typora来。

### 配置腾讯云服务

点击按钮就是让编辑一个config.json文件，点击旁边的说明，会跳转到Typora官网，阅读一下就能看到会让你调整到PicGo的说明文档，直接看软件的配置参数就行。[配置文件 | PicGo-Core](https://picgo.github.io/PicGo-Core-Doc/zh/guide/config.html#默认配置文件)

![image-20220725212124094](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725212124094.png)

腾讯云COS的配置安装其实官方也是有教程的，[配置手册 | PicGo](https://picgo.github.io/PicGo-Doc/zh/guide/config.html#腾讯云cos)，下面讲下我这边的配置结果，方便大家做一个对照。

![image-20220725212232907](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725212232907.png)



我最终配置的结果是这个。

![image-20220725211857862](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725211857862.png)



**1.** 获取你的APPID、SecretId和SecretKey

访问：https://console.cloud.tencent.com/cam/capi，红框里面的3个参数就是了。

![image-20220725212626067](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725212626067.png)

**2.** 获取bucket名以及存储区域代号

访问：https://console.cloud.tencent.com/cos5/bucket

创建一个存储桶。然后找到你的存储桶名和存储区域代号，红框里2个参数就是了。

![image-20220725212822537](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725212822537.png)



### 验证

上述参数配置好了后，验证一下，看到如图的提示说明好了，之后就可以愉快的玩耍了。

![image-20220725213145945](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220725213145945.png)



