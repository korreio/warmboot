# Quality evaluation

## Adoption decision

- Adopt when a bounded measurement can change a real architecture, usability,
  accessibility, performance, or release decision.
- Merge into existing performance, accessibility, visual, or product-quality evidence
  when it already has an owner and threshold.
- Omit when the metric has no decision, representative input, action, owner, or deletion
  rule, or would create dashboard work without value.
- Decision owner: the person accountable for the decision the measurement can change.
- Authority: this card grants no user-data, browser, device, model, credential, network,
  deployment, release, or publication permission.
- Evidence: frozen representative inputs, the cheapest discriminating measure, variance,
  and target-native correctness checks.
- Maintenance: fixture curation, threshold drift, runtime, artifact review, and result
  interpretation.
- Revisit or remove: after the one-time decision when recurrence adds no value, or when
  the user outcome, platform, or observed quality risk changes.

## Target record

- Decision and alternatives: {{DECISION}}
- Representative inputs and owner: {{INPUTS_AND_OWNER}}
- Measure, threshold, and action: {{MEASURE_THRESHOLD_ACTION}}
- Mutable report, browser, device, or model holder: {{RESOURCE_AND_OWNER}}
- Evidence result and variance: {{RESULT}}
- Production or user outcome left `UNPROVED`: {{LIMIT}}

Stop when captured material is sensitive, inputs are not representative, measurements
are unstable, or the result cannot change the decision. A synthetic score does not
prove production usability, accessibility, device behavior, model quality, or user
value.

For a materially complex or multi-component coded project, this card may instead be
merged into the active plan or system map as the current quality-control loop. Gather
evidence and explicit unknowns by component and applicable concern (architecture and
ownership, source comprehension, tests, security/privacy/operations), then record the
next improvement, owner and revisit trigger. A human or independent non-author
reviewer challenges the evidence. Letter grades and scores are optional navigation;
they cannot self-close or replace a tied action. Automate evidence collection and
regression flags where useful, never semantic adequacy.

Related cards: [testing and feedback](testing-feedback.md),
[security, privacy, and secrets](security-privacy-secrets.md).
