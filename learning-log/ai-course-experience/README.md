# AI代理的一次课程学生作业

这是AI编码代理按学生角色完成的一次实际实践，不是真实新手受试者研究。记录日期：2026-09-30；课程基线：`b2bdf9e2c6a817fad22bd9a2aacfe591456d2738`。没有实测8–12小时，也没有代写用户的观点或感受。

作业只位于课程约定的 `learning-log/`；起始应用保持原样。筛选实现以 [补丁](filter-exercise.patch) 交付，应在另一个练习副本应用，勿直接把作业答案当课程starter。作业分支从远端main建立，没有合入课程改进提交。

## 阅读顺序

1. [任务卡](task-card.md)：需求、边界和完成信号。
2. [提示比较](prompt-comparison.md)：两种实际请求的结果，只有整理摘要，没有私人对话。
3. [过程与反思](experience.md)：五单元实际行动、课程支撑与额外知识。
4. [交接说明](handoff.md)、[独立评审与修复](review.md)：新会话执行、可复现失败与复验。
5. [测试证据](evidence/checks.md)：区分19项起始测试、21项练习测试、17个浏览器断言与22项独立HTTP验收。
6. [自媒体素材索引](media-index.md)：故事线、精选截图、可引用事实和不可声称结论。只是素材，不是发布稿或发布授权。

## 复现

在仓库根目录、Python3.12与Git可用时运行：

```bash
python learning-log/ai-course-experience/reproduce.py
```

Windows可用 `py -3.12` 替换 `python`。脚本复制起始项目到临时练习目录，先检查补丁可应用，再应用补丁，运行21项练习测试与22项HTTP验收；不写原始app、不操作日常数据库，也不提交或发布。终端报告每一步真实退出码。

若要重跑浏览器，先在独立副本应用补丁，并准备Playwright和现有Chrome（仅验收依赖，不是课程主线运行依赖）：

```bash
python learning-log/ai-course-experience/browser-check.py --project YOUR_PRACTICE_COPY --chrome YOUR_CHROME_EXECUTABLE --output YOUR_EVIDENCE_DIRECTORY
```

将三个占位参数替换成自己的实际位置，不要直接照抄。脚本使用新临时数据库与本地端口；17个断言覆盖筛选、指定错误输入、失败回滚、键盘/窄屏、同DB重启。浏览器结果不能替代解释代码或真实学员试用。

未提交数据库、依赖包、ZIP大包、个人用户名/路径/邮箱、凭据、私人会话链接或内部调度记录。四张截图均为本地虚构测试数据。没有push、PR、merge、部署或外部发布。
