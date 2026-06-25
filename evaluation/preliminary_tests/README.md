# Preliminary evaluation — one-shot generation baseline

Evidence base for paper §2.2 *"Motivating Scenario in MATISSE"* and §6 *"Lessons Learned
and Guidelines"*. Distinct from the published 55-scenario PMo benchmark in
[`../runs/`](../runs/): different scope, different LLM set, different purpose.

## Contents

```
preliminary_tests/
├── README.md                            ← you are here (full narrative below)
├── prompts/
│   └── S1_simple_document_approval.md   The single scenario exercised
├── modelio_api_examples/                Modelio OSS sample macros given to the LLMs
│   ├── README.md
│   ├── MakeSingleton.py
│   └── Sort.py
└── results/
    ├── scripts/                         All 8 generated Jython scripts (verbatim)
    └── screenshots/                     The 2 converged-diagram screenshots
```

| LLM              | Version             | Rounds on S1 |
|------------------|---------------------|:------------:|
| Claude Opus 4.5  | Anthropic, Dec 2025 | 5            |
| GPT-5.2 Thinking | OpenAI, Dec 2025    | 2            |
| Gemini Pro 3.1   | Google, Dec 2025    | 9            |

---

# Experiment 1: One-Shot Generation Results

## Summary

| Model | S1 (No Example) | S1 (With Example) | S1 (With Debugging) |
|-------|-----------------|-------------------|---------------------|
| Claude Opus 4.5 | Failure (API) | Failure (API) | **Model OK, Layout Broken** (5 rounds) |
| GPT-5.2 Thinking | Failure (Syntax) | **Model OK, Layout Broken** | — |
| Gemini Pro (Dec 2025) | Failure (API) | Failure (API) | **FAILURE** (9 rounds) |

> The preliminary evaluation only exercised **S1**. Medium (M1) and
> Complex (C1) scenarios were designed but never run — the budget was
> spent fully on S1 because all three LLMs needed several rounds even
> at the simplest complexity level. The published 55-scenario PMo
> benchmark in [`../runs/`](../runs/) covers the medium and complex end
> of the space at much greater depth.

**Note:** "Model OK, Layout Broken" = Script executes, BPMN model created correctly, but diagram layout is corrupted. Layout is a separate problem from model generation.

---

# S1 - Document Approval (Simple)

## Prompt

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

---

## S1 - Claude Opus 4.5 (Round 1 - No Example)

**Script:** [results/scripts/s1_claude.py](results/scripts/s1_claude.py)
**Lines of Code:** 267
**Result:** Failure

**Modelio Output:**
```
ImportError: No module named model in <script> at line number 6
```

**Error Type:** API (wrong imports)
**Notes:** Generated plausible-looking but incorrect import statements

---

## S1 - Gemini Pro (Dec 2025) (Round 1 - No Example)

**Script:** [results/scripts/s1_gemini.py](results/scripts/s1_gemini.py)
**Lines of Code:** 148
**Result:** Failure

**Modelio Output:**
```
ImportError: No module named model in <script> at line number 1
```

**Error Type:** API (wrong imports)
**Notes:** Wrong import paths

---

## S1 - GPT-5.2 Thinking (Round 1 - No Example)

**Script:** [results/scripts/s1_gpt5.py](results/scripts/s1_gpt5.py)
**Lines of Code:** 204 (incomplete - script truncated)
**Result:** Failure

**Modelio Output:**
```
org.python.antlr.ParseException: encoding declaration in Unicode string
```

**Error Type:** Syntax (encoding declaration not allowed in Jython)
**Notes:** Added `# -*- coding: utf-8 -*-` which Jython rejects. Script also incomplete.

---

# S1 - Round 2 (With Examples)

## Prompt (Round 2)

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

*(Attached: MakeSingleton.py and Sort.py from Modelio examples)*

---

## S1 - Claude Opus 4.5 (Round 2-5 - With Example + Debugging)

**Final Script:** [results/scripts/s1_claude_r5.py](results/scripts/s1_claude_r5.py)
**Lines of Code:** 191
**Result:** Success (after 5 rounds of debugging)

**Screenshot:** ![Claude S1 r5](results/screenshots/s1_claude_r5.png)

### Debugging Journey

**Round 2:** Initial attempt with examples
- Failed (details not captured)

**Round 3:**
```
AttributeError: 'org.modelio.metamodel.impl.bpmn.events.BpmnStartEv' object has no attribute 'setLane'
```
- **Error Type:** API
- **Fix:** Lane membership must be set from Lane side using `lane.getFlowElementRef().add(element)`, not `element.setLane(lane)`

**Round 4:**
```
AttributeError: 'org.modelio.api.impl.diagrams.DiagramService' object has no attribute 'createDiagram'
```
- **Error Type:** API
- **Fix:** Diagrams created through model factory, not DiagramService

**Round 5:**
```
AttributeError: 'java.util.ArrayList' object has no attribute 'setSize'
```
- **Error Type:** API
- **Fix:** `unmask()` returns ArrayList, not single graphic. Must use `graphics.get(0).setSize()`

**Final Output (Round 5):**
```
Created process: Document Approval Process
Created lane: Reviewer
Created 4 flow elements
Added elements to lane
Created 3 sequence flows
Created diagram: Document Approval Process Diagram
Diagram layout completed

SUCCESS: Document Approval Process created!
```

**Notes:** Required 5 rounds of iterative debugging with error feedback. Each round revealed a different API misconception. Final script is 191 lines with proper helper functions. **Layout corrupted** — same issue as GPT, elements not positioned correctly despite coordinates being set.

---

## S1 - Gemini Pro (Dec 2025) (Round 2-9 - With Example + Debugging)

**Final Script:** [results/scripts/s1_gemini_r9.py](results/scripts/s1_gemini_r9.py)
**Lines of Code:** 169
**Result:** **FAILURE after 9 rounds**

### Debugging Journey (9 rounds - all failed)

**Round 3:**
```
ImportError: No module named process
```
- **Error Type:** API (wrong import path)

**Round 4:**
```
NameError: global name 'Model' is not defined
```
- **Error Type:** API (non-existent global)

**Round 5:**
```
AttributeError: 'SharedModelingSession' object has no attribute 'getMetamodel'
```
- **Error Type:** API (wrong method)

**Round 6:**
```
TypeError: No visible constructors for class (BpmnProcess)
```
- **Error Type:** API (tried to instantiate interface)

**Round 7:**
```
AttributeError: 'SmMetamodel' object has no attribute 'getMObjectFactory'
```
- **Error Type:** API (wrong factory access)

**Round 8:**
```
Error: MClass for BpmnProcess found, but has no attribute 'createInstance'
```
- **Error Type:** API (reflection doesn't work)

**Round 9:**
```
Error: MClass object has no attribute 'createInstance'
```
- **Error Type:** API (still trying reflection)

### Critical Observation

**Gemini went in completely wrong direction after Round 3.**

The working pattern (shown in Claude's R5 and the provided examples) is:
```python
modelingSession.getModel().createBpmnProcess()
```

Instead, Gemini tried increasingly complex approaches:
1. `Model.getMetamodel().getMObjectFactory()` — doesn't exist
2. `new BpmnProcess()` — can't instantiate interfaces
3. `metamodel.getMClass("BpmnProcess").createInstance()` — reflection doesn't work

**Root cause:** Gemini failed to learn from the provided examples (MakeSingleton.py, Sort.py) which clearly show `modelingSession.getModel().createX()` pattern.

**Notes:** After 9 rounds of debugging, Gemini could not produce a working script. Each fix introduced new errors, spiraling away from the correct solution instead of converging.

---

## S1 - GPT-5.2 Thinking (Round 2 - With Example)

**Script:** [results/scripts/s1_gpt5_r2.py](results/scripts/s1_gpt5_r2.py)
**Lines of Code:** 205
**Result:** Partial Success

**Screenshot:** ![GPT-5.2 S1 r2](results/screenshots/s1_gpt5_r2.png)

**Modelio Output:**
```
Script executed successfully (model created)
Diagram layout corrupted
```

**Error Type:** Layout
**Notes:** Script executed without errors and created the BPMN model, but diagram layout is corrupted due to Modelio's unpredictable diagram unmasking behavior. Elements positioned incorrectly.

---

# Observations

## Round 1: No Examples — All Failed

All three models failed when generating Modelio Jython scripts without examples:
- **Claude Opus 4.5:** Wrong import paths (API hallucination)
- **GPT-5.2 Thinking:** Encoding declaration error + incomplete script
- **Gemini Pro:** Wrong import paths (API hallucination)

**Conclusion:** LLMs cannot generate correct Modelio API code from training data alone.

## Round 2+: With Examples + Debugging

| Model | Result | Rounds | Notes |
|-------|--------|--------|-------|
| GPT-5.2 | **Model OK** | 1 | Model created first try, layout corrupted |
| Claude | **Model OK** | 5 | Required iterative debugging, converged |
| Gemini | **FAILURE** | 9 | Diverged from correct solution, never converged |

## Common Failure Patterns

1. **Wrong imports:** `org.modelio.api.model` doesn't exist
2. **Encoding declarations:** Jython rejects `# -*- coding: utf-8 -*-`
3. **API method names:** `element.setLane()` doesn't exist, use `lane.getFlowElementRef().add()`
4. **Diagram creation:** Not via DiagramService, but via model factory
5. **Unmask return type:** Returns ArrayList, not single graphic
6. **Over-engineering:** Gemini tried complex reflection/factory patterns when simple `getModel().createX()` works

## Key Findings (Preliminary)

1. **Zero-shot generation fails 100%** — No model successfully generated working Modelio code without examples
2. **Examples help but not enough** — Even with examples, multiple debugging rounds needed
3. **API knowledge gap** — Models hallucinate plausible but incorrect API methods
4. **Convergence varies by model:**
   - GPT-5.2: Worked on first try with examples (best)
   - Claude: Converged after 5 rounds of debugging (good)
   - Gemini: Diverged after 9 rounds, never converged (failed)
5. **Model creation vs Layout are separate problems:**
   - Model creation: Achievable with examples + debugging (2/3 models)
   - Diagram layout: Broken even with correct coordinates (Modelio API issue)
   - Layout should be handled separately (auto-layout or manual)
6. **Debugging behavior matters:**
   - Some models learn from error messages and converge
   - Some models spiral into increasingly complex wrong solutions
   - Gemini tried reflection/factory patterns instead of simple `modelingSession.getModel().createX()`

---

## How this relates to the published benchmark

These preliminary tests inform but do **not** feed into any number in the
paper's evaluation tables. They exist to substantiate the qualitative
motivation described in paper §2.2 and §6.

| Aspect | Preliminary (this folder) | Published benchmark (`../runs/`) |
|---|---|---|
| Scenarios | 1 (S1, Simple) | 55 (PMo dataset) |
| LLMs | Claude Opus 4.5, GPT-5.2, Gemini Pro 3.1 | Claude Opus 4.5, GPT-5.2, GLM5 |
| Approach | One-shot direct generation only | Config+Helpers vs. No-Helper |
| Runs per cell | 1 + retries until budget exhausted | 1 (retries only for GLM5 syntax errors) |
| Paper section | §2.2 motivation, §6 lessons learned | §5 evaluation tables (Tables 1–5) |
