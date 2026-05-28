#
# CreditScoringRequest.py
#
# Description: Sales clerk requests credit scoring; banking system requests scoring from agency with quick (L1) result or delayed (L2) result path.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "CreditScoringRequest",

    "lanes": ["Sales Clerk", "Banking System", "Credit Agency"],

    "elements": [
        ("Start",                     START,         "Sales Clerk"),
        ("Request credit scoring",     USER_TASK,     "Sales Clerk"),
        ("View scoring result",        USER_TASK,     "Sales Clerk"),
        ("End",                       END,           "Sales Clerk"),

        ("Start scoring process",      SERVICE_TASK,  "Banking System"),
        ("Send scoring request",       SEND_TASK,     "Banking System"),
        ("Receive result",             RECEIVE_TASK,  "Banking System"),
        ("Receive delay notice",       RECEIVE_TASK,  "Banking System"),
        ("Display delay message",      SERVICE_TASK,  "Banking System"),
        ("Wait for final result",      RECEIVE_TASK,  "Banking System"),
        ("Update frontend with result",SERVICE_TASK,  "Banking System"),

        ("Receive scoring request",    RECEIVE_TASK,  "Credit Agency"),
        ("Quick scoring L1",           SERVICE_TASK,  "Credit Agency"),
        ("Result available?",          EXCLUSIVE_GW,  "Credit Agency"),
        ("Send result",                SEND_TASK,     "Credit Agency"),
        ("Send delay notice",          SEND_TASK,     "Credit Agency"),
        ("Level 2 scoring",            SERVICE_TASK,  "Credit Agency"),
        ("Send final result",          SEND_TASK,     "Credit Agency"),
    ],

    "flows": [
        ("Start", "Request credit scoring", ""),
        ("Request credit scoring", "Start scoring process", ""),
        ("Start scoring process", "Send scoring request", ""),

        ("Send scoring request", "Receive scoring request", ""),
        ("Receive scoring request", "Quick scoring L1", ""),
        ("Quick scoring L1", "Result available?", ""),

        ("Result available?", "Send result", "Immediate"),
        ("Result available?", "Send delay notice", "Delayed"),

        ("Send result", "Receive result", ""),
        ("Receive result", "Update frontend with result", ""),

        ("Send delay notice", "Receive delay notice", ""),
        ("Receive delay notice", "Display delay message", ""),
        ("Display delay message", "Wait for final result", ""),

        ("Send delay notice", "Level 2 scoring", ""),
        ("Level 2 scoring", "Send final result", ""),
        ("Send final result", "Wait for final result", ""),

        ("Wait for final result", "Update frontend with result", ""),
        ("Update frontend with result", "View scoring result", ""),
        ("View scoring result", "End", ""),
    ],

    "layout": {
        "Start":                      0,
        "Request credit scoring":     1,

        "Start scoring process":      2,
        "Send scoring request":       3,

        "Receive scoring request":    4,
        "Quick scoring L1":           5,
        "Result available?":          6,
        "Send result":                7,   # auto-stacked with Send delay notice (same lane/column)
        "Send delay notice":          7,

        "Receive result":             8,   # auto-stacked with Receive delay notice (same lane/column)
        "Receive delay notice":       8,
        "Display delay message":      9,
        "Wait for final result":      10,
        "Update frontend with result":11,

        "Level 2 scoring":            9,
        "Send final result":          10,

        "View scoring result":        12,
        "End":                        13,
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
