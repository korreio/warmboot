# Optional engineering capability cards

These cards help a team decide whether a practice belongs in a real target. They are
not a checklist, installer, or claim that every project needs the same machinery.

- Library owner: the maintainer of the template set.
- Authority: guidance only; the library grants no Git, package, network, credential,
  deployment, release, publication, device, or shared-resource permission.
- Evidence boundary: only target-native checks against named inputs can support target
  claims.
- Maintenance: update a card when its decision trigger, risk, or recurring cost changes.
- Revisit or retire: merge overlapping cards and remove cards that no longer improve a
  real decision.

## How to use a card

1. Inspect the target's existing owners, commands, hazards, and documentation.
2. Open only a card with a real trigger.
3. Choose `ADOPT`, `MERGE INTO EXISTING`, `CITE ONLY`, or `OMIT`.
4. Record the surviving owner, authority boundary, target-native evidence, maintenance
   cost, and revisit or removal condition.

Prefer `MERGE INTO EXISTING` when a credible target surface already owns the practice.
Choose `OMIT` when there is no current need, owner, valid evidence, or accepted recurring
cost.
Missing authority is `BLOCKED`; an unavailable observing tier is `UNPROVED`.

## Included cards

| Card | Use it to decide |
|---|---|
| [Testing and feedback](testing-feedback.md) | Which focused and closing checks are worth maintaining |
| [Delivery and Git hooks](delivery-git-hooks.md) | Whether a local hook prevents a reproduced class of mistake |
| [Security, privacy, and secrets](security-privacy-secrets.md) | Which threat-led checks belong at a sensitive boundary |
| [Dependencies and licences](dependencies-licences.md) | How a dependency earns its cost and review burden |
| [Quality evaluation](quality-evaluation.md) | Whether a bounded measurement can change a real decision |

Related cards are navigation only. Selecting one never selects another or authorizes an
action.

