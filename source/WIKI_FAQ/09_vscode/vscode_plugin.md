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

```
//  正常注释
//* 浅绿色
//! 红色
//? 蓝色
//// 灰色
//todo 橘红色
```
