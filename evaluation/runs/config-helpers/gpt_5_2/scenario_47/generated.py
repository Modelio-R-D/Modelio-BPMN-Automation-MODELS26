#
# New_Application_USI_Course_Registration.py
#
# Description: New application process for registering for a USI sports institute course,
# including course selection, account creation/activation, optional tweeting, payment, and ticket issuance.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "New Application for Registering for an USI course",

    "lanes": ["Applicant", "USI System", "USI Admin", "Twitter"],

    "elements": [
        ("Start",                        START,          "Applicant"),

        ("Select course",                USER_TASK,      "Applicant"),
        ("Check slots and show options", SERVICE_TASK,   "USI System"),
        ("Select course date",           USER_TASK,      "Applicant"),

        ("Check existing account",       SERVICE_TASK,   "USI System"),
        ("Account exists?",              EXCLUSIVE_GW,   "USI System"),

        ("Verify university eligibility", SERVICE_TASK,  "USI System"),
        ("Eligible university?",          EXCLUSIVE_GW,  "USI System"),

        ("Request activation",           SEND_TASK,      "Applicant"),
        ("Review activation request",    USER_TASK,      "USI Admin"),
        ("Send activation response",     SEND_TASK,      "USI Admin"),
        ("Activation response received", MESSAGE_CATCH,  "Applicant"),

        ("Create account",               USER_TASK,      "Applicant"),
        ("Log in",                       USER_TASK,      "Applicant"),

        ("Tweet friends?",               EXCLUSIVE_GW,   "Applicant"),
        ("Tweet friends",                USER_TASK,      "Applicant"),
        ("Post tweet",                   SERVICE_TASK,   "Twitter"),

        ("Complete course registration", USER_TASK,      "Applicant"),
        ("Provide payment information",  USER_TASK,      "Applicant"),
        ("Process payment",              SERVICE_TASK,   "USI System"),
        ("Issue course ticket",          SERVICE_TASK,   "USI System"),

        ("Course ticket received",       END,            "Applicant"),
    ],

    "data_objects": [
        ("Payment details", "Applicant", 21),
        ("Course ticket",   "USI System", 23),
    ],

    "data_associations": [
        ("Provide payment information", "Payment details"),
        ("Payment details",             "Process payment"),
        ("Issue course ticket",         "Course ticket"),
        ("Course ticket",               "Course ticket received"),
    ],

    "flows": [
        ("Start",                        "Select course",                ""),
        ("Select course",                "Check slots and show options", ""),
        ("Check slots and show options", "Select course date",           ""),
        ("Select course date",           "Check existing account",       ""),
        ("Check existing account",       "Account exists?",              ""),

        ("Account exists?",              "Log in",                       "Yes"),
        ("Account exists?",              "Verify university eligibility","No"),

        ("Verify university eligibility","Eligible university?",         ""),

        ("Eligible university?",         "Create account",               "Yes"),
        ("Eligible university?",         "Request activation",           "No"),

        ("Request activation",           "Review activation request",    ""),
        ("Review activation request",    "Send activation response",     ""),
        ("Send activation response",     "Activation response received", ""),
        ("Activation response received", "Create account",               ""),

        ("Create account",               "Log in",                       ""),

        ("Log in",                       "Tweet friends?",               ""),

        ("Tweet friends?",               "Tweet friends",                "Yes"),
        ("Tweet friends?",               "Complete course registration", "No"),

        ("Tweet friends",                "Post tweet",                   ""),
        ("Post tweet",                   "Complete course registration", ""),

        ("Complete course registration", "Provide payment information",  ""),
        ("Provide payment information",  "Process payment",              ""),
        ("Process payment",              "Issue course ticket",          ""),
        ("Issue course ticket",          "Course ticket received",       ""),
    ],

    "layout": {
        "Start":                        0,
        "Select course":                1,
        "Check slots and show options": 2,
        "Select course date":           3,

        "Check existing account":       4,
        "Account exists?":              5,

        "Verify university eligibility": 6,
        "Eligible university?":          7,

        "Request activation":           8,
        "Review activation request":    9,
        "Send activation response":     10,
        "Activation response received": 11,

        "Create account":               13,
        "Log in":                       15,

        "Tweet friends?":               16,
        "Tweet friends":                17,
        "Post tweet":                   18,

        "Complete course registration": 20,
        "Provide payment information":  21,
        "Process payment":              22,
        "Issue course ticket":          23,
        "Course ticket received":       24,
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
