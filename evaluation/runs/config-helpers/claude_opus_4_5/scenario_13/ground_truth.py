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
        ("Resolve complaint", USER_TASK, "Process 1"),
        ("Approve and notify customer", USER_TASK, "Process 1"),
        ("Process reimbursement", USER_TASK, "Process 1"),
        ("Provide feedback", USER_TASK, "Process 1"),
        ("Log complaint", USER_TASK, "Process 1"),
        ("Assign complaint to relevant department", USER_TASK, "Process 1"),
        ("File complaint", USER_TASK, "Process 1"),
        ("Reject and notify customer", USER_TASK, "Process 1"),
        ("Review complaint details", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Start", "File complaint", ""),
        ("ExclusiveGateway_3", "Resolve complaint", ""),
        ("Resolve complaint", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_4", "Provide feedback", ""),
        ("ExclusiveGateway_1", "End", ""),
        ("ExclusiveGateway_4", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_2", "Approve and notify customer", ""),
        ("Reject and notify customer", "ExclusiveGateway_3", ""),
        ("Log complaint", "Assign complaint to relevant department", ""),
        ("Review complaint details", "ExclusiveGateway_2", ""),
        ("Provide feedback", "ExclusiveGateway_1", ""),
        ("File complaint", "Log complaint", ""),
        ("ExclusiveGateway_2", "Reject and notify customer", ""),
        ("Process reimbursement", "ExclusiveGateway_3", ""),
        ("Approve and notify customer", "Process reimbursement", ""),
        ("Assign complaint to relevant department", "Review complaint details", ""),
    ],

    "layout": {
        "Start": 0,
        "File complaint": 1,
        "Log complaint": 2,
        "Assign complaint to relevant department": 3,
        "Review complaint details": 4,
        "ExclusiveGateway_2": 5,
        "Approve and notify customer": 6,
        "Reject and notify customer": 6,
        "Process reimbursement": 7,
        "ExclusiveGateway_3": 8,
        "Resolve complaint": 9,
        "ExclusiveGateway_4": 10,
        "Provide feedback": 11,
        "ExclusiveGateway_1": 12,
        "End": 13,
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
