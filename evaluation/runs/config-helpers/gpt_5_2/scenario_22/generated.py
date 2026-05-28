#
# RecourseHandling.py
#
# Description: Handle possible recourse/subrogation against an insurant: assess feasibility, request payment, wait for payment or disagreement (or deadline), then book/close or forward to collection.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RecourseHandling",

    "lanes": [
        "Claims Handler",
        "Collection Agency",
    ],

    "elements": [
        ("Subrogation hint received",      MESSAGE_START,   "Claims Handler"),
        ("Check case",                    USER_TASK,       "Claims Handler"),
        ("Recourse possible?",            EXCLUSIVE_GW,     "Claims Handler"),

        ("Send request for payment",      SEND_TASK,       "Claims Handler"),
        ("Set reminder",                  USER_TASK,       "Claims Handler"),

        ("Wait for payment or response",  EVENT_BASED_GW,   "Claims Handler"),
        ("Payment received",              MESSAGE_CATCH,    "Claims Handler"),
        ("Disagreement received",         MESSAGE_CATCH,    "Claims Handler"),
        ("Disagreement deadline reached", TIMER_CATCH,      "Claims Handler"),

        ("Book payment",                  SERVICE_TASK,     "Claims Handler"),

        ("Check disagreement reasoning",  USER_TASK,        "Claims Handler"),
        ("Insurant right?",               EXCLUSIVE_GW,     "Claims Handler"),

        ("Forward to collection agency",  USER_TASK,        "Collection Agency"),

        ("Close case",                    USER_TASK,        "Claims Handler"),
        ("End",                           END,              "Claims Handler"),
    ],

    "flows": [
        ("Subrogation hint received",      "Check case",                    ""),
        ("Check case",                    "Recourse possible?",            ""),

        ("Recourse possible?",            "Send request for payment",       "Yes"),
        ("Recourse possible?",            "Close case",                    "No"),

        ("Send request for payment",      "Set reminder",                  ""),
        ("Set reminder",                  "Wait for payment or response",   ""),

        # Event-based outcomes
        ("Wait for payment or response",  "Payment received",              "Payment"),
        ("Wait for payment or response",  "Disagreement received",         "Disagreement"),
        ("Wait for payment or response",  "Disagreement deadline reached", "Deadline"),

        # Payment path
        ("Payment received",              "Book payment",                  ""),
        ("Book payment",                  "Close case",                    ""),

        # Disagreement path
        ("Disagreement received",         "Check disagreement reasoning",   ""),
        ("Check disagreement reasoning",  "Insurant right?",               ""),
        ("Insurant right?",               "Close case",                    "Yes"),
        ("Insurant right?",               "Forward to collection agency",  "No"),

        # Deadline path (no money received)
        ("Disagreement deadline reached", "Forward to collection agency",  ""),

        # After forwarding
        ("Forward to collection agency",  "Close case",                    ""),

        ("Close case",                    "End",                           ""),
    ],

    "layout": {
        "Subrogation hint received":      0,
        "Check case":                    1,
        "Recourse possible?":            2,

        "Send request for payment":      3,
        "Set reminder":                  4,

        "Wait for payment or response":  5,

        # Same lane + same column => auto-stacked
        "Payment received":              6,
        "Disagreement received":         6,
        "Disagreement deadline reached": 6,

        # Same lane + same column => auto-stacked (different branches)
        "Book payment":                  7,
        "Check disagreement reasoning":  7,

        "Insurant right?":               8,

        "Forward to collection agency":  9,

        "Close case":                    10,
        "End":                           11,
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
