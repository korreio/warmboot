# Testing and feedback

## Adoption decision

- Adopt when repeated changes need a clear smallest check and a distinct closing set.
- Merge when existing test docs or wrappers already own command selection and proof
  limits.
- Omit when one obvious native command already gives timely, sufficient evidence.
- Decision owner: the target's test-contract owner.
- Authority: local read and execution only when already granted; this card grants no
  package, network, credential, device, Git, deployment, release, or publication access.
- Evidence: target-native focused and closing commands against named inputs.
- Maintenance: wrapper upkeep, fixture ownership, runtime, and flaky-result handling.
- Revisit or remove: when the split stops changing decisions or escaped defects show it
  observes the wrong boundary.

## Target record

- Changed behavior and focused command: {{BOUNDARY_AND_COMMAND}}
- Assertion oracle and fixture independence: {{INDEPENDENTLY_DERIVED_EXPECTATION_AND_FIXTURE_BOUNDARY}}
- Closing command and success meaning: {{COMMAND_AND_SCOPE}}
- Evidence tiers and explained skips: {{UNIT_INTEGRATION_E2E_EXTERNAL_HUMAN_AND_LIMITS}}
- Mutable fixtures or services and holders: {{RESOURCES_AND_OWNERS}}
- Higher tiers left `UNPROVED`: {{LIMITS_OR_NONE}}
- Recovery owner and stop condition: {{OWNER_AND_CONDITION}}

Use the smallest check that can observe the change, then run the project's accepted
closing set. Do not invent a wrapper merely to fill this card. A fake or syntax check
does not prove a live service, device, provider, or production path.

Add a durable regression check only after reproducing a defect. Record the recurrence
signal, why current behavior tests missed it, its owner, upkeep cost, and deletion
condition.

For consequential logic, combine representative examples with independently derived
expectations and property or metamorphic checks when they expose domain invariants.
Use coverage to locate blind critical paths, not as a quality percentage. Consider
mutation testing only when its likely assertion signal repays its runtime and upkeep.

Related cards: [delivery and Git hooks](delivery-git-hooks.md),
[quality evaluation](quality-evaluation.md).
