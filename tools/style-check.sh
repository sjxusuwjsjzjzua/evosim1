#!/usr/bin/env bash
# Fails on banned filler from STYLE.md. Exempts STYLE.md itself (it lists the
# strings) and the audit reports (they quote external agents verbatim).
set -u
cd "$(dirname "$0")/.."
BANNED=$(sed -n '/^    worth noting$/,/^    delve$/p' STYLE.md | sed 's/^    //' | grep -v '^$')
fail=0
while IFS= read -r phrase; do
  hits=$(git grep -n -i -F "$phrase" -- ':!STYLE.md' ':!AUDIT-*.md' ':!HOST-FINDINGS.md' ':!tools/style-check.sh' 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "BANNED: \"$phrase\""
    echo "$hits" | sed 's/^/  /'
    fail=1
  fi
done <<< "$BANNED"
[ $fail -eq 0 ] && echo "style-check: clean" || echo "style-check: FAIL"
exit $fail
