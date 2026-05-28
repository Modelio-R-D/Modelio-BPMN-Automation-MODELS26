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
        ("Install the solution", USER_TASK, "Process 1"),
        ("Assess compatibility", USER_TASK, "Process 1"),
        ("Evaluate cost and resource needs", USER_TASK, "Process 1"),
        ("Procure necessary tools or licenses", USER_TASK, "Process 1"),
        ("Submit IT solution request", USER_TASK, "Process 1"),
        ("Test solution", USER_TASK, "Process 1"),
        ("Roll out solution to requesting department", USER_TASK, "Process 1"),
        ("Provide training", USER_TASK, "Process 1"),
        ("Provide support for troubleshooting", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Provide support for troubleshooting", "ExclusiveGateway_3", ""),
        ("ParallelGateway_2", "ExclusiveGateway_6", ""),
        ("Procure necessary tools or licenses", "Install the solution", ""),
        ("ParallelGateway_4", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_4", "ParallelGateway_4", ""),
        ("ParallelGateway_1", "Assess compatibility", ""),
        ("ParallelGateway_2", "ExclusiveGateway_7", ""),
        ("Test solution", "Roll out solution to requesting department", ""),
        ("ExclusiveGateway_2", "Provide support for troubleshooting", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_5", ""),
        ("Assess compatibility", "ParallelGateway_3", ""),
        ("Evaluate cost and resource needs", "ParallelGateway_3", ""),
        ("ExclusiveGateway_1", "Procure necessary tools or licenses", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_7", "Provide training", ""),
        ("Submit IT solution request", "ParallelGateway_1", ""),
        ("ParallelGateway_3", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_5", "End", ""),
        ("Start", "Submit IT solution request", ""),
        ("Install the solution", "Test solution", ""),
        ("Roll out solution to requesting department", "ParallelGateway_2", ""),
        ("Provide training", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_7", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_8", "ParallelGateway_4", ""),
        ("ParallelGateway_1", "Evaluate cost and resource needs", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_8", ""),
    ],

    "layout": {
        "Start": 0,
        "Submit IT solution request": 1,
        "ParallelGateway_1": 2,
        "Assess compatibility": 3,
        "Evaluate cost and resource needs": 3,
        "ParallelGateway_3": 4,
        "ExclusiveGateway_1": 5,
        "Procure necessary tools or licenses": 6,
        "End": 7,
        "Install the solution": 7,
        "Test solution": 8,
        "Roll out solution to requesting department": 9,
        "ParallelGateway_2": 10,
        "ExclusiveGateway_6": 11,
        "ExclusiveGateway_7": 11,
        "Provide training": 12,
        "ExclusiveGateway_4": 13,
        "Provide support for troubleshooting": 13,
        "ParallelGateway_4": 14,
        "ExclusiveGateway_3": 14,
        "ExclusiveGateway_5": 15,
        "ExclusiveGateway_2": 15,
        "ExclusiveGateway_8": 15,
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
