#!/usr/bin/env bash
# Commit and push the DrainClamp state (.agent/) after every DrainClamp write. Owner rule: DC state is always on GitHub.
#   tools/dc_push.sh "<message>"
set -euo pipefail
cd "$(dirname "$0")/.."
git add -A .agent
git diff --cached --quiet -- .agent && { echo "dc state already pushed"; exit 0; }
git commit -qm "DrainClamp: ${1:-state update}" -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01ALSSt2FX8Jz9oBBX9vzp3h"
for wait in 0 2 4 8 16; do sleep "$wait"; git push -q origin HEAD:main 2>/dev/null && { git log --oneline -1; exit 0; }; done
echo "push failed" >&2; exit 1
