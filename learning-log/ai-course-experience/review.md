# 独立评审：筛选失败后控件和结果错位

评审者为未参与实现的AI助手；另有技术验收者人工式diff审查。不是第二个真人学员，也不是新手用户访谈。仅保留发现与运行结果，未包含内部会话记录。

## 复现与实际/期望

1. 准备未完成任务，成功加载open。
2. 中断下一次done GET，再选择已完成。
3. 观察控件、列表、错误和数据库。

实际：控件done，仍显示2条未勾选open任务，错误Failed to fetch；DB的done为空，数据未变。见 [失败JSON](evidence/filter-failure.json) 和 [失败截图](evidence/screenshots/failure.png)。

期望：控件与可见结果一致，或者隐藏/明确标注旧结果属于上次筛选；不把旧列表表示成新请求成功。

## 采纳、修复、复验

在练习实现中保存displayedStatus；仅最新请求失败时回到最近成功选择、提示保留上次结果与恢复重试；过期成功/失败都忽略。SQL与数据库未改。

独立复验通过：回滚open、保留原列表且中文说明；先挂起旧done，再完成较新open，旧成功响应释放后不覆盖新结果；旧失败释放后不留下过期错误；DB不变。见 [复验JSON](evidence/filter-retest.json) 和 [修复截图](evidence/screenshots/fixed.png)。

失败与复验使用虚构独立夹具，重跑时任务数由2变3；不能把两张截图当同一数据库的精确前后计数比较。相同的是触发逻辑与控件/列表一致性。

实现见 [补丁](filter-exercise.patch)，主流程17个浏览器断言见 [结果](evidence/browser-results.json)。没有残余已确认阻断；指定XSS负载通过不等于全面安全审计。没有虚构漏洞、用户情绪或第三方观点。
