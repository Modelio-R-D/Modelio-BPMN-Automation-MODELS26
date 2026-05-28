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
        ("Transition into new role", USER_TASK, "Process 1"),
        ("Create personal development plan", USER_TASK, "Process 1"),
        ("Consider employee for promotion or new role", USER_TASK, "Process 1"),
        ("Conducts formal performance review", USER_TASK, "Process 1"),
        ("Identify development needs or career aspirations", USER_TASK, "Process 1"),
        ("Work on skill enhancement", USER_TASK, "Process 1"),
        ("Adjust compensation", USER_TASK, "Process 1"),
        ("Receive feedback and evaluation from supervisors", USER_TASK, "Process 1"),
        ("Approve promotion", USER_TASK, "Process 1"),
        ("Set new responsibilities", USER_TASK, "Process 1"),
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
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Adjust compensation", "ParallelGateway_3", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_5", ""),
        ("ParallelGateway_4", "ExclusiveGateway_4", ""),
        ("ParallelGateway_2", "Set new responsibilities", ""),
        ("Set new responsibilities", "ParallelGateway_3", ""),
        ("ExclusiveGateway_4", "Work on skill enhancement", ""),
        ("Start", "Identify development needs or career aspirations", ""),
        ("ExclusiveGateway_6", "ParallelGateway_1", ""),
        ("ExclusiveGateway_5", "Receive feedback and evaluation from supervisors", ""),
        ("Transition into new role", "ExclusiveGateway_3", ""),
        ("ParallelGateway_3", "Transition into new role", ""),
        ("Conducts formal performance review", "ExclusiveGateway_1", ""),
        ("ParallelGateway_2", "Adjust compensation", ""),
        ("ExclusiveGateway_3", "End", ""),
        ("Work on skill enhancement", "ExclusiveGateway_6", ""),
        ("ExclusiveGateway_1", "Approve promotion", ""),
        ("Approve promotion", "ParallelGateway_2", ""),
        ("ParallelGateway_4", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_3", ""),
        ("Consider employee for promotion or new role", "Conducts formal performance review", ""),
        ("Receive feedback and evaluation from supervisors", "ExclusiveGateway_2", ""),
        ("Create personal development plan", "ParallelGateway_4", ""),
        ("ExclusiveGateway_2", "ParallelGateway_1", ""),
        ("Identify development needs or career aspirations", "Create personal development plan", ""),
        ("ParallelGateway_1", "Consider employee for promotion or new role", ""),
    ],

    "layout": {
        "Start": 0,
        "Identify development needs or career aspirations": 1,
        "Create personal development plan": 2,
        "ParallelGateway_4": 3,
        "Work on skill enhancement": 5,
        "Receive feedback and evaluation from supervisors": 5,
        "ExclusiveGateway_6": 6,
        "ExclusiveGateway_2": 6,
        "ExclusiveGateway_4": 7,
        "ExclusiveGateway_5": 7,
        "ParallelGateway_1": 7,
        "Consider employee for promotion or new role": 8,
        "Conducts formal performance review": 9,
        "ExclusiveGateway_1": 10,
        "Approve promotion": 11,
        "ParallelGateway_2": 12,
        "End": 12,
        "Set new responsibilities": 13,
        "Adjust compensation": 13,
        "ParallelGateway_3": 14,
        "Transition into new role": 15,
        "ExclusiveGateway_3": 16,
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
