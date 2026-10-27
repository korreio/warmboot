# System map

Template use: merge into an existing architecture or ownership map when one exists.
Adopt when stable boundaries are hard to find from source. For a small coded project,
merge the proportional map into its root README rather than omitting the ownership
route or creating a separate document. Replace every `{{MARKER}}` and delete this note.

- Map owner: {{OWNER}}
- Authority: routes investigation; grants no mutation or external-effect permission.
- Evidence boundary: this map does not prove that current code matches it.
- Maintenance: update when a boundary, owner, dependency direction, lifecycle, or
  entry path changes.
- Revisit or retire: merge into a stronger architecture source or remove when source
  is the clearer map.

Last verified against: {{SNAPSHOT_OR_DATE}}

## Stable boundaries

| Area | Owner | Invariant | Authoritative source | Allowed direction | Cheapest check | Singleton resource |
|---|---|---|---|---|---|---|
| {{AREA}} | {{OWNER}} | {{INVARIANT}} | `{{SOURCE_PATH}}` | {{DIRECTION}} | `{{CHECK}}` | {{RESOURCE_OR_NONE}} |

## Task routing

| Work shape | Minimum living context | First evidence | Authority or physical limit |
|---|---|---|---|
| {{TASK_SHAPE}} | {{SOURCE_AND_DECISION_PATHS}} | `{{CHECK_OR_OBSERVATION}}` | {{LIMIT}} |

## Troubleshooting route

| Symptom | Look first | Boundary to inspect | Do not infer |
|---|---|---|---|
| {{SYMPTOM}} | `{{PATH_OR_COMPONENT}}` | {{FLOW_OR_RESOURCE}} | {{UNPROVED_CLAIM}} |

## Cross-boundary flow

- {{SOURCE}} → {{DESTINATION}}: {{DATA_OR_CONTROL}}, guarded by {{INVARIANT_AND_CHECK}}.

## Lifecycle

- Composition owner: `{{PATH}}` — {{OWNER}}.
- Startup order and ready signal: {{ORDER_AND_OBSERVABLE_SIGNAL}}.
- Teardown order and completion signal: {{ORDER_AND_OBSERVABLE_SIGNAL}}.
- Alternate entry paths: {{PATHS_OR_NONE}}.
- Temporary bridge: {{PATH_OWNER_RECOVERY_AND_REMOVAL_CONDITION_OR_NONE}}.

Verify the named source and applicable native check before relying on a row. Update or
remove stale rows in the same change.

## Living links

- Active task: `{{TASK_PATH}}`
- Engineering and testing: `{{STANDARDS_AND_TESTING_PATHS}}`
- Architecture decision: `{{ADR_OR_DECISION_PATH}}`
- Operational guide: `{{RUNBOOK_OR_NONE}}`
