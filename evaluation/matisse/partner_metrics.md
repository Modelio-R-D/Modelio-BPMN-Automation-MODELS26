# MATISSE — partner metrics (paper Tables M1–M4)

Aggregated metrics over the 24 industrial scenarios. The raw per-partner
workflows and generated BPMN models are confidential — see
[`README.md`](README.md).

## Table M1 — Detected issues in partner-provided workflows

> 97 issues found across 12 scenarios with quantified reviews
> (avg 8.1 per scenario).

| Category       | Count | %   | Examples                                       |
|----------------|------:|----:|------------------------------------------------|
| Structural     |    34 | 35% | Missing actor lanes, unclear start/end events  |
| Data flow      |    24 | 25% | Undefined data objects, missing associations   |
| Process logic  |    22 | 23% | Missing decision gateways, absent feedback     |
| Traceability   |    17 | 17% | Requirement ID mismatches, coverage gaps       |
| **Total**      |    97 |     | avg 8.1 per scenario                           |

## Table M2 — Partner retention of generated BPMN models

> 22 LLM-generated corrected BPMN models compared against final Modelio
> models.

| Category        | Count | %   | Description                                       |
|-----------------|------:|----:|---------------------------------------------------|
| Adopted as-is   |    14 | 64% | Model accepted in Modelio without modification    |
| Minor changes   |     3 | 14% | Task or lane name adjustments only                |
| Major refactor  |     5 | 22% | Partners change structure or naming conventions   |

## Table M3 — Structural metrics by partner (final BPMN models)

| Partner | Domain           | Scenarios | Avg Lanes | Avg Tasks | Avg Gateways | Avg Data Obj. | Avg Data Assoc. |
|---------|------------------|----------:|----------:|----------:|-------------:|--------------:|----------------:|
| P1      | Railway          |         2 |       3.0 |      13.0 |          6.0 |          10.0 |            17.5 |
| P2      | Energy/microgrid |         3 |       4.3 |      11.0 |          1.3 |           4.0 |             8.7 |
| P3      | Smart grid       |         4 |       5.0 |      15.8 |          3.3 |           9.0 |            15.5 |
| P4      | Infrastructure   |         4 |       4.5 |      11.8 |          4.0 |           6.5 |            11.0 |
| P5      | Manufacturing    |         5 |       5.0 |      15.8 |          3.6 |           6.2 |            12.4 |
| P6      | Automotive       |         4 |      3.75 |      17.3 |          3.5 |          11.8 |            23.8 |
| P7      | Defense          |         2 |       4.0 |      14.0 |          2.5 |          13.0 |            26.0 |
| **All** |                  |    **24** |   **4.3** |  **14.5** |      **3.3** |       **8.2** |        **14.6** |

## Table M4 — MATISSE vs. PMo dataset comparison

| Metric                       | MATISSE (24)         | PMo (55)             | Ratio |
|------------------------------|---------------------:|---------------------:|------:|
| Avg lanes                    |                  4.3 |                  1.1 |  3.9× |
| Avg tasks/elements           |                 14.5 |                 22.6 |  0.6× |
| Avg gateways                 |                  3.3 |                  8.3 |  0.4× |
| Avg data objects             |                  8.2 |                    0 |     — |
| Scenarios with data objects  |          23/24 (96%) |           0/55 (0%)  |     — |
| Avg data associations        |                 14.6 |                    0 |     — |
| Avg lines in output          |   232 (range 116–549)| 137 (range 53–328)   |  1.7× |

> MATISSE scenarios represent collaborative multi-actor workflows
> (4.3 lanes avg), while PMo scenarios are predominantly single-lane
> (1.1 lanes avg) with more complex decision logic (8.3 gateways avg).
> MATISSE outputs are also significantly richer in data objects and
> associations, highlighting dimensions that controlled benchmarks may
> underestimate.
