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
        ("Check desired airplane type", USER_TASK, "Process 1"),
        ("Select number of seats", USER_TASK, "Process 1"),
        ("Select seat color", USER_TASK, "Process 1"),
        ("Introduce amount of water in the toilets", USER_TASK, "Process 1"),
        ("Update flight protocol", USER_TASK, "Process 1"),
        ("Display bar type", SERVICE_TASK, "Process 1"),
        ("Send customizing options", SEND_TASK, "Process 1"),
        ("Send requirements to the russian team", SEND_TASK, "Process 1"),
        ("Send requirements to the irish team", SEND_TASK, "Process 1"),
        ("Send requirements to french team", SEND_TASK, "Process 1"),
        ("Send requirements to the american team", SEND_TASK, "Process 1"),
        ("Send requirements to the italian team", SEND_TASK, "Process 1"),
        ("Send protocol to customer", SEND_TASK, "Process 1"),
        ("Receive customizing requirements", RECEIVE_TASK, "Process 1"),
        ("Receive customer confirmation", RECEIVE_TASK, "Process 1"),
        ("Receive bar components", MANUAL_TASK, "Process 1"),
        ("Assemble interior", MANUAL_TASK, "Process 1"),
        ("Flight test", MANUAL_TASK, "Process 1"),
        ("Sent plane to customer", MANUAL_TASK, "Process 1"),
        ("Ajdust errors", MANUAL_TASK, "Process 1"),
        ("Individual customizing?", EXCLUSIVE_GW, "Process 1"),
        ("Bar type", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("Test succesful", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("Get airplane request", MESSAGE_START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("Get airplane request", "Check desired airplane type", ""),
        ("Check desired airplane type", "Individual customizing?", ""),
        ("ParallelGateway_1", "Display bar type", ""),
        ("ParallelGateway_1", "Select number of seats", ""),
        ("ParallelGateway_1", "Select seat color", ""),
        ("ParallelGateway_1", "Introduce amount of water in the toilets", ""),
        ("Display bar type", "Bar type", ""),
        ("Select number of seats", "ParallelGateway_2", ""),
        ("Select seat color", "ParallelGateway_2", ""),
        ("Introduce amount of water in the toilets", "ParallelGateway_2", ""),
        ("Send customizing options", "Receive customizing requirements", ""),
        ("Receive customizing requirements", "ParallelGateway_1", ""),
        ("Send requirements to the russian team", "ExclusiveGateway_3", ""),
        ("Send requirements to the irish team", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "Receive bar components", ""),
        ("Receive bar components", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Assemble interior", ""),
        ("Sent plane to customer", "Receive customer confirmation", ""),
        ("Receive customer confirmation", "EndEvent_1", ""),
        ("Test succesful", "Ajdust errors", "No"),
        ("ParallelGateway_3", "Flight test", ""),
        ("Flight test", "Test succesful", ""),
        ("ParallelGateway_3", "Update flight protocol", ""),
        ("Update flight protocol", "Send protocol to customer", ""),
        ("Send protocol to customer", "ParallelGateway_4", ""),
        ("Test succesful", "ParallelGateway_4", "Yes"),
        ("ParallelGateway_4", "Sent plane to customer", ""),
        ("Send requirements to french team", "ExclusiveGateway_3", ""),
        ("Send requirements to the american team", "ExclusiveGateway_3", ""),
        ("Send requirements to the italian team", "ExclusiveGateway_3", ""),
        ("Assemble interior", "ParallelGateway_3", ""),
        ("Ajdust errors", "Flight test", ""),
        ("Individual customizing?", "Send customizing options", "Yes"),
        ("Individual customizing?", "Assemble interior", "No"),
        ("Bar type", "Send requirements to the russian team", "Vodka bar"),
        ("Bar type", "Send requirements to the irish team", "Whiskey bar"),
        ("Bar type", "Send requirements to french team", "Wine bar"),
        ("Bar type", "Send requirements to the american team", "Cocktail bar"),
        ("Bar type", "Send requirements to the italian team", "Aperol bar"),
    ],

    "layout": {
        "Get airplane request": 0,
        "Check desired airplane type": 1,
        "Individual customizing?": 2,
        "Send customizing options": 3,
        "Receive customizing requirements": 4,
        "ParallelGateway_3": 4,
        "ParallelGateway_1": 5,
        "Update flight protocol": 5,
        "Display bar type": 6,
        "Select number of seats": 6,
        "Select seat color": 6,
        "Introduce amount of water in the toilets": 6,
        "Test succesful": 6,
        "Send protocol to customer": 6,
        "Bar type": 7,
        "Ajdust errors": 7,
        "ParallelGateway_4": 7,
        "Assemble interior": 8,
        "Flight test": 8,
        "Send requirements to the russian team": 8,
        "Send requirements to the irish team": 8,
        "Send requirements to french team": 8,
        "Send requirements to the american team": 8,
        "Send requirements to the italian team": 8,
        "Sent plane to customer": 8,
        "ExclusiveGateway_3": 9,
        "Receive customer confirmation": 9,
        "Receive bar components": 10,
        "EndEvent_1": 10,
        "ParallelGateway_2": 11,
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
