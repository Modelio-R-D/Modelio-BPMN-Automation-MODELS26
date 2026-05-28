#
# DismissalProcess.py
#
# Description: MPON sends dismissal to MPOO for review and decision
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DismissalProcess",
    
    "lanes": ["MPON", "MPOO"],
    
    "elements": [
        ("Start",            START,         "MPON"),
        ("Send Dismissal",   SERVICE_TASK,  "MPON"),
        ("Review Dismissal", USER_TASK,     "MPOO"),
        ("Decision?",        EXCLUSIVE_GW,  "MPOO"),
        ("End Opposed",      END,           "MPOO"),
        ("End Confirmed",    END,           "MPOO"),
    ],
    
    "flows": [
        ("Start",            "Send Dismissal",   ""),
        ("Send Dismissal",   "Review Dismissal", ""),
        ("Review Dismissal", "Decision?",        ""),
        ("Decision?",        "End Opposed",     "Oppose"),
        ("Decision?",        "End Confirmed",   "Confirm"),
    ],
    
    "layout": {
        "Start":            0,
        "Send Dismissal":   1,
        "Review Dismissal": 2,
        "Decision?":        3,
        "End Opposed":      4,
        "End Confirmed":    4,
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
