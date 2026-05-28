#
# DismissalReviewProcess.py
#
# Description: MSPN sends dismissal to MSPO for review, who either confirms or rejects it
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DismissalReviewProcess",
    
    "lanes": ["MSPN", "MSPO"],
    
    "elements": [
        # MSPN Lane
        ("Start",                   START,        "MSPN"),
        ("Send Dismissal",          SEND_TASK,    "MSPN"),
        
        # MSPO Lane
        ("Review Dismissal",        USER_TASK,    "MSPO"),
        ("Decision",                EXCLUSIVE_GW, "MSPO"),
        ("Reject Dismissal",        USER_TASK,    "MSPO"),
        ("Confirm Dismissal",       USER_TASK,    "MSPO"),
        ("End",                     END,          "MSPO"),
    ],
    
    "flows": [
        ("Start",             "Send Dismissal",    ""),
        ("Send Dismissal",    "Review Dismissal",  ""),
        ("Review Dismissal",  "Decision",          ""),
        ("Decision",          "Reject Dismissal",  "Rejected"),
        ("Decision",          "Confirm Dismissal", "Confirmed"),
        ("Reject Dismissal",  "End",               ""),
        ("Confirm Dismissal", "End",               ""),
    ],
    
    "layout": {
        "Start":             0,
        "Send Dismissal":    1,
        "Review Dismissal":  2,
        "Decision":          3,
        "Reject Dismissal":  4,    # Auto-stacked (same lane, same column)
        "Confirm Dismissal": 4,    # Automatically 90px below Reject Dismissal
        "End":               5,
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
