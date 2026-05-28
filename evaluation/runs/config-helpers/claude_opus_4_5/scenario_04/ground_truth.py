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
        ("Create content", USER_TASK, "Process 1"),
        ("Sales teams follows up on leads", USER_TASK, "Process 1"),
        ("Track performance in real-time", USER_TASK, "Process 1"),
        ("Collect leads in CRM system", USER_TASK, "Process 1"),
        ("Select promotion channels", USER_TASK, "Process 1"),
        ("Analyze performance for future optimization", USER_TASK, "Process 1"),
        ("Launch campaign", USER_TASK, "Process 1"),
        ("Define campaign objectives", USER_TASK, "Process 1"),
        ("Campaign period ends", USER_TASK, "Process 1"),
        ("Design visuals", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
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
        ("ParallelGateway_5", "Analyze performance for future optimization", ""),
        ("ParallelGateway_3", "Select promotion channels", ""),
        ("ParallelGateway_5", "ParallelGateway_4", ""),
        ("ParallelGateway_6", "Collect leads in CRM system", ""),
        ("ExclusiveGateway_1", "ParallelGateway_4", ""),
        ("Track performance in real-time", "ParallelGateway_5", ""),
        ("ParallelGateway_3", "Design visuals", ""),
        ("Define campaign objectives", "ParallelGateway_3", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_1", ""),
        ("Campaign period ends", "ParallelGateway_2", ""),
        ("Select promotion channels", "ParallelGateway_1", ""),
        ("ExclusiveGateway_2", "Sales teams follows up on leads", ""),
        ("Analyze performance for future optimization", "ParallelGateway_2", ""),
        ("Collect leads in CRM system", "ExclusiveGateway_2", ""),
        ("Design visuals", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Launch campaign", ""),
        ("Launch campaign", "ParallelGateway_6", ""),
        ("ParallelGateway_2", "End", ""),
        ("ParallelGateway_4", "Campaign period ends", ""),
        ("ParallelGateway_6", "Track performance in real-time", ""),
        ("Start", "Define campaign objectives", ""),
        ("Sales teams follows up on leads", "ExclusiveGateway_1", ""),
        ("Create content", "ParallelGateway_1", ""),
        ("ParallelGateway_3", "Create content", ""),
    ],

    "layout": {
        "Start": 0,
        "Define campaign objectives": 1,
        "ParallelGateway_3": 2,
        "Select promotion channels": 3,
        "Design visuals": 3,
        "Create content": 3,
        "ParallelGateway_1": 4,
        "Launch campaign": 5,
        "ParallelGateway_6": 6,
        "Collect leads in CRM system": 7,
        "Track performance in real-time": 7,
        "ExclusiveGateway_2": 8,
        "ParallelGateway_5": 8,
        "Sales teams follows up on leads": 9,
        "Analyze performance for future optimization": 9,
        "ExclusiveGateway_1": 10,
        "ParallelGateway_4": 10,
        "Campaign period ends": 11,
        "End": 11,
        "ParallelGateway_2": 12,
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
