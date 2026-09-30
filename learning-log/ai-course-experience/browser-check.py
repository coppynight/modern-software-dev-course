import sys, subprocess, time, json, urllib.request, argparse, tempfile
from pathlib import Path
parser=argparse.ArgumentParser(description='17个练习浏览器断言；不修改课程原件')
parser.add_argument('--project', required=True, type=Path)
parser.add_argument('--chrome', required=True)
parser.add_argument('--output', required=True, type=Path)
args=parser.parse_args()
from playwright.sync_api import sync_playwright
out=args.output.resolve(); out.mkdir(parents=True,exist_ok=True)
temp=tempfile.TemporaryDirectory(prefix='student-browser-')
root=args.project.resolve(); results=[]
log=open(out/'browser-server.log','w',encoding='utf8')
def start():
    proc=subprocess.Popen([sys.executable,'-m','app.server','--port','8018','--db',str(Path(temp.name)/'tasks.db')],cwd=root,stdout=log,stderr=log)
    for _ in range(50):
        try: urllib.request.urlopen('http://127.0.0.1:8018/health',timeout=1); return proc
        except Exception: time.sleep(.1)
    raise RuntimeError('start failed')
def check(name,condition,detail=None):
    results.append(dict(case=name,passed=bool(condition),detail=detail)); assert condition,name
proc=start()
try:
 with sync_playwright() as p:
    browser=p.chromium.launch(executable_path=args.chrome,headless=True)
    page=browser.new_page(viewport=dict(width=1280,height=900)); page.goto('http://127.0.0.1:8018'); page.wait_for_timeout(200)
    # Selector grounded from authored filter markup once implementation is available.
    select=page.locator('select'); check('one filter',select.count()==1)
    for title in ['未完成练习','已完成练习','<img src=x onerror=alert(1)>']:
        page.locator('#title').fill(title); page.locator('#task-form button').click(); page.wait_for_timeout(100)
    page.locator('#tasks input[type=checkbox]').nth(1).check(); page.wait_for_timeout(100)
    check('all 3',page.locator('#tasks li').count()==3)
    select.select_option('open'); page.wait_for_timeout(100); check('open 2',page.locator('#tasks li').count()==2)
    page.route('**/api/tasks?status=done',lambda route:route.abort())
    select.select_option('done'); page.wait_for_timeout(150)
    check('filter failure rolls back',select.input_value()=='open' and page.locator('#tasks li').count()==2)
    check('filter failure explains retry','上次成功' in page.locator('#message').inner_text(),page.locator('#message').inner_text())
    page.screenshot(path=str(out/'08-filter-failure-fixed.png'),full_page=True)
    page.unroute('**/api/tasks?status=done')
    select.select_option('done'); page.wait_for_timeout(100); check('done 1',page.locator('#tasks li').count()==1)
    page.locator('#tasks input[type=checkbox]').first.uncheck(); page.wait_for_timeout(100)
    check('mutation removes from current filter',page.locator('#tasks li').count()==0)
    check('filtered empty visible',page.locator('#empty').is_visible(),page.locator('#empty').inner_text())
    page.screenshot(path=str(out/'05-filter-empty.png'),full_page=True)
    select.select_option('all'); page.wait_for_timeout(100); check('switch does not delete',page.locator('#tasks li').count()==3)
    check('xss text only',page.locator('#tasks img').count()==0)
    for query in ['status=invalid','status=','status=all&status=open']:
        r=page.request.get('http://127.0.0.1:8018/api/tasks?'+query); check('400 '+query,r.status==400,r.json())
    page.set_viewport_size(dict(width=375,height=812)); select.focus(); page.keyboard.press('o'); page.keyboard.press('Enter'); page.wait_for_timeout(100)
    # Explicit keyboard arrows avoid relying on platform type-ahead interpretation.
    select.select_option('all'); select.focus(); page.keyboard.press('ArrowDown'); page.keyboard.press('Enter'); page.wait_for_timeout(150)
    check('keyboard changes filter',select.input_value()=='open',select.input_value())
    check('narrow no overflow',page.evaluate('document.documentElement.scrollWidth===innerWidth'))
    page.screenshot(path=str(out/'06-filter-narrow.png'),full_page=True)
    proc.terminate(); proc.wait(); page.locator('#title').fill('恢复后提交'); page.locator('#task-form button').click(); page.wait_for_timeout(200)
    check('offline retained',page.locator('#title').input_value()=='恢复后提交',page.locator('#message').inner_text())
    page.screenshot(path=str(out/'07-filter-offline.png'),full_page=True)
    proc=start(); page.locator('#task-form button').click(); page.wait_for_timeout(150); select.select_option('all'); page.wait_for_timeout(100)
    check('restart preserves and retry adds',page.locator('#tasks li').count()==4)
    browser.close()
finally:
 proc.terminate(); proc.wait(); log.close()
 temp.cleanup()
 (out/'filter-browser-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(results,ensure_ascii=False))
