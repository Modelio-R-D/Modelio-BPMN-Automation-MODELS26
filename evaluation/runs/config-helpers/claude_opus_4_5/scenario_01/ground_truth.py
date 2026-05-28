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
        ("Record order in system", USER_TASK, "Process 1"),
        ("Collect customer information", USER_TASK, "Process 1"),
        ("Guide customer in selecting product/service", USER_TASK, "Process 1"),
        ("Provide quote", USER_TASK, "Process 1"),
        ("Receive customer inquiry", USER_TASK, "Process 1"),
        ("Place order", USER_TASK, "Process 1"),
        ("Address customer concerns or questions", USER_TASK, "Process 1"),
        ("Send order confirmation to customer", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Send order confirmation to customer", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_3", "End", ""),
        ("ParallelGateway_2", "Address customer concerns or questions", ""),
        ("Record order in system", "Send order confirmation to customer", ""),
        ("Address customer concerns or questions", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_3", ""),
        ("Collect customer information", "ParallelGateway_1", ""),
        ("Start", "Receive customer inquiry", ""),
        ("ParallelGateway_2", "Collect customer information", ""),
        ("ExclusiveGateway_4", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_1", ""),
        ("Place order", "Record order in system", ""),
        ("ExclusiveGateway_4", "Guide customer in selecting product/service", ""),
        ("Provide quote", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Place order", ""),
        ("Receive customer inquiry", "ParallelGateway_2", ""),
        ("Guide customer in selecting product/service", "Provide quote", ""),
    ],

    "layout": {
        "Start": 0,
        "Receive customer inquiry": 1,
        "ParallelGateway_2": 2,
        "Address customer concerns or questions": 3,
        "Collect customer information": 3,
        "ParallelGateway_1": 4,
        "ExclusiveGateway_4": 5,
        "Guide customer in selecting product/service": 6,
        "End": 7,
        "Provide quote": 7,
        "ExclusiveGateway_2": 8,
        "Place order": 9,
        "ExclusiveGateway_3": 10,
        "Record order in system": 10,
        "Send order confirmation to customer": 11,
        "ExclusiveGateway_1": 12,
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
