# Quick Start Guide

Create your first BPMN diagram using AI and Modelio in under 10 minutes.

## Prerequisites

- **Modelio 5.0+** installed ([download](https://www.modelio.org/downloads.html))
- Access to **Claude** ([claude.ai](https://claude.ai)) or another AI assistant

---

## Step 1: Set Up Your AI Assistant

### Option A: Claude Projects (Recommended)

1. Go to [claude.ai](https://claude.ai) and click **Projects** in the sidebar
2. Create a new project (e.g., "Modelio BPMN")
3. In project settings, click **Add files**
4. Upload this file into it:
   - [`approaches/config-helpers/system_prompt.md`](../approaches/config-helpers/system_prompt.md)

### Option B: Other AI Assistants

Attach the same file to your conversation or paste its contents as context.

---

## Step 2: Install the Helper Library (One Time)

Copy [`approaches/config-helpers/BPMN_Helpers.py`](../approaches/config-helpers/BPMN_Helpers.py) to your Modelio macros folder:

| OS | Path |
|----|------|
| Windows (workaround) | `C:\<your Modelio installation folder>\.modelio\5.4\macros\BPMN_Helpers.py` |
| Linux | `~/.modelio/5.4/macros/BPMN_Helpers.py` |

> **Note**: Replace `5.4` with your Modelio version. Create the `macros` folder if it doesn't exist.

---

## Step 3: Describe Your Process to Claude

Start a conversation in your Claude project and describe your business process:

```
Create a BPMN diagram for an order fulfillment process:

Lanes:
- Customer
- Sales  
- Warehouse

Process:
1. Customer places an order
2. Sales receives and validates the order
3. If valid, Sales confirms; if invalid, Sales rejects
4. Warehouse picks and ships items
5. Customer receives delivery
```

Claude will generate a Jython script (Modelio macro) that creates the BPMN diagram. Copy the generated script to your clipboard.

---

## Step 4: Run the Macro in Modelio

Once you have opened Modelio and created or opened a project:
1. **Select a Package** in the model explorer
   - If you don't have one: Right-click root → Create element → Package
2. Go to **Views → Script** to display the Script view, then paste the generated Jython script.
3. Click **Run** (play button)

![modelio script](images/modelio_script.png)
---

## Step 5: View Your Diagram

1. Expand your package in the model explorer
2. Find the new process (named like `OrderFulfillment_12345`)
3. Double-click the process diagram to open it
4. Your BPMN diagram is ready!

---

## Customization

### Adjust Element Sizes

Edit the configuration section in generated scripts:

```python
CONFIG = {
    "TASK_WIDTH": 140,   # Wider tasks for longer labels
    "TASK_HEIGHT": 70,   # Taller tasks
    "SPACING": 180,      # More horizontal space
    # ...
}
```

### Change Element Positions

Modify column indices in the `layout` section:

```python
"layout": {
    "Place Order": 0,        # First column
    "Validate Order": 1,     # Second column
    "Ship Items": 3,         # Skip column 2 for visual spacing
}
```

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No such file" error | Check that `BPMN_Helpers.py` path matches your Modelio version |
| Script doesn't run | Make sure you selected a **Package** before running |
| Diagram is empty | Wait a moment and refresh; check the model tree for the process |
| Elements overlap | Adjust column indices in the `layout` section |
| Unicode/encoding errors | Ensure script uses only ASCII characters |
| Text cut off | Increase `TASK_WIDTH` and `TASK_HEIGHT` |

### Check the Console

The script outputs diagnostic information. Go to **Views → Console** to see:

```
==================================================================
BPMN PROCESS CREATION
==================================================================
Process Name: OrderFulfillment_12345
...
[3] Customer: 2 elements
[4] Sales: 3 elements
...
```

---

## Tips for Better AI Results

| Tip | Example |
|-----|---------|
| Name your lanes clearly | "Lanes: Customer, Sales Team, Warehouse Staff" |
| Describe decisions explicitly | "If order is valid, confirm it; otherwise reject it" |
| Mention parallel work | "While Warehouse picks items, Sales notifies customer" |
| Specify task types | "automated email notification" → Service Task |
| Include error handling | "If shipping fails, notify Sales" |

---

## Example Prompts

### Simple Approval

```
Create a document approval process with:
- Lanes: Author, Reviewer, Manager
- Author submits document
- Reviewer checks it
- If OK, Manager approves; if not, Author revises
```

### Parallel Processing

```
Create an employee onboarding process:
- Lanes: HR, IT, New Employee
- HR and IT work in parallel after employee is hired
- HR handles paperwork while IT sets up accounts
- New Employee completes orientation after both finish
```

### Complex Flow with Loops

```
Create a customer support ticket process:
- Lanes: Customer, Agent, Specialist
- Customer submits ticket
- Agent triages: simple issues handled directly, complex go to Specialist
- If customer not satisfied, reopen ticket
- Track resolution with a final confirmation
```

---

## Next Steps

- See [`approaches/config-helpers/examples/`](../approaches/config-helpers/examples/) for complete working macros
- Read [`approaches/config-helpers/system_prompt.md`](../approaches/config-helpers/system_prompt.md) for all supported BPMN elements
- Check [`approaches/config-helpers/docs/API_REFERENCE.md`](../approaches/config-helpers/docs/API_REFERENCE.md) for configuration options

---

## Quick Reference: Element Types

| Type | Use For |
|------|---------|
| `START` | Process begins |
| `END` | Process ends |
| `USER_TASK` | Human work with IT system |
| `SERVICE_TASK` | Automated/system task |
| `MANUAL_TASK` | Physical work without IT |
| `EXCLUSIVE_GW` | XOR decision (one path) |
| `PARALLEL_GW` | Fork/join (all paths) |
| `MESSAGE_START` | Triggered by message |
| `MESSAGE_END` | Sends message on completion |
| `TIMER_START` | Triggered by schedule |