#
# SupplierSelectionAndOnboarding.py
#
# Description: Supplier/vendor selection from identified need through RFP, evaluation, optional site visit, negotiation, signing, onboarding, and contract execution.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SupplierSelectionAndOnboarding",

    "lanes": ["Company", "Procurement", "Supplier"],

    "elements": [
        ("Start",                         START,          "Company"),
        ("Identify Need",                 USER_TASK,      "Company"),

        ("Issue RFP",                     SEND_TASK,      "Procurement"),
        ("Submit Proposal",               SEND_TASK,      "Supplier"),
        ("Receive Proposals",             RECEIVE_TASK,   "Procurement"),
        ("Evaluate Proposals",            BUSINESS_RULE_TASK, "Procurement"),

        ("Need Site Visit?",              EXCLUSIVE_GW,   "Procurement"),
        ("Conduct Site Visit/Interview",  USER_TASK,      "Procurement"),

        ("Select Supplier",               USER_TASK,      "Procurement"),
        ("Negotiate Contract",            USER_TASK,      "Procurement"),

        ("Terms Agreed?",                 EXCLUSIVE_GW,   "Procurement"),
        ("Revise Terms",                  USER_TASK,      "Procurement"),

        ("Signing Split",                 PARALLEL_GW,    "Procurement"),
        ("Company Signs Contract",        USER_TASK,      "Company"),
        ("Supplier Signs Contract",       USER_TASK,      "Supplier"),
        ("Signing Join",                  PARALLEL_GW,    "Procurement"),

        ("Onboard and Execute Split",     PARALLEL_GW,    "Procurement"),
        ("Onboard Supplier",              USER_TASK,      "Procurement"),
        ("Execute Contract",              SERVICE_TASK,   "Procurement"),
        ("Onboard and Execute Join",      PARALLEL_GW,    "Procurement"),

        ("End",                           END,            "Procurement"),
    ],

    "flows": [
        ("Start",                "Identify Need",                ""),
        ("Identify Need",        "Issue RFP",                     ""),

        ("Issue RFP",            "Submit Proposal",               ""),
        ("Submit Proposal",      "Receive Proposals",             ""),
        ("Receive Proposals",    "Evaluate Proposals",            ""),

        ("Evaluate Proposals",   "Need Site Visit?",              ""),
        ("Need Site Visit?",     "Conduct Site Visit/Interview",  "Yes"),
        ("Need Site Visit?",     "Select Supplier",               "No"),
        ("Conduct Site Visit/Interview", "Select Supplier",        ""),

        ("Select Supplier",      "Negotiate Contract",            ""),
        ("Negotiate Contract",   "Terms Agreed?",                 ""),

        ("Terms Agreed?",        "Signing Split",                 "Yes"),
        ("Terms Agreed?",        "Revise Terms",                  "No"),
        ("Revise Terms",         "Negotiate Contract",            "Rework"),

        ("Signing Split",        "Company Signs Contract",        ""),
        ("Signing Split",        "Supplier Signs Contract",       ""),
        ("Company Signs Contract",  "Signing Join",               ""),
        ("Supplier Signs Contract", "Signing Join",               ""),

        ("Signing Join",         "Onboard and Execute Split",     ""),
        ("Onboard and Execute Split", "Onboard Supplier",         ""),
        ("Onboard and Execute Split", "Execute Contract",         ""),
        ("Onboard Supplier",     "Onboard and Execute Join",      ""),
        ("Execute Contract",     "Onboard and Execute Join",      ""),

        ("Onboard and Execute Join", "End",                       ""),
    ],

    "layout": {
        "Start":                         0,
        "Identify Need":                 1,

        "Issue RFP":                     2,
        "Submit Proposal":               3,
        "Receive Proposals":             4,
        "Evaluate Proposals":            5,

        "Need Site Visit?":              6,
        "Conduct Site Visit/Interview":  7,

        "Select Supplier":               8,
        "Negotiate Contract":            9,

        "Terms Agreed?":                 10,
        # Same lane + same column -> auto-stacked (v3.2)
        "Signing Split":                 11,
        "Revise Terms":                  11,

        "Company Signs Contract":        12,
        "Supplier Signs Contract":       12,
        "Signing Join":                  13,

        "Onboard and Execute Split":     14,
        # Same lane + same column -> auto-stacked (v3.2)
        "Onboard Supplier":              15,
        "Execute Contract":              15,
        "Onboard and Execute Join":      16,

        "End":                           17,
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
