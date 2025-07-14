#!/usr/bin/env bash
# run_all_servers.sh
# 执行 Servers 目录及其子目录下的所有 .py 文件

set -euo pipefail

# 若脚本放在项目根目录，可用此行定位 Servers
ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SERVERS_DIR="${ROOT_DIR}/Servers"

PYTHON_BIN=${PYTHON_BIN:-python}   # 如需自定义解释器，可:  export PYTHON_BIN=python3.10

echo "▶ Using Python interpreter: ${PYTHON_BIN}"
echo "▶ Scanning directory:       ${SERVERS_DIR}"
echo

# 遍历并执行
find "${SERVERS_DIR}" -type f -name "*.py" ! -name "__init__.py" | while read -r file; do
  echo "=== Running: ${file} ==="
  "${PYTHON_BIN}" "${file}"
  echo
done

echo "✓ All server scripts executed successfully."
