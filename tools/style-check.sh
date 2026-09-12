#!/usr/bin/env bash
# Fails on banned filler from STYLE.md. A parenthetical qualifier is stripped,
# so "leverage (as a verb)" matches any "leverage" -- deliberately over-strict,
# since the check cannot do part-of-speech and a false positive costs one
# reword. Exempts STYLE.md itself (it lists the
# strings) and the audit reports (they quote external agents verbatim).
set -u
cd "$(dirname "$0")/.."
# Take EVERY 4-space-indented line after the "Banned phrases" heading. An
# earlier version ranged from "worth noting" to "delve" and silently ignored
# every entry appended after delve.
BANNED=$(sed -n '/^### Banned phrases/,$p' STYLE.md | grep -E '^    [a-z]' | sed 's/^    //')
fail=0
while IFS= read -r raw; do
  # strip a trailing parenthetical qualifier, e.g. "leverage (as a verb)" must
  # match the word "leverage". Grepping the literal string let it through.
  phrase=$(echo "$raw" | sed 's/ *([^)]*)$//')
  hits=$(git grep -n -i -F "$phrase" -- ':!STYLE.md' ':!AUDIT-*.md' ':!AUDIT-DEADEND*' ':!HOST-FINDINGS.md' ':!tools/style-check.sh' 2>/dev/null)
  if [ -n "$hits" ]; then
    echo "BANNED: \"$phrase\""
    echo "$hits" | sed 's/^/  /'
    fail=1
  fi
done <<< "$BANNED"
[ $fail -eq 0 ] && echo "style-check: clean" || echo "style-check: FAIL"
exit $fail
