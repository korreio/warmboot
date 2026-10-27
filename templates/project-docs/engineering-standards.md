# Engineering standards

Template use: merge into an existing contributor or engineering guide when one owns
durable rules. Adopt only for rules that change implementation or review decisions.
Omit a separate guide when configuration and short existing docs are sufficient.
Replace every `{{MARKER}}` and delete this note.

- Standards owner: {{OWNER}}
- Authority: constrains work inside granted scope; grants no Git, package, network,
  credential, deployment, release, or publication permission.
- Evidence boundary: a rule is a gate only when its named enforcement can block.
- Maintenance: update when an invariant, tool owner, native check, or exception path
  changes.
- Revisit or retire: merge into a stronger living owner or remove rules that no longer
  affect decisions.

Applies to: {{PATHS_OR_COMPONENTS}}

## Baseline

- Architecture decision owner: `{{ADR_OR_ARCHITECTURE_PATH}}`
- Runtime and version owners: {{RUNTIME_PATHS_AND_OWNERS}}
- Package and lockfile owner: {{PACKAGE_SURFACE_OR_NONE}}
- Formatting, linting, typing, and build owners: {{TOOLS_AND_OWNERS}}

Changing a language, framework, package manager, lock strategy, or major tool boundary
requires a separate accepted decision. It is not routine maintenance.

## Invariants

- {{BEHAVIOR_OR_SAFETY_INVARIANT}}
- {{COMPATIBILITY_OR_DATA_INVARIANT}}

## Human inspectability

Record target-native rules that help both humans and agents understand and change the
system. Names, types and structure should make the **what** clear. Preserve the **why,
invariants, assumptions, and boundaries** in the smallest living owner that future
maintainers can find:

- place rationale beside consequential algorithms and non-obvious units, coordinate
  systems, projection assumptions, numerical boundaries, concurrency, idempotency,
  retry, caching or privacy behavior;
- document public API usage and contracts at the language-appropriate boundary;
- update the system map or architecture decision when ownership or dependency direction
  changes; use a human-readable Mermaid or source-controlled SVG diagram only when a
  visual makes a material relationship clearer;
- reject a comment that merely restates the code, stale explanation, and comment or
  documentation counts as quality targets.

If oversized units have caused mixed responsibility or poor comprehension, record a
locally calibrated SLOC or complexity review trigger, its counting convention and a
documented exception path. Treat it as triage for refactoring or review, not a universal
file-size limit or a substitute for sound boundaries, rationale and tests.

## Source-file comprehension contract

Adopt the target language and community's standard form: {{MODULE_DOCSTRING_CLASS_DOC_OR_FILE_HEADER}}.
The source owner is {{SOURCE_COMPREHENSION_OWNER}}; the changed-source assessment lives
in `{{TASK_OR_REVIEW_PATH}}`.

- Every human-authored code file immediately states its purpose or responsibility.
  One accurate sentence is sufficient for a simple file.
- Consequential algorithms, constants, reconciliations and state transitions explain
  why beside the operative code, including applicable invariants, units, precedence
  and failure, state, concurrency, security or resource semantics.
- An exact link such as `{{ADR_PATH}}#{{SECTION_ANCHOR}}` may carry extended rationale
  only when source still states its local contract and that section exists.
- Tests, plans and remote ADRs do not substitute for local comprehension. Reject stale,
  decorative or line-by-line narration and any comment-count target.
- Generated, vendored and pure re-export exceptions: {{EXACT_PATHS_REASON_AND_OWNER}}.
- Pre-existing debt inventory, priority and owner: {{PATH_OR_NONE_WITH_EVIDENCE}}.

Before handoff, the coordinator attests the frozen candidate source set and the writer
reconciles and records a result for every path. A fresh non-author reviewer
independently reconciles the inventory and reads the complete set; omission or a
contract breach is `FINDING` even when tests pass. The attestation and writer
assessment remain mandatory. Automated checks may locate missing syntax or broken
links; they do not judge semantic adequacy.

## Rules

| Rule | Strength | Applies at | Enforcement or review evidence | Exception owner and evidence |
|---|---|---|---|---|
| {{RULE}} | `HARD GATE / REVIEW RULE / CONVENTION` | {{BOUNDARY}} | {{CHECK_OR_SOURCE}} | {{OWNER_AND_CONDITION}} |

Use `HARD GATE` only for a mechanically or authoritatively blocking condition. A
convention is a default, not an automated gate.

## Boundaries

| Component or state | Owner | Allowed dependency direction | Composition owner | Focused check |
|---|---|---|---|---|
| {{BOUNDARY}} | {{OWNER}} | {{DIRECTION}} | `{{COMPOSITION_PATH}}` | `{{COMMAND}}` |

- Keep branching policy testable when it carries material risk.
- Construct concrete dependencies at a named composition boundary.
- Select target-native formatting, linting, static-analysis and architecture checks
  proportionally. A tool or threshold belongs only when its result changes a decision,
  and exceptions must preserve the reason rather than silently weaken the rule.
- For a temporary bridge, record old and new owners, parity evidence, recovery path,
  and an observable removal condition in the active task.

## Evidence and changes

| Hazard or change | Cheapest valid check | Evidence owner | Unproved higher tier |
|---|---|---|---|
| {{HAZARD}} | `{{NATIVE_COMMAND_OR_OBSERVATION}}` | {{OWNER}} | {{LIMIT_OR_NONE}} |

Record exact commands, inputs, and results. Do not treat a lower tier as proof of an
unobserved boundary. Preserve unrelated work. Update affected onboarding, system maps,
testing routes, and user-facing notes in the same change that makes them stale.
