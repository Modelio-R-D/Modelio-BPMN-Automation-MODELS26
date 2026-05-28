#
# SupplierProcurement.py
#
# Description: Supplier/Vendor Procurement Process - from RFP to contract execution
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SupplierProcurement",
    
    "lanes": ["Procurement Team", "Suppliers", "Management"],
    
    "elements": [
        # Start
        ("Start",               START,        "Procurement Team"),
        
        # Procurement Team activities
        ("Issue RFP",           USER_TASK,    "Procurement Team"),
        ("Evaluate Proposals",  USER_TASK,    "Procurement Team"),
        ("Conduct Site Visits", USER_TASK,    "Procurement Team"),
        ("Select Supplier",     USER_TASK,    "Procurement Team"),
        ("Negotiate Contract",  USER_TASK,    "Procurement Team"),
        ("Terms Agreed?",       EXCLUSIVE_GW, "Procurement Team"),
        ("Revise Terms",        USER_TASK,    "Procurement Team"),
        ("Onboard Supplier",    USER_TASK,    "Procurement Team"),
        ("Execute Contract",    USER_TASK,    "Procurement Team"),
        
        # Suppliers activities
        ("Submit Proposals",    USER_TASK,    "Suppliers"),
        
        # Management activities
        ("Approve Contract",    USER_TASK,    "Management"),
        ("Sign Contract",       USER_TASK,    "Management"),
        
        # End
        ("End",                 END,          "Procurement Team"),
    ],
    
    "flows": [
        ("Start",               "Issue RFP",           ""),
        ("Issue RFP",           "Submit Proposals",    ""),
        ("Submit Proposals",    "Evaluate Proposals",  ""),
        ("Evaluate Proposals",  "Conduct Site Visits", ""),
        ("Conduct Site Visits", "Select Supplier",     ""),
        ("Select Supplier",     "Negotiate Contract",  ""),
        ("Negotiate Contract",  "Terms Agreed?",       ""),
        ("Terms Agreed?",       "Approve Contract",    "Yes"),
        ("Terms Agreed?",       "Revise Terms",        "No"),
        ("Revise Terms",        "Negotiate Contract",  ""),
        ("Approve Contract",    "Sign Contract",       ""),
        ("Sign Contract",       "Onboard Supplier",    ""),
        ("Onboard Supplier",    "Execute Contract",    ""),
        ("Execute Contract",    "End",                 ""),
    ],
    
    "layout": {
        "Start":               0,
        "Issue RFP":           1,
        "Submit Proposals":    2,
        "Evaluate Proposals":  3,
        "Conduct Site Visits": 4,
        "Select Supplier":     5,
        "Negotiate Contract":  6,
        "Terms Agreed?":       7,
        "Revise Terms":        8,
        "Approve Contract":    8,
        "Sign Contract":       9,
        "Onboard Supplier":    10,
        "Execute Contract":    11,
        "End":                 12,
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
