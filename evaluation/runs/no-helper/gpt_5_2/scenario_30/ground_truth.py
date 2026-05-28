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
        ("Send invites to 10 people", USER_TASK, "Process 1"),
        ("Ask which games do they want to play", USER_TASK, "Process 1"),
        ("Appoint a date", USER_TASK, "Process 1"),
        ("Ask friends how much beer they would like", USER_TASK, "Process 1"),
        ("Order beer for that date", USER_TASK, "Process 1"),
        ("Find where can you download the games", USER_TASK, "Process 1"),
        ("Reserve that day", SERVICE_TASK, "Process 1"),
        ("Download the missing games", SERVICE_TASK, "Process 1"),
        ("Send a notification that the LAN party will be held on that date", SERVICE_TASK, "Process 1"),
        ("How many people can play on that date?", EXCLUSIVE_GW, "Process 1"),
        ("Do we have all the games?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("Do you have enough beer?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Download successful?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Wish for a LAN gameparty", START, "Process 1"),
        ("LAN party done", END, "Process 1"),
        ("Few hours, until the user has all the games that they want to play", TIMER_CATCH, "Process 1"),
        ("Few hours, until all people reply if they can play on that date", TIMER_CATCH, "Process 1"),
        ("Few hours, until all people reply with t he amount of beer", TIMER_CATCH, "Process 1"),
    ],

    "flows": [
        ("Wish for a LAN gameparty", "Send invites to 10 people", ""),
        ("Send invites to 10 people", "Ask which games do they want to play", ""),
        ("Ask which games do they want to play", "Few hours, until the user has all the games that they want to play", ""),
        ("Few hours, until the user has all the games that they want to play", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Appoint a date", ""),
        ("ParallelGateway_1", "Do we have all the games?", ""),
        ("Appoint a date", "Few hours, until all people reply if they can play on that date", ""),
        ("Few hours, until all people reply if they can play on that date", "How many people can play on that date?", ""),
        ("How many people can play on that date?", "Appoint a date", "Less then 8 people can play on that date"),
        ("How many people can play on that date?", "Reserve that day", "8 or more people can play on that date"),
        ("ParallelGateway_2", "Ask friends how much beer they would like", ""),
        ("Ask friends how much beer they would like", "Few hours, until all people reply with t he amount of beer", ""),
        ("Do you have enough beer?", "Order beer for that date", "No"),
        ("Order beer for that date", "ExclusiveGateway_5", ""),
        ("Do we have all the games?", "Find where can you download the games", "No"),
        ("Find where can you download the games", "Download the missing games", ""),
        ("Send a notification that the LAN party will be held on that date", "LAN party done", ""),
        ("Reserve that day", "ParallelGateway_2", ""),
        ("Download successful?", "ExclusiveGateway_3", "Yes"),
        ("Download successful?", "Download the missing games", "No"),
        ("ExclusiveGateway_5", "Send a notification that the LAN party will be held on that date", ""),
        ("Few hours, until all people reply with t he amount of beer", "Do you have enough beer?", ""),
        ("Do you have enough beer?", "ExclusiveGateway_5", "Yes"),
        ("ExclusiveGateway_3", "ParallelGateway_2", ""),
        ("Do we have all the games?", "ExclusiveGateway_3", "Yes"),
        ("Download the missing games", "Download successful?", ""),
    ],

    "layout": {
        "Wish for a LAN gameparty": 0,
        "Send invites to 10 people": 1,
        "Ask which games do they want to play": 2,
        "Few hours, until the user has all the games that they want to play": 3,
        "ParallelGateway_1": 4,
        "Do we have all the games?": 5,
        "Few hours, until all people reply if they can play on that date": 6,
        "Find where can you download the games": 6,
        "How many people can play on that date?": 7,
        "Appoint a date": 8,
        "Reserve that day": 8,
        "Download successful?": 8,
        "Ask friends how much beer they would like": 8,
        "ExclusiveGateway_3": 9,
        "Download the missing games": 9,
        "ParallelGateway_2": 9,
        "Few hours, until all people reply with t he amount of beer": 9,
        "Do you have enough beer?": 10,
        "Order beer for that date": 11,
        "ExclusiveGateway_5": 12,
        "Send a notification that the LAN party will be held on that date": 13,
        "LAN party done": 14,
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
