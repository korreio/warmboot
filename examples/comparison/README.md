# Warmboot comparison protocol

This is a small protocol for comparing a cold coding-agent start with a Warmboot
start. Here, reproducible means the task, controls, interruption, review bundle,
and oracles are frozen before execution. It does not mean an outcome will repeat.
This folder contains no run, result, or claim that either condition is better.
Both conditions permit mutable `TASK.md` and optional `HANDOFF.md` process receipts;
immutable task input is named `BRIEF.md`. Receipts survive interruption but stay out
of product review, with their use reported separately.

- [`brief.md`](brief.md) freezes the task, inputs, conditions, authority, budget,
  interruption, and isolation rules.
- [`rubric.md`](rubric.md) separates finished-software quality from process cost
  and defines categorical reporting for incomplete or intervened runs.

Use disposable, fully synthetic workspaces. Freeze the Warmboot bytes and this
protocol before execution. Review is only a condition-hidden attempt: unchanged
product prose can reveal its origin. A checked-in demonstration can illustrate
the method, but it cannot support a general productivity claim.
