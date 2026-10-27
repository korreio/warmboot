# Security, privacy, and secrets

## Adoption decision

- Adopt when the target handles credentials, personal or sensitive data, external
  exposure, uploads, logs, privileged operations, or material dependency risk.
- Merge into existing security, privacy, and incident authorities whenever they exist.
- Omit a proposed control when it lacks a concrete threat, owner, safe output policy,
  triage path, or permission; do not omit a known risk without recording its consequence.
- Decision owner: the target's named security or privacy owner.
- Authority: this card grants no secret access, scanning, package, network, credential,
  deployment, incident response, release, or publication permission.
- Evidence: synthetic local canaries and target-native checks; external observation
  only under separate exact authority.
- Maintenance: threat model, rules, suppressions, data flows, output retention, and
  false-positive triage.
- Revisit or remove: after changes to exposure, data, authentication, dependencies, or
  when the threat path disappears and another owned control covers it.

## Target record

- Threat and affected boundary: {{THREAT_AND_PATH}}
- Data classification and forbidden output: {{CLASSIFICATION}}
- Local check and owner: {{COMMAND_AND_OWNER}}
- Sensitive resources and holders: {{RESOURCES_AND_OWNERS}}
- External or live behavior left `UNPROVED`: {{LIMITS}}
- Containment and escalation owner: {{OWNER_AND_PROCEDURE}}

Stop on a suspected real secret or sensitive-data disclosure; do not repeat the value
in logs or reports. Scanner silence is not proof of security, and local fixtures do not
prove hosted configuration or external exposure.

Related cards: [dependencies and licences](dependencies-licences.md),
[delivery and Git hooks](delivery-git-hooks.md).

