# MATISSE — generation/review pipeline

Initial validation of the Config+Helpers approach within the
[MATISSE](https://matisse-kdt.eu/) European project (Nov 2025 – Feb 2026).
**24 scenarios · 7 industrial partners · Config+Helpers only.**

## 6-stage pipeline

A 6-stage pipeline was applied to each scenario:

1. **Partner inputs collection** — informal workflow descriptions
   (draw.io, MS Word, or both).
2. **LLM-assisted review** — systematic issue detection before generation
   (the 97 issues in Table M1 were found in this stage).
3. **LLM generation** — Config+Helpers solution used for all scenarios.
4. **Recommendation** — corrected BPMN + structured description shared
   with partners.
5. **Partner review** — accuracy validation, naming alignment, scope
   decisions.
6. **Deliverable** — final BPMN models consolidated into the project
   deliverable.

> **TODO (authors):** add per-partner notes on the review cadence (who
> performed the LLM-assisted review at stage 2, who validated at stage 5,
> typical iteration count). This is the place to address Reviewer 2 Q2 for
> the MATISSE side of the evaluation.

## Why MATISSE is presented separately from the PMo benchmark

The MATISSE evaluation is *qualitative and partner-driven*: partners did
not work from a fixed scoring rubric, and "adopted as-is" reflects partner
acceptance rather than an external ground truth. The PMo controlled
benchmark exists precisely to complement this with metric-driven
comparison. See [`../PROCEDURE.md`](../PROCEDURE.md) for the controlled
benchmark.
