#
# DismissalReviewProcess.py
#
# Description: MPON sends dismissal to MPOO for review. MPOO either opposes or confirms the dismissal.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "DismissalReviewProcess",
    
    "lanes": ["MPON", "MPOO"],
    
    "elements": [
        ("Start",                START,        "MPON"),
        ("Send Dismissal",       SEND_TASK,    "MPON"),
        ("Review Dismissal",     USER_TASK,    "MPOO"),
        ("Decision?",            EXCLUSIVE_GW, "MPOO"),
        ("Oppose Dismissal",     USER_TASK,    "MPOO"),
        ("Confirm Dismissal",    USER_TASK,    "MPOO"),
        ("End Opposed",          END,          "MPOO"),
        ("End Confirmed",        END,          "MPOO"),
    ],
    
    "flows": [
        ("Start",             "Send Dismissal",    ""),
        ("Send Dismissal",    "Review Dismissal",  ""),
        ("Review Dismissal",  "Decision?",         ""),
        ("Decision?",         "Oppose Dismissal",  "Oppose"),
        ("Decision?",         "Confirm Dismissal", "Confirm"),
        ("Oppose Dismissal",  "End Opposed",       ""),
        ("Confirm Dismissal", "End Confirmed",     ""),
    ],
    
    "layout": {
        "Start":             0,
        "Send Dismissal":    1,
        "Review Dismissal":  2,
        "Decision?":         3,
        "Oppose Dismissal":  4,    # Auto-stacked with Confirm Dismissal
        "Confirm Dismissal": 4,    # Automatically 90px below Oppose Dismissal
        "End Opposed":       5,    # Auto-stacked with End Confirmed
        "End Confirmed":     5,    # Automatically 90px below End Opposed
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
