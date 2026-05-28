#
# Dismissal_Process.py
#
# Description: MSPN sends a dismissal to MSPO, MSPO reviews and either rejects or confirms.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Dismissal_Process",

    "lanes": ["MSPN", "MSPO"],

    "elements": [
        ("Start",               START,        "MSPN"),
        ("Send dismissal",      SEND_TASK,    "MSPN"),

        ("Review dismissal",    USER_TASK,    "MSPO"),
        ("Reject or confirm?",  EXCLUSIVE_GW, "MSPO"),
        ("Reject dismissal",    USER_TASK,    "MSPO"),
        ("Confirm dismissal",   USER_TASK,    "MSPO"),
        ("End - Rejected",      END,          "MSPO"),
        ("End - Confirmed",     END,          "MSPO"),
    ],

    "flows": [
        ("Start",              "Send dismissal",      ""),
        ("Send dismissal",     "Review dismissal",    ""),
        ("Review dismissal",   "Reject or confirm?",  ""),
        ("Reject or confirm?", "Reject dismissal",    "Reject"),
        ("Reject or confirm?", "Confirm dismissal",   "Confirm"),
        ("Reject dismissal",   "End - Rejected",      ""),
        ("Confirm dismissal",  "End - Confirmed",     ""),
    ],

    "layout": {
        "Start":               0,
        "Send dismissal":      1,

        "Review dismissal":    2,
        "Reject or confirm?":  3,

        "Reject dismissal":    4,   # auto-stacked with "Confirm dismissal"
        "Confirm dismissal":   4,

        "End - Rejected":      5,   # auto-stacked with "End - Confirmed"
        "End - Confirmed":     5,
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
