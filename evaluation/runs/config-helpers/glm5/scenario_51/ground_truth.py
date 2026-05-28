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
        ("Employee submits a vacation request", USER_TASK, "Process 1"),
        ("Requirement is registered", USER_TASK, "Process 1"),
        ("Employee's supervisor receive the request", USER_TASK, "Process 1"),
        ("Supervisor approve or reject the request", USER_TASK, "Process 1"),
        ("Application is returned to employee", USER_TASK, "Process 1"),
        ("Notification is generated to the HR Representative", USER_TASK, "Process 1"),
        ("HR Representative complete the respective management procedures", USER_TASK, "Process 1"),
        ("Employee can check rejection reasons", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "Employee submits a vacation request", ""),
        ("Employee submits a vacation request", "Requirement is registered", ""),
        ("Requirement is registered", "Employee's supervisor receive the request", ""),
        ("Employee's supervisor receive the request", "Supervisor approve or reject the request", ""),
        ("Supervisor approve or reject the request", "ExclusiveGateway_1", ""),
        ("Notification is generated to the HR Representative", "HR Representative complete the respective management procedures", ""),
        ("HR Representative complete the respective management procedures", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "EndEvent_1", ""),
        ("ExclusiveGateway_1", "Application is returned to employee", "rejected"),
        ("ExclusiveGateway_1", "Notification is generated to the HR Representative", "approved"),
        ("Application is returned to employee", "Employee can check rejection reasons", ""),
        ("Employee can check rejection reasons", "ExclusiveGateway_2", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Employee submits a vacation request": 1,
        "Requirement is registered": 2,
        "Employee's supervisor receive the request": 3,
        "Supervisor approve or reject the request": 4,
        "ExclusiveGateway_1": 5,
        "Application is returned to employee": 6,
        "Notification is generated to the HR Representative": 6,
        "Employee can check rejection reasons": 7,
        "HR Representative complete the respective management procedures": 7,
        "ExclusiveGateway_2": 8,
        "EndEvent_1": 9,
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
