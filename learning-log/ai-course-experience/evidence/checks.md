# 检查对象与阶段

日期：2026-09-30。Windows25H2/构建26200.6584，Python3.12.10，现有Chrome153.0.8010.53，Playwright1.63.0 headless。没有真实触屏或可见窗口手工测试。

| 数字 | 对象与阶段 | 实际结果 |
|---|---|---|
| 19 tests | b2bdf9e起始应用；py -3.12 tools/check.py | unittest OK，另有语法/JSON/本地链接检查通过；不代表筛选完成 |
| 21 tests、1 failure | 起始版加2项筛选HTTP测试、尚未实现 | open包含done项，真实业务红灯 |
| 21 tests | 隔离练习实现；接口完成、页面接线与干净复现 | unittest OK与Course checks passed；不覆盖浏览器失败态 |
| 17 browser assertions | 练习最终修复版主流程 | 全通过；[逐项JSON](browser-results.json) |
| 独立浏览器复验 | 练习修复版失败及旧响应竞争 | 回滚/旧成功忽略/旧失败忽略/DB不变；[JSON](filter-retest.json) |
| 22 HTTP checks | 后续独立黑盒验收脚本；起始版与练习版分别跑 | 起始17/22、5项预期失败；练习22/22通过。它不是19或21项unittest，也不是浏览器断言 |

独立22项脚本作为作业验收工具保存在 [verify-filter.py](../verify-filter.py)，不改课程tests或默认CI。过程中的课程改进提交没有合进本作业分支；仅将这个隔离验收工具放在作业区便于复现。

运行摘要见 [stdout摘录](stdout-excerpts.txt)，为真实输出的必要节选，不是完整日志；原始HTTP request_id、无关日志与个人路径删除。补丁可应用及干净复现由 [reproduce.py](../reproduce.py) 再核验。

未测：真实新人完成率与8–12h、外部商业模型配置/效果、完整Tab/读屏、跨浏览器、全面XSS/并发/公网生产能力。
