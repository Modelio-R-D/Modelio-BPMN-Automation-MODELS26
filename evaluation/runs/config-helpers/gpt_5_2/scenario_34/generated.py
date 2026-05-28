#
# BuildingCustomMachineFromLego.py
#
# Description: BPMN process for building a custom machine from LEGO bricks with sorting, subcomponent build/test loops, and assembly.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Building a custom machine out of Lego bricks",

    "lanes": ["Builder", "Children"],

    "elements": [
        ("Start",                 START,           "Builder"),
        ("Develop basic design",  USER_TASK,       "Builder"),
        ("Order LEGO sets",       USER_TASK,       "Builder"),
        ("Give sets to children", USER_TASK,       "Builder"),

        ("Sort parts into containers", MANUAL_TASK, "Children"),

        ("Build subcomponent",    USER_TASK,       "Builder"),
        ("Parts available?",      EXCLUSIVE_GW,    "Builder"),
        ("Reorder individual parts", USER_TASK,    "Builder"),

        ("Test subcomponent",     SERVICE_TASK,    "Builder"),
        ("Test successful?",      EXCLUSIVE_GW,    "Builder"),
        ("Redesign subcomponent", USER_TASK,       "Builder"),

        ("Assemble subcomponents", USER_TASK,      "Builder"),
        ("More subcomponents?",    EXCLUSIVE_GW,   "Builder"),

        ("End",                   END,             "Builder"),
    ],

    "data_objects": [
        ("Basic design",        "Builder",  1),
        ("LEGO sets",           "Builder",  2),
        ("Sorted containers",   "Children", 4),
        ("Reordered parts",     "Builder",  7),
    ],

    "data_associations": [
        ("Develop basic design", "Basic design"),
        ("Basic design",         "Order LEGO sets"),

        ("Order LEGO sets",      "LEGO sets"),
        ("LEGO sets",            "Give sets to children"),

        ("Sort parts into containers", "Sorted containers"),
        ("Sorted containers",          "Build subcomponent"),

        ("Reorder individual parts", "Reordered parts"),
        ("Reordered parts",          "Build subcomponent"),
    ],

    "flows": [
        ("Start",                 "Develop basic design",        ""),
        ("Develop basic design",  "Order LEGO sets",             ""),
        ("Order LEGO sets",       "Give sets to children",       ""),
        ("Give sets to children", "Sort parts into containers",  ""),

        ("Sort parts into containers", "Build subcomponent",     ""),

        ("Build subcomponent",    "Parts available?",            ""),
        ("Parts available?",      "Reorder individual parts",    "No"),
        ("Reorder individual parts", "Build subcomponent",       ""),

        ("Parts available?",      "Test subcomponent",           "Yes"),
        ("Test subcomponent",     "Test successful?",            ""),
        ("Test successful?",      "Redesign subcomponent",       "No"),
        ("Redesign subcomponent", "Build subcomponent",          ""),

        ("Test successful?",      "Assemble subcomponents",      "Yes"),
        ("Assemble subcomponents", "More subcomponents?",        ""),
        ("More subcomponents?",    "Build subcomponent",         "Yes"),
        ("More subcomponents?",    "End",                        "No"),
    ],

    "layout": {
        "Start":                   0,
        "Develop basic design":    1,
        "Order LEGO sets":         2,
        "Give sets to children":   3,

        "Sort parts into containers": 4,

        "Build subcomponent":      5,
        "Parts available?":        6,

        # Same lane + same column => auto-stacked (v3.2)
        "Reorder individual parts": 7,
        "Test subcomponent":        7,

        "Test successful?":         8,

        # Same lane + same column => auto-stacked (v3.2)
        "Redesign subcomponent":    9,
        "Assemble subcomponents":   9,

        "More subcomponents?":     10,
        "End":                     11,
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
