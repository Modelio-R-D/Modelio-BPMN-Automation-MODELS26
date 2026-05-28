#
# Inspection_EnergyDrink_BottlingMachine.py
#
# Description: BPMN process for inspecting an energy drink bottling machine using an inspection application.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Inspection of an Energy Drink Bottling Machine",

    "lanes": ["Inspector", "Inspection App", "Bottling Machine"],

    "elements": [
        ("Start",                       START,              "Inspector"),
        ("Enter machine type",          USER_TASK,          "Inspector"),
        ("Enter serial number",         USER_TASK,          "Inspector"),

        ("Load inspection checklist",   SERVICE_TASK,       "Inspection App"),
        ("Display questions",           SERVICE_TASK,       "Inspection App"),
        ("Input answers",               USER_TASK,          "Inspector"),
        ("Validate inputs",             SERVICE_TASK,       "Inspection App"),

        ("Press test button",           USER_TASK,          "Inspector"),
        ("Request machine values",      SERVICE_TASK,       "Inspection App"),
        ("Provide sensor values",       SERVICE_TASK,       "Bottling Machine"),
        ("Collect machine values",      SERVICE_TASK,       "Inspection App"),

        ("Evaluate results",            BUSINESS_RULE_TASK, "Inspection App"),
        ("Additional questions needed?", EXCLUSIVE_GW,      "Inspection App"),

        ("Display additional questions", SERVICE_TASK,      "Inspection App"),
        ("Answer additional questions",  USER_TASK,         "Inspector"),
        ("Validate additional inputs",   SERVICE_TASK,      "Inspection App"),

        ("Store inspection record",     SERVICE_TASK,       "Inspection App"),
        ("Show inspection summary",     SERVICE_TASK,       "Inspection App"),
        ("Confirm inspection complete", USER_TASK,          "Inspector"),
        ("End",                         END,                "Inspector"),
    ],

    "data_objects": [
        ("Checklist",          "Inspection App", 3),
        ("Input values",       "Inspector",      5),
        ("Machine readings",   "Inspection App", 10),
        ("Inspection record",  "Inspection App", 16),
    ],

    "data_associations": [
        ("Load inspection checklist", "Checklist"),

        ("Input answers",             "Input values"),
        ("Input values",              "Validate inputs"),

        ("Collect machine values",    "Machine readings"),
        ("Machine readings",          "Evaluate results"),

        ("Store inspection record",   "Inspection record"),
        ("Inspection record",         "Show inspection summary"),
    ],

    "flows": [
        ("Start",                      "Enter machine type",           ""),
        ("Enter machine type",         "Enter serial number",          ""),
        ("Enter serial number",        "Load inspection checklist",    ""),

        ("Load inspection checklist",  "Display questions",            ""),
        ("Display questions",          "Input answers",                ""),
        ("Input answers",              "Validate inputs",              ""),

        ("Validate inputs",            "Press test button",            ""),
        ("Press test button",          "Request machine values",       ""),
        ("Request machine values",     "Provide sensor values",        ""),
        ("Provide sensor values",      "Collect machine values",       ""),
        ("Collect machine values",     "Evaluate results",             ""),

        ("Evaluate results",           "Additional questions needed?", ""),

        ("Additional questions needed?", "Store inspection record",      "No"),
        ("Additional questions needed?", "Display additional questions", "Yes"),

        ("Display additional questions", "Answer additional questions",  ""),
        ("Answer additional questions",  "Validate additional inputs",   ""),
        ("Validate additional inputs",   "Store inspection record",      ""),

        ("Store inspection record",    "Show inspection summary",      ""),
        ("Show inspection summary",    "Confirm inspection complete",  ""),
        ("Confirm inspection complete","End",                          ""),
    ],

    "layout": {
        "Start":                        0,
        "Enter machine type":           1,
        "Enter serial number":          2,

        "Load inspection checklist":    3,
        "Display questions":            4,
        "Input answers":                5,
        "Validate inputs":              6,

        "Press test button":            7,
        "Request machine values":       8,
        "Provide sensor values":        9,
        "Collect machine values":       10,

        "Evaluate results":             11,
        "Additional questions needed?": 12,

        "Display additional questions": 13,
        "Answer additional questions":  14,
        "Validate additional inputs":   15,

        "Store inspection record":      16,
        "Show inspection summary":      17,
        "Confirm inspection complete":  18,
        "End":                          19,
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
