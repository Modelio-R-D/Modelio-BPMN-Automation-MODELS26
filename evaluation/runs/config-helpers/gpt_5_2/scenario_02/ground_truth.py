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
        ("Complete orientation", USER_TASK, "Process 1"),
        ("Conduct initial phone interviews", USER_TASK, "Process 1"),
        ("Conduct a virtual interview", USER_TASK, "Process 1"),
        ("Begin onboarding process", USER_TASK, "Process 1"),
        ("Identify need for new hire", USER_TASK, "Process 1"),
        ("Choose candidate", USER_TASK, "Process 1"),
        ("Collect resumes", USER_TASK, "Process 1"),
        ("Extend offer", USER_TASK, "Process 1"),
        ("Complete training", USER_TASK, "Process 1"),
        ("Complete paperwork", USER_TASK, "Process 1"),
        ("Invite candidates for interviews", USER_TASK, "Process 1"),
        ("Post job description", USER_TASK, "Process 1"),
        ("Create job description", USER_TASK, "Process 1"),
        ("Screen resumes", USER_TASK, "Process 1"),
        ("Negotiate salary", USER_TASK, "Process 1"),
        ("Conduct an in-person interview", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Post job description", "Collect resumes", ""),
        ("Choose candidate", "Extend offer", ""),
        ("Negotiate salary", "ExclusiveGateway_3", ""),
        ("Screen resumes", "Conduct initial phone interviews", ""),
        ("Conduct initial phone interviews", "Invite candidates for interviews", ""),
        ("ExclusiveGateway_2", "Choose candidate", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_5", ""),
        ("ParallelGateway_1", "Complete orientation", ""),
        ("Complete orientation", "ParallelGateway_2", ""),
        ("ParallelGateway_1", "Complete paperwork", ""),
        ("ExclusiveGateway_1", "Conduct a virtual interview", ""),
        ("Extend offer", "ExclusiveGateway_6", ""),
        ("ParallelGateway_2", "End", ""),
        ("ExclusiveGateway_1", "Conduct an in-person interview", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_4", ""),
        ("Conduct an in-person interview", "ExclusiveGateway_2", ""),
        ("Conduct a virtual interview", "ExclusiveGateway_2", ""),
        ("ParallelGateway_1", "Complete training", ""),
        ("Collect resumes", "Screen resumes", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_1", ""),
        ("Complete training", "ParallelGateway_2", ""),
        ("Create job description", "Post job description", ""),
        ("Invite candidates for interviews", "ExclusiveGateway_1", ""),
        ("Complete paperwork", "ParallelGateway_2", ""),
        ("ExclusiveGateway_4", "Negotiate salary", ""),
        ("ExclusiveGateway_5", "Begin onboarding process", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_4", ""),
        ("Identify need for new hire", "Create job description", ""),
        ("Start", "Identify need for new hire", ""),
        ("Begin onboarding process", "ParallelGateway_1", ""),
    ],

    "layout": {
        "Start": 0,
        "Identify need for new hire": 1,
        "Create job description": 2,
        "Post job description": 3,
        "Collect resumes": 4,
        "Screen resumes": 5,
        "Conduct initial phone interviews": 6,
        "Invite candidates for interviews": 7,
        "Conduct a virtual interview": 9,
        "Conduct an in-person interview": 9,
        "ExclusiveGateway_2": 10,
        "ExclusiveGateway_1": 11,
        "Choose candidate": 11,
        "Extend offer": 12,
        "ExclusiveGateway_6": 13,
        "Begin onboarding process": 15,
        "Negotiate salary": 15,
        "ParallelGateway_1": 16,
        "ExclusiveGateway_3": 16,
        "ExclusiveGateway_5": 17,
        "ExclusiveGateway_4": 17,
        "Complete orientation": 17,
        "Complete paperwork": 17,
        "Complete training": 17,
        "ParallelGateway_2": 18,
        "End": 19,
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
