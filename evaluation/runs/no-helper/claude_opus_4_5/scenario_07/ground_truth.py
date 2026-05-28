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
        ("Select route", USER_TASK, "Process 1"),
        ("Send ticket via email", USER_TASK, "Process 1"),
        ("Post-travel feedback or services", USER_TASK, "Process 1"),
        ("Customer completes journey", USER_TASK, "Process 1"),
        ("Provide payment details", USER_TASK, "Process 1"),
        ("Send reminder", USER_TASK, "Process 1"),
        ("Select date and time", USER_TASK, "Process 1"),
        ("Provide personal information", USER_TASK, "Process 1"),
        ("Generate ticket", USER_TASK, "Process 1"),
        ("Update seat inventory", USER_TASK, "Process 1"),
        ("Send instructions", USER_TASK, "Process 1"),
        ("Customer searches for ticket", USER_TASK, "Process 1"),
        ("Send ticket via SMS", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_9", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_10", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_11", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_12", EXCLUSIVE_GW, "Process 1"),
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
        ("Send ticket via email", "ExclusiveGateway_8", ""),
        ("Provide personal information", "ParallelGateway_3", ""),
        ("Customer completes journey", "ExclusiveGateway_5", ""),
        ("ParallelGateway_2", "Select date and time", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_9", ""),
        ("ExclusiveGateway_12", "ParallelGateway_4", ""),
        ("ExclusiveGateway_8", "ParallelGateway_1", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_3", "End", ""),
        ("ParallelGateway_1", "ExclusiveGateway_11", ""),
        ("ExclusiveGateway_11", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_5", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_10", "ExclusiveGateway_12", ""),
        ("Select date and time", "ParallelGateway_5", ""),
        ("Update seat inventory", "ParallelGateway_1", ""),
        ("Send instructions", "ExclusiveGateway_6", ""),
        ("Send reminder", "ExclusiveGateway_10", ""),
        ("ExclusiveGateway_9", "Send instructions", ""),
        ("ExclusiveGateway_2", "ParallelGateway_4", ""),
        ("ParallelGateway_2", "Select route", ""),
        ("ParallelGateway_6", "Update seat inventory", ""),
        ("ParallelGateway_4", "Customer completes journey", ""),
        ("ExclusiveGateway_11", "ExclusiveGateway_12", ""),
        ("ExclusiveGateway_4", "Send reminder", ""),
        ("ParallelGateway_3", "Generate ticket", ""),
        ("ExclusiveGateway_7", "Send ticket via SMS", ""),
        ("ParallelGateway_6", "ExclusiveGateway_7", ""),
        ("ExclusiveGateway_10", "ExclusiveGateway_4", ""),
        ("Generate ticket", "ParallelGateway_6", ""),
        ("Provide payment details", "ParallelGateway_3", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_9", ""),
        ("ExclusiveGateway_5", "Post-travel feedback or services", ""),
        ("Start", "Customer searches for ticket", ""),
        ("ParallelGateway_5", "Provide personal information", ""),
        ("Customer searches for ticket", "ParallelGateway_2", ""),
        ("ParallelGateway_5", "Provide payment details", ""),
        ("Post-travel feedback or services", "ExclusiveGateway_3", ""),
        ("ParallelGateway_1", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_7", "Send ticket via email", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_2", ""),
        ("Select route", "ParallelGateway_5", ""),
        ("Send ticket via SMS", "ExclusiveGateway_8", ""),
    ],

    "layout": {
        "Start": 0,
        "Customer searches for ticket": 1,
        "ParallelGateway_2": 2,
        "Select date and time": 3,
        "Select route": 3,
        "ParallelGateway_5": 4,
        "Provide personal information": 5,
        "Provide payment details": 5,
        "ParallelGateway_3": 6,
        "Generate ticket": 7,
        "ParallelGateway_6": 8,
        "Update seat inventory": 9,
        "ExclusiveGateway_7": 9,
        "Send ticket via SMS": 10,
        "Send ticket via email": 10,
        "ExclusiveGateway_11": 11,
        "ExclusiveGateway_1": 11,
        "ExclusiveGateway_8": 11,
        "ParallelGateway_1": 12,
        "Send reminder": 13,
        "ParallelGateway_4": 13,
        "Send instructions": 13,
        "ExclusiveGateway_10": 14,
        "Customer completes journey": 14,
        "ExclusiveGateway_6": 14,
        "ExclusiveGateway_4": 15,
        "ExclusiveGateway_12": 15,
        "ExclusiveGateway_2": 15,
        "ExclusiveGateway_9": 15,
        "ExclusiveGateway_5": 15,
        "Post-travel feedback or services": 16,
        "ExclusiveGateway_3": 17,
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
