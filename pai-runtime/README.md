# PAI Runtime Runner

S15D introduces a PAI-owned runtime runner. PAI owns run directories, task cards,
schemas, validation, and Memory/ISA/Pulse policy. Runtime providers execute
bounded work under PAI control.

The first provider is `codex`, registered as peer beta. Claude remains the
official/full-support upstream adapter.
