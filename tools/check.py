"""主线统一检查：业务与实验测试、Python 语法、JSON、Markdown 本地目标。"""
import ast
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {'.git', '.venv', 'data', 'dist', 'submissions', '__pycache__', 'research'}


def eligible(path):
    return not any(part in IGNORED or part.startswith('.venv-') for part in path.relative_to(ROOT).parts)


def main():
    result = subprocess.run([sys.executable, '-m', 'unittest', 'discover', '-s', 'tests', '-v'], cwd=ROOT)
    errors = []
    for path in ROOT.rglob('*'):
        if not path.is_file() or not eligible(path):
            continue
        try:
            if path.suffix == '.py':
                ast.parse(path.read_text(encoding='utf-8'), filename=str(path))
            elif path.suffix == '.json':
                json.loads(path.read_text(encoding='utf-8'))
            elif path.suffix == '.md':
                body = re.sub(r'```.*?```', '', path.read_text(encoding='utf-8'), flags=re.S)
                for target in re.findall(r'\]\(([^)]+)\)', body):
                    if re.match(r'^(?:[a-zA-Z][a-zA-Z0-9+.-]*:|#)', target):
                        continue
                    target = unquote(target.split('#')[0])
                    if not (path.parent / target).exists():
                        errors.append(f'{path.relative_to(ROOT)}: missing link {target}')
        except (SyntaxError, ValueError, UnicodeError) as exc:
            errors.append(f'{path.relative_to(ROOT)}: {exc}')
    for error in errors:
        print(error, file=sys.stderr)
    if result.returncode or errors:
        print('Course checks failed', file=sys.stderr)
        return 1
    print('Course checks passed (tests, Python syntax, JSON, local link targets).')
    return 0


if __name__ == '__main__':
    sys.exit(main())
