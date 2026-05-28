#
# Car_Service.py
#
# Description: Police app reminds car owner about required car service, checks registration, notifies owner, fines after 30 days if not attended, and supports service/repair completion and next-service scheduling.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Car Service",

    "lanes": ["Police App", "Car Owner", "Mechanic"],

    "elements": [
        ("Service completed",            MESSAGE_START,     "Police App"),

        ("Check registration",           SERVICE_TASK,      "Police App"),
        ("Registered?",                  EXCLUSIVE_GW,      "Police App"),

        ("Notify owner",                 SEND_TASK,         "Police App"),
        ("Stop reminders",               SERVICE_TASK,      "Police App"),

        ("Wait for service",             EVENT_BASED_GW,    "Police App"),
        ("Service visited",              MESSAGE_CATCH,     "Car Owner"),
        ("30 days passed",               TIMER_CATCH,       "Police App"),
        ("Issue fine",                   SERVICE_TASK,      "Police App"),

        ("Enter car problems",           USER_TASK,         "Mechanic"),
        ("Repair car",                   SERVICE_TASK,      "Mechanic"),
        ("Send status updates",          SERVICE_TASK,      "Police App"),
        ("Notify repair done",           SEND_TASK,         "Police App"),
        ("Pay in app",                   USER_TASK,         "Car Owner"),

        ("Confirm repair and Pickerl",   USER_TASK,         "Mechanic"),
        ("Enter next service time",      USER_TASK,         "Mechanic"),

        ("End",                          END,               "Police App"),
    ],

    "flows": [
        ("Service completed",          "Check registration",          ""),
        ("Check registration",         "Registered?",                 ""),

        ("Registered?",                "Notify owner",                "Yes"),
        ("Registered?",                "Stop reminders",              "No"),

        ("Notify owner",               "Wait for service",            ""),

        ("Wait for service",           "Service visited",             "Goes to service"),
        ("Wait for service",           "30 days passed",              "No show (30 days)"),

        ("30 days passed",             "Issue fine",                  ""),
        ("Issue fine",                 "End",                         ""),

        ("Service visited",            "Enter car problems",          ""),
        ("Enter car problems",         "Repair car",                  ""),
        ("Repair car",                 "Send status updates",         ""),
        ("Send status updates",        "Notify repair done",          ""),
        ("Notify repair done",         "Pay in app",                  ""),
        ("Pay in app",                 "Confirm repair and Pickerl",  ""),
        ("Confirm repair and Pickerl", "Enter next service time",     ""),
        ("Enter next service time",    "End",                         ""),

        ("Stop reminders",             "End",                         ""),
    ],

    "layout": {
        "Service completed":            0,
        "Check registration":           1,
        "Registered?":                  2,

        # Branch after registration check (auto-stacked in same lane/column)
        "Notify owner":                 3,
        "Stop reminders":               3,

        "Wait for service":             4,

        # Event-based gateway outcomes
        "Service visited":              5,
        "30 days passed":               5,

        "Issue fine":                   6,

        "Enter car problems":           6,
        "Repair car":                   7,
        "Send status updates":          8,
        "Notify repair done":           9,
        "Pay in app":                   10,
        "Confirm repair and Pickerl":   11,
        "Enter next service time":      12,

        "End":                          13,
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
