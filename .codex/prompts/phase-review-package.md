# Phase Review Package Prompt

Prepare a review package for architect review. Do not change source files except creating review artifacts if requested by the user.

Collect:

```bash
git status --short
git diff --stat
git diff --binary
```

Report:

1. Current phase and task.
2. Prompt used.
3. Model/profile used if known.
4. Files changed.
5. Tests run and exact results.
6. Review agents run and verdicts.
7. Known failures.
8. Compatibility matrix changes.
9. Protected governance files changed: yes/no.
10. Codex final summary.

Do not declare the phase complete. The architect decides whether it is complete.
