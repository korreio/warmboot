# Testing and evidence

Template use: merge into existing test documentation or engineering standards when
they already route native checks. Adopt when command choice or proof limits are unclear.
Omit a separate guide for a tiny project with one obvious test path. Replace every
`{{MARKER}}` and delete this note.

- Test-contract owner: {{OWNER}}
- Authority: records approved local checks; grants no package, network, credential,
  device, deployment, release, publication, or shared-resource permission.
- Evidence boundary: each pass proves only the behavior its environment can observe.
- Maintenance: update when commands, tiers, fixtures, owners, or evidence meaning
  changes.
- Revisit or retire: merge when another guide owns these routes; remove tiers that no
  longer change a decision.

Applies to: {{PATHS_OR_COMPONENTS}}
Last verified against: {{SNAPSHOT_OR_DATE}}

## Canonical commands

| Intent | Project-native command | A pass proves | It does not prove |
|---|---|---|---|
| Focused iteration | `{{FOCUSED_COMMAND}}` | {{LOCAL_SCOPE}} | {{HIGHER_TIER_LIMIT}} |
| Ordinary closing suite | `{{CLOSING_COMMAND}}` | {{REPOSITORY_SCOPE}} | {{EXTERNAL_LIMIT}} |
| Integration or runtime boundary | `{{INTEGRATION_COMMAND_OR_NONE}}` | {{BOUNDARY_SCOPE}} | {{PHYSICAL_OR_HOSTED_LIMIT}} |

Focused evidence diagnoses a change. It is closing evidence only when the project's
current contract says so.

## Assertion and fixture quality

- For each non-trivial formula, state transition or boundary, use examples whose
  expected result comes from an independent oracle: a contract, external standard,
  hand calculation or implementation-independent derivation. Do not calculate expected
  values with the production path under test.
- Add tables for meaningful partitions and property or metamorphic tests when invariants
  across ranges, orderings or transformations are more informative than isolated cases.
  Keep representative real fixtures where synthetic data cannot establish route
  usefulness.
- Separate fixture builders from expectations. Shared production-shaped fixtures may
  reduce setup duplication, but they must not make implementation and assertion fail in
  the same way.
- Zero unexplained skips are permitted in final acceptance. Give every intentional skip
  an owner, reason, affected claim and condition for running or removal; classify its
  consequence as `UNPROVED` or `BLOCKED`.

Coverage locates blind critical paths; percentages do not prove behavior and are not
targets by themselves. Use meaningful mutation testing where surviving mutants can
reveal weak assertions at proportionate cost. Record scope, exclusions, survivors and
tool limitations rather than treating a mutation score as a universal gate.

## Escalation

| Changed boundary | Minimum focused set | Required closing set | Escalate when | Clean-state requirement |
|---|---|---|---|---|
| {{BOUNDARY}} | `{{FOCUSED_SET}}` | `{{CLOSING_SET}}` | {{TRIGGER}} | {{PROCESS_FIXTURE_OR_RESULT_STATE}} |

After a fix, rerun the failure and applicable closing set against named inputs. A pass
that reused suspect mutable state is not closing evidence.

Keep the escaped-defect reproduction RED before the fix, then retain the smallest
ordinary regression test that expresses the behavior. A special permanent gate still
needs the regression-pin owner, reach, cost and deletion condition from the evidence
route.

## Evidence tiers

| Hazard | Cheapest observing tier | Mutable resource and holder | Unavailable result |
|---|---|---|---|
| {{STATIC_HAZARD}} | `{{STATIC_CHECK}}` | {{NONE_OR_RESOURCE_OWNER}} | `UNPROVED / BLOCKED` |
| {{LOCAL_BEHAVIOR_HAZARD}} | `{{LOCAL_CHECK}}` | {{RESOURCE_AND_OWNER}} | `UNPROVED / BLOCKED` |
| {{EXTERNAL_HAZARD}} | {{AUTHORIZED_OBSERVATION}} | {{ENVIRONMENT_AND_OWNER}} | `UNPROVED / BLOCKED` |

Only a named holder may reset or interpret a shared report path, browser, database,
port, device, or service. Required external evidence waits for separate authority.

## Recording rule

For each claim, record the exact command or observation, result, snapshot, relevant
configuration, and limit. Recheck inherited evidence against current inputs. Add a
durable regression check only after reproducing a defect; name its owner, recurrence
signal, cost, and deletion condition.
