# PAI v5 Codex Peer Beta Adapter Router

Codex is a peer beta adapter for PAI v5.
Claude remains the official/full-support upstream adapter.
PAI v5 is a Life OS, not just Claude config.
PAI_DIR is the v5 PAI subsystem root, usually ~/.claude/PAI.
PAI_SYSTEM_PROMPT.md is a high-authority instruction layer.
Pulse is the central daemon/dashboard/event surface on localhost:31337.
ISA replaces PRD as the work/system-of-record primitive.
Memory v7.6 has WORK, LEARNING, and KNOWLEDGE.

When operating in a PAI workspace, identify PAI_DIR, read PAI_SYSTEM_PROMPT.md if available, then follow Codex adapter constraints.

Codex must not write PAI Memory unless a later architect-approved policy allows it.
Codex must not write ISA unless a later architect-approved policy allows it.
Codex must not create or emulate Claude-specific hooks, agents, commands, or runtime files.

AGENTS.md is a router into PAI v5, not a clone of CLAUDE.md.

This router does not authorize Codex to start, probe, or call Pulse.
This router does not authorize Codex hooks, rules, skills, agents, commands, launchers, Memory writers, ISA writers, Pulse bridges, repo root AGENTS.md, repo .codex/, or ~/.codex/.
Claude-shaped files must not be copied directly into Codex native surfaces.
