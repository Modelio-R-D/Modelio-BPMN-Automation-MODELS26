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
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Claim is registered", USER_TASK, "Process 1"),
        ("Claim is examined by a claims officer", USER_TASK, "Process 1"),
        ("Claims officer writes a settlement recommendation", USER_TASK, "Process 1"),
        ("Recommendation is checked by a senior claims officer", USER_TASK, "Process 1"),
        ("Senior claims officer marks the claim", USER_TASK, "Process 1"),
        ("Claim is sent back", USER_TASK, "Process 1"),
        ("Claim handling process proceeds", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "Claim is registered", ""),
        ("Claim is registered", "Claim is examined by a claims officer", ""),
        ("Claims officer writes a settlement recommendation", "Recommendation is checked by a senior claims officer", ""),
        ("Recommendation is checked by a senior claims officer", "Senior claims officer marks the claim", ""),
        ("Senior claims officer marks the claim", "ExclusiveGateway_1", ""),
        ("Claim is examined by a claims officer", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Claims officer writes a settlement recommendation", ""),
        ("Claim is sent back", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_1", "Claim handling process proceeds", "OK"),
        ("ExclusiveGateway_1", "Claim is sent back", "Not OK"),
        ("Claim handling process proceeds", "EndEvent_1", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Claim is registered": 1,
        "Claim is examined by a claims officer": 2,
        "Claims officer writes a settlement recommendation": 4,
        "Recommendation is checked by a senior claims officer": 5,
        "Senior claims officer marks the claim": 6,
        "ExclusiveGateway_1": 7,
        "Claim handling process proceeds": 8,
        "Claim is sent back": 8,
        "ExclusiveGateway_2": 9,
        "EndEvent_1": 9,
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
