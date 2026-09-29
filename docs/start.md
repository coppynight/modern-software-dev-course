# 5 分钟准备

[课程首页](../README.md) · [开始主线 1](../lessons/01-spec.md)

## 选一个项目和一款助手

使用熟悉的小项目，或附带的「小事板」。准备一款可用的聊天/编码助手：能直接读写仓库更方便；只有聊天工具也可以由你执行命令、回传必要结果。记录真实调用与执行，不把离线模拟当作 AI 实践。

主线默认你能读懂函数、运行项目、查看 diff 并保存修改。不熟悉时，按需进入 [编程与运行基础](../optional/00-foundations.md) 或 [环境与 Git 补课](../optional/setup-git.md)，无需先学完所有选学。

## 使用「小事板」时

在仓库根目录执行，示例验证基线为 Python 3.12，无第三方运行依赖：

```bash
python3 tools/check.py
python3 -m app.server
```

Windows 用 `py -3.12`；虚拟环境内也可用 `python`。看到 `Course checks passed` 后启动服务，打开 <http://127.0.0.1:8000>，创建一条任务并刷新，确认仍在。按 Ctrl+C 停止。

入口：`app/domain.py` 是业务规则，`app/store.py` 是存储，`app/server.py` 是接口，`app/static/` 是页面，`tests/` 是测试。需要时查 [API 文档](api.md)，报错时查 [排错表](troubleshooting.md)。

## 只选一个变化

推荐任务：增加「全部 / 未完成 / 已完成」筛选。也可选择自己项目中一个同等大小、可在几小时内完成的功能。

复制 [任务卡](../templates/task-card.md)，接下来 5 个单元持续完善它。自有项目使用自己的启动与测试命令，完成标准保持一致。
