"""纯业务函数：不连接网络或数据库，适合练习契约与测试。"""

MAX_TITLE = 120
MAX_NOTE = 4000


def clean_title(value):
    if not isinstance(value, str):
        raise ValueError("标题必须是字符串")
    value = value.strip()
    if not value or len(value) > MAX_TITLE:
        raise ValueError("标题须为 1–120 个字符")
    return value


def extract_tasks(note):
    """确定性规则基线，不是 LLM：提取显式标记的任务，按原顺序去重。"""
    if not isinstance(note, str) or len(note) > MAX_NOTE:
        raise ValueError("笔记必须为不超过 4000 字符的字符串")
    tasks = []
    for line in note.splitlines():
        line = line.strip()
        for prefix in ("- ", "* ", "TODO:", "待办："):
            if line.startswith(prefix):
                candidate = line[len(prefix):].strip()
                if candidate:
                    candidate = clean_title(candidate)
                    if candidate not in tasks:
                        tasks.append(candidate)
                break
    return tasks
