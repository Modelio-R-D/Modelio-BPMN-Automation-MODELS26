#
# EvanstonianRoomService.py
#
# Description: Room service order handling at The Evanstonian (kitchen + optional sommelier + waiter prep in parallel, then delivery and billing).
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EvanstonianRoomService",

    "lanes": ["Guest", "Room Service Manager", "Kitchen", "Sommelier", "Waiter"],

    "elements": [
        ("Call room service",                    START,          "Guest"),

        ("Take down order",                      USER_TASK,      "Room Service Manager"),
        ("Include alcohol?",                     INCLUSIVE_GW,   "Room Service Manager"),

        ("Submit order ticket to kitchen",       SEND_TASK,      "Room Service Manager"),
        ("Send beverage order to sommelier",     SEND_TASK,      "Room Service Manager"),
        ("Assign order to waiter",               USER_TASK,      "Room Service Manager"),

        ("Prepare food",                         MANUAL_TASK,    "Kitchen"),
        ("Fetch wine and prepare alcohol",       MANUAL_TASK,    "Sommelier"),
        ("Ready cart and nonalcoholic drinks",   MANUAL_TASK,    "Waiter"),

        ("All items ready",                      INCLUSIVE_GW,   "Waiter"),
        ("Deliver order to guest room",          MANUAL_TASK,    "Waiter"),
        ("Return to room-service station",       MANUAL_TASK,    "Waiter"),

        ("Bill now?",                            EXCLUSIVE_GW,   "Waiter"),
        ("Wait until free to bill",              TIMER_CATCH,    "Waiter"),
        ("Debit guest account",                  SERVICE_TASK,   "Waiter"),

        ("End",                                  END,            "Waiter"),
    ],

    "flows": [
        ("Call room service",                  "Take down order",                    ""),
        ("Take down order",                    "Include alcohol?",                   ""),

        # Inclusive split: kitchen + waiter always, sommelier only when alcohol is included (about 80%)
        ("Include alcohol?",                   "Submit order ticket to kitchen",     "Food"),
        ("Include alcohol?",                   "Assign order to waiter",             "Waiter"),
        ("Include alcohol?",                   "Send beverage order to sommelier",   "Alcohol (80%)"),

        ("Submit order ticket to kitchen",     "Prepare food",                       ""),
        ("Send beverage order to sommelier",   "Fetch wine and prepare alcohol",     ""),
        ("Assign order to waiter",             "Ready cart and nonalcoholic drinks", ""),

        # Join (wait for whichever branches were activated)
        ("Prepare food",                       "All items ready",                    ""),
        ("Fetch wine and prepare alcohol",     "All items ready",                    ""),
        ("Ready cart and nonalcoholic drinks", "All items ready",                    ""),

        ("All items ready",                    "Deliver order to guest room",        ""),
        ("Deliver order to guest room",        "Return to room-service station",     ""),

        # Billing may be delayed if waiter has another order to handle
        ("Return to room-service station",     "Bill now?",                          ""),
        ("Bill now?",                          "Debit guest account",                "Yes"),
        ("Bill now?",                          "Wait until free to bill",            "No"),
        ("Wait until free to bill",            "Debit guest account",                ""),

        ("Debit guest account",                "End",                                ""),
    ],

    "layout": {
        "Call room service":                    0,
        "Take down order":                      1,
        "Include alcohol?":                     2,

        # Same lane + same column => auto-stacked
        "Submit order ticket to kitchen":       3,
        "Send beverage order to sommelier":     3,
        "Assign order to waiter":               3,

        "Prepare food":                         4,
        "Fetch wine and prepare alcohol":       4,
        "Ready cart and nonalcoholic drinks":   4,

        "All items ready":                      5,
        "Deliver order to guest room":          6,
        "Return to room-service station":       7,

        "Bill now?":                            8,
        "Wait until free to bill":              9,
        "Debit guest account":                  10,
        "End":                                  11,
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
