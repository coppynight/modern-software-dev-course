"""供没有 cwd 配置项的 MCP 客户端使用。"""
import os
import runpy
import sys
from pathlib import Path

root = Path(__file__).resolve().parents[2]
os.chdir(root)
sys.path.insert(0, str(root))
runpy.run_module('labs.mcp.server', run_name='__main__')
