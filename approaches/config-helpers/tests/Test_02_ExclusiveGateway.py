#
# Test_02_ExclusiveGateway.py
#
# Description:
#   Test Case 2: Process with exclusive gateway and guards
#   Tests: EXCLUSIVE_GW, guards on flows, multiple end events
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Test02_ExclusiveGateway",
    
    "lanes": ["Handler"],
    
    "elements": [
        ("Start",        START,        "Handler"),
        ("Check Request", USER_TASK,   "Handler"),
        ("Valid?",       EXCLUSIVE_GW, "Handler"),
        ("Process Valid", USER_TASK,   "Handler"),
        ("Reject Invalid", USER_TASK,  "Handler"),
        ("End Success",  END,          "Handler"),
        ("End Rejected", END,          "Handler"),
    ],
    
    "flows": [
        ("Start",         "Check Request",  ""),
        ("Check Request", "Valid?",         ""),
        ("Valid?",        "Process Valid",  "Yes"),
        ("Valid?",        "Reject Invalid", "No"),
        ("Process Valid", "End Success",    ""),
        ("Reject Invalid", "End Rejected",  ""),
    ],
    
    "layout": {
        "Start":         0,
        "Check Request": 1,
        "Valid?":        2,
        "Process Valid": 3,
        "Reject Invalid": 3,
        "End Success":   4,
        "End Rejected":  4,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
