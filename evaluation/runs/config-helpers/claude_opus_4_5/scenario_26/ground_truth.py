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
        ("receive confirmation from employer", SERVICE_TASK, "Process 1"),
        ("fetch information about leave models", SERVICE_TASK, "Process 1"),
        ("fetch information about financial support", SERVICE_TASK, "Process 1"),
        ("check if all necessary documents gathered", SERVICE_TASK, "Process 1"),
        ("select appropriate model", MANUAL_TASK, "Process 1"),
        ("notify employer", MANUAL_TASK, "Process 1"),
        ("notify social security", MANUAL_TASK, "Process 1"),
        ("prepare necessary documents for leave", MANUAL_TASK, "Process 1"),
        ("do maternity/paternity leave", MANUAL_TASK, "Process 1"),
        ("decide if extend leave or return to work", MANUAL_TASK, "Process 1"),
        ("apply for financial support", MANUAL_TASK, "Process 1"),
        ("decide if apply for financial support", MANUAL_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("return to job", END, "Process 1"),
    ],

    "flows": [
        ("notify social security", "ParallelGateway_2", ""),
        ("notify employer", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "receive confirmation from employer", ""),
        ("do maternity/paternity leave", "decide if extend leave or return to work", ""),
        ("decide if extend leave or return to work", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "return to job", ""),
        ("StartEvent_1", "ParallelGateway_3", ""),
        ("ParallelGateway_3", "fetch information about financial support", ""),
        ("ParallelGateway_3", "fetch information about leave models", ""),
        ("fetch information about financial support", "ParallelGateway_4", ""),
        ("fetch information about leave models", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "select appropriate model", ""),
        ("ExclusiveGateway_2", "apply for financial support", ""),
        ("apply for financial support", "ExclusiveGateway_3", ""),
        ("decide if apply for financial support", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_3", ""),
        ("receive confirmation from employer", "check if all necessary documents gathered", ""),
        ("check if all necessary documents gathered", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_4", "do maternity/paternity leave", ""),
        ("ParallelGateway_1", "notify employer", ""),
        ("ParallelGateway_1", "notify social security", ""),
        ("ExclusiveGateway_4", "prepare necessary documents for leave", ""),
        ("ExclusiveGateway_3", "prepare necessary documents for leave", ""),
        ("prepare necessary documents for leave", "ParallelGateway_1", ""),
        ("select appropriate model", "decide if apply for financial support", ""),
        ("ExclusiveGateway_1", "prepare necessary documents for leave", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "ParallelGateway_3": 1,
        "fetch information about financial support": 2,
        "fetch information about leave models": 2,
        "ParallelGateway_4": 3,
        "select appropriate model": 4,
        "decide if apply for financial support": 5,
        "ExclusiveGateway_2": 6,
        "apply for financial support": 7,
        "ExclusiveGateway_3": 8,
        "ParallelGateway_1": 10,
        "notify employer": 11,
        "notify social security": 11,
        "ParallelGateway_2": 12,
        "receive confirmation from employer": 13,
        "check if all necessary documents gathered": 14,
        "ExclusiveGateway_4": 15,
        "do maternity/paternity leave": 16,
        "decide if extend leave or return to work": 17,
        "ExclusiveGateway_1": 18,
        "prepare necessary documents for leave": 19,
        "return to job": 19,
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
