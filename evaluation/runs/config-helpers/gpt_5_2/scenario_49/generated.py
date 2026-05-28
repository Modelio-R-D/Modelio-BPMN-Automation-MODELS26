#
# ComputerRepairProcess.py
#
# Description: Customer brings defective computer, CRS provides cost estimate, customer accepts/rejects.
# If accepted, hardware and software repair are performed in arbitrary order, each followed by a test.
# On detected error, repair work is repeated; otherwise the computer is returned.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ComputerRepairProcess",

    "lanes": ["Customer", "CRS", "Workshop"],

    "elements": [
        ("Start",                          START,         "Customer"),
        ("Bring defective computer",       USER_TASK,     "Customer"),

        ("Check defect",                   USER_TASK,     "CRS"),
        ("Calculate repair cost",          SERVICE_TASK,  "CRS"),
        ("Provide cost estimate",          USER_TASK,     "CRS"),

        ("Decide on costs",                USER_TASK,     "Customer"),
        ("Costs acceptable?",              EXCLUSIVE_GW,  "Customer"),

        ("Take computer home unrepaired",  MANUAL_TASK,   "Customer"),
        ("End (unrepaired)",               END,           "Customer"),

        ("Start repair (any order)",       PARALLEL_GW,   "Workshop"),

        ("Repair hardware",                MANUAL_TASK,   "Workshop"),
        ("Test after hardware",            SERVICE_TASK,  "Workshop"),
        ("Error after hardware?",          EXCLUSIVE_GW,  "Workshop"),

        ("Configure software",             SERVICE_TASK,  "Workshop"),
        ("Test after software",            SERVICE_TASK,  "Workshop"),
        ("Error after software?",          EXCLUSIVE_GW,  "Workshop"),

        ("Repair complete",                PARALLEL_GW,   "Workshop"),

        ("Hand over repaired computer",    USER_TASK,     "CRS"),
        ("Receive repaired computer",      USER_TASK,     "Customer"),
        ("End (repaired)",                 END,           "Customer"),
    ],

    "flows": [
        ("Start",                    "Bring defective computer",      ""),
        ("Bring defective computer", "Check defect",                  ""),
        ("Check defect",             "Calculate repair cost",         ""),
        ("Calculate repair cost",    "Provide cost estimate",         ""),
        ("Provide cost estimate",    "Decide on costs",               ""),
        ("Decide on costs",          "Costs acceptable?",             ""),

        ("Costs acceptable?",        "Take computer home unrepaired", "No"),
        ("Take computer home unrepaired", "End (unrepaired)",         ""),

        ("Costs acceptable?",        "Start repair (any order)",      "Yes"),

        # Parallel repair activities (arbitrary order)
        ("Start repair (any order)", "Repair hardware",               ""),
        ("Start repair (any order)", "Configure software",            ""),

        ("Repair hardware",          "Test after hardware",           ""),
        ("Test after hardware",      "Error after hardware?",         ""),
        ("Error after hardware?",    "Start repair (any order)",      "Error"),
        ("Error after hardware?",    "Repair complete",               "OK"),

        ("Configure software",       "Test after software",           ""),
        ("Test after software",      "Error after software?",         ""),
        ("Error after software?",    "Start repair (any order)",      "Error"),
        ("Error after software?",    "Repair complete",               "OK"),

        ("Repair complete",          "Hand over repaired computer",   ""),
        ("Hand over repaired computer", "Receive repaired computer",  ""),
        ("Receive repaired computer","End (repaired)",                ""),
    ],

    "layout": {
        "Start":                          0,
        "Bring defective computer":       1,

        "Check defect":                   2,
        "Calculate repair cost":          3,
        "Provide cost estimate":          4,

        "Decide on costs":                5,
        "Costs acceptable?":              6,

        "Take computer home unrepaired":  7,
        "End (unrepaired)":               8,

        "Start repair (any order)":       7,

        # Same lane + same column = auto-stacked (v3.2)
        "Repair hardware":                8,
        "Configure software":             8,

        "Test after hardware":            9,
        "Test after software":            9,

        "Error after hardware?":          10,
        "Error after software?":          10,

        "Repair complete":                11,

        "Hand over repaired computer":    12,
        "Receive repaired computer":      13,
        "End (repaired)":                 14,
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
