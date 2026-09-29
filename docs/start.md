# 学习指南与环境准备

## 开始前你只需要这些

一台能运行 Python 的电脑、浏览器、文本编辑器、每周两三个不被打断的时段。主线不需要显卡，不需要安装 Node、Conda、Poetry 或数据库服务。浏览器聊天助手、IDE 助手、终端 Agent 可以任选，也可以先不接模型。

先做三个动作自测：看懂 `if` 的两个分支；给函数传入字符串并打印结果；找到一条异常信息的最后一行。做不到就先完成预备课，卡住是补基础的信号。

## 安装与确认

从 [Python 官网](https://www.python.org/downloads/) 安装 Python 3.12；Windows 安装时启用命令行启动器与 PATH 选项。Mac/Linux 终端输入 `python3 --version`，Windows PowerShell 输入 `py -3.12 --version`。Linux 若系统已有其他版本，可使用发行版支持的安装方式，不要覆盖系统 Python。

主线只用标准库，无须执行 `pip install`。可选 MCP 实验另有独立环境，不能把其依赖混进主线。项目命令都从**仓库根目录**执行，那里能同时看到 `README.md`、`app` 和 `tools`。

| 动作 | macOS / Linux | Windows PowerShell |
| --- | --- | --- |
| 检查位置 | `pwd` | `Get-Location` |
| 列出文件 | `ls` | `Get-ChildItem` |
| 进入解压后的文件夹 | `cd modern-software-dev-course` | `cd modern-software-dev-course` |
| 检查课程 | `python3 tools/check.py` | `py -3.12 tools/check.py` |
| 启动应用 | `python3 -m app.server` | `py -3.12 -m app.server` |
| 停止应用 | Ctrl+C | Ctrl+C |

文件夹名以你实际解压的名字为准；GitHub ZIP 常带 `-main` 后缀。后文用 `python` 表示已确认的解释器；如果电脑只有 `python3` 或 `py -3.12`，替换命令的第一部分即可。

## 30 分钟开箱

1. 运行检查，观察 `OK` 和 `Course checks passed`。第一次不理解全部代码没有关系。
2. 启动应用，打开终端显示的本地地址。
3. 添加「完成预备课」，标记完成，改名；刷新页面，再重启服务确认数据仍在。
4. 笔记区输入两行：`- 看第一课` 和 `今天心情不错`。预览应只有一个候选任务，且尚未保存。
5. 逐条添加候选任务。检查 `data/tasks.db` 已出现；它是本地数据库，不提交到 Git。
6. 复制 [周报](../templates/weekly-report.md) 到自己的笔记中，写下版本、命令、观察结果。

## Git 和 GitHub 的最短路线

Git 是本地修改历史，GitHub 是存放仓库与协作的服务。下载 ZIP 可以学习；需要 PR 时再安装 [Git](https://git-scm.com/downloads)。学习仓库可从课程仓库 Fork 到自己账号，再克隆你的 Fork。

```bash
git status
git switch -c week01/prompt-experiment
git diff
git add lessons/01-prompting.md
git commit -m "docs: record my first prompt experiment"
```

上面的 `git add` 是演示路径；实际提交你改过的文件。不要把示例周报写进共享讲义，建议在自己的 Fork 新建 `learning-log/week01.md`。首次提交若要求作者身份，配置自己的姓名和邮箱；需要保护邮箱时使用 GitHub 提供的 noreply 地址。

提交前用 `git diff --cached` 看清要上传什么，然后 `git push -u origin week01/prompt-experiment`。到自己 Fork 页面创建 PR，base 选择自己 Fork 的主分支。无需向上游课程仓库提交个人作业。

## 固定一周的节奏

30 分钟回顾与概念 → 45 分钟跟做 → 90–150 分钟练习 → 30–45 分钟测试和写周报 → 15 分钟复盘。若超时，保住必做目标，跳过进阶。遇到环境问题连续 30 分钟没进展，就带命令、完整报错、系统版本求助；不要只说「不能运行」。

每周保留三个证据：一个能运行的行为、一条真实失败及其处理、一段你自己写的解释。完成按钮点了多少次、模型输出了多少行，都不等于学会。

## 工具替代原则

| 需要的能力 | 最低配置 | 可选升级 | 受限时怎么做 |
| --- | --- | --- | --- |
| 讨论需求与解释代码 | 任意可用聊天助手 | 能读取仓库的编码助手 | 用讲义样例与同学互评 |
| 执行与验证 | 系统终端 + Python | IDE 集成终端 | 完全相同的命令手动执行 |
| 版本与评审 | Git + 本地 diff | GitHub PR | 导出 diff 并写评审记录 |
| 模型实验 | 手工保存真实回答 | 本地模型或 API | 用规则基线练评测，不把结果称为模型效果 |
| MCP | 契约 + 离线工具调用 | 官方 SDK + 支持 MCP 的客户端 | 交基础作业，真实集成单独标为未完成 |

AI 工具的可用地区、登录方式、费用和套餐会变化，以使用时的官方说明为准。不要为完成基础线购买指定产品。每次模型实验记下工具、模型标识（若可见）、日期与设置；不捏造未显示的信息。
