# GitLab CI/CD

## 关于GitLab

- [官网地址](https://gitlab.com/)，可以通过Github账号, Google账号注册体验
-  [官方文档地址](https://docs.gitlab.com/ee/)

- [如何安装GitLab]([Install GitLab | GitLab](https://docs.gitlab.com/ee/install/))
- GitLab是一个Git服务器，存放代码，类似于Github

## 关于关于GitLab CI/CD

- CI/CD是一种软件开发的方法，策略，CI 表示持续集成， CD表示持续部署，这种迭代有助于减少基于错误或失败的版本进行开发新代码的可能性。使用这种方法，从新代码开发到部署，可以减少人工干预甚至不用干预。

- 直观体验

  ![image-20230903104440887](figures/GitLab_CICD/image-20230903104440887.png)

  ![CI_JOBS](figures/GitLab_CICD/CI_JOBS.gif)

## 搭建CI/CD开发环境步骤

### 安装Gitlab服务器

- 可以参考：[安装GitLab图文教程](https://blog.csdn.net/m0_62147585/article/details/126053120?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522169370925016800227496168%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=169370925016800227496168&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-2-126053120-null-null.142^v93^chatsearchT3_2&utm_term=gitlab%20%E5%AE%89%E8%A3%85&spm=1018.2226.3001.4187)

### GitLab Runner服务器

- 一般来讲GitLab服务器和GitLab Runner服务器不是同一台服务器，避免文件的错误
- 环境准备
  - 在服务器上安装必要软件，以MDK KEIL开发为例，需要安装KEIL, GIT, Python等软件
  - 由于GitLab Runner都是执行shell脚本，需要将开发环境的所有可执行文件，放到环境变量中
  - 配置好Git客户端，用户名，ssh公钥，确保Git可用
  - 下载并安装powershell 7 的msi安装包 [64位](https://objects.githubusercontent.com/github-production-release-asset-2e65be/49609581/bc890692-e2c5-4ee6-873a-e8959adec3fc?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230518%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230518T102103Z&X-Amz-Expires=300&X-Amz-Signature=1d4fa8867e835e9ff92a9c2dd43adaf0e864848c30d195d0fbf0381c4a08e4eb&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=49609581&response-content-disposition=attachment%3B%20filename%3DPowerShell-7.3.4-win-x64.msi&response-content-type=application%2Foctet-stream) 或 [32位](https://objects.githubusercontent.com/github-production-release-asset-2e65be/49609581/9668dc6b-e014-41c4-b088-b6db3e60adc5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAIWNJYAX4CSVEH53A%2F20230518%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20230518T102047Z&X-Amz-Expires=300&X-Amz-Signature=09d17369e5478857557fd62285b8934cbcda3847a3fa23c64268795c2caf875f&X-Amz-SignedHeaders=host&actor_id=0&key_id=0&repo_id=49609581&response-content-disposition=attachment%3B%20filename%3DPowerShell-7.3.4-win-x86.msi&response-content-type=application%2Foctet-stream)，确保pwsh.exe所在路径在系统环境变量PATH中，gitlab-runner会用到pwsh.exe；[在 Windows 上安装 PowerShell - PowerShell | Microsoft Learn](https://learn.microsoft.com/zh-cn/powershell/scripting/install/installing-powershell-on-windows?view=powershell-7.3#msi)

### 安装Gitlab Runner

- [官方文档位置](https://docs.gitlab.com/runner/install/)

- 支持windows， Linux，Docker等安装方式

  ![image-20230903105721283](figures/GitLab_CICD/image-20230903105721283.png)

### 以Windows平台为类，具体说一下如何安装

- 创建存放GitLab-Runner相关文件的文件夹

  ![image-20230903111449254](figures/GitLab_CICD/image-20230903111449254.png)

- 下载GitLab Runner可执行文件，该可执行文件是跨平台的

- windows版本：[Install GitLab Runner on Windows | GitLab](https://docs.gitlab.com/runner/install/windows.html)

  ![image-20230903110325769](figures/GitLab_CICD/image-20230903110325769.png)

- 下载后，将文件重命名，方便后续执行命令：`gitlab-runner-windows-amd64.exe` 修改为 `gitlab-runner.exe`

  ![image-20230903111719237](figures/GitLab_CICD/image-20230903111719237.png)

- 以管理员方式运行cmd命令行窗口，并cd  C:\GitLab-Runner

  ![image-20230903111843420](figures/GitLab_CICD/image-20230903111843420.png)

- 运行GitLab runner

  ![image-20230903112010310](figures/GitLab_CICD/image-20230903112010310.png)

- 注册GitLab Runner

  ![image-20230903110148926](figures/GitLab_CICD/image-20230903110148926.png)

- ![image-20230903145832547](figures/GitLab_CICD/image-20230903145832547.png)

- 安装了`PowerShell-7.3.6-win-x64.msi`后，确认是否已经将`pwsh.exe`放到了Path中，如果有，仍然出现下面的问题，可以尝试重启一下系统

  ![image-20230903173808252](figures/GitLab_CICD/image-20230903173808252.png)

  ![image-20230903175655768](figures/GitLab_CICD/image-20230903175655768.png)

  - 注释说明

    ```
    c:\GitLab-Runner>gitlab-runner.exe register
    Runtime platform                                    arch=amd64 os=windows pid=15596 revision=8ec04662 version=16.3.0
    Enter the GitLab instance URL (for example, https://gitlab.com/):
    #Gitlab网址
    Enter the registration token:
    #上面token可在下个图片所示位置找到，需要与项目匹配；
    Enter a description for the runner:
    [DESKTOP-7NOSC7V]: WX-CYC-Gitrunner	# description这个可以随意是可修改的，可以描述该runner是干什么用的
    Enter tags for the runner (comma-separated):
    # tags很重要!后面也可以修改但不建议后期修改，一旦修改会影响已经绑定该runner的CI运行，.gitlab-ci.yml会定义使用的tags即该名字的runner
    WX-CYC-Gitlabrunner
    Enter optional maintenance note for the runner:
    WX-CYC-Gitlabrunner,build,pwsh  # 输入这个 Runner 的可选维护说明，可以随意写
    WARNING: Support for registration tokens and runner parameters in the 'register' command has been deprecated in GitLab Runner 15.6 and will be replaced with support for authentication tokens. For more information, see https://gitlab.com/gitlab-org/gitlab/-/issues/380872
    Registering runner... succeeded                     runner=E8rHK3x7
    Enter an executor: custom, shell, virtualbox, docker+machine, instance, docker, docker-windows, parallels, ssh, docker-autoscaler, kubernetes:
    [pwsh]: shell  # 会在windows上自动映射到pwsh.exe，所以需要安装powershell 7
    Runner registered successfully. Feel free to start it, but if it's running already the config should be automatically reloaded!
    
    Configuration (with the authentication token) was saved in "c:\\GitLab-Runner\\config.toml"
    ```

    打开Gitlab项目设置中的CI/CD，找到注册好的runner信息

- ![image-20230903112845164](figures/GitLab_CICD/image-20230903112845164.png)

- 至此，Runner已经注册完成，具备一个可部署的环境了



## GitLab CI的语法介绍

[参考文档](http://gitlab.zgmicro.com/help/ci/yaml/README)

```
#流水线的stages的顺序可以自己定义,Runner会按照该顺序执行
#相同阶段的任务将会并发的执行，上一个阶段的任务完整的结束之后，下一个阶段的任务才会开始执行 
stages:
  - build
  - test
  - build-schedules
  - test-schedules

variables:
  GIT_SUBMODULE_STRATEGY: recursive # 拉取 Submodule 内容
  
# patch构建，只要有修改了*.c，*.h，west.yml，.gitlab-ci.yml，*.py相关提交就会触发；
build:
  stage: build
  tags:
    - WX-Gitlabrunner
  script:
    - echo 'stage build' # 显示当前阶段
    - echo 'west update'
    - west update
    - cd tools/CI/	# bat命令：切到工程的tools/CI目录
    - echo "$PWD"	# bat命令：显示所在当前路径
    - echo $CI_COMMIT_SHA	# $CI_COMMIT_SHA 代表本次CI执行拉取代码的哈希值
    #- python CI_build.py	# 执行python脚本，编译top.bin bt.bin，也可通过使用keil相关cmd命令编译
    #- python pack.py $CI_COMMIT_SHA	# 执行python脚本，保存编译后的bin及相关map文件
  allow_failure: false # 是否允许本阶段失败，false：不允许，true：允许
  only: # only:在满足某些条件时执行，
    refs:
      - WS9652 # 仅当分支名是 WS9652 时生效
    changes: #修改了*.c，*.h，west.yml，.gitlab-ci.yml，*.py文件时触发
      - "*.c"
      - "*.h"
      - "west.yml"
      - ".gitlab-ci.yml"
      - "*.py"
  except: # except：在满足某些条件时不执行；only和except冲突时，except优先级更高
    changes:
      - "*.md" # *.md 文件修改不触发

# 构建后测试
test:
  stage: test
  tags:
    - WX-Gitlabrunner
  script:
    - echo 'stage test'
    - cd tools/CI
    - echo "$PWD"
    # - pip install paramiko
    #- python auto_write_test.py $CI_COMMIT_SHA # 执行python脚本，包括自动烧录release/debug版本flash，及烧录后开机测试
  when: manual
  allow_failure: false
  only:
    refs:
      - WS9652
    changes:
      - "*.c"
      - "*.h"
      - "west.yml"
      - ".gitlab-ci.yml"
      - "*.py"
  except:
    changes:
      - "*.md"
 
# 计划构建，仅通过计划触发
build-schedules:
  stage: build-schedules
  tags:
    - WX-Gitlabrunner
  script:
    - echo 'stage build-schedules'
    - echo 'west update'
    - west update
    - cd tools/CI/
    - echo "$PWD"
    - echo $CI_COMMIT_SHA
    - python CI_build.py
    - python pack.py $CI_COMMIT_SHA
  allow_failure: false
  only:
    - schedules # 表示仅允许计划触发

# 计划测试，仅通过计划触发
test-schedules:
  stage: test-schedules
  tags:
    - WX-Gitlabrunner
  script:
    - echo 'stage test-schedules'
    - cd tools/CI
    - echo "$PWD"
    # - pip install paramiko
    - python auto_write_test.py $CI_COMMIT_SHA
  when: manual
  allow_failure: false
  only:
    - schedules 

```

