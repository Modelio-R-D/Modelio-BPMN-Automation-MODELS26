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
        ("check case", USER_TASK, "Process 1"),
        ("send request for payment", USER_TASK, "Process 1"),
        ("close case", USER_TASK, "Process 1"),
        ("send reminder", USER_TASK, "Process 1"),
        ("check reasoning", USER_TASK, "Process 1"),
        ("close case", USER_TASK, "Process 1"),
        ("hand over to collection agency", USER_TASK, "Process 1"),
        ("make booking", USER_TASK, "Process 1"),
        ("close case", USER_TASK, "Process 1"),
        ("recourse possible?", EXCLUSIVE_GW, "Process 1"),
        ("OK?", EXCLUSIVE_GW, "Process 1"),
        ("EventBasedGateway_1", EVENT_BASED_GW, "Process 1"),
        ("probable recourse detected", MESSAGE_START, "Process 1"),
        ("case closed", END, "Process 1"),
        ("case closed", END, "Process 1"),
        ("case open", END, "Process 1"),
        ("case closed", END, "Process 1"),
        ("disagreement letter received", MESSAGE_CATCH, "Process 1"),
        ("Reminder is due", TIMER_CATCH, "Process 1"),
        ("Money received", MESSAGE_CATCH, "Process 1"),
    ],

    "flows": [
        ("probable recourse detected", "check case", ""),
        ("check case", "recourse possible?", ""),
        ("recourse possible?", "send request for payment", "yes"),
        ("recourse possible?", "close case", "no"),
        ("close case", "case closed", ""),
        ("send request for payment", "send reminder", ""),
        ("send reminder", "EventBasedGateway_1", ""),
        ("EventBasedGateway_1", "disagreement letter received", ""),
        ("disagreement letter received", "check reasoning", ""),
        ("check reasoning", "OK?", ""),
        ("OK?", "close case", "yes"),
        ("close case", "case closed", ""),
        ("EventBasedGateway_1", "Reminder is due", ""),
        ("Reminder is due", "hand over to collection agency", ""),
        ("OK?", "hand over to collection agency", "no"),
        ("hand over to collection agency", "case open", ""),
        ("EventBasedGateway_1", "Money received", ""),
        ("Money received", "make booking", ""),
        ("make booking", "close case", ""),
        ("close case", "case closed", ""),
    ],

    "layout": {
        "probable recourse detected": 0,
        "check case": 1,
        "recourse possible?": 2,
        "send request for payment": 3,
        "send reminder": 4,
        "case closed": 4,
        "EventBasedGateway_1": 5,
        "disagreement letter received": 6,
        "Reminder is due": 6,
        "Money received": 6,
        "check reasoning": 7,
        "make booking": 7,
        "OK?": 8,
        "case open": 8,
        "close case": 9,
        "hand over to collection agency": 9,
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
