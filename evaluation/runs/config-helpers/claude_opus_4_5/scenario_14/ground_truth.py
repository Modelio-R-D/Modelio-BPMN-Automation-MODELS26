#
# Process_1.py
#
# Auto-generated from BPMN XML: Process_1
# Compatible with BPMN_Helpers.py v3.2
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Implement plan", USER_TASK, "Process 1"),
        ("Approve final budget", USER_TASK, "Process 1"),
        ("Provide feedback", USER_TASK, "Process 1"),
        ("Distribute budget", USER_TASK, "Process 1"),
        ("Outline objectives", USER_TASK, "Process 1"),
        ("Draft plan", USER_TASK, "Process 1"),
        ("Documented and approve adjustment", USER_TASK, "Process 1"),
        ("Review budget feasibility", USER_TASK, "Process 1"),
        ("Adjust Plan", USER_TASK, "Process 1"),
        ("Conduct strategic alignment meeting", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Conduct strategic alignment meeting", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Review budget feasibility", ""),
        ("Documented and approve adjustment", "ExclusiveGateway_2", ""),
        ("Outline objectives", "Draft plan", ""),
        ("Implement plan", "End", ""),
        ("Provide feedback", "ExclusiveGateway_1", ""),
        ("Distribute budget", "Implement plan", ""),
        ("Adjust Plan", "Documented and approve adjustment", ""),
        ("ExclusiveGateway_1", "Approve final budget", ""),
        ("Review budget feasibility", "Provide feedback", ""),
        ("ExclusiveGateway_1", "Adjust Plan", ""),
        ("Approve final budget", "Distribute budget", ""),
        ("Draft plan", "Conduct strategic alignment meeting", ""),
        ("Start", "Outline objectives", ""),
    ],

    "layout": {
        "Start": 0,
        "Outline objectives": 1,
        "Draft plan": 2,
        "Conduct strategic alignment meeting": 3,
        "Review budget feasibility": 5,
        "Provide feedback": 6,
        "ExclusiveGateway_1": 7,
        "Approve final budget": 8,
        "Adjust Plan": 8,
        "Distribute budget": 9,
        "Documented and approve adjustment": 9,
        "ExclusiveGateway_2": 10,
        "Implement plan": 10,
        "End": 11,
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
