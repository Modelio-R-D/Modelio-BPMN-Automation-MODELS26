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
        ("Conduct self-assessment", USER_TASK, "Process 1"),
        ("Make necessary corrections or improvements", USER_TASK, "Process 1"),
        ("Issue official documents", USER_TASK, "Process 1"),
        ("Conduct external audit", USER_TASK, "Process 1"),
        ("Award certification", USER_TASK, "Process 1"),
        ("Schedule compliance audit", USER_TASK, "Process 1"),
        ("Identify gaps or issues", USER_TASK, "Process 1"),
        ("Prepare documentation", USER_TASK, "Process 1"),
        ("Gather evidence", USER_TASK, "Process 1"),
        ("Conduct final audit", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Gather evidence", "ParallelGateway_2", ""),
        ("ParallelGateway_1", "Conduct self-assessment", ""),
        ("Issue official documents", "ExclusiveGateway_2", ""),
        ("ParallelGateway_2", "Conduct external audit", ""),
        ("ExclusiveGateway_2", "End", ""),
        ("ExclusiveGateway_1", "Award certification", ""),
        ("Identify gaps or issues", "Make necessary corrections or improvements", ""),
        ("Conduct external audit", "Identify gaps or issues", ""),
        ("Schedule compliance audit", "ParallelGateway_1", ""),
        ("Prepare documentation", "ParallelGateway_2", ""),
        ("Conduct self-assessment", "ParallelGateway_2", ""),
        ("Award certification", "Issue official documents", ""),
        ("Start", "Schedule compliance audit", ""),
        ("Make necessary corrections or improvements", "Conduct final audit", ""),
        ("ParallelGateway_1", "Gather evidence", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_2", ""),
        ("ParallelGateway_1", "Prepare documentation", ""),
        ("Conduct final audit", "ExclusiveGateway_1", ""),
    ],

    "layout": {
        "Start": 0,
        "Schedule compliance audit": 1,
        "ParallelGateway_1": 2,
        "Conduct self-assessment": 3,
        "Gather evidence": 3,
        "Prepare documentation": 3,
        "ParallelGateway_2": 4,
        "Conduct external audit": 5,
        "Identify gaps or issues": 6,
        "Make necessary corrections or improvements": 7,
        "Conduct final audit": 8,
        "ExclusiveGateway_1": 9,
        "Award certification": 10,
        "Issue official documents": 11,
        "End": 11,
        "ExclusiveGateway_2": 12,
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
