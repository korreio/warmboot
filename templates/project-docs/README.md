# {{PROJECT_NAME}}

Template use: merge into the existing project README when it already orients people.
Adopt only when the project lacks a current entry point. Omit a second README. Replace
every `{{MARKER}}`, remove inapplicable rows, and delete this note.

- Document owner: {{ONBOARDING_OWNER}}
- Authority: explains the project; grants no Git, package, network, credential,
  deployment, release, or publication permission.
- Evidence boundary: commands below establish only their stated local result.
- Maintenance: update when setup, entry points, architecture routes, or user-visible
  purpose changes.
- Revisit or retire: merge when another entry point becomes authoritative; remove when
  the project no longer needs separate onboarding.

{{ONE_SENTENCE_OUTCOME}}

## Current state

- Status and last verified date: {{STATUS_AND_DATE}}
- Active task or plan: {{TASK_PATH}}
- Known limits: {{UNPROVED_OR_BLOCKED_BOUNDARIES}}

{{PLAIN_LANGUAGE_SYSTEM_SHAPE}}

## Start locally

Requirements: {{RUNTIME_AND_VERSION}}

Open `{{ROOT_WORKSPACE_PATH}}` for project navigation.

| Intent | Project-native command | A successful result establishes |
|---|---|---|
| Set up | `{{SETUP_COMMAND}}` | {{SETUP_SCOPE}} |
| Run a focused check | `{{FOCUSED_COMMAND}}` | {{FOCUSED_SCOPE}} |
| Run the ordinary suite | `{{TEST_COMMAND}}` | {{TEST_SCOPE}} |
| Run locally | `{{RUN_COMMAND}}` | {{LOCAL_RUNTIME_SCOPE}} |

Report what actually ran. A local pass does not prove hosted, external, device, or
production behavior.

## Boundaries and routes

- Source owner: {{SOURCE_OWNER}}
- Current coordinator and Git holder: {{TASK_PATH}}
- Agent instructions: `{{AGENT_INSTRUCTIONS_PATH}}`
- Sensitive or excluded inputs: {{PRIVACY_BOUNDARY}}
- External effects: {{EXACT_AUTHORITY_OR_NONE}}

| Need | Living owner |
|---|---|
| Architecture and ownership | `{{SYSTEM_MAP_OR_SOURCE_PATH}}` |
| Engineering and testing | `{{STANDARDS_AND_TESTING_PATHS}}` |
| Change and escaped-defect history | `{{CHANGELOG_AND_BUGFIX_PATHS}}` |
| Current execution state | `{{TASK_PATH}}` |
