#
# UniversityEnrollment.py
#
# Description: BPMN diagram for a university enrollment lifecycle, including application review, decision, enrollment confirmation, onboarding, semester loop, and appeals.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "UniversityEnrollment",

    "lanes": [
        "Prospective Student",
        "Admissions Office",
        "Admissions Committee",
        "Finance Dept",
        "IT Dept",
        "International Office",
        "Academic Advisor",
        "Registrar",
        "Appeals Committee",
    ],

    "elements": [
        ("Start",                              START,            "Prospective Student"),
        ("Submit application online",          USER_TASK,        "Prospective Student"),

        ("Review application and documents",   USER_TASK,        "Admissions Office"),
        ("Documents complete?",                EXCLUSIVE_GW,     "Admissions Office"),
        ("Notify missing documents",           SEND_TASK,        "Admissions Office"),
        ("Provide missing items",              USER_TASK,        "Prospective Student"),

        ("Parallel split: eval and fees",      PARALLEL_GW,      "Admissions Office"),
        ("Evaluate application",               USER_TASK,        "Admissions Committee"),
        ("Process application fee or waiver",  USER_TASK,        "Finance Dept"),
        ("Parallel join: eval and fees",       PARALLEL_GW,      "Admissions Office"),

        ("Accepted?",                          EXCLUSIVE_GW,     "Admissions Office"),
        ("Send acceptance letter",             SEND_TASK,        "Admissions Office"),
        ("Send rejection letter",              SEND_TASK,        "Admissions Office"),
        ("End rejected",                       END,              "Admissions Office"),

        ("Wait for enrollment confirmation",   EVENT_BASED_GW,   "Prospective Student"),
        ("Confirmation received",              MESSAGE_CATCH,    "Prospective Student"),
        ("Deadline reached",                   TIMER_CATCH,      "Prospective Student"),
        ("Cancel application",                 TASK,             "Admissions Office"),
        ("End canceled",                       END,              "Admissions Office"),

        ("Parallel split: onboarding",         PARALLEL_GW,      "Admissions Office"),
        ("Send orientation materials",         SEND_TASK,        "Admissions Office"),
        ("Set up student accounts",            SERVICE_TASK,     "IT Dept"),
        ("Parallel join: onboarding",          PARALLEL_GW,      "Admissions Office"),

        ("International student?",             EXCLUSIVE_GW,     "Admissions Office"),
        ("Assist visa processing",             USER_TASK,        "International Office"),

        ("Obtain student ID card",             USER_TASK,        "Prospective Student"),

        ("Meet academic advisor",              USER_TASK,        "Academic Advisor"),
        ("Select courses",                     USER_TASK,        "Prospective Student"),
        ("Resolve schedule conflicts",         USER_TASK,        "Registrar"),
        ("Attend classes",                     USER_TASK,        "Prospective Student"),

        ("Add or drop courses (period)",       USER_TASK,        "Prospective Student"),
        ("Post grades",                        SERVICE_TASK,     "Registrar"),
        ("Review grades online",               USER_TASK,        "Prospective Student"),

        ("Any grievances?",                    EXCLUSIVE_GW,     "Prospective Student"),
        ("Submit appeal form",                 USER_TASK,        "Prospective Student"),
        ("Meet appeals committee",             USER_TASK,        "Appeals Committee"),
        ("Await appeal decision",              USER_TASK,        "Prospective Student"),

        ("Graduate or withdraw?",              EXCLUSIVE_GW,     "Prospective Student"),
        ("End graduated or withdrawn",         END,              "Prospective Student"),

        ("Start next semester",                TASK,             "Prospective Student"),
    ],

    "flows": [
        ("Start",                            "Submit application online",        ""),
        ("Submit application online",        "Review application and documents",  ""),

        ("Review application and documents", "Documents complete?",               ""),
        ("Documents complete?",              "Notify missing documents",          "No"),
        ("Notify missing documents",         "Provide missing items",             ""),
        ("Provide missing items",            "Review application and documents",  ""),

        ("Documents complete?",              "Parallel split: eval and fees",     "Yes"),
        ("Parallel split: eval and fees",    "Evaluate application",              ""),
        ("Parallel split: eval and fees",    "Process application fee or waiver", ""),
        ("Evaluate application",             "Parallel join: eval and fees",      ""),
        ("Process application fee or waiver","Parallel join: eval and fees",      ""),

        ("Parallel join: eval and fees",     "Accepted?",                         ""),
        ("Accepted?",                        "Send acceptance letter",            "Yes"),
        ("Accepted?",                        "Send rejection letter",             "No"),
        ("Send rejection letter",            "End rejected",                      ""),

        ("Send acceptance letter",           "Wait for enrollment confirmation",  ""),
        ("Wait for enrollment confirmation", "Confirmation received",             ""),
        ("Wait for enrollment confirmation", "Deadline reached",                  ""),

        ("Deadline reached",                 "Cancel application",                ""),
        ("Cancel application",               "End canceled",                      ""),

        ("Confirmation received",            "Parallel split: onboarding",         ""),
        ("Parallel split: onboarding",       "Send orientation materials",         ""),
        ("Parallel split: onboarding",       "Set up student accounts",            ""),
        ("Send orientation materials",       "Parallel join: onboarding",          ""),
        ("Set up student accounts",          "Parallel join: onboarding",          ""),

        ("Parallel join: onboarding",        "International student?",            ""),
        ("International student?",           "Assist visa processing",             "Yes"),
        ("International student?",           "Obtain student ID card",             "No"),
        ("Assist visa processing",           "Obtain student ID card",             ""),

        ("Obtain student ID card",           "Meet academic advisor",              ""),
        ("Meet academic advisor",            "Select courses",                     ""),
        ("Select courses",                   "Resolve schedule conflicts",         ""),
        ("Resolve schedule conflicts",       "Attend classes",                     ""),

        ("Attend classes",                   "Add or drop courses (period)",       ""),
        ("Add or drop courses (period)",     "Post grades",                        ""),
        ("Post grades",                      "Review grades online",               ""),
        ("Review grades online",             "Any grievances?",                    ""),

        ("Any grievances?",                  "Submit appeal form",                "Yes"),
        ("Any grievances?",                  "Graduate or withdraw?",              "No"),
        ("Submit appeal form",               "Meet appeals committee",             ""),
        ("Meet appeals committee",           "Await appeal decision",              ""),
        ("Await appeal decision",            "Graduate or withdraw?",              ""),

        ("Graduate or withdraw?",            "End graduated or withdrawn",         "Yes"),
        ("Graduate or withdraw?",            "Start next semester",                "No"),
        ("Start next semester",              "Attend classes",                     ""),
    ],

    "layout": {
        "Start":                              0,
        "Submit application online":          1,

        "Review application and documents":   2,
        "Documents complete?":                3,
        "Notify missing documents":           4,
        "Provide missing items":              5,

        "Parallel split: eval and fees":      6,
        "Evaluate application":               7,
        "Process application fee or waiver":  7,
        "Parallel join: eval and fees":       8,

        "Accepted?":                          9,
        "Send acceptance letter":             10,
        "Send rejection letter":              10,
        "End rejected":                       11,

        "Wait for enrollment confirmation":   12,
        "Confirmation received":              13,
        "Deadline reached":                   13,
        "Cancel application":                 14,
        "End canceled":                       15,

        "Parallel split: onboarding":         14,
        "Send orientation materials":         15,
        "Set up student accounts":            15,
        "Parallel join: onboarding":          16,

        "International student?":             17,
        "Assist visa processing":             18,

        "Obtain student ID card":             19,

        "Meet academic advisor":              20,
        "Select courses":                     21,
        "Resolve schedule conflicts":         22,
        "Attend classes":                     23,

        "Add or drop courses (period)":       24,
        "Post grades":                        25,
        "Review grades online":               26,

        "Any grievances?":                    27,
        "Submit appeal form":                 28,
        "Meet appeals committee":             29,
        "Await appeal decision":              30,

        "Graduate or withdraw?":              31,
        "End graduated or withdrawn":         32,

        "Start next semester":                33,
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
