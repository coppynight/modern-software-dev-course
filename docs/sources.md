# 来源、版本与改编说明

核对日期：2026-09-28。这里记录可查证的材料边界，方便课程维护者检查；未取得的课堂内容不补写成教师原话。

## 一手材料

| 编号 | 来源 | 本次实际核对的内容 |
| --- | --- | --- |
| S1 | [Stanford Bulletin / CS146S](https://bulletin.stanford.edu/courses/2274401) | 课程身份与课程描述 |
| S2 | [课程官网 · Fall 2025](https://themodernsoftware.dev/fall2025) | Syllabus 标签页对应的 10 周主题、阅读与作业链接；从公开网页脚本中的 2025 课程数据核对 |
| S3 | [2025 作业固定版本](https://github.com/mihail911/modern-software-dev-assignments/tree/ca2df55b78d6194612b65ae3fbfaa55a4678a683) | `fall2025` 分支的 week1–week8 作业全文、目录与 starter 结构 |
| S4 | [课程官网 · Fall 2026](https://themodernsoftware.dev/) | 2026 公开排期、10 周主题；未来周属于计划，不当作已经讲授的内容 |
| S5 | [2026 作业固定版本](https://github.com/mihail911/modern-software-dev-assignments/tree/90a2fbb8b1fe98674dbba6719724c373fb27734f) | master 当时仅有 week1：真实编码 Agent 会话请求与工具轨迹剖析 |

官网部分 2025 作业链接仍指向 `master/weekN`，而 master 已切换学期。重访旧作业请使用这里的固定 SHA 或 `fall2025` 分支。2025 树未发现 week9、week10 作业；不能据此推断原课堂没有其他活动。

本次以公开大纲、作业文字和起始项目结构为依据，没有逐页核验全部 Slides、未公开的课堂讲述、学生答案、嘉宾发言或校内系统。下表的「还原」指重建学习目标与实践链路，不是复刻每节课堂。

## 逐周映射

| 原大纲周次与主题（简译） | 已核对的官方作业 | 本课程的改编与新增 |
| --- | --- | --- |
| 1：编码 LLM 与提示 | [6 类提示练习](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week1/assignment.md)：样例提示、分步求解、工具调用、多次采样、检索、反馈迭代 | 中文任务提取、冻结评测集、规则基线；不要求运行原本的 8B/12B 模型 |
| 2：编码 Agent 组成 | [行动项提取器](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week2/assignment.md)：模型替换、测试、重构、接口、README | 原创标准库应用，降低 FastAPI/SQLAlchemy/环境安装负担；LLM 接入为完整 AI 线 |
| 3：AI IDE、上下文和规格 | [自定义 MCP Server](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week3/assignment.md)：封装外部 API，至少 2 工具、错误处理、部署模式 | 先写上下文与接口契约，再用本地数据练两工具；连接外部 API 和真实 MCP 为进阶 |
| 4：Agent 协作模式 | [Claude Code 自动化](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week4/assignment.md)：至少两种自动化并实际使用 | 工具中立的项目指令与检查、文档同步流程，允许同一人分角色串行完成 |
| 5：现代终端 | [Warp 自动化与多 Agent](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week5/assignment.md) | 系统终端与 Git worktree；真实并行 Agent 为选做，记录合并与协调成本 |
| 6：测试与安全 | [Semgrep 扫描与至少 3 项修复](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week6/assignment.md) | 三类课堂风险审查与回归测试；扫描工具可选，不能把零告警等同安全 |
| 7：支持、诊断、评审 | [Graphite 人工/AI 评审与 4 PR](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week7/assignment.md) | 必做 2 个小 PR、先人工后 AI 的对照；进阶 4 PR，不依赖教育试用 |
| 8：UI 与应用生成 | [同一应用 3 技术栈](https://github.com/mihail911/modern-software-dev-assignments/blob/ca2df55b78d6194612b65ae3fbfaa55a4678a683/week8/assignment.md)，含 Bolt 与非 JS 栈 | 必做一个完整流程与用户观察；第二/第三栈为选做，保留比较分析 |
| 9：部署后的 Agent | 该固定仓库无对应周作业 | 依据大纲的日志、诊断、事故响应主题，新增本地故障恢复实验 |
| 10：软件工程未来 | 该固定仓库无对应周作业 | 新增毕业评分、可复现交付与个人工作流复盘 |

第 0 课、中文讲解、课时、示例答案、自检标准、评分比例、主线代码、模板和讲师手册均为本项目原创设计。不要把它们称为 Stanford 要求。

## 技术依据与继续阅读

- [Python 3.12 Tutorial](https://docs.python.org/3.12/tutorial/)：预备课查语法。
- [Python http.server](https://docs.python.org/3.12/library/http.server.html)：本地教学服务器的接口及生产用途限制。
- [Python sqlite3](https://docs.python.org/3.12/library/sqlite3.html)：参数绑定与事务。
- [Git Book](https://git-scm.com/book/en/v2)：分支、提交、撤销和协作。
- [GitHub Actions 快速开始](https://docs.github.com/en/actions/get-started/quickstart)：仓库检查流程。
- [MCP 官方构建指南](https://modelcontextprotocol.io/docs/develop/build-server) 与 [Python SDK](https://github.com/modelcontextprotocol/python-sdk)：真实协议接入；SDK 随版本变化，实验记录需写明版本。
- [Google SRE：Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)：监控指标与告警的延伸阅读。

每课页尾将引用映射到此处。阅读材料用于核验与继续学习；本项目不打包第三方讲义或商业产品的教育优惠码。上游固定树未见明确 LICENSE 文件，因此未搬运其代码，未对其材料重新授权。

## 维护检查清单

更新课程时先记录检查日期、官网学期和作业 SHA，再检查哪些周有实际作业。对于排期只写「计划」。若新版本改变工具或模型，先跑通示例，再更新课文与验收命令。价格、优惠和账号能力不写死。更正事实时在 CHANGELOG 标出影响哪些周。
