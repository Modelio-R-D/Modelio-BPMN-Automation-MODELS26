#
# INQ_IP_TransactionDataRequest.py
#
# Description: INQ sends a transaction data request to IP. IP checks the request and responds with data or rejection.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "INQ_IP_TransactionDataRequest",

    "lanes": ["INQ", "IP"],

    "elements": [
        ("Start",                 START,         "INQ"),
        ("Send data request",     SEND_TASK,     "INQ"),

        ("Check request",         SERVICE_TASK,  "IP"),
        ("Request valid?",        EXCLUSIVE_GW,  "IP"),
        ("Transmit data",         SEND_TASK,     "IP"),
        ("Reject request",        SEND_TASK,     "IP"),

        ("Receive data",          RECEIVE_TASK,  "INQ"),
        ("Receive rejection",     RECEIVE_TASK,  "INQ"),
        ("End",                   END,           "INQ"),
    ],

    "flows": [
        ("Start",             "Send data request",    ""),
        ("Send data request", "Check request",        ""),

        ("Check request",     "Request valid?",       ""),
        ("Request valid?",    "Transmit data",        "Valid"),
        ("Request valid?",    "Reject request",       "Invalid"),

        ("Transmit data",     "Receive data",         ""),
        ("Reject request",    "Receive rejection",    ""),

        ("Receive data",      "End",                  ""),
        ("Receive rejection", "End",                  ""),
    ],

    "layout": {
        "Start":             0,
        "Send data request": 1,

        "Check request":     2,
        "Request valid?":    3,
        "Transmit data":     4,   # Same lane + same column as "Reject request" => auto-stacked
        "Reject request":    4,

        "Receive data":      5,   # Same lane + same column as "Receive rejection" => auto-stacked
        "Receive rejection": 5,

        "End":               6,
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
