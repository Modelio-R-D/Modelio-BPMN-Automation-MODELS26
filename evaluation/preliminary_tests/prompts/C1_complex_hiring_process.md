# C1 — Complex: Hiring Process

The complex-scale preliminary scenario. Four lanes (HR / Hiring
Manager / Candidate / IT), three exclusive gateways with three
decision points and cross-lane handoffs, multiple end events.

## Prompt

```
Generate a complete Jython script for Modelio that creates a BPMN diagram for the following process:

A complete hiring workflow:

Lanes: HR, Hiring Manager, Candidate, IT

Flow:
 1. Start (HR)
 2. Post Job Opening (User Task, HR)
 3. Receive Applications (User Task, HR)
 4. Screen Candidates (User Task, HR)
 5. Decision: Qualified? (Exclusive Gateway, HR)
 6. If No: Send Rejection (Send Task, HR) -> End
 7. If Yes: Schedule Interview (User Task, HR)
 8. Conduct Interview (User Task, Hiring Manager)
 9. Decision: Hire? (Exclusive Gateway, Hiring Manager)
10. If No: Send Rejection (Send Task, HR) -> End
11. If Yes: Make Offer (User Task, HR)
12. Candidate Decision (User Task, Candidate)
13. Decision: Accepted? (Exclusive Gateway, Candidate)
14. If No: End
15. If Yes: Setup Account (Service Task, IT)
16. Onboard Employee (User Task, HR)
17. End

Multiple decision points and four lanes with cross-lane handoffs.

The script should:
1. Create a new BpmnProcess
2. Create BpmnLanes for each role
3. Create all BPMN elements (tasks, events, gateways)
4. Create sequence flows connecting elements
5. Create a BpmnProcessDesignDiagram
6. Position all elements in the diagram with proper layout

Output only the complete, executable Jython script.
```

Same with-examples convention as S1 applies for the round-2+ form.

## Results

Only one generated script exists at
[`../results/scripts/c1_claude.py`](../results/scripts/c1_claude.py).
The source narrative captures the prompt and the script but did not
record a per-round outcome — the C1 row in the results table is
intentionally marked incomplete.
