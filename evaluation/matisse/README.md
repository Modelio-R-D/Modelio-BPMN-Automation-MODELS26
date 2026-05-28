# MATISSE industrial validation

The MATISSE European project (Grant Agreement ID 101140216) provided the
real-world validation context for the Config+Helpers approach — 24 scenarios
from 7 industrial partners across railway, energy, manufacturing,
infrastructure, automotive, and defense domains.

## What is and isn't in this repository

- ✅ **Aggregated structural metrics** are in
  [`partner_metrics.md`](partner_metrics.md) (paper Tables M1, M2, M3, M4).
- ✅ **The 6-stage generation/review pipeline** is documented in
  [`procedure.md`](procedure.md).
- ❌ **Partner-provided workflows and generated BPMN models** are
  **confidential** and remain inside the MATISSE project deliverables.
  They are not shared in this repository.

This division was explicit in the consortium agreement; the public artifact
is restricted to aggregate metrics and methodology.

## How MATISSE differs from the PMo controlled benchmark

| Dimension                          | MATISSE (24) | PMo benchmark (55) |
|------------------------------------|-------------:|-------------------:|
| Average lanes per process          | 4.3          | 1.1                |
| Average data objects per process   | 8.2          | 0                  |
| Average data associations          | 14.6         | 0                  |
| Average output lines               | 232          | 137                |

MATISSE processes are *multi-actor and data-rich*; PMo scenarios are
*single-lane with complex decision logic*. Together they probe different
ends of the BPMN complexity space — a point Reviewer 3 raised as a strength
of the dual-track evaluation.
