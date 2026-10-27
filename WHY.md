# Why Warmboot Light exists

Coding agents often begin with too much repository context and too little operational context. They can read code yet still miss the active objective, overwrite concurrent work, confuse a passing command with sufficient evidence, or treat a handoff as permission.

Warmboot addresses that startup gap with a small contract loaded before task work. The core establishes stable boundaries; focused routes add detail only when the task needs it. The approach is deliberately plain text and provider-neutral so the target project owns the resulting instructions.

The contract centers on five habits:

1. select the smallest context that can change the decision;
2. name one holder for each mutable or scarce resource;
3. preserve routine state by reference and revalidate freshness;
4. match proof to the actual hazard;
5. use independent review for every code change and wherever else the risk warrants it.

Warmboot requires source documentation that outlasts an agent, provider, budget or
transcript: every human-authored code file needs immediate, language-native orientation,
and consequential decisions need local rationale and invariants. Review checks this
requirement; it is not a demand for long comments or generated prose.

Warmboot is not a substitute for project knowledge, architecture judgment, tests,
access control, or human accountability. It cannot make weak instructions correct,
and its checker verifies managed bytes rather than the quality of the work. Its useful
result is narrower: a repeatable starting contract that makes scope, ownership,
source comprehension, evidence, and recovery explicit.
