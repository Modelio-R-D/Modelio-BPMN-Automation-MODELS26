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

Per-partner review cadence (who performed the stage-2 LLM-assisted
review, who validated at stage 5, typical iteration counts) is
documented in the MATISSE consortium deliverable and is **not
disclosed in this public artifact** — consistent with the
confidentiality boundary stated in [`README.md`](README.md). Aggregate
retention figures and structural metrics are in
[`partner_metrics.md`](partner_metrics.md).

## Why MATISSE is presented separately from the PMo benchmark

The MATISSE evaluation is *qualitative and partner-driven*: partners did
not work from a fixed scoring rubric, and "adopted as-is" reflects partner
acceptance rather than an external ground truth. The PMo controlled
benchmark exists precisely to complement this with metric-driven
comparison. See [`../PROCEDURE.md`](../PROCEDURE.md) for the controlled
benchmark.
