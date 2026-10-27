# Frozen categorical review and reporting rubric

Review each neutral product bundle under the controls in
[`brief.md`](brief.md). The condition mapping stays sealed until the reviewer
records the initial checks and whether they inferred a condition. This is a
condition-hidden attempt, not a guaranteed blind review.

## Evidence labels

Use one label for every required check:

- `PASS`: the check ran against the frozen bytes and matched every stated
  expectation.
- `FAIL`: the check ran and differed, or a required deliverable was absent.
- `UNPROVED`: the check could not run or its evidence could not see the stated
  requirement. Record why; missing evidence is never a pass.

## Record completion first

Completion describes the run, not product quality:

- `COMPLETE`: all three deliverables exist and the runner ended within the frozen
  limit without human product changes.
- `INCOMPLETE`: a deliverable is missing or the runner stopped with unfinished
  work.
- `INTERVENED`: a human coached the run or changed product bytes.
- `INFRASTRUCTURE FAILURE`: the frozen environment failed before the runner had a
  fair opportunity.

Record one completion category before product review. Do not turn it into points
or silently retry it as another category.

## Frozen CLI cases

Every runner receives these cases and expectations before execution. Create the
fixture bytes outside the product bundle. Each displayed CSV ends with one final
newline. From the bundle root, invoke
`python3 inventory_total.py FIXTURE_PATH` with bytecode writes disabled.

Successful stdout below is exact, including JSON spacing and final newline;
successful stderr is empty.

### F1 — valid rows

```csv
item,quantity,unit_price
Notebook,2,3.50
Pen,3,1.20
```

- Exit: `0`
- Stdout: `{"item_count":2,"total_quantity":5,"total_value":"10.60"}\n`

### F2 — header only

```csv
item,quantity,unit_price
```

- Exit: `0`
- Stdout: `{"item_count":0,"total_quantity":0,"total_value":"0.00"}\n`

### F3 — decimal half-up boundary

```csv
item,quantity,unit_price
Pin,1,1.005
```

- Exit: `0`
- Stdout: `{"item_count":1,"total_quantity":1,"total_value":"1.01"}\n`

For F4–F10, exit must be `2`, stdout must be empty, and stderr must be exactly the
one concise line shown, with no traceback.

### F4 — missing column

```csv
item,quantity
Notebook,2
```

- Stderr: `error: missing column: unit_price\n`

### F5 — malformed number

```csv
item,quantity,unit_price
Notebook,two,3.50
```

- Stderr: `error: malformed number on row 2\n`

### F6 — negative quantity

```csv
item,quantity,unit_price
Notebook,-1,3.50
```

- Stderr: `error: negative quantity on row 2\n`

### F7 — negative price

```csv
item,quantity,unit_price
Notebook,1,-3.50
```

- Stderr: `error: negative unit_price on row 2\n`

### F8 — unreadable deterministic boundary

Create an evaluator-owned directory named `not-a-file` and pass that directory
path as `FIXTURE_PATH`. Do not use permissions as the boundary because they vary
by platform.

- Stderr: `error: cannot read input\n`

### F9 — reordered header

```csv
quantity,item,unit_price
2,Notebook,3.50
```

- Stderr: `error: invalid header\n`

### F10 — extra column

```csv
item,quantity,unit_price,notes
Notebook,2,3.50,plain
```

- Stderr: `error: invalid header\n`

## Required categorical checks

Record `PASS`, `FAIL`, or `UNPROVED` independently for every row.

| ID | Check | `PASS` requires |
|---|---|---|
| C1 | Exact product layout | All three required regular UTF-8 files exist, and the program and tests need no product file outside the review bundle. |
| C2 | Valid calculation | F1 matches its exact exit, stdout, and stderr. |
| C3 | Empty dataset | F2 matches its exact exit, stdout, and stderr. |
| C4 | Decimal rounding | F3 matches its exact exit, stdout, and stderr. |
| C5 | Failure boundaries | F4–F10 each match exact exit, stdout, and stderr without a traceback. |
| C6 | Runner tests | `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v` exits `0`, and `tests/test_inventory_total.py` directly exercises F1–F10. |
| C7 | Runtime and maintenance boundary | Inspection finds only standard-library imports, no network, subprocess, installation, persistence, or external service; importing `inventory_total.py` performs no CLI I/O; parsing, calculation, and CLI responsibilities are identifiable and testable. |
| C8 | User documentation | `README.md` states the exact invocation, required header, three JSON fields, exit-2 boundary, standard-library no-install path, test command, and limits. |
| C9 | Review-bundle integrity | The copy receipt accounts for missing paths and content or structural leakage, runner-authored bytes were not edited, and the condition mapping remained hidden through initial review. |

Do not total these checks, weight them, rank the conditions, or replace the row
results with a convenience category. Report the completion category and all nine
check labels side by side, with the exact commands and reviewer notes.

## Process measures — separate from product checks

Report each run as one row with:

- neutral directory ID, with the condition revealed only after initial review;
- completion category and reason;
- condition-inference guess and the later content or structural leakage report;
- human interventions, retries, and infrastructure failures;
- wall-clock time before interruption, after resumption, and total;
- model and tool usage in native units, using `UNAVAILABLE` rather than an
  estimate when it cannot be exported;
- number of tool calls and child workers started;
- scope or authority violations;
- whether `TASK.md` or `HANDOFF.md` was used, which receipt bytes survived the
  interruption, and whether the receiver used them to continue the next outcome;
- whether evidence was rerun after resumption and whether unrelated files changed.

Retain individual rows. Product checks, interventions, time, and usage remain
separate and are never combined into a score.

## Interpretation limits

This repository contains a frozen process, not a result. One pair would describe
only this task under its recorded settings. Disclose changed controls, incomplete
runs, failed checks, condition leakage, review disagreement, and exclusions. The
protocol must be able to report no difference or a worse Warmboot result without
changing the rules.
