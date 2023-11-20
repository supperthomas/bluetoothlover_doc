# action 理解

assigner.yml     =》如何分配PR的CI   set_assignees.py
backport.yml  =》 Backport 有这个标号的会对其进行反馈
backport_issue_check.yml => 对backport的branch进行处理  list_backports.py
bsim-tests-publish.yaml   =》对下面那个测试的发布
bsim-tests.yaml  =》蓝牙相关的PR ， 这个比较复杂，也比较重要。
bug_snapshot.yaml  =》 将bug上传到亚马逊云

clang.yaml =》用twist测试框架进行测试，
codecov.yaml  =》 覆盖率测试并上传结果
coding_guidelines.yml  =》 guideline_check.py 来检查PR的coding guide
compliance.yml     =》check_compliance.py 来检查遵守原则
daily_test_version.yml  =》日常版本检查
devicetree_checks.yml  =》负责scripts/dts文件夹下面的修改，看起来像是用来测试设备树的
doc-build.yml  =》 doxygen version的修改，这里有doxygen的版本下载和使用，主要来执行doc里面的Makefile
doc-publish-pr.yml  =》这个依赖上面的workfolw的完成，会把结果上传到亚马逊平台上
doc-publish.yml  =》这个也会上传到亚马逊平台上
do_not_merge.yml  =》对于标记DNM 和TSC 的PR会特殊处理，不要merge， 不是很重要
errno.yml   =>scripts/ci/errno.py 执行这个，看代码好像检查error 的number是否一样
footprint-tracking.yml  =》  这个是用来跟踪ROM代码大小和RAM代码大小的比较，跟踪每一个commit
footprint.yml     =》这个对ROM size和RAM size进行比较
greet_first_time_contributor.yml  =》 对于第一次贡献的人进行commit ，如果PR merged的话，提供感谢
issues-report-config.json => 给yml使用的
issue_count.yml  =》收集每天issue 数量，并统计到https://testing.zephyrproject.org/issues/zephyrproject-rtos/zephyr/index.html
license_check.yml  =》 zephyrproject-rtos/action_scancode 用这个action来检查license
manifest.yml  => zephyrproject-rtos/action-manifest  manifest 来集成
release.yml  =》 打tag之后，发布release版本
scripts_tests.yml   =》用pytest 对scripts\build 下面的脚本进行测试
stale-workflow-queue-cleanup.yml  =》MajorScruffy/delete-old-workflow-runs 清理陈旧的workflow
stale_issue.yml  =》 关闭陈旧的issue
twister.yaml  =》运行twister单元测试
twister_tests.yml  => pytest ./scripts/pylib/pytest-twister-harness/tests  pytest 执行twister的测试，修改twister的时候需要测试

west_cmds.yml=》./scripts/west_commands/run_tests.py  执行west command的测试。



## 重要的action

### twister.yaml

```
    branches:
      - main
      - v*-branch
```

对所有分支进行检查



```
python3 ./scripts/ci/test_plan.py -c origin/${BASE_REF}.. --pull-request -t $TESTS_PER_BUILDER
```

产生test plan

twister 介绍

https://www.yii666.com/blog/378468.html



cmd

```
./scripts/twister -p nucleo_l496zg --device-testing --device-serial /dev/ttyACM0 -T tests/kernel/common/
```

log 在twister-out/twister.log

如果想要html显示的话：

```
          pip3 install junitparser junit2html
          junitparser merge artifacts/*/*/twister.xml junit.xml
          junit2html junit.xml junit.html
```





### bsim-tests.yaml

蓝牙相关,模拟测试



### codecov.yaml





### 其他文本的检查

