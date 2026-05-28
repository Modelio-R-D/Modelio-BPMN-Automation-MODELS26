#
# Building_a_House.py
#
# Description: BPMN process for building a tree house: requirements + architect iterations, materials ordering, recruiting friends, building, and party planning.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Building a House",

    "lanes": ["Builder", "Architect", "Online Stores", "Friends"],

    "elements": [
        ("Start",                     START,            "Builder"),
        ("Collect Requirements",       USER_TASK,        "Builder"),
        ("Send Requirements to Architect", SEND_TASK,    "Builder"),

        ("Review Requirements",        USER_TASK,        "Architect"),
        ("Create Draft Plan",          USER_TASK,        "Architect"),
        ("Send Draft Plan",            SEND_TASK,        "Architect"),

        ("Receive Draft Plan",         RECEIVE_TASK,     "Builder"),
        ("Need Changes?",              EXCLUSIVE_GW,     "Builder"),
        ("Refine Requirements",        USER_TASK,        "Builder"),
        ("Send Additional Requirements", SEND_TASK,      "Builder"),

        ("Incorporate Changes",        USER_TASK,        "Architect"),
        ("Send Updated Draft",         SEND_TASK,        "Architect"),

        ("Approve Final Plan",         USER_TASK,        "Builder"),
        ("Create Materials List",      USER_TASK,        "Builder"),

        ("Procure And Recruit",        PARALLEL_GW,      "Builder"),

        ("Order Materials",            PARALLEL_GW,      "Builder"),
        ("Order Lumber",               SERVICE_TASK,     "Online Stores"),
        ("Order Hardware",             SERVICE_TASK,     "Online Stores"),
        ("Order Tools",                SERVICE_TASK,     "Online Stores"),
        ("Orders Processed",           PARALLEL_GW,      "Builder"),
        ("Materials Delivered",        RECEIVE_TASK,     "Builder"),

        ("Request Friends To Build",   SEND_TASK,        "Builder"),
        ("Friends Confirm",            USER_TASK,        "Friends"),
        ("Friends Ready",              RECEIVE_TASK,     "Builder"),

        ("Ready To Build",             PARALLEL_GW,      "Builder"),
        ("Build Tree House",           MANUAL_TASK,      "Friends"),

        ("Send Party Invitations",     SEND_TASK,        "Builder"),
        ("Friends Receive Invitations", RECEIVE_TASK,    "Friends"),
        ("Send RSVP",                  SEND_TASK,        "Friends"),
        ("Receive RSVPs",              RECEIVE_TASK,     "Builder"),
        ("Create Attendee List",       USER_TASK,        "Builder"),
        ("Buy Snacks",                 SERVICE_TASK,     "Builder"),

        ("End",                       END,              "Builder"),
    ],

    "data_objects": [
        ("Requirements Doc", "Builder", 1),
        ("Draft Plan",       "Builder", 6),
        ("Final Plan",       "Builder", 8),
        ("Materials List",   "Builder", 9),
        ("Attendee List",    "Builder", 21),
    ],

    "data_associations": [
        ("Collect Requirements",          "Requirements Doc"),
        ("Requirements Doc",              "Send Requirements to Architect"),

        ("Receive Draft Plan",            "Draft Plan"),
        ("Draft Plan",                    "Refine Requirements"),

        ("Approve Final Plan",            "Final Plan"),
        ("Final Plan",                    "Create Materials List"),

        ("Create Materials List",         "Materials List"),
        ("Materials List",                "Order Lumber"),
        ("Materials List",                "Order Hardware"),
        ("Materials List",                "Order Tools"),

        ("Create Attendee List",          "Attendee List"),
        ("Attendee List",                 "Buy Snacks"),
    ],

    "flows": [
        ("Start",                     "Collect Requirements",            ""),
        ("Collect Requirements",       "Send Requirements to Architect",  ""),
        ("Send Requirements to Architect", "Review Requirements",         ""),

        ("Review Requirements",        "Create Draft Plan",               ""),
        ("Create Draft Plan",          "Send Draft Plan",                 ""),
        ("Send Draft Plan",            "Receive Draft Plan",              ""),

        ("Receive Draft Plan",         "Need Changes?",                   ""),
        ("Need Changes?",              "Refine Requirements",             "More changes"),
        ("Need Changes?",              "Approve Final Plan",              "Approved"),

        ("Refine Requirements",        "Send Additional Requirements",    ""),
        ("Send Additional Requirements","Incorporate Changes",            ""),
        ("Incorporate Changes",        "Send Updated Draft",              ""),
        ("Send Updated Draft",         "Receive Draft Plan",              ""),

        ("Approve Final Plan",         "Create Materials List",           ""),
        ("Create Materials List",      "Procure And Recruit",             ""),

        ("Procure And Recruit",        "Order Materials",                 ""),
        ("Procure And Recruit",        "Request Friends To Build",        ""),

        ("Order Materials",            "Order Lumber",                    ""),
        ("Order Materials",            "Order Hardware",                  ""),
        ("Order Materials",            "Order Tools",                     ""),

        ("Order Lumber",               "Orders Processed",                ""),
        ("Order Hardware",             "Orders Processed",                ""),
        ("Order Tools",                "Orders Processed",                ""),
        ("Orders Processed",           "Materials Delivered",             ""),

        ("Request Friends To Build",   "Friends Confirm",                 ""),
        ("Friends Confirm",            "Friends Ready",                   ""),

        ("Materials Delivered",        "Ready To Build",                  ""),
        ("Friends Ready",              "Ready To Build",                  ""),

        ("Ready To Build",             "Build Tree House",                ""),
        ("Build Tree House",           "Send Party Invitations",          ""),

        ("Send Party Invitations",     "Friends Receive Invitations",     ""),
        ("Friends Receive Invitations","Send RSVP",                       ""),
        ("Send RSVP",                  "Receive RSVPs",                   ""),

        ("Receive RSVPs",              "Create Attendee List",            ""),
        ("Create Attendee List",       "Buy Snacks",                      ""),
        ("Buy Snacks",                 "End",                             ""),
    ],

    "layout": {
        "Start":                          0,
        "Collect Requirements":            1,
        "Send Requirements to Architect":  2,

        "Review Requirements":             3,
        "Create Draft Plan":               4,
        "Send Draft Plan":                 5,

        "Receive Draft Plan":              6,
        "Need Changes?":                   7,
        "Refine Requirements":             8,
        "Approve Final Plan":              8,
        "Send Additional Requirements":    9,

        "Incorporate Changes":            10,
        "Send Updated Draft":             11,

        "Create Materials List":           9,

        "Procure And Recruit":            10,

        "Order Materials":                11,
        "Request Friends To Build":       11,

        "Order Lumber":                   12,
        "Order Hardware":                 12,
        "Order Tools":                    12,

        "Orders Processed":               13,
        "Friends Confirm":                12,
        "Friends Ready":                  13,

        "Materials Delivered":            14,
        "Ready To Build":                 15,
        "Build Tree House":               16,

        "Send Party Invitations":         17,
        "Friends Receive Invitations":    18,
        "Send RSVP":                      19,
        "Receive RSVPs":                  20,
        "Create Attendee List":           21,
        "Buy Snacks":                     22,
        "End":                            23,
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
