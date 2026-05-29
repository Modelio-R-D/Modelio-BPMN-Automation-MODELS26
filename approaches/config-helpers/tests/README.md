# Helper-library tests

Feature-level test cases for [`BPMN_Helpers.py`](../BPMN_Helpers.py).
Each `Test_NN_*.py` exercises one isolated capability — they are intended
to be pasted into Modelio's script panel and run individually.

| File                             | Exercises                                  |
|----------------------------------|--------------------------------------------|
| `Test_01_SimpleLinear.py`        | Two-lane linear sequence                   |
| `Test_02_ExclusiveGateway.py`    | XOR decision gateway                       |
| `Test_03_ParallelGateway.py`     | Parallel split/join                        |
| `Test_04_TimerMessageEvents.py`  | Timer and message events                   |
| `Test_05_DataObjects.py`         | Data object association rules              |

`test_prompts.md` contains complexity-graded prompts for stress-testing
the LLM generation step. These are independent from — and pre-date — the
PMo benchmark in [`../../../evaluation/`](../../../evaluation/).
