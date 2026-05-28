#
# VacationRequestProcess.py
#
# Description: BPMN process for submitting, approving/rejecting, and processing a vacation request.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Vacation Request Process",

    "lanes": [
        "Employee",
        "Supervisor",
        "Human Resources"
    ],

    "elements": [
        ("Start",                        START,         "Employee"),
        ("Submit Vacation Request",      USER_TASK,     "Employee"),

        ("Receive Request",              USER_TASK,     "Supervisor"),
        ("Approve Request?",             EXCLUSIVE_GW,  "Supervisor"),

        ("Return Rejection to Employee", SEND_TASK,     "Supervisor"),
        ("Notify HR (Approved)",         SEND_TASK,     "Supervisor"),

        ("Review Rejection Reasons",     USER_TASK,     "Employee"),
        ("Complete HR Procedures",       USER_TASK,     "Human Resources"),

        ("End (Rejected)",               END,           "Employee"),
        ("End (Approved)",               END,           "Human Resources"),
    ],

    "flows": [
        ("Start",                   "Submit Vacation Request",      ""),
        ("Submit Vacation Request", "Receive Request",              ""),

        ("Receive Request",         "Approve Request?",             ""),

        ("Approve Request?",        "Return Rejection to Employee", "Rejected"),
        ("Approve Request?",        "Notify HR (Approved)",         "Approved"),

        ("Return Rejection to Employee", "Review Rejection Reasons", ""),
        ("Review Rejection Reasons",     "End (Rejected)",           ""),

        ("Notify HR (Approved)",    "Complete HR Procedures",       ""),
        ("Complete HR Procedures",  "End (Approved)",               ""),
    ],

    "layout": {
        "Start":                        0,
        "Submit Vacation Request":      1,

        "Receive Request":              2,
        "Approve Request?":             3,

        # Same lane + same column => auto-stacked (v3.2)
        "Return Rejection to Employee": 4,
        "Notify HR (Approved)":         4,

        "Review Rejection Reasons":     5,
        "Complete HR Procedures":       5,

        "End (Rejected)":               6,
        "End (Approved)":               6,
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
