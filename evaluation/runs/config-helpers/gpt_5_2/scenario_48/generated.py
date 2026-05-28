#
# App_For_Participating_at_the_Vienna_Night_Run.py
#
# Description: App-supported preparation and participation workflow for the Vienna Night Run,
#              including fitness gadget time measurements and a training loop until under 25 minutes.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "App For Participating at the Vienna Night Run",

    "lanes": ["Runner", "App", "Fitness Gadget"],

    "elements": [
        ("Start",                       START,          "Runner"),

        ("Select starting block",        USER_TASK,      "App"),

        ("Test run 5km",                MANUAL_TASK,    "Runner"),
        ("Measure 5km time",            SERVICE_TASK,   "Fitness Gadget"),
        ("Record 5km time",             SERVICE_TASK,   "App"),

        ("Time under 25 min?",          EXCLUSIVE_GW,   "App"),
        ("Train",                       MANUAL_TASK,    "Runner"),

        ("Get starting number",         USER_TASK,      "App"),

        ("Enter workday end time",      USER_TASK,      "App"),
        ("Determine departure option",  SERVICE_TASK,   "App"),
        ("More than 1 hour left?",      EXCLUSIVE_GW,   "App"),

        ("Go from home",                MANUAL_TASK,    "Runner"),
        ("Leave directly from work",    MANUAL_TASK,    "Runner"),
        ("Departure decided",           EXCLUSIVE_GW,   "App"),

        ("Run and drink",               PARALLEL_GW,    "Runner"),
        ("Run Vienna Night Run 5km",    MANUAL_TASK,    "Runner"),
        ("Drink during run",            MANUAL_TASK,    "Runner"),
        ("Done running and drinking",   PARALLEL_GW,    "Runner"),

        ("Measure final time",          SERVICE_TASK,   "Fitness Gadget"),
        ("Show final time",             SERVICE_TASK,   "App"),

        ("End",                         END,            "Runner"),
    ],

    "data_objects": [
        ("Start Time",      "App",            1),
        ("5km Time",        "Fitness Gadget", 3),
        ("Starting Number", "App",            6),
        ("Workday End",     "App",            7),
        ("Final Time",      "Fitness Gadget", 15),
    ],

    "data_associations": [
        ("Select starting block",       "Start Time"),

        ("Measure 5km time",           "5km Time"),
        ("5km Time",                   "Record 5km time"),

        ("Get starting number",        "Starting Number"),

        ("Enter workday end time",     "Workday End"),
        ("Start Time",                 "Determine departure option"),
        ("Workday End",                "Determine departure option"),

        ("Measure final time",         "Final Time"),
        ("Final Time",                 "Show final time"),
    ],

    "flows": [
        ("Start",                      "Select starting block",        ""),
        ("Select starting block",      "Test run 5km",                 ""),

        ("Test run 5km",               "Measure 5km time",             ""),
        ("Measure 5km time",           "Record 5km time",              ""),
        ("Record 5km time",            "Time under 25 min?",           ""),

        ("Time under 25 min?",         "Get starting number",          "Yes"),
        ("Time under 25 min?",         "Train",                        "No"),
        ("Train",                      "Test run 5km",                 ""),

        ("Get starting number",        "Enter workday end time",       ""),
        ("Enter workday end time",     "Determine departure option",   ""),
        ("Determine departure option", "More than 1 hour left?",       ""),

        ("More than 1 hour left?",     "Go from home",                 "Yes"),
        ("More than 1 hour left?",     "Leave directly from work",     "No"),

        ("Go from home",               "Departure decided",            ""),
        ("Leave directly from work",   "Departure decided",            ""),

        ("Departure decided",          "Run and drink",                ""),

        ("Run and drink",              "Run Vienna Night Run 5km",     ""),
        ("Run and drink",              "Drink during run",             ""),

        ("Run Vienna Night Run 5km",   "Done running and drinking",    ""),
        ("Drink during run",           "Done running and drinking",    ""),

        ("Done running and drinking",  "Measure final time",           ""),
        ("Measure final time",         "Show final time",              ""),
        ("Show final time",            "End",                          ""),
    ],

    "layout": {
        "Start":                      0,
        "Select starting block":      1,

        "Test run 5km":               2,
        "Measure 5km time":           3,
        "Record 5km time":            4,

        "Time under 25 min?":         5,
        "Train":                      6,
        "Get starting number":        6,

        "Enter workday end time":     7,
        "Determine departure option": 8,
        "More than 1 hour left?":     9,

        "Go from home":               10,
        "Leave directly from work":   10,

        "Departure decided":          11,

        "Run and drink":              12,
        "Run Vienna Night Run 5km":   13,
        "Drink during run":           13,
        "Done running and drinking":  14,

        "Measure final time":         15,
        "Show final time":            16,
        "End":                        17,
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
