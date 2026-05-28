#
# TransactionDataRequest.py
#
# Description: INQ requests data from IP, IP checks and responds.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "TransactionDataRequest",
    
    "lanes": ["INQ", "IP"],
    
    "elements": [
        # INQ Lane
        ("Start", START, "INQ"),
        ("Transmit Data Request", SEND_TASK, "INQ"),
        ("End", END, "INQ"),
        
        # IP Lane
        ("Check Request", SERVICE_TASK, "IP"),
        ("Valid?", EXCLUSIVE_GW, "IP"),
        ("Transmit Data", SEND_TASK, "IP"),
        ("Reject Request", TASK, "IP"),
    ],
    
    "flows": [
        ("Start", "Transmit Data Request", ""),
        ("Transmit Data Request", "Check Request", ""),
        ("Check Request", "Valid?", ""),
        ("Valid?", "Transmit Data", "Approved"),
        ("Valid?", "Reject Request", "Rejected"),
        ("Transmit Data", "End", ""),
        ("Reject Request", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Transmit Data Request": 1,
        "Check Request": 2,
        "Valid?": 3,
        # Column 4: Auto-stacking (Transmit Data on top, Reject Request below)
        "Transmit Data": 4,
        "Reject Request": 4,
        "End": 5,
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
