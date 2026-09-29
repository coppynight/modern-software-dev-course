const $ = (id) => document.getElementById(id);
async function api(path, method = 'GET', body) {
  const response = await fetch(path, {method, headers: {'Content-Type': 'application/json'},
    body: body === undefined ? undefined : JSON.stringify(body)});
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || '请求失败');
  return data;
}
async function safely(action) {
  $('message').textContent = '';
  try { await action(); } catch (error) { $('message').textContent = error.message; }
}
function button(label, action) {
  const node = document.createElement('button');
  node.type = 'button'; node.className = 'secondary'; node.textContent = label;
  node.addEventListener('click', () => safely(async () => {
    node.disabled = true;
    try { await action(); } finally { node.disabled = false; }
  }));
  return node;
}
async function refresh() {
  const tasks = await api('/api/tasks');
  $('tasks').replaceChildren(); $('empty').hidden = tasks.length > 0;
  for (const task of tasks) {
    const row = document.createElement('li'); row.classList.toggle('done', task.done);
    const check = document.createElement('input'); check.type = 'checkbox'; check.checked = task.done;
    check.setAttribute('aria-label', `完成：${task.title}`);
    check.addEventListener('change', () => safely(async () => {
      check.disabled = true;
      try { await api(`/api/tasks/${task.id}`, 'PATCH', {done: check.checked}); await refresh(); }
      catch (error) { check.checked = task.done; throw error; }
      finally { check.disabled = false; }
    }));
    const title = document.createElement('span'); title.textContent = task.title;
    row.append(check, title, button('改名', async () => {
      const value = prompt('新的任务标题', task.title);
      if (value !== null) { await api(`/api/tasks/${task.id}`, 'PATCH', {title: value}); await refresh(); }
    }), button('删除', async () => {
      if (confirm(`删除「${task.title}」？`)) { await api(`/api/tasks/${task.id}`, 'DELETE'); await refresh(); }
    }));
    $('tasks').append(row);
  }
}
$('task-form').addEventListener('submit', (event) => {
  event.preventDefault(); const submit = event.target.querySelector('button');
  safely(async () => {
    submit.disabled = true;
    try { await api('/api/tasks', 'POST', {title: $('title').value}); $('title').value = ''; await refresh(); }
    finally { submit.disabled = false; }
  });
});
$('note-form').addEventListener('submit', (event) => {
  event.preventDefault(); const submit = event.target.querySelector('button');
  safely(async () => {
    submit.disabled = true;
    try {
      const result = await api('/api/extract', 'POST', {note: $('note').value});
      $('preview').replaceChildren();
      if (!result.tasks.length) $('message').textContent = '没有找到带标记的任务，试试在行首加上「- 」。';
      for (const title of result.tasks) {
        const row = document.createElement('li'); const text = document.createElement('span'); text.textContent = title;
        row.append(text, button('添加', async () => { await api('/api/tasks', 'POST', {title}); row.remove(); await refresh(); }));
        $('preview').append(row);
      }
    } finally { submit.disabled = false; }
  });
});
safely(refresh);
