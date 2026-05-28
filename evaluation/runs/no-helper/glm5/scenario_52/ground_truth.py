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
        ("MPON sents the dismissal to the MPOO", USER_TASK, "Process 1"),
        ("MPOO reviews the dismissal", USER_TASK, "Process 1"),
        ("MPOO opposes the dismissal", USER_TASK, "Process 1"),
        ("MPOO confirmes the dismissal", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "MPON sents the dismissal to the MPOO", ""),
        ("MPON sents the dismissal to the MPOO", "MPOO reviews the dismissal", ""),
        ("MPOO reviews the dismissal", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "MPOO opposes the dismissal", ""),
        ("ExclusiveGateway_1", "MPOO confirmes the dismissal", ""),
        ("MPOO opposes the dismissal", "ExclusiveGateway_2", ""),
        ("MPOO confirmes the dismissal", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "EndEvent_1", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "MPON sents the dismissal to the MPOO": 1,
        "MPOO reviews the dismissal": 2,
        "ExclusiveGateway_1": 3,
        "MPOO opposes the dismissal": 4,
        "MPOO confirmes the dismissal": 4,
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
