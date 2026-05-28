#
# ProductPrototypeValidation.py
#
# Description: New product/improvement idea -> research -> design -> prototype -> test/refine loop -> approve or discard.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ProductPrototypeValidation",

    "lanes": ["R&D", "Test Lab", "Product Steering"],

    "elements": [
        ("Start",                         START,        "R&D"),
        ("Identify Idea",                 USER_TASK,    "R&D"),
        ("Research and Feasibility",      USER_TASK,    "R&D"),
        ("Draft Design Concepts",         USER_TASK,    "R&D"),
        ("Select Promising Design",       USER_TASK,    "R&D"),
        ("Build Prototype",               MANUAL_TASK,  "R&D"),

        ("Test Prototype",                USER_TASK,    "Test Lab"),
        ("Collect Test Feedback",         USER_TASK,    "Test Lab"),

        ("Refinement Needed?",            EXCLUSIVE_GW, "R&D"),
        ("Refine Prototype",              USER_TASK,    "R&D"),

        ("Review Results",                USER_TASK,    "Product Steering"),
        ("Approved for Further Dev?",     EXCLUSIVE_GW, "Product Steering"),
        ("Approved for Development",      END,          "Product Steering"),
        ("Discard Prototype",             END,          "Product Steering"),
    ],

    "flows": [
        ("Start",                    "Identify Idea",             ""),
        ("Identify Idea",            "Research and Feasibility",   ""),
        ("Research and Feasibility", "Draft Design Concepts",      ""),
        ("Draft Design Concepts",    "Select Promising Design",    ""),
        ("Select Promising Design",  "Build Prototype",            ""),
        ("Build Prototype",          "Test Prototype",             ""),
        ("Test Prototype",           "Collect Test Feedback",      ""),
        ("Collect Test Feedback",    "Refinement Needed?",         ""),

        ("Refinement Needed?",       "Refine Prototype",           "Yes"),
        ("Refine Prototype",         "Test Prototype",             "Retest"),

        ("Refinement Needed?",       "Review Results",             "No"),
        ("Review Results",           "Approved for Further Dev?",  ""),

        ("Approved for Further Dev?", "Approved for Development",  "Approved"),
        ("Approved for Further Dev?", "Discard Prototype",         "Discarded"),
    ],

    "layout": {
        "Start":                     0,
        "Identify Idea":             1,
        "Research and Feasibility":  2,
        "Draft Design Concepts":     3,
        "Select Promising Design":   4,
        "Build Prototype":           5,
        "Test Prototype":            6,
        "Collect Test Feedback":     7,
        "Refinement Needed?":        8,
        "Refine Prototype":          9,
        "Review Results":            9,
        "Approved for Further Dev?": 10,
        "Approved for Development":  11,
        "Discard Prototype":         11,   # auto-stacked under "Approved for Development"
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
