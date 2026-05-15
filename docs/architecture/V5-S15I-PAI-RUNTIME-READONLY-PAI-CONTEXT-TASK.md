# V5-S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK: PAI Runtime Provides Sanitized Read-Only PAI Metadata Context to runtime=codex

## 1. Architect decision

S15I is approved as an implementation and live runtime milestone for a read-only PAI metadata context task. The implementation reached live execution but did not pass validation within the three permitted live attempts. A fourth live attempt was explicitly authorized after architect/user review; that attempt failed before report generation because Codex rejected the provider-facing report schema, and rollback completed.

## 2. Dependency on accepted S15H

S15I depends on the accepted S15F/G/H combined runtime-control-plane batch at `6485c3ceed3cb6d28131cb0c3722bed6fe1444f4`.

## 3. Read-only PAI context target

PAI_DIR was ~/.claude/PAI. S15I used pai-runtime run-pai-context --runtime codex. PAI created a sanitized context capsule before invoking Codex. Codex consumed the context capsule rather than directly traversing live PAI state. The successful acceptance claim is blocked pending revision because the third live attempt failed report validation and the explicitly authorized fourth attempt failed on Codex structured-output schema compatibility before producing an accepted report.

## 4. Files implemented

files changed

## 5. Backup result

Initial backup root: `/home/maca/.pai-codex-adapter-backups/s15i-20260515T090750Z`.

Fourth-attempt backup root: `/home/maca/.pai-codex-adapter-backups/s15i-20260515T162158Z`.

Backup completed: yes.

## 6. Live install result

S15I executed a read-only PAI metadata context task through the live PAI runtime runner. Live install passed on each live attempt before the context task failed. Rollback was required after the third failed live context-task attempt. The explicitly authorized fourth attempt installed the live runner, passed `doctor`, passed `providers validate codex`, and failed during `run-pai-context` before report generation.

## 7. Context capsule result

S15I produced pai-context-capsule.json. The context capsule contained metadata only. The context capsule was validated as metadata-only before invoking Codex, but live acceptance is blocked by the failed report validation and the live copy was removed by rollback.

## 8. Codex context report result

S15I produced pai-context-report.json. That report was produced during earlier failed attempts, not as accepted live evidence. The third attempt failed because the Codex-produced report contained the forbidden literal `localhost:31337`. The fourth attempt failed earlier because Codex rejected the provider-facing report schema due to an unsupported structured-output keyword. The repository revision now uses a Codex-compatible provider-facing report schema and keeps forbidden-text/provider-capability semantics in PAI validation. The runtime observed PAI_CODEX_PEER_BETA_ADAPTER. Claude remains the official/full-support upstream adapter. Codex remains peer beta.

## 9. Event-attributed validation result

S15I produced pai-context-events.jsonl. S15I produced pai-context-validation.json. Those artifacts were produced during earlier failed attempts, not as accepted live evidence. The fourth attempt produced a capsule, provider event log, and copied report schema, but failed before report and validation artifact generation. No accepted validation artifact remains because validation failed before acceptance and rollback was required.

## 10. Sensitive-data boundary result

No accepted validation artifact was produced. Synthetic tests cover the intended sensitive-data boundary: No PAI Memory body was read. No ISA body was read. No Pulse event payload was read. No Claude project memory was read. No Codex memory was read. No Codex-attributed PAI Memory write was performed. No Codex-attributed ISA write was performed. Pulse was not started or probed by Codex. localhost:31337 was not called by Codex.

## 11. Ambient PAI churn classification

Ambient PAI state/cache/log churn is not adapter evidence.

## 12. Rollback command

Rollback completed successfully.

```bash
python3 -m tools.pai_runtime_runner \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15i-20260515T090750Z" \
  --rollback
```

Fourth-attempt rollback completed successfully.

```bash
python3 -m tools.pai_runtime_runner \
  --pai-dir "$HOME/.claude/PAI" \
  --backup-root "/home/maca/.pai-codex-adapter-backups/s15i-20260515T162158Z" \
  --rollback
```

## 13. Protected surfaces

No repo root AGENTS.md was created. No repo .codex/ directory was created. No PAI adapter files were installed under ~/.codex. Protected files changed yes/no: no.

## 14. Known risks

The live run did not pass within the three-attempt policy. A fourth live attempt was explicitly authorized and failed before report generation because Codex rejected the provider-facing report schema. The repository revision now uses a Codex-compatible provider-facing report schema and keeps semantic safety in PAI validation, but that revision is not live-proven because another live attempt requires separate architect approval.

Completion audit as of the rolled-back S15I state:

| Requirement | Evidence | State |
| --- | --- | --- |
| Start from accepted S15F/G/H commit | `git rev-parse HEAD` returned `6485c3ceed3cb6d28131cb0c3722bed6fe1444f4` | satisfied |
| Repository changes limited to approved S15I write set | approved-path validation passed; `git status --short --untracked-files=all` shows only S15I paths | satisfied |
| Patch hygiene passes | `git diff --check` passed with no whitespace errors | satisfied |
| Context collector, schemas, task card, runner, audit, and tests exist | files are present under the approved repository paths | satisfied |
| S15I JSON files parse | all four `pai-context-*.schema.json` files and `s15i-readonly-pai-context-task.json` parsed as JSON objects | satisfied |
| Synthetic metadata-boundary tests pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest tests.test_pai_runtime_readonly_pai_context` passed with 61 tests | satisfied |
| Adjacent runtime-control-plane tests pass | S15I is covered in the broader PAI runtime unittest slice with capability, provider lifecycle, and related runtime-control-plane tests | satisfied |
| Broad PAI runtime regression tests pass | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p 'test_pai_runtime*.py'` passed with 142 tests | satisfied |
| Full unittest discovery | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests` ran 238 tests and failed with 4 failures and 4 errors in non-S15I adapter activation/S15B workloop tests outside the approved S15I write set | blocked outside S15I scope |
| Modified Python modules compile | in-memory `compile(...)` passed for the modified runner, audit, install, capabilities, PAI context, Codex provider, and S15I test modules without creating `__pycache__` files | satisfied |
| S15I schemas pass Draft 2020-12 schema validation | `jsonschema.Draft202012Validator.check_schema` passed for all four `pai-context-*.schema.json` files | satisfied |
| Capsule/report schemas are enforced by runner before provider acceptance | `run-pai-context` validates the capsule and normalized report against installed schemas; synthetic schema-mismatch tests pass | satisfied |
| Capsule/report schemas are enforced by audit | `audit-pai-context` validates capsule and report artifacts against installed schemas; synthetic schema-violation tests pass | satisfied |
| Validation schema rejects failed accepted artifacts | synthetic tests reject body-read flags, forbidden/unknown write arrays, and empty event logs | satisfied |
| Validation schema requires complete attribution events | synthetic schema tests verify command/file attribution events must include their required fields and accepted file-change events must be approved | satisfied |
| Validation schema requires command evidence | synthetic schema test verifies validation artifacts must include `run-pai-context` and redacted Codex `exec` provider command markers | satisfied |
| Raw audit requires command evidence | synthetic audit test verifies missing `run-pai-context` or redacted Codex `exec` state evidence fails event attribution and validation before schema acceptance | satisfied |
| PAI runtime command evidence targets S15I | synthetic schema and audit tests verify accepted `run-pai-context` command evidence must use `~/.claude/PAI/bin/pai-runtime` and target `runtime=codex`, the S15I task card, and the approved S15I run directory | satisfied |
| Command evidence requires read-only containment | synthetic schema and audit tests verify accepted provider command evidence must include the redacted Codex `exec` command with `--sandbox read-only`, `--cd`, `--add-dir`, structured-output flags, and the approved S15I run artifact targets | satisfied |
| Audit rejects malformed JSONL event logs | synthetic audit test verifies malformed JSONL creates runtime warnings, fails event attribution, and fails validation | satisfied |
| Audit rejects forbidden JSONL event text | synthetic audit test verifies non-command Codex event messages containing forbidden endpoint, Linux/macOS/Windows personal path, Codex home, Claude settings, credential, or product-memory text fail event attribution and validation while keeping validation output redacted | satisfied |
| Validation artifact redacts PAI absolute paths | synthetic audit test verifies the S15I validation result omits the concrete `PAI_DIR` path and uses `~/.claude/PAI` labels | satisfied |
| Validation schema rejects unredacted command/write strings | synthetic schema tests verify `pai-context-validation.schema.json` rejects case-variant personal paths, forbidden markers such as `CLAUDE.md contents`, and nested event command/path records | satisfied |
| Validation schema enforces bounded attempt and redacted limits | synthetic schema tests verify `runtime_attempt_number` must be at least 1 and `known_limits` entries use the redacted-string boundary | satisfied |
| Endpoint redaction rejects case variants | synthetic capsule, report, and validation schema tests verify mixed-case local endpoint strings are rejected before acceptance | satisfied |
| Codex home surface text is not accepted as artifact metadata | synthetic capsule, report, and validation schema tests verify `~/.codex` references are rejected from free-text artifact fields | satisfied |
| Claude protected surface text is not accepted as artifact metadata | synthetic capsule, report, and validation schema tests verify case-variant Claude project-memory path references are rejected from free-text artifact fields | satisfied |
| Audit rejects protected surface reads and probes | synthetic audit tests verify Claude project memory reads, Codex memory reads, PAI Memory/ISA/Pulse body reads, Pulse probes, and localhost 31337 calls fail validation | satisfied |
| ISA/Pulse metadata count boundary | synthetic collector test verifies ISA and Pulse expose presence without collecting payload file counts or payload file names | satisfied |
| Capsule schema enforces ISA/Pulse presence-only metadata | synthetic schema test verifies `pai-context-capsule.schema.json` rejects ISA/Pulse file counts and Pulse payload filenames | satisfied |
| Capsule schema requires Codex provider metadata | synthetic schema test verifies `pai-context-capsule.schema.json` rejects capsules missing the `codex` runtime provider name, provider object, or `pai.context.read.metadata` provider capability | satisfied |
| Capsule schema rejects unknown raw-content fields | synthetic schema test verifies `pai-context-capsule.schema.json` rejects unexpected top-level fields | satisfied |
| Capsule schema rejects unredacted nested metadata | synthetic schema test verifies `pai-context-capsule.schema.json` rejects forbidden endpoint literals, case-variant personal paths, credential/product-memory markers, and unredacted run-artifact paths in provider, runtime-state, run-artifact, and policy metadata | satisfied |
| Task schema enforces metadata-only no-direct-traversal contract | synthetic schema test verifies `pai-context-task.schema.json` rejects direct live PAI traversal, Memory write capability, and incomplete forbidden-read surface lists | satisfied |
| Task schema guards free-text summary | synthetic schema test verifies `pai-context-task.schema.json` rejects forbidden path, credential, and endpoint markers in `task_summary`; schema audit verifies all S15I non-const free-text fields use the shared redacted-string boundary | satisfied |
| Runtime and install validate S15I task card schema | install preflight validates the staged S15I task card against `pai-context-task.schema.json`, and `run-pai-context` rejects installed task-card schema violations before execution | satisfied |
| Install preflight validates Codex provider capabilities | synthetic install test verifies staged provider manifest validation rejects a Codex provider capability set missing `pai.context.read.metadata` | satisfied |
| S15I provider prompt avoids forbidden literal surfaces | synthetic provider-command test verifies the context prompt expresses the Pulse no-probe policy without embedding the forbidden endpoint literal, raw Codex home label, or Claude project-memory path label | satisfied |
| Live-mode install write boundary | synthetic live-mode installer test verifies changed targets stay within the S15I mutable install target set | satisfied |
| Audit CLI validates accepted validation artifact schema | `audit-pai-context` validates a passing `pai-context-validation.json` result against the installed validation schema before returning success | satisfied |
| Accepted validation artifact has no runtime warnings | synthetic schema test verifies `pai-context-validation.schema.json` rejects a `validation_passed: true` artifact that carries runtime warnings | satisfied |
| Audit CLI default attempt number | synthetic CLI test verifies `audit-pai-context` without `--runtime-attempt-number` writes `runtime_attempt_number: 1`, matching the Goal Card validation command shape | satisfied |
| Audit validation output write boundary | synthetic wrapper test verifies `audit-pai-context` rejects validation output outside `runs/s15i/read-only-pai-context` and rejects unexpected validation artifact names | satisfied |
| Validation schema rejects unknown raw-content fields | synthetic schema test verifies `pai-context-validation.schema.json` rejects unexpected top-level fields, while allowing the known `runtime_warnings` field | satisfied |
| Report semantic validator rejects unredacted report text | synthetic validation test verifies `validate_context_report` rejects forbidden endpoint literals, case-variant personal paths, credential/product-memory markers, and unredacted path text in report text/list fields while the provider-facing schema remains Codex structured-output compatible | satisfied |
| Report semantic validator requires Codex provider capability evidence | synthetic validation test verifies `validate_context_report` rejects reports missing the `codex` runtime provider name, a positive provider count, or `pai.context.read.metadata` in observed Codex capabilities | satisfied |
| Provider report normalization writes schema-valid clean report | synthetic fake-Codex test verifies provider free text containing a forbidden endpoint literal and unredacted personal path is normalized out before `pai-context-report.json` is written, then validates the saved report against `pai-context-report.schema.json` and `validate_context_report` | satisfied |
| Symlink metadata/write boundary | synthetic tests verify the collector ignores symlinked metadata files and symlinked Memory category directories, and `audit-pai-context` rejects new symlink writes as unknown | satisfied |
| Isolated dry-run install, doctor, provider validation, and context command wiring | temporary `/tmp` PAI fixture installed successfully; `doctor`, `providers validate codex`, and `run-pai-context --dry-run` passed without touching live `~/.claude/PAI` | satisfied |
| Isolated full fake-Codex context run and audit | temporary `/tmp` PAI fixture ran installed `pai-runtime doctor`, `providers validate codex`, `run-pai-context`, and `audit-pai-context` with a fake `codex`; validation passed, events were non-empty, endpoint literals were absent, and validation output redacted the concrete temp `PAI_DIR` | satisfied |
| Full local `~/.claude` backup exists | `/home/maca/.pai-codex-adapter-backups/s15i-20260515T090750Z/.claude` exists | satisfied |
| Fourth-attempt full local `~/.claude` backup exists | `/home/maca/.pai-codex-adapter-backups/s15i-20260515T162158Z/.claude` exists | satisfied |
| Live install, doctor, and provider validation | passed during the three original live attempts and during the explicitly authorized fourth attempt before rollback | satisfied for attempted run |
| Fourth live attempt | failed during `run-pai-context` because Codex rejected the provider-facing report schema before report generation; rollback completed from `/home/maca/.pai-codex-adapter-backups/s15i-20260515T162158Z` | failed |
| Accepted live `pai-context-capsule.json` | live S15I run directory is absent after rollback | missing |
| Accepted live `pai-context-report.json` | live S15I run directory is absent after rollback | missing |
| Accepted live `pai-context-events.jsonl` | live S15I run directory is absent after rollback | missing |
| Accepted live `pai-context-validation.json` with `validation_passed: true` | `~/.claude/PAI/runs/s15i/read-only-pai-context/pai-context-validation.json` is absent after rollback | missing |
| Event-attributed validation passed | no accepted validation artifact exists | missing |
| Activation note success claims are true | blocked by missing accepted live artifacts | missing |

## 15. Required final handoff format

files changed

behavior changed

tests run

known risks

protected files changed yes/no

goal state

recommended next architect decision only

## 16. Proposed next architect decision

Request rollback/revision of S15I-PAI-RUNTIME-READONLY-PAI-CONTEXT-TASK before beta-readiness gate work. A later Memory/ISA proposal policy milestone requires a separate architect-approved Goal Card.
