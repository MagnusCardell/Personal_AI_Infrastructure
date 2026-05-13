# S15D Synthetic Bugfix Task

Fix `normalize_priority` in `src/pai_priority.py`.

Expected behavior:

- Low aliases return `low`.
- Medium aliases return `medium`.
- High aliases return `high`.
- Urgent aliases return `urgent`.
- Invalid or non-string priorities raise `ValueError`.
- The public function name remains `normalize_priority`.
