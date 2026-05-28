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
        ("Register for internship", USER_TASK, "Process 1"),
        ("Enter topic", USER_TASK, "Process 1"),
        ("Enter expected income", USER_TASK, "Process 1"),
        ("Enter experience", USER_TASK, "Process 1"),
        ("Enter hobbies", USER_TASK, "Process 1"),
        ("Accept offer", USER_TASK, "Process 1"),
        ("Deny offer", USER_TASK, "Process 1"),
        ("Publish your application", USER_TASK, "Process 1"),
        ("Begin internship", USER_TASK, "Process 1"),
        ("Write at least 3 status updates every week", USER_TASK, "Process 1"),
        ("End internship", USER_TASK, "Process 1"),
        ("Recieve offer", SERVICE_TASK, "Process 1"),
        ("Invalidate all other offers", SERVICE_TASK, "Process 1"),
        ("Recommend company to a list of friends via twitter api", SERVICE_TASK, "Process 1"),
        ("Recieve 3 status updates from the company", SERVICE_TASK, "Process 1"),
        ("Accept offer?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("Recommend company?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_5", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_6", PARALLEL_GW, "Process 1"),
        ("InclusiveGateway_1", INCLUSIVE_GW, "Process 1"),
        ("InclusiveGateway_2", INCLUSIVE_GW, "Process 1"),
        ("Internship process is started", START, "Process 1"),
        ("Internship succesful", END, "Process 1"),
    ],

    "flows": [
        ("Internship process is started", "Register for internship", ""),
        ("InclusiveGateway_1", "Enter hobbies", ""),
        ("Enter hobbies", "InclusiveGateway_2", ""),
        ("Recieve offer", "Accept offer?", ""),
        ("ExclusiveGateway_2", "Recieve offer", ""),
        ("Deny offer", "ExclusiveGateway_2", ""),
        ("Publish your application", "ExclusiveGateway_2", ""),
        ("ParallelGateway_2", "Accept offer", ""),
        ("ParallelGateway_2", "Invalidate all other offers", ""),
        ("Accept offer", "ParallelGateway_1", ""),
        ("Invalidate all other offers", "ParallelGateway_1", ""),
        ("Begin internship", "ParallelGateway_3", ""),
        ("InclusiveGateway_1", "Enter experience", ""),
        ("InclusiveGateway_1", "Enter expected income", ""),
        ("Enter experience", "InclusiveGateway_2", ""),
        ("Enter expected income", "InclusiveGateway_2", ""),
        ("ParallelGateway_3", "Write at least 3 status updates every week", ""),
        ("ParallelGateway_3", "Recieve 3 status updates from the company", ""),
        ("Recieve 3 status updates from the company", "ParallelGateway_4", ""),
        ("Write at least 3 status updates every week", "ParallelGateway_4", ""),
        ("Recommend company?", "Recommend company to a list of friends via twitter api", "Yes"),
        ("ParallelGateway_1", "Begin internship", ""),
        ("End internship", "Recommend company?", ""),
        ("Register for internship", "ParallelGateway_5", ""),
        ("ParallelGateway_4", "End internship", ""),
        ("ParallelGateway_5", "Enter topic", ""),
        ("InclusiveGateway_2", "ParallelGateway_6", ""),
        ("Enter topic", "ParallelGateway_6", ""),
        ("ParallelGateway_5", "InclusiveGateway_1", ""),
        ("ParallelGateway_6", "Publish your application", ""),
        ("Accept offer?", "Deny offer", "No"),
        ("Accept offer?", "ParallelGateway_2", "Yes"),
        ("Recommend company?", "ExclusiveGateway_4", "No"),
        ("ExclusiveGateway_4", "Internship succesful", ""),
        ("Recommend company to a list of friends via twitter api", "ExclusiveGateway_4", ""),
    ],

    "layout": {
        "Internship process is started": 0,
        "Register for internship": 1,
        "ParallelGateway_5": 2,
        "Enter topic": 3,
        "InclusiveGateway_1": 3,
        "Enter hobbies": 4,
        "Enter experience": 4,
        "Enter expected income": 4,
        "Publish your application": 5,
        "InclusiveGateway_2": 5,
        "ParallelGateway_6": 6,
        "Recieve offer": 7,
        "Accept offer?": 8,
        "Deny offer": 9,
        "ParallelGateway_2": 9,
        "ExclusiveGateway_2": 10,
        "Accept offer": 10,
        "Invalidate all other offers": 10,
        "ParallelGateway_1": 11,
        "Begin internship": 12,
        "ParallelGateway_3": 13,
        "Write at least 3 status updates every week": 14,
        "Recieve 3 status updates from the company": 14,
        "ParallelGateway_4": 15,
        "End internship": 16,
        "Recommend company?": 17,
        "Recommend company to a list of friends via twitter api": 18,
        "ExclusiveGateway_4": 19,
        "Internship succesful": 20,
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
