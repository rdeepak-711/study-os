#!/usr/bin/env bash
# Daily commit helper. Usage:
#   ./save.sh "day 3: rebuilt FastAPI endpoint, DDIA ch1 notes"
set -e
cd "$(dirname "$0")"
git add -A
git commit -m "${1:-progress}"
git push
echo "pushed ✓  green square earned"
