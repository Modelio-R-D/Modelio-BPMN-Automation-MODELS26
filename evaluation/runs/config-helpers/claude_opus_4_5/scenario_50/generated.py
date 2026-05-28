#
# ClaimHandlingProcess.py
#
# Description: Claim registration, examination, settlement recommendation with senior review loop
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ClaimHandlingProcess",
    
    "lanes": ["Claims Officer", "Senior Claims Officer"],
    
    "elements": [
        ("Claim Registered",              START,        "Claims Officer"),
        ("Examine Claim",                 USER_TASK,    "Claims Officer"),
        ("Write Settlement Recommendation", USER_TASK,  "Claims Officer"),
        ("Check Recommendation",          USER_TASK,    "Senior Claims Officer"),
        ("Claim OK?",                     EXCLUSIVE_GW, "Senior Claims Officer"),
        ("Claim Handling Proceeds",       END,          "Senior Claims Officer"),
    ],
    
    "flows": [
        ("Claim Registered",              "Examine Claim",                  ""),
        ("Examine Claim",                 "Write Settlement Recommendation", ""),
        ("Write Settlement Recommendation", "Check Recommendation",         ""),
        ("Check Recommendation",          "Claim OK?",                      ""),
        ("Claim OK?",                     "Claim Handling Proceeds",        "OK"),
        ("Claim OK?",                     "Write Settlement Recommendation", "Not OK"),
    ],
    
    "layout": {
        "Claim Registered":              0,
        "Examine Claim":                 1,
        "Write Settlement Recommendation": 2,
        "Check Recommendation":          3,
        "Claim OK?":                     4,
        "Claim Handling Proceeds":       5,
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
