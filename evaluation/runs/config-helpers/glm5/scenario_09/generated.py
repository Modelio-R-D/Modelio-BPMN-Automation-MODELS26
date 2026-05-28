#
# ProductDevelopment.py
#
# Description: Product development process with prototype testing and refinement loop
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ProductDevelopment",
    
    "lanes": ["R&D Team"],
    
    "elements": [
        ("Start",                    START,        "R&D Team"),
        ("Identify Idea",            USER_TASK,    "R&D Team"),
        ("Conduct Research",         SERVICE_TASK, "R&D Team"),
        ("Draft Design Concepts",    USER_TASK,    "R&D Team"),
        ("Build Prototype",          MANUAL_TASK,  "R&D Team"),
        ("Test Prototype",           SERVICE_TASK, "R&D Team"),
        ("Collect Feedback",         USER_TASK,    "R&D Team"),
        ("Refinement Needed?",       EXCLUSIVE_GW, "R&D Team"),
        ("Refine Prototype",         USER_TASK,    "R&D Team"),
        ("Approved for Development?", EXCLUSIVE_GW, "R&D Team"),
        ("End Approved",             END,          "R&D Team"),
        ("End Discarded",            END,          "R&D Team"),
    ],
    
    "flows": [
        ("Start",                    "Identify Idea",         ""),
        ("Identify Idea",            "Conduct Research",      ""),
        ("Conduct Research",         "Draft Design Concepts", ""),
        ("Draft Design Concepts",    "Build Prototype",       ""),
        ("Build Prototype",          "Test Prototype",        ""),
        ("Test Prototype",           "Collect Feedback",      ""),
        ("Collect Feedback",         "Refinement Needed?",    ""),
        ("Refinement Needed?",       "Refine Prototype",      "Yes"),
        ("Refine Prototype",         "Test Prototype",        ""),
        ("Refinement Needed?",       "Approved for Development?", "No"),
        ("Approved for Development?", "End Approved",         "Approved"),
        ("Approved for Development?", "End Discarded",        "Discarded"),
    ],
    
    "layout": {
        "Start":                     0,
        "Identify Idea":             1,
        "Conduct Research":          2,
        "Draft Design Concepts":     3,
        "Build Prototype":           4,
        "Test Prototype":            5,
        "Collect Feedback":          6,
        "Refinement Needed?":        7,
        "Refine Prototype":          8,
        "Approved for Development?": 8,  # Auto-stacked with Refine Prototype
        "End Approved":              9,
        "End Discarded":             9,  # Auto-stacked with End Approved
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
