#
# DismissalProcess.py
#
# Description: MPON sends a dismissal to MPOO, MPOO reviews and either opposes or confirms.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DismissalProcess",

    "lanes": ["MPON", "MPOO"],

    "elements": [
        ("Start",                 START,        "MPON"),
        ("Send dismissal",        SEND_TASK,    "MPON"),

        ("Review dismissal",      USER_TASK,    "MPOO"),
        ("Oppose or confirm?",    EXCLUSIVE_GW, "MPOO"),

        ("Oppose dismissal",      USER_TASK,    "MPOO"),
        ("Confirm dismissal",     USER_TASK,    "MPOO"),

        ("Merge",                 EXCLUSIVE_GW, "MPOO"),
        ("End",                   END,          "MPOO"),
    ],

    "flows": [
        ("Start",              "Send dismissal",     ""),
        ("Send dismissal",     "Review dismissal",   ""),
        ("Review dismissal",   "Oppose or confirm?", ""),

        ("Oppose or confirm?", "Oppose dismissal",   "Oppose"),
        ("Oppose or confirm?", "Confirm dismissal",  "Confirm"),

        ("Oppose dismissal",   "Merge",              ""),
        ("Confirm dismissal",  "Merge",              ""),

        ("Merge",              "End",                ""),
    ],

    "layout": {
        "Start":              0,
        "Send dismissal":     1,

        "Review dismissal":   2,
        "Oppose or confirm?": 3,

        # Same lane + same column => auto-stacked
        "Oppose dismissal":   4,
        "Confirm dismissal":  4,

        "Merge":              5,
        "End":                6,
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
