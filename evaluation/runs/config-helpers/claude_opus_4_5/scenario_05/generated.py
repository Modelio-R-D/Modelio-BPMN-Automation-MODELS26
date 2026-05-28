#
# SupplierSelectionProcess.py
#
# Description: Supplier selection and onboarding process from need identification through contract execution
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "SupplierSelectionProcess",
    
    "lanes": ["Procurement Team", "Management", "Supplier"],
    
    "elements": [
        # Start
        ("Start",                    START,        "Procurement Team"),
        
        # Initial phases
        ("Identify Supplier Need",   USER_TASK,    "Procurement Team"),
        ("Issue RFP",                SEND_TASK,    "Procurement Team"),
        ("Receive Proposals",        RECEIVE_TASK, "Procurement Team"),
        
        # Evaluation phase
        ("Evaluate Proposals",       USER_TASK,    "Procurement Team"),
        ("Site Visit Required?",     EXCLUSIVE_GW, "Procurement Team"),
        ("Conduct Site Visit",       USER_TASK,    "Procurement Team"),
        ("Conduct Interviews",       USER_TASK,    "Procurement Team"),
        ("Merge Evaluation",         EXCLUSIVE_GW, "Procurement Team"),
        
        # Selection and analysis
        ("Analyze Results",          USER_TASK,    "Procurement Team"),
        ("Select Supplier",          USER_TASK,    "Management"),
        
        # Contract phase
        ("Negotiate Contract",       USER_TASK,    "Procurement Team"),
        ("Terms Agreed?",            EXCLUSIVE_GW, "Procurement Team"),
        ("Sign Contract",            USER_TASK,    "Management"),
        ("Countersign Contract",     USER_TASK,    "Supplier"),
        
        # Completion
        ("Onboard Supplier",         SERVICE_TASK, "Procurement Team"),
        ("Execute Contract",         SERVICE_TASK, "Procurement Team"),
        ("End",                      END,          "Procurement Team"),
    ],
    
    "data_objects": [
        ("RFP Document",      "Procurement Team", 2),
        ("Proposals",         "Procurement Team", 3),
        ("Evaluation Report", "Procurement Team", 6),
        ("Contract",          "Management",       10),
    ],
    
    "data_associations": [
        ("Issue RFP",         "RFP Document"),
        ("RFP Document",      "Receive Proposals"),
        ("Receive Proposals", "Proposals"),
        ("Proposals",         "Evaluate Proposals"),
        ("Analyze Results",   "Evaluation Report"),
        ("Evaluation Report", "Select Supplier"),
        ("Sign Contract",     "Contract"),
        ("Contract",          "Countersign Contract"),
    ],
    
    "flows": [
        ("Start",                  "Identify Supplier Need", ""),
        ("Identify Supplier Need", "Issue RFP",              ""),
        ("Issue RFP",              "Receive Proposals",      ""),
        ("Receive Proposals",      "Evaluate Proposals",     ""),
        ("Evaluate Proposals",     "Site Visit Required?",   ""),
        ("Site Visit Required?",   "Conduct Site Visit",     "Yes"),
        ("Site Visit Required?",   "Conduct Interviews",     "No"),
        ("Conduct Site Visit",     "Merge Evaluation",       ""),
        ("Conduct Interviews",     "Merge Evaluation",       ""),
        ("Merge Evaluation",       "Analyze Results",        ""),
        ("Analyze Results",        "Select Supplier",        ""),
        ("Select Supplier",        "Negotiate Contract",     ""),
        ("Negotiate Contract",     "Terms Agreed?",          ""),
        ("Terms Agreed?",          "Negotiate Contract",     "No"),
        ("Terms Agreed?",          "Sign Contract",          "Yes"),
        ("Sign Contract",          "Countersign Contract",   ""),
        ("Countersign Contract",   "Onboard Supplier",       ""),
        ("Onboard Supplier",       "Execute Contract",       ""),
        ("Execute Contract",       "End",                    ""),
    ],
    
    "layout": {
        "Start":                  0,
        "Identify Supplier Need": 1,
        "Issue RFP":              2,
        "Receive Proposals":      3,
        "Evaluate Proposals":     4,
        "Site Visit Required?":   5,
        "Conduct Site Visit":     6,
        "Conduct Interviews":     6,
        "Merge Evaluation":       7,
        "Analyze Results":        8,
        "Select Supplier":        9,
        "Negotiate Contract":     10,
        "Terms Agreed?":          11,
        "Sign Contract":          12,
        "Countersign Contract":   13,
        "Onboard Supplier":       14,
        "Execute Contract":       15,
        "End":                    16,
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
