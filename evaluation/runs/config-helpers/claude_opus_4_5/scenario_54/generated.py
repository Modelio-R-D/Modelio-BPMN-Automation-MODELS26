#
# TransactionDataRequest.py
#
# Description: INQ requests transaction data from IP, IP examines and responds
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "TransactionDataRequest",
    
    "lanes": ["INQ", "IP"],
    
    "elements": [
        # INQ Lane
        ("Start",                    START,        "INQ"),
        ("Transmit Data Request",    SEND_TASK,    "INQ"),
        ("Receive Data",             RECEIVE_TASK, "INQ"),
        ("Receive Rejection",        RECEIVE_TASK, "INQ"),
        ("End Success",              END,          "INQ"),
        ("End Rejected",             END,          "INQ"),
        
        # IP Lane
        ("Receive Request",          RECEIVE_TASK, "IP"),
        ("Check Request",            USER_TASK,    "IP"),
        ("Request Valid?",           EXCLUSIVE_GW, "IP"),
        ("Transmit Data",            SEND_TASK,    "IP"),
        ("Send Rejection",           SEND_TASK,    "IP"),
    ],
    
    "flows": [
        # INQ flow
        ("Start",                 "Transmit Data Request", ""),
        ("Transmit Data Request", "Receive Request",       ""),
        
        # IP examination flow
        ("Receive Request",       "Check Request",         ""),
        ("Check Request",         "Request Valid?",        ""),
        ("Request Valid?",        "Transmit Data",         "Yes"),
        ("Request Valid?",        "Send Rejection",        "No"),
        
        # Response flows back to INQ
        ("Transmit Data",         "Receive Data",          ""),
        ("Send Rejection",        "Receive Rejection",     ""),
        
        # INQ completion
        ("Receive Data",          "End Success",           ""),
        ("Receive Rejection",     "End Rejected",          ""),
    ],
    
    "layout": {
        # INQ Lane
        "Start":                  0,
        "Transmit Data Request":  1,
        "Receive Data":           5,
        "Receive Rejection":      5,    # Auto-stacked below Receive Data
        "End Success":            6,
        "End Rejected":           6,    # Auto-stacked below End Success
        
        # IP Lane
        "Receive Request":        2,
        "Check Request":          3,
        "Request Valid?":         4,
        "Transmit Data":          5,
        "Send Rejection":         5,    # Auto-stacked below Transmit Data
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
