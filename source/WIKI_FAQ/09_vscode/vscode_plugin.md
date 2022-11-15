# VSCode 常用插件

更全面的信息可以参考官方 [调试手册](https://code.visualstudio.com/docs/editor/debugging#_launch-configurations) ，

## 快捷键

- ctrl + shift + p  显示命令
- ctrl + alt + F 格式化文件

## files.exclude 和 search.exclude

- files.exclude 用于从当前工作区排除一些文件，也就是不在左侧的工作区间显示。
- search.exclude 用于从搜索路径里排除一些文件，当我们全局搜索某个变量、函数名或字符串时，不会搜索这些文件里的内容。

上述两个配置项我一般都是成对使用，对于不想显示的文件，自然也不想搜索。

官方介绍链接：https://code.visualstudio.com/docs/getstarted/userinterface

files.exclude 和 search.exclude 配置项都是在 .vscode/settings 文件里，下面列出一些常用的点：

- `**` 代码当前工作区目录，`**/.git` 即当前工作区下的 .git 目录。
- 配置的路径支持[通配符](https://m.linuxidc.com/Linux/2017-08/146463.htm)，`[]` 代表可选，例如 [1234] 代表可选 1,2,3,4，当然也可以写成 [1-4]；`*` 代表可匹配任意个字。例如 `[**/bsp/[a-y]*]` 代表匹配工作目录 bsp 目录下，从 a 到 y 字母开头的目录。

## 插件

### git graph  git图形化工具类似于git gui
- Git Graph extension for Visual Studio Code

### Git-commit-plugin For Vscode  
- git commit 图形化工具

### indent-rainbow 
- 代码格式对齐
- 代码块着色，使得代码整齐美观

### Bracket Pair Colorizer
- 括号成对带颜色，非常方便

### Markdown All in One
- markdown写作利器，可以预览，可以直接转成pdf

### Intel Hex format
- 能看hex文件和bin文件

### koroFileHeader
- 用于生成文件头部和函数的注释

### Better Comments
- 代码注释高亮，具体使用如下:
  - ！红色注释
  - ? 蓝色注释
  - // 灰色删除线注释
  - todo 橘红色注释
  - * 浅绿色注释

```json
//  正常注释
//* 浅绿色
//! 红色
//? 蓝色
//// 灰色
//todo 橘红色
```

### highlight-words
[参考链接](https://blog.csdn.net/palmer_kai/article/details/79548164)
- 可以达到类似于SourceInsight高亮的效果

#### 安装配置步骤
- 安装插件
- 进行快捷键绑定，只需要绑定Highlight Toggle Current，比如F8，注意，可能需要解绑其他的F8快捷键
- 在setting.json中加入配置选项： "highlightwords.defaultMode": 1





### Doxygen Documentation Generator

[Doxygen Documentation Generator](https://blog.csdn.net/lblmlms/article/details/113662339)



可以达到如下效果

![](https://gitee.com/chenyingchun0312/article-images/raw/master/Typora/test11112.gif)

Doxygen Documentation Generator插件可以方便地生成规范的注释。使用方式：

1. 当在文件头部输入 “/**” 后回车,自动生成模板文件注释。

2. 在函数上面 “/**” 后回车,自动生成模板函数注释。

3. 如果上面两种方式无效果（可能和其他插件冲突），在输入```/***/```后，将光标移动至第二个```*```后，按下enter回车

   

**在settings.json中配置如下（也可以使用默认值，看需要）：**

```json
	// /**回车后最多向下多少行去找函数声明
 	"doxdocgen.generic.linesToGet": 4,
	// 作者名和邮箱
	"doxdocgen.generic.authorName": "name",
    "doxdocgen.generic.authorEmail": "xx@foxmail.com",
    "doxdocgen.generic.authorTag": "@Author : {author} ({email})",
	// 日期格式
    "doxdocgen.generic.dateFormat": "YYYY-MM-DD",
    "doxdocgen.generic.dateTemplate": "@Creat Date : {date}",
	// 简介格式
    "doxdocgen.generic.briefTemplate": "@Brief : {text}",
   
    // 文件注释的格式
    "doxdocgen.file.fileTemplate": "@File Name: {name}",
    "doxdocgen.file.versionTag": "@Version : 1.0",
    "doxdocgen.file.copyrightTag": [
        "@copyright Copyright (c) {year} XXXX技术有限公司"
    ],
    
    // 自定义文件注释格式
    "doxdocgen.file.customTag": [
        "modification history :",
        "Date:       Version:      Author:     ",
        "Changes: ",
    ],
    // 文件注释组成及顺序
    "doxdocgen.file.fileOrder": [
        "file",		// @file
        "brief",	// @brief 简介
        "author",	// 作者
        "version",	// 版本
        "date",		// 日期
        "empty",	// 空行
        // "copyright",// 版权
        // "custom"	// 自定义
    ],

	// 参数注释和返回注释的格式
	"doxdocgen.generic.paramTemplate": "@param{indent:8}{param}{indent:25}",
    "doxdocgen.generic.returnTemplate": "@return{indent:8}{type}{indent:25}",
    // 函数注释组成及顺序
    "doxdocgen.generic.order": [
        "brief",
        "tparam",
        "param",
        "return"
    ],
```
### Code Spell Checker
- 检查单词拼写，以及单词纠正

### Draw.io Integration
- draw io 画流程图
- 
https://github.com/supperthomas/vscode-plugin-drawio

###  GitHub Pull Requests and Issues
 处理pull request 和issue的工具

###  github remote tool （container，ssh，wsl）
remote- Container
remote - ssh
remote - wsl

### WaveDrom
画时序图
https://mp.weixin.qq.com/s/XUQcsaFhyfEQZ25Gc0p-nQ

### Power Mode

Vscode 里面一款炫酷的代码编辑插件，打字时可根据自己的设置展现出非常炫酷的动画效果；

使用步骤：

1. 在商店里面扩展->搜索Power Mode,点击安装;
2. 打开vscode左下角设置图标，选择设置；
3. 选择右上角的三个点展开->点击类似油壶的图标（setting.json);
4. Copy下面代码点击保存即可；

```json
  //是否开启
    "powermode.enabled": true,
    //效果样式  “水花-particles”, “烟花-fireworks”, “火焰-flames”, “雪花-magic”, “幽灵-clippy”, “激光-simple-rift”, “大激光-exploding-rift”
    "powermode.presets": "flames",
    //时间间隔
    "powermode.combo.timeout": 5,
    //是否抖动
    "powermode.shake.enabled": false,
```

说明：可根据自己喜欢的样式根据语法更改

### change-case

Vscode 里面一款可以修改变量名为小驼峰的插件；

使用步骤：

1. 在商店里面扩展->搜索change-case,点击安装;
2. 选中变量；
3. 按F1 输入camel（小驼峰）;

也可以点击后面的设置快捷键


