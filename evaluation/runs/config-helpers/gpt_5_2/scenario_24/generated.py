#
# RestaurantMealPickup.py
#
# Description: Guest orders and pays, chef prepares meal, employee notifies via buzzer; if guest does not react, employee calls every 5 minutes until pickup.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "RestaurantMealPickup",

    "lanes": ["Guest", "Employee", "Chef"],

    "elements": [
        ("Start",                         START,            "Guest"),
        ("Enter restaurant",              TASK,             "Guest"),
        ("Choose dish",                   USER_TASK,        "Guest"),
        ("Wait for turn",                 INTERMEDIATE_CATCH,"Guest"),
        ("Place order",                   USER_TASK,        "Guest"),
        ("Receive buzzer and instruction",RECEIVE_TASK,     "Guest"),
        ("Wait for buzzer ring",          SIGNAL_CATCH,     "Guest"),
        ("Go to service hatch?",          EXCLUSIVE_GW,     "Guest"),
        ("Go to service hatch",           USER_TASK,        "Guest"),
        ("Receive meal",                  USER_TASK,        "Guest"),
        ("Eat meal",                      TASK,             "Guest"),
        ("End",                           END,              "Guest"),

        ("Take order",                    USER_TASK,        "Employee"),
        ("Enter order in POS",            SERVICE_TASK,     "Employee"),
        ("Collect payment",               USER_TASK,        "Employee"),
        ("Set up buzzer",                 USER_TASK,        "Employee"),
        ("Give buzzer and instruction",   SEND_TASK,        "Employee"),
        ("Notify chef of order",          SEND_TASK,        "Employee"),
        ("Receive meal ready notice",     MESSAGE_CATCH,    "Employee"),
        ("Ring guest buzzer",             SIGNAL_THROW,     "Employee"),
        ("Wait 5 minutes",                TIMER_CATCH,      "Employee"),
        ("Call guest",                    USER_TASK,        "Employee"),
        ("Hand over meal",                USER_TASK,        "Employee"),

        ("Receive new order",             MESSAGE_CATCH,    "Chef"),
        ("Prepare meal",                  TASK,             "Chef"),
        ("Place meal in service hatch",   MANUAL_TASK,      "Chef"),
        ("Notify employee meal ready",    MESSAGE_THROW,    "Chef"),
    ],

    "flows": [
        ("Start",                         "Enter restaurant",               ""),
        ("Enter restaurant",              "Choose dish",                    ""),
        ("Choose dish",                   "Wait for turn",                  ""),
        ("Wait for turn",                 "Place order",                    ""),
        ("Place order",                   "Take order",                     ""),
        ("Take order",                    "Enter order in POS",             ""),
        ("Enter order in POS",            "Collect payment",                ""),
        ("Collect payment",               "Set up buzzer",                  ""),
        ("Set up buzzer",                 "Give buzzer and instruction",    ""),
        ("Give buzzer and instruction",   "Receive buzzer and instruction", ""),
        ("Receive buzzer and instruction","Notify chef of order",           ""),
        ("Notify chef of order",          "Receive new order",              ""),
        ("Receive new order",             "Prepare meal",                   ""),
        ("Prepare meal",                  "Place meal in service hatch",    ""),
        ("Place meal in service hatch",   "Notify employee meal ready",     ""),
        ("Notify employee meal ready",    "Receive meal ready notice",      ""),
        ("Receive meal ready notice",     "Ring guest buzzer",              ""),
        ("Ring guest buzzer",             "Wait for buzzer ring",           ""),
        ("Wait for buzzer ring",          "Go to service hatch?",           ""),

        ("Go to service hatch?",          "Go to service hatch",            "Yes"),
        ("Go to service hatch?",          "Wait 5 minutes",                 "No"),
        ("Wait 5 minutes",                "Call guest",                     ""),
        ("Call guest",                    "Go to service hatch?",           ""),

        ("Go to service hatch",           "Hand over meal",                 ""),
        ("Hand over meal",                "Receive meal",                   ""),
        ("Receive meal",                  "Eat meal",                       ""),
        ("Eat meal",                      "End",                            ""),
    ],

    "layout": {
        "Start":                          0,
        "Enter restaurant":               1,
        "Choose dish":                    2,
        "Wait for turn":                  3,
        "Place order":                    4,

        "Take order":                     5,
        "Enter order in POS":             6,
        "Collect payment":                7,
        "Set up buzzer":                  8,
        "Give buzzer and instruction":    9,

        "Receive buzzer and instruction": 10,
        "Notify chef of order":           11,

        "Receive new order":              12,
        "Prepare meal":                   13,
        "Place meal in service hatch":    14,
        "Notify employee meal ready":     15,

        "Receive meal ready notice":      16,
        "Ring guest buzzer":              17,
        "Wait for buzzer ring":           18,
        "Go to service hatch?":           19,
        "Go to service hatch":            20,

        # Same lane + same column -> auto-stacked (alternative paths after the gateway)
        "Wait 5 minutes":                 21,
        "Hand over meal":                 21,

        "Call guest":                     22,
        "Receive meal":                   22,
        "Eat meal":                       23,
        "End":                            24,
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
