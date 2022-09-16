# sphinx-autobuild OSError: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。

## 引言

最近在搭建在线电子书：Sphinx + Github + ReadTheDocs，每次都需要打开index.html很麻烦，尝试《sphinx-autobuild》来自动构建，这样就不需要每次都通过《make html来操作》



## 搭建环境

如何构建环境网上有很多大佬写好了，就不在此展示了。

[搭建在线电子书：Sphinx + Github + ReadTheDocs_测试开发小记的博客-CSDN博客](https://blog.csdn.net/u010698107/article/details/120640628)

[Sphinx+gitee+Read the Docs搭建在线文档系统_DLGG创客DIY的博客-CSDN博客](https://blog.csdn.net/tiandiren111/article/details/119524919?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-119524919-blog-120640628.pc_relevant_multi_platform_featuressortv2removedup&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~CTRLIST~default-1-119524919-blog-120640628.pc_relevant_multi_platform_featuressortv2removedup&utm_relevant_index=2)



## 问题

按照操作执行《**sphinx-autobuild source build/html**》，而后提示：**OSError: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。**

```python
D:\worksplace\github\read_the_doc\study_docs\docs>sphinx-autobuild source build/html
[sphinx-autobuild] > sphinx-build 'D:\worksplace\github\read_the_doc\study_docs\docs\source' 'D:\worksplace\github\read_the_doc\study_docs\docs\build\html'
Running Sphinx v5.1.1
loading translations [zh_CN]... done
loading pickled environment... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 0 source files that are out of date
updating environment: [extensions changed ('sphinx_markdown_tables')] 3 added, 0 changed, 0 removed
C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\recommonmark\parser.py:75: UserWarning: Container node skipped: type=document
  warn("Container node skipped: type={0}".format(mdnode.t))
reading sources... [100%] markdown/index
looking for now-outdated files... none found
pickling environment... done
checking consistency... done
preparing documents... done
writing output... [100%] markdown/index
generating indices... genindex done
writing additional pages... search done
copying static files... WARNING: Failed to copy a file in html_static_file: C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\sphinx\templates\apidoc/package.rst_t: TemplateRuntimeError("No filter named 'heading' found.")
WARNING: Failed to copy a file in html_static_file: C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\sphinx\templates\apidoc/toc.rst_t: TemplateAssertionError("No filter named 'heading'.")
WARNING: Failed to copy a file in html_static_file: C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\sphinx\templates\quickstart/conf.py_t: TemplateAssertionError("No filter named 'repr'.")
done
copying extra files... done
dumping search index in Chinese (code: zh)... done
dumping object inventory... done
build succeeded, 3 warnings.

The HTML pages are in build\html.
[I 220803 20:29:18 server:335] Serving on http://127.0.0.1:8000
Traceback (most recent call last):
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 196, in _run_module_as_main
    return _run_code(code, main_globals, None,
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\runpy.py", line 86, in _run_code
    exec(code, run_globals)
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\Scripts\sphinx-autobuild.exe\__main__.py", line 7, in <module>
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\sphinx_autobuild\cli.py", line 196, in main
    server.serve(port=portn, host=args.host, root=outdir)
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\livereload\server.py", line 339, in serve
    self.application(
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\livereload\server.py", line 291, in application
    app.listen(port, address=host)
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\tornado\web.py", line 2134, in listen
    server.listen(
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\tornado\tcpserver.py", line 183, in listen
    sockets = bind_sockets(
  File "C:\Users\wenbo\AppData\Local\Programs\Python\Python310\lib\site-packages\tornado\netutil.py", line 162, in bind_sockets
    sock.bind(sockaddr)
OSError: [WinError 10013] 以一种访问权限不允许的方式做了一个访问套接字的尝试。
```

网上直接搜索没看到基本都是讲别的问题，[Error: [WinError 10013\] 以一种访问权限不允许的方式做了一个访问套接字的尝试 (bbsmax.com)](https://www.bbsmax.com/A/KE5Qwk24zL/)，但是大体是知道这个端口被占用了。

```python
C:\Users\Administrator>netstat -ano|findstr 端口号

C:\Users\Administrator>tasklist |findstr pid号

C:\Users\Administrator>taskkill /pid pid号 /F
```



一查，确实有东西在占用，也不知道是什么，直接干掉怕有别的问题，先不管。想着不可能只有我遇到问题，help里面肯定有说明。

```python
D:\worksplace\github\read_the_doc\study_docs\docs>netstat -ano|findstr 8000
  TCP    0.0.0.0:8000           0.0.0.0:0              LISTENING       32308
  UDP    0.0.0.0:8000           *:*                                    32308
```



直接输入《**sphinx-autobuild**》可以看到《**[--port PORT]**》的配置，那一下就懂了，肯定用他可以改端口。

```python
D:\worksplace\github\read_the_doc\study_docs\docs>sphinx-autobuild
usage: sphinx-autobuild [-h] [--port PORT] [--host HOST] [--re-ignore RE_IGNORE] [--ignore IGNORE] [--no-initial]
                        [--open-browser] [--delay DELAY] [--watch DIR] [--pre-build COMMAND] [--version]
                        sourcedir outdir [filenames ...]
sphinx-autobuild: error: the following arguments are required: sourcedir, outdir, filenames
```





执行《**sphinx-autobuild source build/html --port 8001**》指定port为8001，就OK了。

```python
D:\worksplace\github\read_the_doc\study_docs\docs>sphinx-autobuild source build/html --port 8001
[sphinx-autobuild] > sphinx-build 'D:\worksplace\github\read_the_doc\study_docs\docs\source' 'D:\worksplace\github\read_the_doc\study_docs\docs\build\html'
Running Sphinx v5.1.1
loading translations [zh_CN]... done
loading pickled environment... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 0 source files that are out of date
updating environment: 0 added, 0 changed, 0 removed
looking for now-outdated files... none found
no targets are out of date.
build succeeded.

The HTML pages are in build\html.
[I 220803 20:33:35 server:335] Serving on http://127.0.0.1:8001
[I 220803 20:33:35 handlers:62] Start watching changes
[I 220803 20:33:35 handlers:64] Start detecting changes
[I 220803 20:34:20 handlers:135] Browser Connected: http://127.0.0.1:8001/
[W 220803 20:34:20 web:2271] 404 GET /favicon.ico (127.0.0.1) 1.59ms
[I 220803 20:34:23 handlers:135] Browser Connected: http://127.0.0.1:8001/markdown/index.html
[I 220803 20:34:24 handlers:135] Browser Connected: http://127.0.0.1:8001/markdown/Typora%2BPicGo%2B%E8%85%BE%E8%AE%AF%E4%BA%91.html
[I 220803 20:38:45 watcher:110] Running task: build (delay: None)
[sphinx-autobuild] Detected change: D:\worksplace\github\read_the_doc\study_docs\docs\source\markdown\sphinx-autobuild_error.md
[sphinx-autobuild] > sphinx-build 'D:\worksplace\github\read_the_doc\study_docs\docs\source' 'D:\worksplace\github\read_the_doc\study_docs\docs\build\html'
```



打开网站《http://127.0.0.1:8001》，只要终端不关闭，只要检测到有改动，就会自动更新，还是蛮方便的。

![image-20220803205150542](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220803205150542.png)

