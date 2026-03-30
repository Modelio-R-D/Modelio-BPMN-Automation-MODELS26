# Modelio BPMN Generator with Claude, ChatGPT, Gemini AI or Local LLM

Generate BPMN (Business Process Model and Notation) diagrams in [Modelio](https://www.modelio.org/) using AI. Describe your business process in plain language and get a complete, runnable Modelio macro.

![BPMN Example](docs/images/expense-approval-example.png)

## For Researchers & Reproducibility

This repository is the open-source artifact accompanying the MODELS '26 paper:
**"Towards LLM-Assisted Business Process Modeling in an Industrial Modeling Tool: An Experience Report"**

The evaluation data and results are in the [`Evaluation/`](Evaluation/) folder:

| File | Content |
|------|---------|
| [`Evaluation/Eval.md`](Evaluation/Eval.md) | Full evaluation results : MATISSE industrial validation (24 scenarios, 7 partners) and controlled benchmark (55 PMo scenarios, 3 LLMs) with all paper tables |
| [`Evaluation/Evals.ipynb`](Evaluation/Evals.ipynb) | Jupyter notebook that loads the JSONL experiment data and reproduces all paper tables |
| [`Evaluation/output/exp_config_helper/`](Evaluation/output/exp_config_helper/) | Raw JSONL data for the Config+Helpers experiment (Claude Opus 4.5, GPT-5.2, GLM5) |
| [`Evaluation/output/exp_no_helper/`](Evaluation/output/exp_no_helper/) | Raw JSONL data for the No-Helper experiment (Claude Opus 4.5, GPT-5.2, GLM5) |

---
## Overview

This project enables you to:

- **Describe a business process in plain language** and have Claude, ChatGPT, or Gemini generate the Modelio macro
- **Automatically create BPMN diagrams** with lanes, tasks, gateways, data objects, and flows
- **Customize layout** with configurable spacing, task dimensions, and positioning

## Features

- ✅ Support for all common BPMN elements (Start/End Events, User/Service/Manual Tasks, Gateways)
- ✅ **Data Objects** with input/output associations to tasks
- ✅ Automatic swim lane creation and element positioning
- ✅ Sequence flows with labels for gateway decisions
- ✅ Configurable task dimensions and spacing
- ✅ Robust element unmasking with fallback mechanisms
- ✅ Two-file architecture for faster, more reliable AI generation
- ✅ **NEW: Auto-stacking** - Same lane + same column elements automatically stacked (v3.2)
- ✅ Export/Import - Clone or migrate existing diagrams between projects
- ✅ Extended element types - Script, Business Rule, Send/Receive tasks, additional gateways and events

## Requirements

- [Modelio](https://www.modelio.org/) 5.0 or later
- Access to [Claude](https://claude.ai/), [ChatGPT](https://chat.openai.com/) with GPT-4o, or [Gemini](https://gemini.google.com/)
- Also works with Qwen via LM Studio—see the guide [here](lm_studio/LMStudio_Qwen_Guide_v5_Final.md)

---

## Quick Start

### 1. Install the Helper Library (One Time)

Copy [`BPMN_Helpers.py`](BPMN_Helpers.py) to your Modelio macros folder:

| OS | Path |
|----|------|
| Windows (workaround) | `C:\<your Modelio installation folder>\.modelio\5.4\macros\BPMN_Helpers.py` |
| Linux | `~/.modelio/5.4/macros/BPMN_Helpers.py` |

> Replace `5.4` with your Modelio version. Create the `macros` folder if it doesn't exist.

### 2. Set Up Your AI Assistant

Copy the contents of [`CLAUDE_INSTRUCTIONS.md`](CLAUDE_INSTRUCTIONS.md) into:

| AI | How to Set Up |
|----|---------------|
| **Claude** | Create a Project → Add as custom instructions |
| **ChatGPT** | Add to Custom Instructions or first system message |
| **Gemini** | Add as system/developer message |
| **LM Studio + Qwen** | See [`lm_studio/LMStudio_Qwen_with_helpers.md`](lm_studio/LMStudio_Qwen_with_helpers.md) |

**Tip for ChatGPT/Gemini:** Start with: *"You are generating Modelio Jython BPMN macros. Follow these instructions exactly."*

### 3. Describe Your Process

Tell the AI what you need:

```
Create a BPMN diagram for an expense approval process with 3 lanes: 
Employee, Manager, and Finance. 

The employee submits an expense report, the manager reviews and 
approves or rejects it, and finance processes the payment.
```

### 4. Run in Modelio

1. Copy the generated Python script
2. Open Modelio and select a **Package** in the model explorer
3. Go to **Views → Script**
4. Paste the script and click **Run**

Your BPMN diagram will appear automatically!

---

## Project Structure

```
Modelio-Automation/
├── README.md                 # This file
├── BPMN_Helpers.py           # Helper library (install to Modelio)
├── BPMN_Export.py            # Export macro (install to Modelio) - NEW in v3.x
├── CLAUDE_INSTRUCTIONS.md    # AI instructions for macro generation
├── docs/
│   ├── QUICK_START.md        # Detailed setup guide
│   ├── API_REFERENCE.md      # Configuration options
│   ├── APPROACHES.md         # Architecture comparison
│   └── images/
├── examples/
│   └── ExpenseApprovalProcess.py
├── lm_studio/
│    └── LMStudio_Qwen_Guide_with_helpers.md
├── Evaluation/       # Evaluation data, results and analysis for the paper
│   ├── Eval.md               # Evaluation methodology, metrics, and all results tables
│   ├── Evals.ipynb           # Main analysis notebook
│   └── output/
│       ├── exp_config_helper/   # Config+Helpers experiment JSONL data
│       │   ├── generated_configs_modelio_claude_opus_4_5.jsonl
│       │   ├── generated_configs_helper_GPT_5_2_modelio.jsonl
│       │   └── generated_configs_helper_GLM5_modelio.jsonl
│       └── exp_no_helper/       # No-Helper (direct native) experiment JSONL data
│           ├── generated_configs_no_helper_claude_opus_4_5_modelio.jsonl
│           ├── generated_configs_no_helper_gpt_5_2_modelio.jsonl
│           └── generated_configs_no_helper_GLM5_modelio.jsonl
└── v1/                       # Previous single-file version with examples
```

---

## How It Works

### Two-File Architecture

```
┌────────────────────────────────┐
│  BPMN_Helpers.py               │  ← Install once in Modelio
│  (500+ lines of tested code)   │
└────────────────────────────────┘
              ▲
              │ execfile()
              │
┌────────────────────────────────┐
│  YourProcess.py                │  ← AI generates this (~100 lines)
│  (Pure configuration)          │
└────────────────────────────────┘
```

**Benefits:**
- ⚡ **Fast generation** - AI only generates configuration, not 500+ lines of helpers
- ✅ **Reliable** - Helper code is tested; only config varies
- 🔧 **Maintainable** - Fix bugs once in helper library
- 📖 **Readable** - Process structure is clear and declarative

### Generated Configuration Format

```python
CONFIG = {
    "name": "ExpenseApproval",
    "lanes": ["Employee", "Manager", "Finance"],
    "elements": [
        ("Submit Expense", START, "Employee"),
        ("Review", USER_TASK, "Manager"),
        ("Approved?", EXCLUSIVE_GW, "Manager"),
        ("Process Payment", SERVICE_TASK, "Finance"),
        ("Rejected", END, "Manager"),
        # ...
    ],
    "flows": [
        ("Submit Expense", "Review", ""),
        ("Approved?", "Process Payment", "Yes"),
        ("Approved?", "Rejected", "No"),
    ],
    "layout": {
        "Submit Expense": 0,
        "Review": 1,
        "Approved?": 2,
        "Process Payment": 3,    # Same column = auto-stacked (v3.2)
        "Rejected": 3,           # Automatically 90px below
        # ...
    },
    # Optional: Data Objects
    "data_objects": [
        ("Expense Report", "Employee", 0),
    ],
    "data_associations": [
        ("Submit Expense", "Expense Report"),
        ("Expense Report", "Review"),
    ],
}
```

### Modelio Auto-Unmask Behavior

When a BPMN diagram is created, Modelio automatically "unmasks" elements. However:

- Auto-unmask is **non-deterministic** - sometimes all elements appear, sometimes only some
- The helper library handles this with automatic fallback to manual unmasking
- Manual unmask is done at the correct Y position inside each lane

---

## Available BPMN Elements

| Type | Constant | Icon | Description |
|------|----------|------|-------------|
| Start Event | `START` | ○ | Process start (green circle) |
| End Event | `END` | ◉ | Process end (red circle) |
| Message Start | `MESSAGE_START` | ✉○ | Triggered by message |
| Message End | `MESSAGE_END` | ✉◉ | Sends message on completion |
| Timer Start | `TIMER_START` | ⏱○ | Triggered by schedule |
| Signal Start | `SIGNAL_START` | ○ | Triggered by signal |
| Conditional Start | `CONDITIONAL_START` | ○ | Triggered by condition |
| Signal End | `SIGNAL_END` | ◉ | Sends signal on completion |
| Terminate End | `TERMINATE_END` | ◉ | Terminates all instances |
| Error End | `ERROR_END` | ◉ | Throws error |
| Intermediate Catch | `INTERMEDIATE_CATCH` | ◎ | Generic catch event |
| Intermediate Throw | `INTERMEDIATE_THROW` | ◎ | Generic throw event |
| Message Catch | `MESSAGE_CATCH` | ✉◎ | Wait for message |
| Message Throw | `MESSAGE_THROW` | ✉◎ | Send message |
| Timer Catch | `TIMER_CATCH` | ⏱◎ | Wait for timer |
| Signal Catch | `SIGNAL_CATCH` | ◎ | Wait for signal |
| Signal Throw | `SIGNAL_THROW` | ◎ | Send signal |
| User Task | `USER_TASK` | 👤▭ | Human activity with IT system |
| Manual Task | `MANUAL_TASK` | ✋▭ | Physical task without IT |
| Service Task | `SERVICE_TASK` | ⚙▭ | Automated/system task |
| Script Task | `SCRIPT_TASK` | ▭ | Script execution task |
| Business Rule Task | `BUSINESS_RULE_TASK` | ▭ | Business rule evaluation |
| Send Task | `SEND_TASK` | ▭ | Send message task |
| Receive Task | `RECEIVE_TASK` | ▭ | Receive message task |
| Generic Task | `TASK` | ▭ | Generic task |
| Exclusive Gateway | `EXCLUSIVE_GW` | ◇ | XOR decision (one path) |
| Parallel Gateway | `PARALLEL_GW` | ⊕ | AND split/join (all paths) |
| Inclusive Gateway | `INCLUSIVE_GW` | ◇ | OR decision (one or more paths) |
| Complex Gateway | `COMPLEX_GW` | ◇ | Complex routing logic |
| Event-Based Gateway | `EVENT_BASED_GW` | ◇ | Wait for event |
| Data Object | `DATA_OBJECT` | 📄 | Document or data in process |

---

## Configuration Options

```python
CONFIG = {
    # Required
    "name": "ProcessName",
    "lanes": [...],
    "elements": [...],
    "flows": [...],
    "layout": {...},
    
    # Optional - Data Objects (v2.1+)
    "data_objects": [...],      # List of (name, lane, column)
    "data_associations": [...], # List of (source, target)
    
    # Optional - Layout Settings (with defaults)
    "SPACING": 150,        # Horizontal spacing between columns
    "START_X": 80,         # Starting X position
    "TASK_WIDTH": 120,     # Width for task elements
    "TASK_HEIGHT": 60,     # Height for task elements
    "DATA_WIDTH": 40,      # Width for data objects
    "DATA_HEIGHT": 50,     # Height for data objects
    "DATA_OFFSET_X": 90,   # Data object X offset (near right side of task)
    "DATA_OFFSET_Y": 10,   # Data object Y gap below source task
    "WAIT_TIME_MS": 50,    # Time between unmask attempts
    "MAX_ATTEMPTS": 3,     # Maximum unmask attempts
}
```

### Data Objects Configuration

```python
# Format: (name, lane, column)
"data_objects": [
    ("Draft Document", "Author", 1),
    ("Final Report", "Reviewer", 3),
]
```

### Data Associations Configuration

```python
# Format: (source, target) - direction is auto-detected
"data_associations": [
    ("Write Document", "Draft Document"),  # Task → Data (task produces data)
    ("Draft Document", "Review Task"),     # Data → Task (task consumes data)
]
```

---

## Example Output

Running the ExpenseApprovalProcess example produces:

```
==================================================================
BPMN PROCESS CREATION
==================================================================
Process Name: ExpenseApproval_83950

== PHASE 1: CREATE PROCESS & LANES ==============================
[1] Process: ExpenseApproval_83950
[2] Lanes: Employee, Manager, Finance

== PHASE 2: CREATE ELEMENTS =====================================
[3] Employee: 7 elements
[4] Manager: 5 elements
[5] Finance: 7 elements
  Total: 19 elements

== PHASE 4: WAIT FOR AUTO-UNMASK ================================
  [Attempt 1] Found: 7/19 | Missing: Review Expense...
  [Unmask] Review Expense -> Y=161 (Manager): OK
  ...

== PHASE 5: REPOSITION ELEMENTS =================================
  Repositioned: 19/19

== PHASE 6: CREATE FLOWS ========================================
  Created 20 sequence flows

== PHASE 7: CREATE DATA OBJECTS =================================
  Created 2 data objects

== PHASE 8: CREATE DATA ASSOCIATIONS ============================
  Created 4 data associations

==================================================================
COMPLETE
==================================================================
```

---

## Tips for Better AI Results

| Tip | Example |
|-----|---------|
| Name lanes clearly | "Lanes: Customer, Sales Team, Warehouse" |
| Describe decisions explicitly | "If approved, proceed; otherwise reject" |
| Mention parallel work | "HR and IT work in parallel" |
| Specify task types | "automated email" → Service Task |
| Include error paths | "If validation fails, return to customer" |
| Mention documents/data | "produces an invoice" → Data Object |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No such file" error | Check `BPMN_Helpers.py` path matches your Modelio version |
| Script doesn't run | Select a **Package** before running |
| UnicodeDecodeError | Use ASCII only - no special characters like ✓ or → |
| Element in wrong lane | Check lane name spelling (case-sensitive) |
| Elements overlap | Increase `SPACING` or adjust column indices in layout |
| Text doesn't fit | Increase `TASK_WIDTH` and `TASK_HEIGHT` |
| Diagram is empty | Wait and refresh; check model tree for the process |
| Data object overlaps task | Adjust `DATA_OFFSET_Y` configuration |
| Data association arrow wrong | Verify source and target order |

---

## Documentation

- [Quick Start Guide](docs/QUICK_START.md) - Detailed setup walkthrough
- [API Reference](docs/API_REFERENCE.md) - All configuration options
- [Approaches Comparison](docs/APPROACHES.md) - Architecture details

---

## Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

---

## Acknowledgments

- [Modelio](https://www.modelio.org/) - Open source modeling environment
- [Anthropic Claude](https://www.anthropic.com/) - AI assistant for code generation
- Modelio development team for insights on auto-unmask behavior
- [MATISSE](https://matisse-kdt.eu/) - Project co-funded by the European Union under the Key Digital Technologies Joint Undertaking and participating national authorities (Grant Agreement ID: 101140216)

---

## Version History

- **v3.2** (Dec 2025) - Auto-stacking for same-lane/same-column elements (90px spacing)
- **v3.1** (Dec 2025) - Fixed data association export, Y-offset layout support, data objects below source task
- **v3.0** (Dec 2025) - Export/Import feature, lane-relative positioning, extended element types
- **v2.5** (Dec 2025) - Clarified BPMN rules - Events CAN have data associations, Gateways CANNOT
- **v2.4** (Dec 2025) - Simplified data objects by removing position parameter (always below)
- **v2.3** (Dec 2025) - Simplified data associations by auto-detecting direction
- **v2.2** (Dec 2025) - Fixed Data Association semantics, lane-by-lane data object positioning
- **v2.1** (Dec 2025) - Added Data Objects and Data Associations support
- **v2.0** (Dec 2025) - Two-file architecture with helper library
- **v1.0** (Dec 2025) - Single-file approach with inline helpers

### Previous Single-File Versions
- v0.9.1 - Guards for gateway conditions
- v0.9.0 - Configurable task dimensions
- v0.8.3 - Manual unmask inside correct lane Y position
- v0.8.0 - Auto-unmask discovery and waiting mechanism

---

## License

Apache License 2.0 - See [LICENSE](LICENSE)
