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
        ("Update inventory levels", USER_TASK, "Process 1"),
        ("Update inventory system with expected delivery dates", USER_TASK, "Process 1"),
        ("Inspect stock for quality", USER_TASK, "Process 1"),
        ("Place order with suppliers", USER_TASK, "Process 1"),
        ("Receive stock", USER_TASK, "Process 1"),
        ("Place stock on shelves", USER_TASK, "Process 1"),
        ("Check current inventory level", USER_TASK, "Process 1"),
        ("Send a manual alert", USER_TASK, "Process 1"),
        ("Send an automated alert", USER_TASK, "Process 1"),
        ("Place stock in storage", USER_TASK, "Process 1"),
        ("Record stock in system", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Place stock on shelves", "ExclusiveGateway_6", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_6", "ParallelGateway_2", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_4", "Send a manual alert", ""),
        ("Place stock in storage", "ExclusiveGateway_6", ""),
        ("Check current inventory level", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_4", "Send an automated alert", ""),
        ("Inspect stock for quality", "ExclusiveGateway_2", ""),
        ("Receive stock", "ParallelGateway_1", ""),
        ("Record stock in system", "ParallelGateway_2", ""),
        ("Send a manual alert", "ExclusiveGateway_5", ""),
        ("Update inventory system with expected delivery dates", "Receive stock", ""),
        ("ParallelGateway_2", "Update inventory levels", ""),
        ("ExclusiveGateway_2", "Place stock on shelves", ""),
        ("ExclusiveGateway_2", "Place stock in storage", ""),
        ("Place order with suppliers", "Update inventory system with expected delivery dates", ""),
        ("Start", "ExclusiveGateway_1", ""),
        ("Update inventory levels", "End", ""),
        ("ParallelGateway_1", "Record stock in system", ""),
        ("ExclusiveGateway_5", "Place order with suppliers", ""),
        ("ParallelGateway_1", "Inspect stock for quality", ""),
        ("ExclusiveGateway_1", "Check current inventory level", ""),
        ("Send an automated alert", "ExclusiveGateway_5", ""),
    ],

    "layout": {
        "Start": 0,
        "Check current inventory level": 2,
        "ExclusiveGateway_3": 3,
        "ExclusiveGateway_1": 4,
        "ExclusiveGateway_4": 4,
        "Send a manual alert": 5,
        "Send an automated alert": 5,
        "ExclusiveGateway_5": 6,
        "Place order with suppliers": 7,
        "Update inventory system with expected delivery dates": 8,
        "Receive stock": 9,
        "ParallelGateway_1": 10,
        "Record stock in system": 11,
        "Inspect stock for quality": 11,
        "ExclusiveGateway_2": 12,
        "Update inventory levels": 13,
        "Place stock on shelves": 13,
        "Place stock in storage": 13,
        "End": 14,
        "ExclusiveGateway_6": 14,
        "ParallelGateway_2": 15,
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
