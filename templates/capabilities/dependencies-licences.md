# Dependencies, licences, and supply chain

## Adoption decision

- Adopt when a package, runtime, generated artifact, or vendored component affects
  installation, security, reproducibility, support, or distribution decisions.
- Merge into existing package, update, and notice ownership when it is current.
- Omit an extra process when no dependency decision is changing; never add inventory
  work only to appear complete.
- Decision owner: one named owner for each package, runtime, or vendored surface.
- Authority: this card grants no installation, registry, credential, network, lockfile,
  vendoring, release, or publication permission.
- Evidence: frozen manifest and lock consistency, target-native build or test, and
  appropriate provenance and licence review for intended use.
- Maintenance: updates, advisories, runtime support, lock conflicts, provenance, and
  required notices.
- Revisit or remove: when a dependency becomes unused, an advisory or licence changes,
  distribution intent changes, or a platform feature can replace it more simply.

## Target record

- Capability need and simpler alternatives: {{NEED_AND_OPTIONS}}
- Manifest, lock, and owner: {{PATHS_AND_OWNER}}
- Intended use or distribution boundary: {{BOUNDARY}}
- Native checks and results: {{COMMANDS_AND_RESULTS}}
- Unknown platform, security, or licence questions: {{UNPROVED_OR_BLOCKED}}
- Recovery choice owner: {{OWNER_AND_REMOVE_PIN_OR_REPLACE_OPTIONS}}

Stop on an unknown licence, mutable source, unexpected lock rewrite, unavailable private
registry, or unresolved advisory that matters to the target. A clean scanner result does
not establish absence of vulnerabilities or suitability for every use.

Related cards: [security, privacy, and secrets](security-privacy-secrets.md),
[testing and feedback](testing-feedback.md).

