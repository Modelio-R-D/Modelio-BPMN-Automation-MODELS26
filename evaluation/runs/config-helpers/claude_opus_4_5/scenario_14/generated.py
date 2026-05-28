#
# BudgetPlanningProcess.py
#
# Description: Departmental budget planning from objectives through allocation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BudgetPlanningProcess",
    
    "lanes": ["Department", "Strategy Team", "Finance", "Stakeholders"],
    
    "elements": [
        # Department activities
        ("Start",                    START,        "Department"),
        ("Outline Objectives",       USER_TASK,    "Department"),
        ("Draft Budget Plan",        USER_TASK,    "Department"),
        ("Make Adjustments",         USER_TASK,    "Department"),
        ("Implement Plan",           USER_TASK,    "Department"),
        ("End",                      END,          "Department"),
        
        # Strategy Team review
        ("Strategic Alignment Review", USER_TASK,  "Strategy Team"),
        ("Aligns with Goals?",       EXCLUSIVE_GW, "Strategy Team"),
        
        # Finance review
        ("Feasibility Review",       USER_TASK,    "Finance"),
        ("Budget Feasible?",         EXCLUSIVE_GW, "Finance"),
        ("Allocate Budget",          SERVICE_TASK, "Finance"),
        
        # Stakeholder approval
        ("Document Adjustments",     USER_TASK,    "Stakeholders"),
        ("Stakeholder Approval",     USER_TASK,    "Stakeholders"),
        ("Final Approval",           USER_TASK,    "Stakeholders"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",                    "Outline Objectives",        ""),
        ("Outline Objectives",       "Draft Budget Plan",         ""),
        ("Draft Budget Plan",        "Strategic Alignment Review", ""),
        
        # Strategic review
        ("Strategic Alignment Review", "Aligns with Goals?",      ""),
        ("Aligns with Goals?",       "Feasibility Review",        "Yes"),
        ("Aligns with Goals?",       "Make Adjustments",          "No"),
        
        # Finance review
        ("Feasibility Review",       "Budget Feasible?",          ""),
        ("Budget Feasible?",         "Document Adjustments",      "Yes"),
        ("Budget Feasible?",         "Make Adjustments",          "No"),
        
        # Adjustment loop
        ("Make Adjustments",         "Strategic Alignment Review", ""),
        
        # Approval flow
        ("Document Adjustments",     "Stakeholder Approval",      ""),
        ("Stakeholder Approval",     "Final Approval",            ""),
        ("Final Approval",           "Allocate Budget",           ""),
        
        # Final steps
        ("Allocate Budget",          "Implement Plan",            ""),
        ("Implement Plan",           "End",                       ""),
    ],
    
    "data_objects": [
        ("Budget Plan",              "Department",    2),
        ("Review Feedback",          "Strategy Team", 4),
        ("Approved Budget",          "Finance",       9),
    ],
    
    "data_associations": [
        ("Draft Budget Plan",        "Budget Plan"),
        ("Budget Plan",              "Strategic Alignment Review"),
        ("Strategic Alignment Review", "Review Feedback"),
        ("Review Feedback",          "Make Adjustments"),
        ("Final Approval",           "Approved Budget"),
        ("Approved Budget",          "Allocate Budget"),
    ],
    
    "layout": {
        "Start":                     0,
        "Outline Objectives":        1,
        "Draft Budget Plan":         2,
        "Strategic Alignment Review": 3,
        "Aligns with Goals?":        4,
        "Feasibility Review":        5,
        "Budget Feasible?":          6,
        "Make Adjustments":          4,
        "Document Adjustments":      7,
        "Stakeholder Approval":      8,
        "Final Approval":            9,
        "Allocate Budget":           10,
        "Implement Plan":            11,
        "End":                       12,
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
