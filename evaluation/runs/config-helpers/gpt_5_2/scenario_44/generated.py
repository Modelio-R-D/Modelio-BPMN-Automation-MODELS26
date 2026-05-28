#
# RoboticBurgerSeller_UniVienna.py
#
# Description: Robot takes an order, checks menu vs burger-only, prepares drink + side in parallel for menu,
# then prepares burger with periodic status updates, and delivers via conveyor belt.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Robotic Burger Seller near the University of Vienna",

    "lanes": ["Robot"],

    "elements": [
        ("Order received",            MESSAGE_START,   "Robot"),
        ("Ask menu or burger",        USER_TASK,       "Robot"),
        ("Menu?",                     EXCLUSIVE_GW,    "Robot"),

        ("Menu prep split",           PARALLEL_GW,     "Robot"),
        ("Prepare drink",             SERVICE_TASK,    "Robot"),
        ("Ask fries or wedges",       USER_TASK,       "Robot"),
        ("Side choice?",              EXCLUSIVE_GW,    "Robot"),
        ("Prepare fries",             SERVICE_TASK,    "Robot"),
        ("Prepare wedges",            SERVICE_TASK,    "Robot"),
        ("Side ready",                EXCLUSIVE_GW,    "Robot"),
        ("Menu prep join",            PARALLEL_GW,     "Robot"),

        ("Burger prep split",         PARALLEL_GW,     "Robot"),
        ("Prepare burger",            SERVICE_TASK,    "Robot"),

        ("Wait 30s",                  TIMER_CATCH,     "Robot"),
        ("Send update 1",             SEND_TASK,       "Robot"),
        ("Wait 30s 2",                TIMER_CATCH,     "Robot"),
        ("Send update 2",             SEND_TASK,       "Robot"),
        ("Wait 30s 3",                TIMER_CATCH,     "Robot"),
        ("Send update 3",             SEND_TASK,       "Robot"),

        ("Burger ready",              PARALLEL_GW,     "Robot"),
        ("Deliver via conveyor belt", SERVICE_TASK,    "Robot"),
        ("Order complete",            END,             "Robot"),
    ],

    "flows": [
        ("Order received",      "Ask menu or burger",        ""),
        ("Ask menu or burger",  "Menu?",                     ""),

        ("Menu?",               "Menu prep split",           "Menu"),
        ("Menu?",               "Burger prep split",         "Burger only"),

        # Menu preparation in parallel: drink + side
        ("Menu prep split",     "Prepare drink",             ""),
        ("Menu prep split",     "Ask fries or wedges",       ""),

        ("Prepare drink",       "Menu prep join",            ""),

        ("Ask fries or wedges", "Side choice?",              ""),
        ("Side choice?",        "Prepare fries",             "Fries"),
        ("Side choice?",        "Prepare wedges",            "Wedges"),
        ("Prepare fries",       "Side ready",                ""),
        ("Prepare wedges",      "Side ready",                ""),
        ("Side ready",          "Menu prep join",            ""),

        ("Menu prep join",      "Burger prep split",         ""),

        # Burger preparation + periodic updates in parallel
        ("Burger prep split",   "Prepare burger",            ""),
        ("Burger prep split",   "Wait 30s",                  ""),

        ("Wait 30s",            "Send update 1",             ""),
        ("Send update 1",       "Wait 30s 2",                ""),
        ("Wait 30s 2",          "Send update 2",             ""),
        ("Send update 2",       "Wait 30s 3",                ""),
        ("Wait 30s 3",          "Send update 3",             ""),
        ("Send update 3",       "Burger ready",              ""),

        ("Prepare burger",      "Burger ready",              ""),

        ("Burger ready",        "Deliver via conveyor belt", ""),
        ("Deliver via conveyor belt", "Order complete",      ""),
    ],

    "layout": {
        "Order received":            0,
        "Ask menu or burger":        1,
        "Menu?":                     2,

        "Menu prep split":           3,
        "Prepare drink":             4,
        "Ask fries or wedges":       4,
        "Side choice?":              5,
        "Prepare fries":             6,
        "Prepare wedges":            6,
        "Side ready":                7,
        "Menu prep join":            8,

        "Burger prep split":         9,
        "Prepare burger":            10,
        "Wait 30s":                  10,
        "Send update 1":             11,
        "Wait 30s 2":                12,
        "Send update 2":             13,
        "Wait 30s 3":                14,
        "Send update 3":             15,
        "Burger ready":              16,

        "Deliver via conveyor belt": 17,
        "Order complete":            18,
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
