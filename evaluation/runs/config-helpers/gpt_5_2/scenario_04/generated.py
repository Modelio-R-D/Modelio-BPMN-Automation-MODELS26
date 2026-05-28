#
# MarketingCampaignProcess.py
#
# Description: BPMN for planning, launching, tracking, and closing a marketing campaign with lead handoff to sales.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "MarketingCampaignProcess",

    "lanes": ["Marketing", "Sales"],

    "elements": [
        ("Start",                    START,         "Marketing"),
        ("Define Objectives",        USER_TASK,     "Marketing"),
        ("Create Content",           USER_TASK,     "Marketing"),
        ("Design Visuals",           USER_TASK,     "Marketing"),
        ("Select Promotion Channels",USER_TASK,     "Marketing"),
        ("Launch Campaign",          USER_TASK,     "Marketing"),
        ("Track Performance",        SERVICE_TASK,  "Marketing"),

        ("Collect Leads in CRM",     SERVICE_TASK,  "Sales"),
        ("Sales Follow Up",          USER_TASK,     "Sales"),

        ("End Campaign Period",      USER_TASK,     "Marketing"),
        ("Analyze Performance",      USER_TASK,     "Marketing"),
        ("End",                      END,           "Marketing"),
    ],

    "data_objects": [
        ("Campaign Brief",       "Marketing", 1),
        ("Content Draft",        "Marketing", 2),
        ("Visual Assets",        "Marketing", 3),
        ("Channel Plan",         "Marketing", 4),
        ("Campaign Instance",    "Marketing", 5),
        ("Performance Metrics",  "Marketing", 6),

        ("Leads (CRM)",          "Sales",     7),
        ("Follow Up Notes",      "Sales",     8),

        ("Performance Report",   "Marketing", 10),
    ],

    "data_associations": [
        ("Define Objectives",        "Campaign Brief"),
        ("Create Content",           "Content Draft"),
        ("Design Visuals",           "Visual Assets"),
        ("Select Promotion Channels","Channel Plan"),
        ("Launch Campaign",          "Campaign Instance"),
        ("Track Performance",        "Performance Metrics"),

        ("Collect Leads in CRM",     "Leads (CRM)"),
        ("Leads (CRM)",              "Sales Follow Up"),
        ("Sales Follow Up",          "Follow Up Notes"),

        ("Analyze Performance",      "Performance Report"),
    ],

    "flows": [
        ("Start",                    "Define Objectives",         ""),
        ("Define Objectives",        "Create Content",            ""),
        ("Create Content",           "Design Visuals",            ""),
        ("Design Visuals",           "Select Promotion Channels", ""),
        ("Select Promotion Channels","Launch Campaign",           ""),
        ("Launch Campaign",          "Track Performance",         ""),
        ("Track Performance",        "Collect Leads in CRM",      ""),
        ("Collect Leads in CRM",     "Sales Follow Up",           ""),
        ("Sales Follow Up",          "End Campaign Period",       ""),
        ("End Campaign Period",      "Analyze Performance",       ""),
        ("Analyze Performance",      "End",                       ""),
    ],

    "layout": {
        "Start":                     0,
        "Define Objectives":         1,
        "Create Content":            2,
        "Design Visuals":            3,
        "Select Promotion Channels": 4,
        "Launch Campaign":           5,
        "Track Performance":         6,

        "Collect Leads in CRM":      7,
        "Sales Follow Up":           8,

        "End Campaign Period":       9,
        "Analyze Performance":       10,
        "End":                       11,
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
