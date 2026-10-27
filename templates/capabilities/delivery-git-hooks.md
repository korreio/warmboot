# Delivery and Git hooks

## Adoption decision

- Adopt when a repeated local mistake can be caught cheaply before a checkpoint by an
  existing native check.
- Merge when the target already owns a reliable local hook or delivery gate.
- Omit when a hook duplicates a gate, surprises users, rewrites files, or obscures
  repository state.
- Decision owner: the target coordinator or named delivery owner; the coordinator
  remains the sole Git operator.
- Authority: describing a hook grants no hook installation, staging, commit, push,
  package, network, credential, release, or publication permission.
- Evidence: compare the native check and hook outcome on isolated success and failure
  cases, then run the closing check outside the hook.
- Maintenance: installation instructions, platform behavior, command parity, and false
  positives.
- Revisit or remove: when the canonical check alone prevents recurrence or hook upkeep
  costs more than the failure it catches.

## Target record

- Reproduced failure class: {{FAILURE}}
- Native check and owner: {{COMMAND_AND_OWNER}}
- Hook boundary: {{EVENT_AND_FILES}}
- Isolated evidence: {{PROCEDURE_AND_RESULT}}
- Recovery or bypass owner: {{OWNER_AND_CONDITION}}

A hook may return pass or fail from one reviewed check. It must not commit, push, stage,
rewrite unrelated files, print sensitive staged content, or silently widen the target.
Treat the index and working tree as singleton mutable resources. A bypass addresses tool
failure; it is not evidence that skipped checks passed.

Related cards: [testing and feedback](testing-feedback.md),
[security, privacy, and secrets](security-privacy-secrets.md).

