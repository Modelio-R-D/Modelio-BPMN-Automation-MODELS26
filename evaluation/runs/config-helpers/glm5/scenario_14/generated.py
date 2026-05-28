#
# BudgetPlanningProcess.py
#
# Description: Budget planning and allocation process with review cycles
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BudgetPlanningProcess",
    
    "lanes": ["Department Team", "Strategic Committee", "Finance Department", "Stakeholders"],
    
    "elements": [
        # Start - Department outlines objectives
        ("Start", START, "Department Team"),
        ("Outline Objectives", USER_TASK, "Department Team"),
        
        # Team drafts plan with cost estimates
        ("Draft Budget Plan", USER_TASK, "Department Team"),
        
        # Strategic alignment review
        ("Strategic Alignment Review", USER_TASK, "Strategic Committee"),
        
        # Finance detailed review
        ("Finance Review", USER_TASK, "Finance Department"),
        
        # Decision point - approved or needs adjustment
        ("Approved?", EXCLUSIVE_GW, "Finance Department"),
        
        # If approved - allocate and distribute
        ("Allocate Budget", SERVICE_TASK, "Finance Department"),
        
        # If not approved - document and get stakeholder approval
        ("Document Adjustments", USER_TASK, "Department Team"),
        ("Stakeholder Approval", USER_TASK, "Stakeholders"),
        
        # Final distribution
        ("Distribute Budget", SERVICE_TASK, "Finance Department"),
        
        # End - department begins implementation
        ("End", END, "Department Team"),
    ],
    
    "flows": [
        ("Start", "Outline Objectives", ""),
        ("Outline Objectives", "Draft Budget Plan", ""),
        ("Draft Budget Plan", "Strategic Alignment Review", ""),
        ("Strategic Alignment Review", "Finance Review", ""),
        ("Finance Review", "Approved?", ""),
        ("Approved?", "Allocate Budget", "Yes"),
        ("Approved?", "Document Adjustments", "No"),
        ("Document Adjustments", "Stakeholder Approval", ""),
        ("Stakeholder Approval", "Finance Review", ""),  # Loop back for re-review
        ("Allocate Budget", "Distribute Budget", ""),
        ("Distribute Budget", "End", ""),
    ],
    
    "data_objects": [
        ("Budget Plan", "Department Team", 2),
        ("Adjustment Records", "Department Team", 6),
    ],
    
    "data_associations": [
        ("Draft Budget Plan", "Budget Plan"),
        ("Budget Plan", "Strategic Alignment Review"),
        ("Budget Plan", "Finance Review"),
        ("Document Adjustments", "Adjustment Records"),
    ],
    
    "layout": {
        "Start": 0,
        "Outline Objectives": 1,
        "Draft Budget Plan": 2,
        "Strategic Alignment Review": 3,
        "Finance Review": 4,
        "Approved?": 5,
        "Allocate Budget": 6,
        "Document Adjustments": 6,
        "Distribute Budget": 7,
        "Stakeholder Approval": 7,
        "End": 8,
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
