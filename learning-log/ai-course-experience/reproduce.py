"""把作业补丁应用到临时练习副本并检查；不修改原starter。"""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    with tempfile.TemporaryDirectory(prefix='student-reproduce-') as temp:
        project = Path(temp) / 'practice'
        shutil.copytree(ROOT, project, ignore=shutil.ignore_patterns(
            '.git', 'learning-log', 'data', '__pycache__', '.venv', '.venv-*'))
        env = os.environ.copy()
        env['PYTHONUTF8'] = '1'

        def run(label, command):
            result = subprocess.run(command, cwd=project, env=env, capture_output=True, text=True, encoding='utf8')
            # 输出失败原因而不暴露本地个人路径。
            output = (result.stdout + result.stderr).replace(str(project), '<practice>').replace(str(HERE), '<assignment>')
            print(label + ': exit=' + str(result.returncode))
            if result.returncode:
                print(output)
                raise RuntimeError(label + ' failed')
            for line in output.splitlines():
                if line.startswith(('Ran ', 'OK', 'Course checks passed', '22/22')):
                    print(line)

        run('补丁可应用', ['git', 'apply', '--check', str(HERE / 'filter-exercise.patch')])
        run('隔离应用', ['git', 'apply', str(HERE / 'filter-exercise.patch')])
        run('练习单元与静态检查', [sys.executable, 'tools/check.py'])
        run('独立HTTP验收', [sys.executable, str(HERE / 'verify-filter.py'), '--project', str(project)])
    print('临时练习检查完成；starter未修改。')


if __name__ == '__main__':
    main()
