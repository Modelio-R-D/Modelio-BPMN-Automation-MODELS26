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
        ("select a starting block", USER_TASK, "Process 1"),
        ("get your starting number", USER_TASK, "Process 1"),
        ("measure the time", SERVICE_TASK, "Process 1"),
        ("receive your final running time", SERVICE_TASK, "Process 1"),
        ("calculate time between starting time and the end of workday", SERVICE_TASK, "Process 1"),
        ("measure the time", SERVICE_TASK, "Process 1"),
        ("run for 5km", MANUAL_TASK, "Process 1"),
        ("train", MANUAL_TASK, "Process 1"),
        ("go to home", MANUAL_TASK, "Process 1"),
        ("run", MANUAL_TASK, "Process 1"),
        ("drink", MANUAL_TASK, "Process 1"),
        ("time less than 25 minutes?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("time more than 1 hour?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "select a starting block", ""),
        ("ParallelGateway_1", "run for 5km", ""),
        ("ParallelGateway_1", "measure the time", ""),
        ("run for 5km", "ParallelGateway_2", ""),
        ("measure the time", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "time less than 25 minutes?", ""),
        ("train", "ExclusiveGateway_2", ""),
        ("time less than 25 minutes?", "train", "No"),
        ("get your starting number", "calculate time between starting time and the end of workday", ""),
        ("ExclusiveGateway_4", "ParallelGateway_3", ""),
        ("ParallelGateway_3", "run", ""),
        ("ParallelGateway_4", "receive your final running time", ""),
        ("receive your final running time", "EndEvent_1", ""),
        ("time more than 1 hour?", "ExclusiveGateway_4", "No"),
        ("calculate time between starting time and the end of workday", "time more than 1 hour?", ""),
        ("run", "ParallelGateway_4", ""),
        ("drink", "ParallelGateway_4", ""),
        ("time less than 25 minutes?", "get your starting number", "Yes"),
        ("select a starting block", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "ParallelGateway_1", ""),
        ("ParallelGateway_3", "drink", ""),
        ("ParallelGateway_3", "measure the time", ""),
        ("measure the time", "ParallelGateway_4", ""),
        ("go to home", "ExclusiveGateway_4", ""),
        ("time more than 1 hour?", "go to home", "Yes"),
    ],

    "layout": {
        "StartEvent_1": 0,
        "select a starting block": 1,
        "ParallelGateway_1": 3,
        "run for 5km": 4,
        "ParallelGateway_2": 5,
        "time less than 25 minutes?": 6,
        "receive your final running time": 6,
        "train": 7,
        "get your starting number": 7,
        "EndEvent_1": 7,
        "ExclusiveGateway_2": 8,
        "calculate time between starting time and the end of workday": 8,
        "time more than 1 hour?": 9,
        "go to home": 10,
        "ExclusiveGateway_4": 11,
        "ParallelGateway_3": 11,
        "measure the time": 12,
        "run": 12,
        "drink": 12,
        "ParallelGateway_4": 13,
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
