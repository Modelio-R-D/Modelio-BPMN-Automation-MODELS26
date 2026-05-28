#
# ProductPrototypingProcess.py
#
# Description: R&D product prototyping process from idea to approval/discard
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ProductPrototypingProcess",
    
    "lanes": ["R&D Team", "Testing Team", "Management"],
    
    "elements": [
        # R&D Team activities
        ("Start",                   START,        "R&D Team"),
        ("Identify Idea",           USER_TASK,    "R&D Team"),
        ("Conduct Research",        USER_TASK,    "R&D Team"),
        ("Draft Design Concepts",   USER_TASK,    "R&D Team"),
        ("Select Design",           USER_TASK,    "R&D Team"),
        ("Build Prototype",         MANUAL_TASK,  "R&D Team"),
        ("Refine Prototype",        MANUAL_TASK,  "R&D Team"),
        
        # Testing Team activities
        ("Test Prototype",          USER_TASK,    "Testing Team"),
        ("Collect Feedback",        USER_TASK,    "Testing Team"),
        
        # Decision gateways
        ("Refinement Needed?",      EXCLUSIVE_GW, "Testing Team"),
        ("Approval Decision",       EXCLUSIVE_GW, "Management"),
        
        # End events
        ("Approved for Development", END,         "Management"),
        ("Prototype Discarded",      END,         "Management"),
    ],
    
    "flows": [
        ("Start",                   "Identify Idea",            ""),
        ("Identify Idea",           "Conduct Research",         ""),
        ("Conduct Research",        "Draft Design Concepts",    ""),
        ("Draft Design Concepts",   "Select Design",            ""),
        ("Select Design",           "Build Prototype",          ""),
        ("Build Prototype",         "Test Prototype",           ""),
        ("Test Prototype",          "Collect Feedback",         ""),
        ("Collect Feedback",        "Refinement Needed?",       ""),
        ("Refinement Needed?",      "Refine Prototype",         "Yes"),
        ("Refinement Needed?",      "Approval Decision",        "No"),
        ("Refine Prototype",        "Test Prototype",           ""),
        ("Approval Decision",       "Approved for Development", "Approved"),
        ("Approval Decision",       "Prototype Discarded",      "Discarded"),
    ],
    
    "layout": {
        "Start":                    0,
        "Identify Idea":            1,
        "Conduct Research":         2,
        "Draft Design Concepts":    3,
        "Select Design":            4,
        "Build Prototype":          5,
        "Test Prototype":           6,
        "Collect Feedback":         7,
        "Refinement Needed?":       8,
        "Refine Prototype":         9,
        "Approval Decision":        10,
        "Approved for Development": 11,
        "Prototype Discarded":      11,
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
