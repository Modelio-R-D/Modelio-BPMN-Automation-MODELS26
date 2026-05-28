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

    "lanes": ["Player", "Farming Bot"],

    "elements": [
        ("Collect urgently needed resources", USER_TASK, "Player"),
        ("Collect the remained resources", USER_TASK, "Player"),
        ("Check repo for already available resources", USER_TASK, "Player"),
        ("Build tools", USER_TASK, "Player"),
        ("Start farming", USER_TASK, "Farming Bot"),
        ("Continue farming", USER_TASK, "Farming Bot"),
        ("Update list of resources", USER_TASK, "Farming Bot"),
        ("Wait for random natural event for some time", USER_TASK, "Farming Bot"),
        ("Find out wanted resources", USER_TASK, "Player"),
        ("Read message", USER_TASK, "Player"),
        ("Brag to friends", USER_TASK, "Farming Bot"),
        ("Help with materials", USER_TASK, "Farming Bot"),
        ("Reset bot", SERVICE_TASK, "Farming Bot"),
        ("Notify player", SERVICE_TASK, "Farming Bot"),
        ("Give bot a sleeping break", SERVICE_TASK, "Farming Bot"),
        ("New tools needed?", EXCLUSIVE_GW, "Player"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Player"),
        ("New milestone achieved?", EXCLUSIVE_GW, "Farming Bot"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Farming Bot"),
        ("Bot finished?", EXCLUSIVE_GW, "Farming Bot"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Farming Bot"),
        ("RNE happened?", EXCLUSIVE_GW, "Farming Bot"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Farming Bot"),
        ("ParallelGateway_1", PARALLEL_GW, "Player"),
        ("ParallelGateway_2", PARALLEL_GW, "Player"),
        ("ParallelGateway_3", PARALLEL_GW, "Farming Bot"),
        ("ParallelGateway_4", PARALLEL_GW, "Farming Bot"),
        ("InclusiveGateway_1", INCLUSIVE_GW, "Farming Bot"),
        ("InclusiveGateway_2", INCLUSIVE_GW, "Farming Bot"),
        ("Farming bot creation desire", START, "Player"),
        ("EndEvent_1", END, "Farming Bot"),
    ],

    "flows": [
        ("Farming bot creation desire", "Find out wanted resources", ""),
        ("New milestone achieved?", "Notify player", "Yes"),
        ("Help with materials", "InclusiveGateway_2", ""),
        ("Brag to friends", "InclusiveGateway_2", ""),
        ("ParallelGateway_1", "Check repo for already available resources", ""),
        ("Check repo for already available resources", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "New tools needed?", ""),
        ("Build tools", "ExclusiveGateway_2", ""),
        ("ParallelGateway_1", "Collect urgently needed resources", ""),
        ("Collect urgently needed resources", "ParallelGateway_2", ""),
        ("New tools needed?", "Build tools", "Yes"),
        ("ExclusiveGateway_2", "Collect the remained resources", ""),
        ("New tools needed?", "ExclusiveGateway_2", "No"),
        ("Read message", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_4", "Bot finished?", ""),
        ("Reset bot", "Continue farming", ""),
        ("Start farming", "ExclusiveGateway_6", ""),
        ("Find out wanted resources", "ParallelGateway_1", ""),
        ("Notify player", "Read message", ""),
        ("ExclusiveGateway_6", "New milestone achieved?", ""),
        ("Continue farming", "ExclusiveGateway_6", ""),
        ("Wait for random natural event for some time", "RNE happened?", ""),
        ("RNE happened?", "Reset bot", "Yes"),
        ("ParallelGateway_3", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_8", "Wait for random natural event for some time", ""),
        ("Collect the remained resources", "ParallelGateway_3", ""),
        ("RNE happened?", "Start farming", "No"),
        ("ParallelGateway_3", "Update list of resources", ""),
        ("New milestone achieved?", "ExclusiveGateway_4", "No"),
        ("Give bot a sleeping break", "ExclusiveGateway_8", ""),
        ("Bot finished?", "InclusiveGateway_1", "Yes"),
        ("InclusiveGateway_2", "ParallelGateway_4", ""),
        ("Update list of resources", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "EndEvent_1", ""),
        ("Bot finished?", "Give bot a sleeping break", "No"),
        ("InclusiveGateway_1", "Brag to friends", "brag"),
        ("InclusiveGateway_1", "Help with materials", "help"),
    ],

    "layout": {
        "Farming bot creation desire": 0,
        "Find out wanted resources": 1,
        "ParallelGateway_1": 2,
        "Check repo for already available resources": 3,
        "Collect urgently needed resources": 3,
        "ParallelGateway_2": 4,
        "New tools needed?": 5,
        "Build tools": 6,
        "ExclusiveGateway_2": 7,
        "Collect the remained resources": 8,
        "ParallelGateway_3": 9,
        "Update list of resources": 10,
        "Wait for random natural event for some time": 11,
        "RNE happened?": 12,
        "EndEvent_1": 12,
        "Reset bot": 13,
        "Start farming": 13,
        "Continue farming": 14,
        "ExclusiveGateway_6": 15,
        "New milestone achieved?": 16,
        "Notify player": 17,
        "Read message": 18,
        "Bot finished?": 18,
        "ExclusiveGateway_4": 19,
        "InclusiveGateway_1": 19,
        "Give bot a sleeping break": 19,
        "ExclusiveGateway_8": 20,
        "Brag to friends": 20,
        "Help with materials": 20,
        "InclusiveGateway_2": 21,
        "ParallelGateway_4": 22,
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
