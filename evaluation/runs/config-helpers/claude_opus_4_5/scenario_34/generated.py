#
# LegoBuildProcess.py
#
# Description: Process for building a custom machine out of Lego bricks,
#              including design, ordering, sorting, building subcomponents,
#              testing, and assembly.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LegoBuildProcess",
    
    "lanes": ["Designer", "Children", "Builder"],
    
    "elements": [
        # Designer lane
        ("Start",                  START,        "Designer"),
        ("Develop Basic Design",   USER_TASK,    "Designer"),
        ("Order Lego Sets",        USER_TASK,    "Designer"),
        ("Redesign Subcomponent",  USER_TASK,    "Designer"),
        
        # Children lane
        ("Sort Parts",             MANUAL_TASK,  "Children"),
        
        # Builder lane
        ("Parts Available?",       EXCLUSIVE_GW, "Builder"),
        ("Reorder Parts",          USER_TASK,    "Builder"),
        ("Build Subcomponent",     MANUAL_TASK,  "Builder"),
        ("Test Subcomponent",      USER_TASK,    "Builder"),
        ("Test OK?",               EXCLUSIVE_GW, "Builder"),
        ("More Subcomponents?",    EXCLUSIVE_GW, "Builder"),
        ("Assemble Machine",       MANUAL_TASK,  "Builder"),
        ("End",                    END,          "Builder"),
    ],
    
    "flows": [
        ("Start",                 "Develop Basic Design",  ""),
        ("Develop Basic Design",  "Order Lego Sets",       ""),
        ("Order Lego Sets",       "Sort Parts",            ""),
        ("Sort Parts",            "Parts Available?",      ""),
        ("Parts Available?",      "Build Subcomponent",    "Yes"),
        ("Parts Available?",      "Reorder Parts",         "No"),
        ("Reorder Parts",         "Parts Available?",      ""),
        ("Build Subcomponent",    "Test Subcomponent",     ""),
        ("Test Subcomponent",     "Test OK?",              ""),
        ("Test OK?",              "More Subcomponents?",   "Yes"),
        ("Test OK?",              "Redesign Subcomponent", "No"),
        ("Redesign Subcomponent", "Build Subcomponent",    ""),
        ("More Subcomponents?",   "Parts Available?",      "Yes"),
        ("More Subcomponents?",   "Assemble Machine",      "No"),
        ("Assemble Machine",      "End",                   ""),
    ],
    
    "data_objects": [
        ("Design Specs",       "Designer",  1),
        ("Sorted Containers",  "Children",  3),
    ],
    
    "data_associations": [
        ("Develop Basic Design", "Design Specs"),
        ("Design Specs",         "Order Lego Sets"),
        ("Sort Parts",           "Sorted Containers"),
        ("Sorted Containers",    "Build Subcomponent"),
    ],
    
    "layout": {
        "Start":                  0,
        "Develop Basic Design":   1,
        "Order Lego Sets":        2,
        "Sort Parts":             3,
        "Parts Available?":       4,
        "Reorder Parts":          5,
        "Build Subcomponent":     6,
        "Test Subcomponent":      7,
        "Test OK?":               8,
        "More Subcomponents?":    9,
        "Redesign Subcomponent":  8,
        "Assemble Machine":       10,
        "End":                    11,
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
