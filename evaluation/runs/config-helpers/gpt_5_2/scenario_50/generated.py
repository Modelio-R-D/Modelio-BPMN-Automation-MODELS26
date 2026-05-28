#
# ClaimSettlementRecommendation.py
#
# Description: Claim is examined, settlement recommendation written, checked by senior officer.
#              If Not OK, loop back to rewrite recommendation. If OK, proceed with claim handling.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ClaimSettlementRecommendation",

    "lanes": [
        "Claims Officer",
        "Senior Claims Officer",
    ],

    "elements": [
        ("Claim Registered",                 START,        "Claims Officer"),
        ("Examine Claim",                    USER_TASK,    "Claims Officer"),
        ("Write Settlement Recommendation",  USER_TASK,    "Claims Officer"),
        ("Check Recommendation",             USER_TASK,    "Senior Claims Officer"),
        ("Recommendation OK?",               EXCLUSIVE_GW, "Senior Claims Officer"),
        ("Proceed With Claim Handling",      USER_TASK,    "Claims Officer"),
        ("End",                              END,          "Claims Officer"),
    ],

    "flows": [
        ("Claim Registered",                "Examine Claim",                   ""),
        ("Examine Claim",                   "Write Settlement Recommendation", ""),
        ("Write Settlement Recommendation", "Check Recommendation",            ""),
        ("Check Recommendation",            "Recommendation OK?",              ""),

        ("Recommendation OK?",              "Write Settlement Recommendation", "Not OK"),
        ("Recommendation OK?",              "Proceed With Claim Handling",     "OK"),

        ("Proceed With Claim Handling",     "End",                             ""),
    ],

    "layout": {
        "Claim Registered":                0,
        "Examine Claim":                   1,
        "Write Settlement Recommendation": 2,
        "Check Recommendation":            3,
        "Recommendation OK?":              4,
        "Proceed With Claim Handling":     5,
        "End":                             6,
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
