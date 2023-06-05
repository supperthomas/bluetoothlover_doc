# 【github】如何制作一个github 的package

## 简介

本文面向一些devops工作人员，需要稍微了解一点点docker。

github有个package功能，如果你用过docker的话，其实package功能就和dockerhub差不多。

通常我们会将image存到dockerhub中（相当于docker里面的github，就是存放一些公开的镜像），而dockerhub这种网站还有很多，github自己就做了个类似于dockerhub的网站。







GitHub Packages 是一个软件包管理工具，它允许开发人员和团队在 GitHub 上发布和共享软件包。这些软件包可以是公开的，也可以是私有的，可以包含任何语言和框架的代码。创建自己的 GitHub Packages 软件包非常简单，只需要遵循以下步骤：

### 1. 创建一个 GitHub 账号

首先，您需要在 GitHub 上创建一个账号。如果您已经有了 GitHub 账号，请跳过这一步。

### 2. 创建一个新的仓库

接下来，您需要在 GitHub 上创建一个新的仓库。这个仓库将用于存储您的软件包。请确保仓库是公开的。

### 3. 创建一个新的 PAT

GitHub Packages 需要一个名为 PAT（Personal Access Token）的令牌来进行身份验证和授权。您可以在您的 GitHub 账号设置中创建一个新的 PAT。

### 4. 创建一个 Dockerfile

接下来，您需要创建一个 Dockerfile。Dockerfile 是一个包含一系列指令的文件，用于构建 Docker 镜像。您可以在 Dockerfile 中指定您的软件包需要的所有依赖项、环境变量等。

### 5. 构建 Docker 镜像

使用 Dockerfile 构建 Docker 镜像。如果您不熟悉如何构建 Docker 镜像，请查看 Docker 文档。

### 6. 标记 Docker 镜像

在构建 Docker 镜像后，您需要使用 docker tag 命令为镜像打标签。标签应该包含您的 GitHub 用户名、软件包名称和版本号。例如：

```
docker tag myimage:latest docker.pkg.github.com/username/myrepo/myimage:latest
```

### 7. 授权 Docker

接下来，您需要使用以下命令将 Docker 授权到 GitHub Packages：

```
docker login docker.pkg.github.com -u USERNAME -p TOKEN
```

其中，USERNAME 是您的 GitHub 用户名，TOKEN 是您在第三步中创建的 PAT。

### 8. 推送 Docker 镜像

最后，您可以使用以下命令将 Docker 镜像推送到 GitHub Packages：

```
docker push docker.pkg.github.com/username/myrepo/myimage:latest
```

其中，USERNAME 是您的 GitHub 用户名，myrepo 是您在第二步中创建的仓库名称，myimage 是 Docker 镜像的名称，latest 是版本号。

完成上述步骤后，您的软件包已经可以在 GitHub Packages 中使用了。其他人可以使用以下命令来从 GitHub Packages 中拉取您的软件包：

```
docker pull docker.pkg.github.com/username/myrepo/myimage:latest
```

GitHub Packages 是一个非常强大的工具，它可以帮助开发人员和团队更轻松地管理和共享软件包。如果您想了解更多关于 GitHub Packages 的信息，请查看 GitHub 文档。





本地验证action工具



https://github.com/nektos/act/