#
# VacationRequest.py
#
# Description: Vacation request process from employee submission through supervisor approval to HR processing
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "VacationRequest",
    
    "lanes": ["Employee", "Supervisor", "HR Representative"],
    
    "elements": [
        # Employee lane
        ("Start",                   START,        "Employee"),
        ("Submit Vacation Request", USER_TASK,    "Employee"),
        ("Review Rejection",        USER_TASK,    "Employee"),
        
        # Supervisor lane
        ("Receive Request",         USER_TASK,    "Supervisor"),
        ("Approved?",               EXCLUSIVE_GW, "Supervisor"),
        
        # HR Representative lane
        ("Receive Notification",    USER_TASK,    "HR Representative"),
        ("Complete HR Procedures",  USER_TASK,    "HR Representative"),
        ("End",                     END,          "HR Representative"),
    ],
    
    "flows": [
        ("Start",                   "Submit Vacation Request", ""),
        ("Submit Vacation Request", "Receive Request",         ""),
        ("Receive Request",         "Approved?",               ""),
        ("Approved?",               "Review Rejection",        "No"),
        ("Approved?",               "Receive Notification",    "Yes"),
        ("Review Rejection",        "Submit Vacation Request", ""),
        ("Receive Notification",    "Complete HR Procedures",  ""),
        ("Complete HR Procedures",  "End",                     ""),
    ],
    
    "layout": {
        "Start":                   0,
        "Submit Vacation Request": 1,
        "Receive Request":         2,
        "Approved?":               3,
        "Review Rejection":        4,
        "Receive Notification":    4,
        "Complete HR Procedures":  5,
        "End":                     6,
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
