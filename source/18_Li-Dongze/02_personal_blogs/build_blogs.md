# 使用Astro搭建个人博客

## [Astro](https://docs.astro.build/zh-cn/getting-started/)介绍

本站是使用Astro博客框架搭建的，最终部署到github page

Astro有好多好看的模板，可以去主题[地址](https://astro.build/themes/)选择自己喜欢的博客模板，我比较喜欢[Gyoza](https://github.com/lxchapu/astro-gyoza)，也是本站的模板

如果你也想拥有一个这样的属于自己的博客，恭喜你来对地方了，接下来我将向你一步步介绍如何搭建像我这样的Blog，写本篇教程不仅仅是教你，也是在帮未来的我，如果哪天忘记如何搭建了，可以回来反复回忆。

## 前置知识

- 有一个github账号
- 会git基础操作，可以参考我的git教程（待更新）

## 搭建教程

### 步骤1. fork原作者模板到自己的github

以[Gyoza](https://github.com/lxchapu/astro-gyoza)为例，打开它的github仓库地址，fork到自己的github

> 注意：fork到自己仓库时起名一定要和自己的github账号名相同

![image-20241117210123971](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411172101199.png)

![image-20241118001040785](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411180010937.png)此时可以在自己的仓库看到博客模板，将该项目clone到本地，我们就可以在此基础上添加博客，部署githubpage

![image-20241118001117348](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411180011385.png)

### 步骤2. 配置Github Pages

打开项目检查，以后你的每次push都会github自动开启检查，保证网页格式正确

![image-20241117213633040](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411172136136.png)

跳转到存储库的 **Settings** 选项卡并找到设置的 **Pages** 部分，选择 **GitHub Actions** 作为你网站的 **Source**，然后按 **Save**

![image-20241117213859016](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411172138161.png)

### 步骤3. 修改原作者模板的部署信息

最主要的一步是在astro.config.mjs 文件中将site配置为自己的github.io

> 把仓库名改为自己的即可

![image-20241117213040106](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411172130197.png)

详细可以参考[官方教程](https://docs.astro.build/zh-cn/guides/deploy/github/)，只改上述一个地方即可，其他保持模板默认即可

## 博客启动！欢迎来到属于自己的博客

至此我们已经基本完成了博客的搭建，还差最后一步，进行我们的第一次push，让github检测一次。

![image-20241118002745119](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411180027165.png)

当最左边的标记变为绿色的勾时，就可以把项目名称直接输入浏览器，看到博客界面了

> 这里根据上面做下了应该显示的是原作者的博客模板界面，这里为了显示输入就展示我自己的了

![image-20241118003252020](https://picture-note-1328988318.cos.ap-nanjing.myqcloud.com/Typora/202411180032228.png)

接下来关于如何修改模板为自己的，可以看我的下一篇：博客模板的修改和使用（待更新）

## 总结

1. fork到自己仓库取名一定要和自己的账号名称一致
2. 配置githubpage
3. 修改为自己网址

一个github账号只能创建一个这样的博客页面；至于这样部署要不要交钱，要不要担心网址会崩，因为这种方法本质就是访问github界面，github会崩吗，我想只要程序员存在应该永远不会崩吧...
