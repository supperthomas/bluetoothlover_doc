# Read The Docs上架加入sphinx_markdown_tables后的问题

部署好GitHub后，在Read the Docs官网上构建，提示《**ModuleNotFoundError: No module named 'sphinx_markdown_tables'**》

![image-20220804090054937](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220804090054937.png)

```python
Running Sphinx v5.1.1

Traceback (most recent call last):
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/registry.py", line 442, in load_extension
    mod = import_module(extname)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/importlib/__init__.py", line 127, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 1006, in _gcd_import
  File "<frozen importlib._bootstrap>", line 983, in _find_and_load
  File "<frozen importlib._bootstrap>", line 965, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'sphinx_markdown_tables'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/cmd/build.py", line 276, in build_main
    args.pdb)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/application.py", line 222, in __init__
    self.setup_extension(extension)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/application.py", line 400, in setup_extension
    self.registry.load_extension(self, extname)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/registry.py", line 446, in load_extension
    err) from err
sphinx.errors.ExtensionError: Could not import extension sphinx_markdown_tables (exception: No module named 'sphinx_markdown_tables')

Extension error:
Could not import extension sphinx_markdown_tables (exception: No module named 'sphinx_markdown_tables')
命令耗时： 0s 返回: 2
Stay Up
```





按照别的博客分享的建议，新建了：《**requirements.txt**》在里面加入了《**sphinx-markdown-tables==0.0.15**》。

![image-20220804092059266](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220804092059266.png)



本来以为就好了，再次构建，依然提示有问题。提示《`TypeError: __init__() missing 1 required positional argument: 'config'`》。

![image-20220804091342518](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220804091342518.png)

```python
Running Sphinx v5.1.1
making output directory... done
building [mo]: targets for 0 po files that are out of date
building [html]: targets for 4 source files that are out of date
updating environment: [new config] 4 added, 0 changed, 0 removed
reading sources... [ 25%] index

Traceback (most recent call last):
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/events.py", line 94, in emit
    results.append(listener.handler(self.app, *args))
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx_markdown_tables/__init__.py", line 24, in process_tables
    table_processor = markdown.extensions.tables.TableProcessor(md.parser)
TypeError: __init__() missing 1 required positional argument: 'config'

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/cmd/build.py", line 277, in build_main
    app.build(args.force_all, filenames)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/application.py", line 349, in build
    self.builder.build_update()
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/builders/__init__.py", line 303, in build_update
    len(to_build))
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/builders/__init__.py", line 317, in build
    updated_docnames = set(self.read())
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/builders/__init__.py", line 424, in read
    self._read_serial(docnames)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/builders/__init__.py", line 445, in _read_serial
    self.read_doc(docname)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/builders/__init__.py", line 498, in read_doc
    publisher.publish()
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/docutils/core.py", line 218, in publish
    self.settings)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/io.py", line 103, in read
    self.input = self.read_source(settings.env)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/io.py", line 113, in read_source
    env.events.emit('source-read', env.docname, arg)
  File "/home/docs/checkouts/readthedocs.org/user_builds/study-docs/envs/latest/lib/python3.7/site-packages/sphinx/events.py", line 106, in emit
    (listener.handler, name), exc, modname=modname) from exc
sphinx.errors.ExtensionError: Handler <function process_tables at 0x7f7e17408290> for event 'source-read' threw an exception (exception: __init__() missing 1 required positional argument: 'config')

Extension error (sphinx_markdown_tables):
Handler <function process_tables at 0x7f7e17408290> for event 'source-read' threw an exception (exception: __init__() missing 1 required positional argument: 'config')
命令耗时： 0s 返回: 2
```



不用想，肯定是版本有问题，博客上大佬用得是4.x.x的Sphinx版本，我这边都到5.1.1。通过`python -m pip list`查看本地安装的包依赖。要加入的模块版本是0.0.17，`sphinx-markdown-tables        0.0.17`。

```python
D:\worksplace\github\read_the_doc\zephyr_polling\porting\windows_libusb_win32>python -m pip list
Package                       Version
----------------------------- -----------
alabaster                     0.7.12
Babel                         2.10.3
certifi                       2022.6.15
charset-normalizer            2.1.0
colorama                      0.4.5
commonmark                    0.9.1
construct                     2.10.68
docutils                      0.17.1
future                        0.18.2
idna                          3.3
imagesize                     1.4.1
iso8601                       1.0.2
Jinja2                        3.1.2
livereload                    2.6.3
Markdown                      3.4.1
MarkupSafe                    2.1.1
packaging                     21.3
pip                           22.1.2
Pygments                      2.12.0
pyparsing                     3.0.9
pyserial                      3.5
pytz                          2022.1
pyusb                         1.2.1
PyYAML                        6.0
recommonmark                  0.7.1
requests                      2.28.1
SCons                         4.3.0
serial                        0.0.97
setuptools                    58.1.0
six                           1.16.0
snowballstemmer               2.2.0
Sphinx                        5.1.1
sphinx-autobuild              2021.3.14
sphinx-markdown-tables        0.0.17
sphinx-rtd-theme              1.0.0
sphinxcontrib-applehelp       1.0.2
sphinxcontrib-devhelp         1.0.2
sphinxcontrib-htmlhelp        2.0.0
sphinxcontrib-jsmath          1.0.1
sphinxcontrib-qthelp          1.0.3
sphinxcontrib-serializinghtml 1.1.5
tornado                       6.2
urllib3                       1.26.11
usb                           0.0.83.dev0
xlrd                          2.0.1

[notice] A new release of pip available: 22.1.2 -> 22.2.1
[notice] To update, run: python.exe -m pip install --upgrade pip
```



既然确定了是版本不一致，直接改《**requirements.txt**》在里面调整为《**sphinx-markdown-tables==0.0.17**》。当然为了避免后续Read The Doc服务器更新版本导致我本地不能用得问题，再把一些我觉得需要的也加入进去。

![image-20220804092021866](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220804092021866.png)

再次到Read The Docs官网查看，已经是构建通过了。项目地址在这[Welcome to study_docs’s documentation! — study_docs 0.0.0 documentation (study-docs.readthedocs.io)](https://study-docs.readthedocs.io/en/latest/)，可以直接进去看源码。

![image-20220804092345128](https://markdown-1306347444.cos.ap-shanghai.myqcloud.com/img/image-20220804092345128.png)