# M1 — Medium: Employee Leave Request

The medium-complexity preliminary scenario. Two lanes (Employee /
Manager), one decision gateway, two parallel end events for the
approved/rejected branches.

## Prompt

```
Generate a complete Jython script for Modelio that creates a BPMN diagram for the following process:

An employee leave request process:

Lanes: Employee, Manager

Flow:
1. Start (Employee)
2. Submit Leave Request (User Task, Employee)
3. Review Request (User Task, Manager)
4. Decision Gateway (Manager)
5. If Approved: Update Calendar (Service Task, Employee)
6. If Rejected: Notify Employee (Send Task, Manager)
7. End (Employee for approved path, Manager for rejected path)

The manager reviews and either approves or rejects the request.

The script should:
1. Create a new BpmnProcess
2. Create BpmnLanes for each role
3. Create all BPMN elements (tasks, events, gateways)
4. Create sequence flows connecting elements
5. Create a BpmnProcessDesignDiagram
6. Position all elements in the diagram with proper layout

Output only the complete, executable Jython script.
```

Same with-examples convention as S1 (see
[`S1_simple_document_approval.md`](S1_simple_document_approval.md))
applies for the round-2+ form.

## Results

Only one generated script exists at
[`../results/scripts/m1_claude.py`](../results/scripts/m1_claude.py).
The source narrative captures the prompt and the script but did not
record a per-round outcome — the M1 row in the results table is
intentionally marked incomplete.
