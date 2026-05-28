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
        ("Successful delivery", USER_TASK, "Process 1"),
        ("Customer places order online", USER_TASK, "Process 1"),
        ("Hand over order to logistics provider", USER_TASK, "Process 1"),
        ("Customer places order over the phone", USER_TASK, "Process 1"),
        ("Monitor shipment", USER_TASK, "Process 1"),
        ("Pick and pack items", USER_TASK, "Process 1"),
        ("Generate and send order confirmation", USER_TASK, "Process 1"),
        ("Process customer feedback or returns", USER_TASK, "Process 1"),
        ("Generate shipping label", USER_TASK, "Process 1"),
        ("Send tracking information to customer", USER_TASK, "Process 1"),
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
        ("ParallelGateway_1", "Generate shipping label", ""),
        ("ExclusiveGateway_1", "Customer places order online", ""),
        ("Customer places order online", "ExclusiveGateway_2", ""),
        ("Start", "ExclusiveGateway_1", ""),
        ("Successful delivery", "ExclusiveGateway_3", ""),
        ("Send tracking information to customer", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_2", "Generate and send order confirmation", ""),
        ("Customer places order over the phone", "ExclusiveGateway_2", ""),
        ("Generate and send order confirmation", "ParallelGateway_1", ""),
        ("Process customer feedback or returns", "ExclusiveGateway_5", ""),
        ("ParallelGateway_1", "Pick and pack items", ""),
        ("Monitor shipment", "ExclusiveGateway_6", ""),
        ("Generate shipping label", "ParallelGateway_2", ""),
        ("Pick and pack items", "ParallelGateway_2", ""),
        ("ExclusiveGateway_1", "Customer places order over the phone", ""),
        ("ExclusiveGateway_3", "Process customer feedback or returns", ""),
        ("ExclusiveGateway_6", "Successful delivery", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_5", "End", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_5", ""),
        ("ParallelGateway_2", "Hand over order to logistics provider", ""),
        ("ExclusiveGateway_4", "Monitor shipment", ""),
        ("Hand over order to logistics provider", "Send tracking information to customer", ""),
    ],

    "layout": {
        "Start": 0,
        "ExclusiveGateway_1": 1,
        "Customer places order online": 2,
        "Customer places order over the phone": 2,
        "ExclusiveGateway_2": 3,
        "Generate and send order confirmation": 4,
        "ParallelGateway_1": 5,
        "Generate shipping label": 6,
        "Pick and pack items": 6,
        "ParallelGateway_2": 7,
        "Hand over order to logistics provider": 8,
        "Send tracking information to customer": 9,
        "Monitor shipment": 11,
        "ExclusiveGateway_6": 12,
        "ExclusiveGateway_4": 13,
        "Successful delivery": 13,
        "ExclusiveGateway_3": 14,
        "Process customer feedback or returns": 15,
        "ExclusiveGateway_5": 16,
        "End": 17,
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
