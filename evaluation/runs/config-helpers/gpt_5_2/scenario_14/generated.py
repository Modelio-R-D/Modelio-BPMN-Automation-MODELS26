#
# DepartmentBudgetPlanning.py
#
# Description: Department creates a budget plan, undergoes strategic and finance reviews with iterative adjustments,
#              then final approval leads to allocation and distribution of budget for implementation.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DepartmentBudgetPlanning",

    "lanes": [
        "Department",
        "Strategy",
        "Finance",
        "Stakeholders",
    ],

    "elements": [
        ("Start",                         START,       "Department"),
        ("Outline Objectives",            USER_TASK,    "Department"),
        ("Draft Budget Plan",             USER_TASK,    "Department"),

        ("Strategic Alignment Review",    USER_TASK,    "Strategy"),
        ("Finance Detailed Review",       USER_TASK,    "Finance"),

        ("Changes Needed?",               EXCLUSIVE_GW, "Finance"),

        ("Revise Plan",                   USER_TASK,    "Department"),
        ("Document Adjustments",          USER_TASK,    "Department"),
        ("Approve Adjustments",           USER_TASK,    "Stakeholders"),

        ("Approve Final Budget",          USER_TASK,    "Stakeholders"),
        ("Allocate Budget",               USER_TASK,    "Finance"),
        ("Distribute Budget",             USER_TASK,    "Finance"),
        ("Begin Implementation",          USER_TASK,    "Department"),
        ("End",                           END,         "Department"),
    ],

    "flows": [
        ("Start",                      "Outline Objectives",         ""),
        ("Outline Objectives",         "Draft Budget Plan",          ""),
        ("Draft Budget Plan",          "Strategic Alignment Review", ""),
        ("Strategic Alignment Review", "Finance Detailed Review",    ""),

        ("Finance Detailed Review",    "Changes Needed?",            ""),

        ("Changes Needed?",            "Revise Plan",                "Yes"),
        ("Revise Plan",                "Document Adjustments",       ""),
        ("Document Adjustments",       "Approve Adjustments",        ""),
        ("Approve Adjustments",        "Strategic Alignment Review", "Resubmit"),

        ("Changes Needed?",            "Approve Final Budget",       "No"),
        ("Approve Final Budget",       "Allocate Budget",            ""),
        ("Allocate Budget",            "Distribute Budget",          ""),
        ("Distribute Budget",          "Begin Implementation",       ""),
        ("Begin Implementation",       "End",                        ""),
    ],

    "layout": {
        "Start":                      0,
        "Outline Objectives":         1,
        "Draft Budget Plan":          2,
        "Strategic Alignment Review": 3,
        "Finance Detailed Review":    4,
        "Changes Needed?":            5,

        "Revise Plan":                6,
        "Document Adjustments":       7,
        "Approve Adjustments":        8,

        "Approve Final Budget":       6,
        "Allocate Budget":            7,
        "Distribute Budget":          8,
        "Begin Implementation":       9,
        "End":                        10,
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
