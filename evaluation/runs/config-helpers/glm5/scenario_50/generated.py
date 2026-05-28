#
# ClaimsHandling.py
#
# Description: Claims handling process with senior officer review loop
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ClaimsHandling",
    
    "lanes": ["Claims Officer", "Senior Claims Officer"],
    
    "elements": [
        ("Start", START, "Claims Officer"),
        ("Examine Claim", USER_TASK, "Claims Officer"),
        ("Write Recommendation", USER_TASK, "Claims Officer"),
        ("Check Recommendation", USER_TASK, "Senior Claims Officer"),
        ("OK?", EXCLUSIVE_GW, "Senior Claims Officer"),
        ("End", END, "Senior Claims Officer"),
    ],
    
    "flows": [
        ("Start", "Examine Claim", ""),
        ("Examine Claim", "Write Recommendation", ""),
        ("Write Recommendation", "Check Recommendation", ""),
        ("Check Recommendation", "OK?", ""),
        ("OK?", "End", "OK"),
        ("OK?", "Write Recommendation", "Not OK"),
    ],
    
    "layout": {
        "Start": 0,
        "Examine Claim": 1,
        "Write Recommendation": 2,
        "Check Recommendation": 3,
        "OK?": 4,
        "End": 5,
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
