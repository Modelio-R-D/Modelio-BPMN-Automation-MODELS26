#
# EmployeeDevelopmentAndPromotion.py
#
# Description: Personal development planning, ongoing skill enhancement with feedback, milestone check, and promotion approval/finalization.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EmployeeDevelopmentAndPromotion",

    "lanes": ["Employee", "Manager", "Supervisor", "HR"],

    "elements": [
        ("Start",                               START,        "Employee"),
        ("Identify development needs",           USER_TASK,    "Employee"),

        ("Draft personal development plan",      USER_TASK,    "Manager"),
        ("Co-create plan with HR",              USER_TASK,    "HR"),

        ("Execute development activities",       USER_TASK,    "Employee"),
        ("Provide feedback and evaluation",      USER_TASK,    "Supervisor"),
        ("Milestones reached?",                 EXCLUSIVE_GW, "Supervisor"),

        ("Continue skill enhancement",           USER_TASK,    "Employee"),
        ("Ongoing feedback",                    USER_TASK,    "Supervisor"),

        ("Consider promotion or new role",       USER_TASK,    "Manager"),
        ("HR formal performance review",         USER_TASK,    "HR"),
        ("Promotion approved?",                 EXCLUSIVE_GW, "HR"),

        ("Finalize promotion and adjust compensation", USER_TASK, "HR"),
        ("Transition into new role",             USER_TASK,    "Employee"),
        ("End",                                 END,          "Employee"),

        ("Revise development plan",              USER_TASK,    "Manager"),
        ("Align revised plan with HR",           USER_TASK,    "HR"),
    ],

    "flows": [
        ("Start",                          "Identify development needs", ""),
        ("Identify development needs",      "Draft personal development plan", ""),
        ("Draft personal development plan", "Co-create plan with HR", ""),
        ("Co-create plan with HR",         "Execute development activities", ""),
        ("Execute development activities",  "Provide feedback and evaluation", ""),
        ("Provide feedback and evaluation", "Milestones reached?", ""),

        ("Milestones reached?",            "Continue skill enhancement", "No"),
        ("Continue skill enhancement",     "Ongoing feedback", ""),
        ("Ongoing feedback",               "Milestones reached?", ""),

        ("Milestones reached?",            "Consider promotion or new role", "Yes"),
        ("Consider promotion or new role", "HR formal performance review", ""),
        ("HR formal performance review",   "Promotion approved?", ""),

        ("Promotion approved?",            "Finalize promotion and adjust compensation", "Yes"),
        ("Finalize promotion and adjust compensation", "Transition into new role", ""),
        ("Transition into new role",       "End", ""),

        ("Promotion approved?",            "Revise development plan", "No"),
        ("Revise development plan",        "Align revised plan with HR", ""),
        ("Align revised plan with HR",     "Execute development activities", ""),
    ],

    "layout": {
        "Start":                               0,
        "Identify development needs":           1,
        "Draft personal development plan":      2,
        "Co-create plan with HR":              3,
        "Execute development activities":       4,
        "Provide feedback and evaluation":      5,
        "Milestones reached?":                 6,

        "Continue skill enhancement":           7,
        "Ongoing feedback":                    8,

        "Consider promotion or new role":       7,
        "HR formal performance review":         8,
        "Promotion approved?":                 9,

        "Finalize promotion and adjust compensation": 10,
        "Transition into new role":             11,
        "End":                                 12,

        "Revise development plan":              10,
        "Align revised plan with HR":           11,
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
