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
        ("select course", USER_TASK, "Process 1"),
        ("select specific course", USER_TASK, "Process 1"),
        ("check if registered at eligible university", USER_TASK, "Process 1"),
        ("log into account", USER_TASK, "Process 1"),
        ("register account", USER_TASK, "Process 1"),
        ("request activation", USER_TASK, "Process 1"),
        ("connect to twitter account", USER_TASK, "Process 1"),
        ("invite friends to course", USER_TASK, "Process 1"),
        ("provide payment info", USER_TASK, "Process 1"),
        ("check if another course is interesting", USER_TASK, "Process 1"),
        ("system shows parallel courses and dates", SERVICE_TASK, "Process 1"),
        ("system checks eligibility", SERVICE_TASK, "Process 1"),
        ("system issues course tickets", SERVICE_TASK, "Process 1"),
        ("free spots?", EXCLUSIVE_GW, "Process 1"),
        ("already registered?", EXCLUSIVE_GW, "Process 1"),
        ("eligible university?", EXCLUSIVE_GW, "Process 1"),
        ("person eligible?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_9", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_10", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("wish to enroll in course", START, "Process 1"),
        ("end process", END, "Process 1"),
    ],

    "flows": [
        ("select course", "free spots?", ""),
        ("system shows parallel courses and dates", "select specific course", ""),
        ("check if registered at eligible university", "eligible university?", ""),
        ("eligible university?", "request activation", "no"),
        ("request activation", "system checks eligibility", ""),
        ("system checks eligibility", "person eligible?", ""),
        ("connect to twitter account", "invite friends to course", ""),
        ("free spots?", "system shows parallel courses and dates", "yes"),
        ("already registered?", "check if registered at eligible university", "no"),
        ("log into account", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "connect to twitter account", ""),
        ("check if another course is interesting", "ExclusiveGateway_5", ""),
        ("ParallelGateway_2", "system issues course tickets", ""),
        ("invite friends to course", "ParallelGateway_2", ""),
        ("provide payment info", "ParallelGateway_2", ""),
        ("free spots?", "check if another course is interesting", "no"),
        ("select specific course", "already registered?", ""),
        ("wish to enroll in course", "ExclusiveGateway_6", ""),
        ("ExclusiveGateway_6", "select course", ""),
        ("ExclusiveGateway_5", "ExclusiveGateway_6", "yes"),
        ("system issues course tickets", "ExclusiveGateway_7", ""),
        ("ExclusiveGateway_7", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_8", "end process", ""),
        ("ExclusiveGateway_5", "ExclusiveGateway_7", "no"),
        ("person eligible?", "ExclusiveGateway_8", "no"),
        ("ParallelGateway_1", "provide payment info", ""),
        ("ExclusiveGateway_9", "register account", ""),
        ("already registered?", "ExclusiveGateway_10", "yes"),
        ("ExclusiveGateway_10", "log into account", ""),
        ("register account", "ExclusiveGateway_10", ""),
        ("person eligible?", "ExclusiveGateway_9", "yes"),
        ("eligible university?", "ExclusiveGateway_9", "yes"),
    ],

    "layout": {
        "wish to enroll in course": 0,
        "select course": 2,
        "free spots?": 3,
        "system shows parallel courses and dates": 4,
        "check if another course is interesting": 4,
        "select specific course": 5,
        "ExclusiveGateway_5": 5,
        "ExclusiveGateway_6": 6,
        "already registered?": 6,
        "check if registered at eligible university": 7,
        "eligible university?": 8,
        "log into account": 8,
        "end process": 8,
        "request activation": 9,
        "ParallelGateway_1": 9,
        "system checks eligibility": 10,
        "register account": 10,
        "connect to twitter account": 10,
        "provide payment info": 10,
        "ExclusiveGateway_10": 11,
        "person eligible?": 11,
        "invite friends to course": 11,
        "ExclusiveGateway_8": 12,
        "ExclusiveGateway_9": 12,
        "ParallelGateway_2": 12,
        "system issues course tickets": 13,
        "ExclusiveGateway_7": 14,
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
