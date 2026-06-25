# S1 — Simple: Document Approval

The first preliminary scenario. One reviewer, one lane, four elements
in a linear flow. Used to test whether the LLMs can produce *any*
working Modelio Jython script.

## Round-1 prompt (zero-shot)

This is the prompt sent to each LLM with **no API examples** attached.

```
Generate a complete Jython script for Modelio that creates a BPMN diagram for the following process:

A simple document approval process with one reviewer:
1. Start
2. Submit Document (user task)
3. Review Document (user task)
4. End

Single lane: "Reviewer"
Linear flow from start to end.

The script should:
1. Create a new BpmnProcess
2. Create BpmnLanes for each role
3. Create all BPMN elements (tasks, events, gateways)
4. Create sequence flows connecting elements
5. Create a BpmnProcessDesignDiagram
6. Position all elements in the diagram with proper layout

Output only the complete, executable Jython script.
```

## Round-2+ prompt (with-examples condition)

Same prompt as above, with the trailing line *"See examples in
attachment. Fix BPMN."* and the two Modelio sample macros from
[`../modelio_api_examples/`](../modelio_api_examples/) attached as
context:
[`MakeSingleton.py`](../modelio_api_examples/MakeSingleton.py) and
[`Sort.py`](../modelio_api_examples/Sort.py).

```
Generate a complete Jython script for Modelio that creates a BPMN diagram for the following process:

A simple document approval process with one reviewer:
1. Start
2. Submit Document (user task)
3. Review Document (user task)
4. End

Single lane: "Reviewer"
Linear flow from start to end.

The script should:
1. Create a new BpmnProcess
2. Create BpmnLanes for each role
3. Create all BPMN elements (tasks, events, gateways)
4. Create sequence flows connecting elements
5. Create a BpmnProcessDesignDiagram
6. Position all elements in the diagram with proper layout

See examples in attachment. Fix BPMN.

Output only the complete, executable Jython script.
```

## Results

Round-by-round outcomes per LLM are tabulated in
[`../README.md`](../README.md). The generated
scripts for S1 are at
[`../results/scripts/`](../results/scripts/):
`s1_claude.py`, `s1_claude_r2.py`, `s1_claude_r5.py`,
`s1_gpt5.py`, `s1_gpt5_r2.py`,
`s1_gemini.py`, `s1_gemini_r2.py`, `s1_gemini_r9.py`.
