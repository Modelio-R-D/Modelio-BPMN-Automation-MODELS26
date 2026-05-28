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
        ("MSPN sends a dismissal to MSPO", USER_TASK, "Process 1"),
        ("MSPO reviews the dismissal", USER_TASK, "Process 1"),
        ("MSPO rejects the dismissal of the MSPN", USER_TASK, "Process 1"),
        ("MSPO confirms the dismissal of the MSPN", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "MSPN sends a dismissal to MSPO", ""),
        ("MSPN sends a dismissal to MSPO", "MSPO reviews the dismissal", ""),
        ("MSPO reviews the dismissal", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "MSPO rejects the dismissal of the MSPN", ""),
        ("ExclusiveGateway_1", "MSPO confirms the dismissal of the MSPN", ""),
        ("MSPO rejects the dismissal of the MSPN", "ExclusiveGateway_2", ""),
        ("MSPO confirms the dismissal of the MSPN", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "EndEvent_1", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "MSPN sends a dismissal to MSPO": 1,
        "MSPO reviews the dismissal": 2,
        "ExclusiveGateway_1": 3,
        "MSPO rejects the dismissal of the MSPN": 4,
        "MSPO confirms the dismissal of the MSPN": 4,
        "ExclusiveGateway_2": 5,
        "EndEvent_1": 6,
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
