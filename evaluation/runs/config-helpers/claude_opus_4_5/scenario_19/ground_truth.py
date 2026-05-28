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
        ("Select items", USER_TASK, "Process 1"),
        ("Set payment method", USER_TASK, "Process 1"),
        ("Select free reward", USER_TASK, "Process 1"),
        ("Deliver items", USER_TASK, "Process 1"),
        ("Pay", USER_TASK, "Process 1"),
        ("Login", USER_TASK, "Process 1"),
        ("Return items", USER_TASK, "Process 1"),
        ("Complete installment agreement", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("ExclusiveGateway_2", "Return items", ""),
        ("Start", "Login", ""),
        ("Select free reward", "ParallelGateway_3", ""),
        ("Complete installment agreement", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "ParallelGateway_3", ""),
        ("ParallelGateway_2", "Select free reward", ""),
        ("Select items", "ParallelGateway_2", ""),
        ("ParallelGateway_3", "ExclusiveGateway_3", ""),
        ("Set payment method", "ParallelGateway_1", ""),
        ("ParallelGateway_4", "Select items", ""),
        ("Return items", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "Deliver items", ""),
        ("ExclusiveGateway_4", "Complete installment agreement", ""),
        ("Login", "ParallelGateway_4", ""),
        ("ParallelGateway_1", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_2", "End", ""),
        ("Pay", "ExclusiveGateway_1", ""),
        ("ParallelGateway_2", "ParallelGateway_1", ""),
        ("ExclusiveGateway_4", "Pay", ""),
        ("Deliver items", "ExclusiveGateway_2", ""),
        ("ParallelGateway_4", "Set payment method", ""),
    ],

    "layout": {
        "Start": 0,
        "Login": 1,
        "ParallelGateway_4": 2,
        "Select items": 3,
        "Set payment method": 3,
        "ParallelGateway_2": 4,
        "ParallelGateway_1": 5,
        "Select free reward": 5,
        "ExclusiveGateway_4": 6,
        "Complete installment agreement": 7,
        "Pay": 7,
        "ExclusiveGateway_1": 8,
        "Deliver items": 8,
        "ParallelGateway_3": 9,
        "ExclusiveGateway_2": 9,
        "Return items": 10,
        "End": 10,
        "ExclusiveGateway_3": 11,
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
