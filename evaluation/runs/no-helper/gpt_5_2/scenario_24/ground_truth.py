#
# Process_1.py
#
# Auto-generated from BPMN XML: Process_1
# Compatible with BPMN_Helpers.py v3.2
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Enter restaurant", USER_TASK, "Process 1"),
        ("Choose dish", USER_TASK, "Process 1"),
        ("Place order", USER_TASK, "Process 1"),
        ("Pay money", USER_TASK, "Process 1"),
        ("Take buzzer", USER_TASK, "Process 1"),
        ("Get meal", USER_TASK, "Process 1"),
        ("Eat meal", USER_TASK, "Process 1"),
        ("Hunger noticed", CONDITIONAL_START, "Process 1"),
        ("Not hungry anymore", END, "Process 1"),
        ("wait for turn", INTERMEDIATE_CATCH, "Process 1"),
        ("Meal ready", MESSAGE_CATCH, "Process 1"),
    ],

    "flows": [
        ("Hunger noticed", "Enter restaurant", ""),
        ("Enter restaurant", "Choose dish", ""),
        ("Choose dish", "wait for turn", ""),
        ("wait for turn", "Place order", ""),
        ("Place order", "Pay money", ""),
        ("Pay money", "Take buzzer", ""),
        ("Take buzzer", "Meal ready", ""),
        ("Meal ready", "Get meal", ""),
        ("Get meal", "Eat meal", ""),
        ("Eat meal", "Not hungry anymore", ""),
    ],

    "layout": {
        "Hunger noticed": 0,
        "Enter restaurant": 1,
        "Choose dish": 2,
        "wait for turn": 3,
        "Place order": 4,
        "Pay money": 5,
        "Take buzzer": 6,
        "Meal ready": 7,
        "Get meal": 8,
        "Eat meal": 9,
        "Not hungry anymore": 10,
    },
}

# Entry point
if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
