# S15C Synthetic Bugfix Task

Fix `normalize_priority` in `src/pai_priority.py`.

The function must normalize these canonical priority values:

- `low`
- `medium`
- `high`
- `urgent`

Aliases should be accepted case-insensitively after trimming whitespace. Invalid, empty, or non-string values must raise `ValueError`. Preserve the public function name.

Run the task tests with:

```bash
python3 -m unittest discover -s tests
```
