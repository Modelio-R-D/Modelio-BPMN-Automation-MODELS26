#
# Test_01_SimpleLinear.py
#
# Description:
#   Test Case 1: Simple linear process with 3 tasks
#   Tests: START, END, USER_TASK, basic flows
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Test01_SimpleLinear",
    
    "lanes": ["Clerk"],
    
    "elements": [
        ("Start",          START,     "Clerk"),
        ("Receive Request", USER_TASK, "Clerk"),
        ("Process Request", USER_TASK, "Clerk"),
        ("Send Response",   USER_TASK, "Clerk"),
        ("End",            END,       "Clerk"),
    ],
    
    "flows": [
        ("Start",           "Receive Request", ""),
        ("Receive Request", "Process Request", ""),
        ("Process Request", "Send Response",   ""),
        ("Send Response",   "End",             ""),
    ],
    
    "layout": {
        "Start":           0,
        "Receive Request": 1,
        "Process Request": 2,
        "Send Response":   3,
        "End":             4,
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
