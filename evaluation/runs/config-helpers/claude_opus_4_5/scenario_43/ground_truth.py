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
        ("Mechanic check a car and enter problems", USER_TASK, "Process 1"),
        ("Pay per App", USER_TASK, "Process 1"),
        ("Save repair infos", USER_TASK, "Process 1"),
        ("Make appointment for next service", USER_TASK, "Process 1"),
        ("Make new appointment", USER_TASK, "Process 1"),
        ("Check if car is still registered?", SERVICE_TASK, "Process 1"),
        ("User fined", SERVICE_TASK, "Process 1"),
        ("Receive updates while waiting", SERVICE_TASK, "Process 1"),
        ("Send 'Pickerl'", SERVICE_TASK, "Process 1"),
        ("Check appointment for service", SERVICE_TASK, "Process 1"),
        ("Send reminder notification to user", SEND_TASK, "Process 1"),
        ("Received a notificiation", RECEIVE_TASK, "Process 1"),
        ("Bring Documents for Registration", MANUAL_TASK, "Process 1"),
        ("Registered?", EXCLUSIVE_GW, "Process 1"),
        ("Gone to service?", EXCLUSIVE_GW, "Process 1"),
        ("> 30 days?", EXCLUSIVE_GW, "Process 1"),
        ("Repair done?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "Bring Documents for Registration", ""),
        ("Bring Documents for Registration", "Check if car is still registered?", ""),
        ("Check if car is still registered?", "Registered?", ""),
        ("Registered?", "Bring Documents for Registration", "no"),
        ("Send reminder notification to user", "Received a notificiation", ""),
        ("Gone to service?", "Mechanic check a car and enter problems", "yes"),
        ("> 30 days?", "User fined", "yes"),
        ("Mechanic check a car and enter problems", "Receive updates while waiting", ""),
        ("Receive updates while waiting", "Repair done?", ""),
        ("Repair done?", "Pay per App", "yes"),
        ("Pay per App", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Save repair infos", ""),
        ("ParallelGateway_1", "Send 'Pickerl'", ""),
        ("Save repair infos", "ParallelGateway_2", ""),
        ("Send 'Pickerl'", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Make appointment for next service", ""),
        ("Gone to service?", "> 30 days?", "no"),
        ("Repair done?", "Receive updates while waiting", "no"),
        ("Make appointment for next service", "EndEvent_1", ""),
        ("Received a notificiation", "Gone to service?", ""),
        ("Check appointment for service", "Send reminder notification to user", ""),
        ("Registered?", "Check appointment for service", "yes"),
        ("User fined", "Make new appointment", ""),
        ("Make new appointment", "Check appointment for service", ""),
        ("> 30 days?", "Send reminder notification to user", "no"),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Check if car is still registered?": 2,
        "Registered?": 3,
        "Bring Documents for Registration": 4,
        "Received a notificiation": 6,
        "Gone to service?": 7,
        "Mechanic check a car and enter problems": 8,
        "> 30 days?": 8,
        "Send reminder notification to user": 9,
        "User fined": 9,
        "Repair done?": 10,
        "Make new appointment": 10,
        "Check appointment for service": 11,
        "Receive updates while waiting": 11,
        "Pay per App": 11,
        "ParallelGateway_1": 12,
        "Save repair infos": 13,
        "Send 'Pickerl'": 13,
        "ParallelGateway_2": 14,
        "Make appointment for next service": 15,
        "EndEvent_1": 16,
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
