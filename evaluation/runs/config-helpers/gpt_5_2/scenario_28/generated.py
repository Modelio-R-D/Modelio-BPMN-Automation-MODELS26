#
# Internship.py
#
# Description: Internship process from entering preferences to receiving offers, completing internship updates, and tweeting recommendations in parallel.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Internship",

    "lanes": ["Student", "Company", "Twitter"],

    "elements": [
        ("Start",                          START,            "Student"),
        ("Enter preferences",              USER_TASK,        "Student"),
        ("Publish profile",                SERVICE_TASK,     "Student"),

        ("Wait for offer",                 MESSAGE_CATCH,    "Student"),
        ("Review offer",                   USER_TASK,        "Student"),
        ("Accept offer?",                  EXCLUSIVE_GW,     "Student"),
        ("Accept offer",                   USER_TASK,        "Student"),
        ("Deny offer",                     USER_TASK,        "Student"),
        ("Invalidate other offers",        SERVICE_TASK,     "Student"),

        ("Begin internship",               USER_TASK,        "Student"),
        ("Parallel updates",               PARALLEL_GW,      "Student"),

        ("Student status update 1",        USER_TASK,        "Student"),
        ("Student status update 2",        USER_TASK,        "Student"),
        ("Student status update 3",        USER_TASK,        "Student"),

        ("Company status update 1",        USER_TASK,        "Company"),
        ("Company status update 2",        USER_TASK,        "Company"),
        ("Company status update 3",        USER_TASK,        "Company"),

        ("Join updates",                   PARALLEL_GW,      "Student"),
        ("Finish internship",              USER_TASK,        "Student"),

        ("Recommend company",              USER_TASK,        "Student"),
        ("Parallel tweets",                PARALLEL_GW,      "Twitter"),
        ("Tweet to friend 1",              SEND_TASK,        "Twitter"),
        ("Tweet to friend 2",              SEND_TASK,        "Twitter"),
        ("Tweet to friend 3",              SEND_TASK,        "Twitter"),
        ("Join tweets",                    PARALLEL_GW,      "Twitter"),

        ("End",                            END,              "Student"),
    ],

    "flows": [
        ("Start",                   "Enter preferences",          ""),
        ("Enter preferences",       "Publish profile",            ""),

        ("Publish profile",         "Wait for offer",             ""),
        ("Wait for offer",          "Review offer",               ""),
        ("Review offer",            "Accept offer?",              ""),
        ("Accept offer?",           "Accept offer",               "Yes"),
        ("Accept offer?",           "Deny offer",                 "No"),
        ("Deny offer",              "Wait for offer",             ""),

        ("Accept offer",            "Invalidate other offers",    ""),
        ("Invalidate other offers", "Begin internship",           ""),

        ("Begin internship",        "Parallel updates",           ""),

        ("Parallel updates",        "Student status update 1",    ""),
        ("Student status update 1", "Student status update 2",    ""),
        ("Student status update 2", "Student status update 3",    ""),
        ("Student status update 3", "Join updates",               ""),

        ("Parallel updates",        "Company status update 1",    ""),
        ("Company status update 1", "Company status update 2",    ""),
        ("Company status update 2", "Company status update 3",    ""),
        ("Company status update 3", "Join updates",               ""),

        ("Join updates",            "Finish internship",          ""),
        ("Finish internship",       "Recommend company",          ""),

        ("Recommend company",       "Parallel tweets",            ""),
        ("Parallel tweets",         "Tweet to friend 1",          ""),
        ("Parallel tweets",         "Tweet to friend 2",          ""),
        ("Parallel tweets",         "Tweet to friend 3",          ""),
        ("Tweet to friend 1",       "Join tweets",                ""),
        ("Tweet to friend 2",       "Join tweets",                ""),
        ("Tweet to friend 3",       "Join tweets",                ""),

        ("Join tweets",             "End",                        ""),
    ],

    "layout": {
        "Start":                   0,
        "Enter preferences":       1,
        "Publish profile":         2,

        "Wait for offer":          3,
        "Review offer":            4,
        "Accept offer?":           5,
        "Accept offer":            6,
        "Deny offer":              6,   # auto-stacked under "Accept offer"
        "Invalidate other offers": 7,

        "Begin internship":        8,
        "Parallel updates":        9,

        # Updates in parallel (aligned by column across lanes)
        "Student status update 1": 10,
        "Student status update 2": 11,
        "Student status update 3": 12,

        "Company status update 1": 10,
        "Company status update 2": 11,
        "Company status update 3": 12,

        "Join updates":            13,
        "Finish internship":       14,

        "Recommend company":       15,
        "Parallel tweets":         16,

        # Parallel tweets in same lane + same column -> auto-stacked
        "Tweet to friend 1":       17,
        "Tweet to friend 2":       17,
        "Tweet to friend 3":       17,

        "Join tweets":             18,
        "End":                     19,
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
