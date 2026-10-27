# Frozen comparison brief

## Question

Under the same small offline task and resource limits, how do a cold start and a
Warmboot start differ in completion, software quality, intervention, elapsed time,
and recorded usage? Report each dimension separately. One run cannot establish a
general advantage.

## Frozen task

Place the following paragraph in immutable `BRIEF.md` for each runner and supply
the same frozen cases in [`rubric.md`](rubric.md):

> Build a Python 3.11-or-newer command-line program named `inventory-total` that runs as `python3 inventory_total.py INPUT.csv`; reads a UTF-8 CSV file with the exact header `item,quantity,unit_price`; prints one JSON object containing `item_count`, `total_quantity`, and a decimal-string `total_value` rounded half-up to two places; matches every supplied success and failure case; uses only the standard library; and delivers exactly three runner-authored product files: `inventory_total.py`, `tests/test_inventory_total.py`, and `README.md`.

All rubric cases are visible before execution; there are no hidden cases. The
runner may change only the three product paths plus `TASK.md` and optional
`HANDOFF.md` process receipts. Give both conditions the same initially empty
`TASK.md` and permission to create `HANDOFF.md`; neither receipt is a product
requirement. `BRIEF.md`, rubric, fixtures, settings and control files are immutable
pre-existing inputs, not receipts or deliverables. This path permission adds no
Warmboot guidance to the cold condition. The closing command is:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

## Conditions

- **Cold:** a fresh workspace containing the frozen inputs and empty `TASK.md`,
  plus the ordinary runtime instructions needed to access the tools.
- **Warmboot:** an identical fresh workspace and task, initialized from one exact
  frozen Warmboot snapshot before the runner starts.

Use isolated workspaces and fresh sessions. Randomize condition order. Never carry
messages, files, fixes, or lessons from one run into the other.

## Shared controls

Before starting, record one settings card and apply it unchanged to both runs:

- exact model and reasoning settings;
- interpreter and operating-system versions;
- available tools and maximum of two child workers;
- no network, package installation, remote, credentials, or human coaching;
- writes allowed only inside the assigned disposable workspace;
- a 45-minute wall-clock limit and the same predeclared native usage cap;
- one retry only for infrastructure failure, never for a poor solution.

Interruption uses the same rule in both conditions: stop immediately after the
first test-suite command finishes, or at minute 20 if no suite has run. Preserve
only the workspace, including any `TASK.md`/`HANDOFF.md` receipts, then resume in a
fresh session with the same settings and remaining time and usage budget. If a run
finishes before the trigger, record it as completed without interruption rather than
extending it.

At the limit, stop without coaching. Preserve the workspace and record the run as
`COMPLETE`, `INCOMPLETE`, `INTERVENED`, or `INFRASTRUCTURE FAILURE` before review.

## Product-only review bundle

After both runs stop, a preparer who is not the product reviewer creates two
randomly assigned neutral directories and seals the condition-to-directory map.
For each run, copy the existing bytes at exactly these relative paths, without
editing prose, comments, whitespace, or code:

- `inventory_total.py`
- `tests/test_inventory_total.py`
- `README.md`

Do not copy immutable `BRIEF.md`, fixtures, rubric, settings or control files. Keep
`TASK.md` and `HANDOFF.md` for process analysis but explicitly exclude both from the
product bundle. Also exclude `.agent-warmboot/`, `AGENTS.md`, `CLAUDE.md`, Git data,
caches, logs, transcripts, and usage records. A missing deliverable remains missing; never
fabricate a file or repair the runner's output. The reviewer receives only each
neutral directory and the frozen rubric.

Before review, scan copied content case-insensitively for `warmboot`,
`.agent-warmboot`, `AGENTS.md`, `CLAUDE.md`, `TASK.md`, `HANDOFF.md`, `BRIEF.md`,
`cold`, and explicit condition labels.
Record every hit without removing it. Also record structural leakage: missing or
extra deliverables, imports or links to excluded paths, differing text encodings,
and any copy failure. Keep the map and leakage report sealed until the reviewer
records the initial categorical review and whether they inferred a condition.
Then reveal the labels and leakage report.

This is a condition-hidden attempt, never a blind review when content or structure
can reveal a condition. Revealing terms remain in runner-authored prose; report
the limitation instead of sanitizing the evidence.

Do not alter the prompt, cases, limits, interruption rule, or rubric after the
first run starts. If any control differs, disclose it and do not present the pair
as controlled.
