# 第 7 周评审案例：看起来很短的筛选功能

规格：`done=None` 返回全部；`done=False` 返回未完成；`done=True` 返回已完成。`limit` 必须是 1–50 的整数，不能接受布尔值。函数不能改变输入列表。

候选实现（阅读练习，不进入起始应用）：

```python
def select_tasks(tasks, done=None, limit=10):
    if done:
        tasks = [task for task in tasks if task['done'] == done]
    tasks.sort(key=lambda task: task['id'])
    return tasks[:limit]
```

先写意见，再展开答案。建议构造 id 顺序颠倒、一个已完成一个未完成的输入。

<details><summary>参考发现与核验方向</summary>

1. `if done` 忽略了 False 分支。应先验证参数类型，再用 `done is not None` 区分「全部」与布尔值。
2. 未筛选时 `sort` 会原地修改调用者列表。用独立列表或 `sorted`，测试调用后原列表顺序未变。
3. limit 未验证：负数会切掉尾部，True 会作为 1 使用，字符串会异常。按契约拒绝它们。
4. done 接受任意真值，字符串可能产生误导结果。契约明确只允许 None 或真正布尔值。

评审意见要附具体反例，不必强求修改成某一种唯一写法。测试覆盖外部行为，避免断言实现必须使用特定语法。

</details>
