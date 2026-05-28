#
# ServiceForYourFridge.py
#
# Description: Customer reports strange fridge noises to a central service center, which assigns a local facility.
# The facility schedules a visit; technician may need extra parts and reschedule. After repair, customer confirms and rates.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Service for Your Fridge",

    "lanes": [
        "Customer",
        "Central Service Center",
        "Service Facility",
    ],

    "elements": [
        ("Start",                     START,          "Customer"),
        ("Describe symptoms",         USER_TASK,      "Customer"),
        ("Send request",              SEND_TASK,      "Customer"),

        ("Receive request",           RECEIVE_TASK,   "Central Service Center"),
        ("Select service facility",   SERVICE_TASK,   "Central Service Center"),
        ("Send job to facility",      SEND_TASK,      "Central Service Center"),

        ("Receive job",               RECEIVE_TASK,   "Service Facility"),
        ("Set appointment",           TASK,           "Service Facility"),
        ("Notify customer",           SEND_TASK,      "Service Facility"),

        ("Receive appointment",       RECEIVE_TASK,   "Customer"),

        ("Wait until appointment",    TIMER_CATCH,    "Service Facility"),
        ("Arrive on site",            TASK,           "Service Facility"),
        ("Inspect fridge",            TASK,           "Service Facility"),
        ("Need additional parts?",    EXCLUSIVE_GW,   "Service Facility"),

        ("Order parts",               SERVICE_TASK,   "Service Facility"),
        ("Repair fridge",             TASK,           "Service Facility"),

        ("Set follow-up appointment", TASK,           "Service Facility"),
        ("Send completion notice",    SEND_TASK,      "Service Facility"),

        ("Confirm fridge OK",         USER_TASK,      "Customer"),
        ("Rate service facility",     USER_TASK,      "Customer"),
        ("End",                       END,            "Customer"),
    ],

    "flows": [
        ("Start",                   "Describe symptoms",         ""),
        ("Describe symptoms",       "Send request",              ""),
        ("Send request",            "Receive request",           ""),

        ("Receive request",         "Select service facility",   ""),
        ("Select service facility", "Send job to facility",      ""),
        ("Send job to facility",    "Receive job",               ""),

        ("Receive job",             "Set appointment",           ""),
        ("Set appointment",         "Notify customer",           ""),
        ("Notify customer",         "Receive appointment",       ""),

        ("Receive appointment",     "Wait until appointment",    ""),
        ("Wait until appointment",  "Arrive on site",            ""),
        ("Arrive on site",          "Inspect fridge",            ""),
        ("Inspect fridge",          "Need additional parts?",    ""),

        ("Need additional parts?",  "Order parts",               "Yes"),
        ("Need additional parts?",  "Repair fridge",             "No"),

        ("Order parts",             "Set follow-up appointment", ""),
        ("Set follow-up appointment","Notify customer",          ""),

        ("Repair fridge",           "Send completion notice",    ""),
        ("Send completion notice",  "Confirm fridge OK",         ""),
        ("Confirm fridge OK",       "Rate service facility",     ""),
        ("Rate service facility",   "End",                       ""),
    ],

    "layout": {
        "Start":                      0,
        "Describe symptoms":          1,
        "Send request":               2,

        "Receive request":            3,
        "Select service facility":    4,
        "Send job to facility":       5,

        "Receive job":                6,
        "Set appointment":            7,
        "Notify customer":            8,

        "Receive appointment":        9,

        "Wait until appointment":     10,
        "Arrive on site":             11,
        "Inspect fridge":             12,
        "Need additional parts?":     13,

        # Same lane + same column -> auto-stacked (v3.2)
        "Order parts":                14,
        "Repair fridge":              14,

        # Same lane + same column -> auto-stacked (v3.2)
        "Set follow-up appointment":  15,
        "Send completion notice":     15,

        "Confirm fridge OK":          16,
        "Rate service facility":      17,
        "End":                        18,
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
