#
# HiringAndOnboardingProcess.py
#
# Description: Hiring process from identifying a staffing need through recruiting, interviewing (virtual or in-person),
#              offer/negotiation, and onboarding until the new hire is integrated into the team.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "HiringAndOnboardingProcess",

    "lanes": ["Department", "HR", "Candidate", "Hiring Team"],

    "elements": [
        ("Need identified",            START,        "Department"),
        ("Request new hire",           USER_TASK,    "Department"),

        ("Create job description",     USER_TASK,    "HR"),
        ("Post job to boards",         USER_TASK,    "HR"),
        ("Collect resumes",            USER_TASK,    "HR"),
        ("Screen resumes",             USER_TASK,    "HR"),
        ("Phone interviews",           USER_TASK,    "HR"),
        ("Invite to interview",        USER_TASK,    "HR"),

        ("Interview mode?",            EXCLUSIVE_GW, "HR"),
        ("Virtual interview",          USER_TASK,    "Hiring Team"),
        ("In-person interview",        USER_TASK,    "Hiring Team"),

        ("Evaluate candidates",        USER_TASK,    "Hiring Team"),
        ("Select candidate",           USER_TASK,    "Hiring Team"),

        ("Extend offer",               USER_TASK,    "HR"),
        ("Negotiate salary?",          EXCLUSIVE_GW, "HR"),
        ("Negotiate salary",           USER_TASK,    "HR"),
        ("Issue revised offer",        USER_TASK,    "HR"),

        ("Review offer",               USER_TASK,    "Candidate"),
        ("Offer accepted?",            EXCLUSIVE_GW, "Candidate"),
        ("Offer declined",             END,          "Candidate"),

        ("Begin onboarding",           USER_TASK,    "HR"),
        ("Complete paperwork",         USER_TASK,    "HR"),
        ("Orientation",                USER_TASK,    "HR"),
        ("Training",                   USER_TASK,    "Hiring Team"),

        ("Integrated into team",       END,          "Department"),
    ],

    "flows": [
        ("Need identified",        "Request new hire",        ""),
        ("Request new hire",       "Create job description",  ""),
        ("Create job description", "Post job to boards",      ""),
        ("Post job to boards",     "Collect resumes",         ""),
        ("Collect resumes",        "Screen resumes",          ""),
        ("Screen resumes",         "Phone interviews",        ""),
        ("Phone interviews",       "Invite to interview",     ""),
        ("Invite to interview",    "Interview mode?",         ""),

        ("Interview mode?",        "Virtual interview",       "Virtual"),
        ("Interview mode?",        "In-person interview",     "In-person"),
        ("Virtual interview",      "Evaluate candidates",     ""),
        ("In-person interview",    "Evaluate candidates",     ""),

        ("Evaluate candidates",    "Select candidate",        ""),
        ("Select candidate",       "Extend offer",            ""),

        ("Extend offer",           "Negotiate salary?",       ""),
        ("Negotiate salary?",      "Negotiate salary",        "Yes"),
        ("Negotiate salary?",      "Review offer",            "No"),
        ("Negotiate salary",       "Issue revised offer",     ""),
        ("Issue revised offer",    "Review offer",            ""),

        ("Review offer",           "Offer accepted?",         ""),
        ("Offer accepted?",        "Begin onboarding",        "Yes"),
        ("Offer accepted?",        "Offer declined",          "No"),

        ("Begin onboarding",       "Complete paperwork",      ""),
        ("Complete paperwork",     "Orientation",             ""),
        ("Orientation",            "Training",                ""),
        ("Training",               "Integrated into team",    ""),
    ],

    "layout": {
        "Need identified":        0,
        "Request new hire":       1,

        "Create job description": 2,
        "Post job to boards":     3,
        "Collect resumes":        4,
        "Screen resumes":         5,
        "Phone interviews":       6,
        "Invite to interview":    7,

        "Interview mode?":        8,

        # Same lane + same column -> auto-stacked (v3.2)
        "Virtual interview":      9,
        "In-person interview":    9,

        "Evaluate candidates":    10,
        "Select candidate":       11,

        "Extend offer":           12,
        "Negotiate salary?":      13,
        "Negotiate salary":       14,
        "Issue revised offer":    15,

        "Review offer":           16,
        "Offer accepted?":        17,
        "Offer declined":         18,

        "Begin onboarding":       18,
        "Complete paperwork":     19,
        "Orientation":            20,
        "Training":               21,
        "Integrated into team":   22,
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
