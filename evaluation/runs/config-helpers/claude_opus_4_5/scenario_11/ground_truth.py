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
        ("Assign access", USER_TASK, "Process 1"),
        ("Customer submits cancellation request", USER_TASK, "Process 1"),
        ("apply charges", USER_TASK, "Process 1"),
        ("Generate account", USER_TASK, "Process 1"),
        ("Send regular updates", USER_TASK, "Process 1"),
        ("Deactivate subscription", USER_TASK, "Process 1"),
        ("Settle final account balance", USER_TASK, "Process 1"),
        ("apply refund", USER_TASK, "Process 1"),
        ("Send renewal notifications", USER_TASK, "Process 1"),
        ("Customer signs up", USER_TASK, "Process 1"),
        ("Set automatic triggers for billing cycles", USER_TASK, "Process 1"),
        ("Send product enhancements", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_5", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_6", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("ExclusiveGateway_6", "apply refund", ""),
        ("Set automatic triggers for billing cycles", "ParallelGateway_5", ""),
        ("Send regular updates", "ParallelGateway_2", ""),
        ("ParallelGateway_1", "Assign access", ""),
        ("ExclusiveGateway_6", "apply charges", ""),
        ("ExclusiveGateway_4", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "Send renewal notifications", ""),
        ("Generate account", "ParallelGateway_1", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_3", ""),
        ("ParallelGateway_6", "ExclusiveGateway_2", ""),
        ("apply charges", "ExclusiveGateway_5", ""),
        ("Send product enhancements", "ParallelGateway_2", ""),
        ("ParallelGateway_4", "Send regular updates", ""),
        ("ParallelGateway_5", "ExclusiveGateway_4", ""),
        ("Assign access", "ParallelGateway_5", ""),
        ("Settle final account balance", "ParallelGateway_6", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_2", ""),
        ("Start", "Customer signs up", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_4", ""),
        ("ParallelGateway_3", "Deactivate subscription", ""),
        ("ParallelGateway_1", "Set automatic triggers for billing cycles", ""),
        ("ExclusiveGateway_2", "End", ""),
        ("Send renewal notifications", "ParallelGateway_2", ""),
        ("ExclusiveGateway_3", "Customer submits cancellation request", ""),
        ("ParallelGateway_3", "ExclusiveGateway_6", ""),
        ("Customer submits cancellation request", "ParallelGateway_3", ""),
        ("apply refund", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_5", "Settle final account balance", ""),
        ("ParallelGateway_2", "ExclusiveGateway_1", ""),
        ("Deactivate subscription", "ParallelGateway_6", ""),
        ("ParallelGateway_4", "Send product enhancements", ""),
        ("Customer signs up", "Generate account", ""),
    ],

    "layout": {
        "Start": 0,
        "Customer signs up": 1,
        "Generate account": 2,
        "ParallelGateway_1": 3,
        "Assign access": 4,
        "Set automatic triggers for billing cycles": 4,
        "ParallelGateway_5": 5,
        "ParallelGateway_4": 7,
        "Send renewal notifications": 8,
        "Send regular updates": 8,
        "Send product enhancements": 8,
        "ParallelGateway_2": 9,
        "ExclusiveGateway_1": 10,
        "ExclusiveGateway_4": 11,
        "ExclusiveGateway_3": 11,
        "Customer submits cancellation request": 12,
        "End": 13,
        "ParallelGateway_3": 13,
        "Deactivate subscription": 14,
        "ExclusiveGateway_6": 14,
        "apply refund": 15,
        "apply charges": 15,
        "ExclusiveGateway_2": 16,
        "ExclusiveGateway_5": 16,
        "Settle final account balance": 17,
        "ParallelGateway_6": 18,
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
