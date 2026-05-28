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
        ("Propose corrective actions", USER_TASK, "Process 1"),
        ("Log report into tracking system", USER_TASK, "Process 1"),
        ("Close incident report", USER_TASK, "Process 1"),
        ("Change policy", USER_TASK, "Process 1"),
        ("Assign report to appropriate team", USER_TASK, "Process 1"),
        ("Report incident", USER_TASK, "Process 1"),
        ("Conduct training", USER_TASK, "Process 1"),
        ("Gather necessary information", USER_TASK, "Process 1"),
        ("Identify cause of incident", USER_TASK, "Process 1"),
        ("Notify all stakeholders", USER_TASK, "Process 1"),
        ("Implement fix", USER_TASK, "Process 1"),
        ("Conduct follow-up", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Change policy", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_2", "Implement fix", ""),
        ("ExclusiveGateway_1", "Conduct follow-up", ""),
        ("Start", "Report incident", ""),
        ("ParallelGateway_1", "Propose corrective actions", ""),
        ("Gather necessary information", "ParallelGateway_1", ""),
        ("Log report into tracking system", "Assign report to appropriate team", ""),
        ("ParallelGateway_2", "Gather necessary information", ""),
        ("Conduct follow-up", "Close incident report", ""),
        ("Notify all stakeholders", "End", ""),
        ("ExclusiveGateway_2", "Change policy", ""),
        ("Identify cause of incident", "ParallelGateway_1", ""),
        ("Close incident report", "Notify all stakeholders", ""),
        ("Implement fix", "ExclusiveGateway_1", ""),
        ("Report incident", "Log report into tracking system", ""),
        ("Propose corrective actions", "ExclusiveGateway_2", ""),
        ("Conduct training", "ExclusiveGateway_1", ""),
        ("Assign report to appropriate team", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Identify cause of incident", ""),
        ("ExclusiveGateway_2", "Conduct training", ""),
    ],

    "layout": {
        "Start": 0,
        "Report incident": 1,
        "Log report into tracking system": 2,
        "Assign report to appropriate team": 3,
        "ParallelGateway_2": 4,
        "Gather necessary information": 5,
        "Identify cause of incident": 5,
        "ParallelGateway_1": 6,
        "Propose corrective actions": 7,
        "ExclusiveGateway_2": 8,
        "Implement fix": 9,
        "Change policy": 9,
        "Conduct training": 9,
        "ExclusiveGateway_1": 10,
        "Conduct follow-up": 11,
        "Close incident report": 12,
        "Notify all stakeholders": 13,
        "End": 14,
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
