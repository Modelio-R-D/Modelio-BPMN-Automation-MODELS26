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
        ("Sign contract", USER_TASK, "Process 1"),
        ("Conduct site visit", USER_TASK, "Process 1"),
        ("Execute contract", USER_TASK, "Process 1"),
        ("Identify need for new supplier or vendor", USER_TASK, "Process 1"),
        ("Evaluate proposal", USER_TASK, "Process 1"),
        ("Receive supplier proposals", USER_TASK, "Process 1"),
        ("Begin contract negotiations", USER_TASK, "Process 1"),
        ("Select supplier", USER_TASK, "Process 1"),
        ("Conduct interview", USER_TASK, "Process 1"),
        ("Issue request for proposals (RFP)", USER_TASK, "Process 1"),
        ("Onboard supplier", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("Conduct site visit", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_4", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_4", "Conduct interview", ""),
        ("ExclusiveGateway_2", "Select supplier", ""),
        ("Execute contract", "End", ""),
        ("Receive supplier proposals", "ExclusiveGateway_3", ""),
        ("Start", "Identify need for new supplier or vendor", ""),
        ("ExclusiveGateway_3", "Evaluate proposal", ""),
        ("Conduct interview", "ExclusiveGateway_1", ""),
        ("Begin contract negotiations", "Sign contract", ""),
        ("ExclusiveGateway_4", "Conduct site visit", ""),
        ("ExclusiveGateway_1", "ExclusiveGateway_2", ""),
        ("Sign contract", "Onboard supplier", ""),
        ("Issue request for proposals (RFP)", "Receive supplier proposals", ""),
        ("Evaluate proposal", "ExclusiveGateway_4", ""),
        ("Onboard supplier", "Execute contract", ""),
        ("ExclusiveGateway_2", "ExclusiveGateway_3", ""),
        ("Select supplier", "Begin contract negotiations", ""),
        ("Identify need for new supplier or vendor", "Issue request for proposals (RFP)", ""),
    ],

    "layout": {
        "Start": 0,
        "Identify need for new supplier or vendor": 1,
        "Issue request for proposals (RFP)": 2,
        "Receive supplier proposals": 3,
        "Evaluate proposal": 5,
        "ExclusiveGateway_4": 6,
        "Conduct interview": 7,
        "Conduct site visit": 7,
        "ExclusiveGateway_1": 8,
        "ExclusiveGateway_2": 8,
        "ExclusiveGateway_3": 9,
        "Select supplier": 9,
        "Begin contract negotiations": 10,
        "Sign contract": 11,
        "Onboard supplier": 12,
        "Execute contract": 13,
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
