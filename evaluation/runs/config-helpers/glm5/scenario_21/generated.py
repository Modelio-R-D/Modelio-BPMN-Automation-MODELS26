#
# ShippingProcess.py
#
# Description: BPMN diagram for goods shipping process with parallel packaging
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ShippingProcess",
    
    "lanes": ["Secretary", "Logistics Department Head", "Warehousemen"],
    
    "elements": [
        # Start
        ("Start", START, "Secretary"),
        
        # Initial clarification
        ("Clarify Shipping", USER_TASK, "Secretary"),
        
        # Parallel gateway - shipping arrangement and packaging happen simultaneously
        ("Fork", PARALLEL_GW, "Secretary"),
        
        # Decision gateway
        ("Large Amount?", EXCLUSIVE_GW, "Secretary"),
        
        # Large amount path (Secretary)
        ("Invite Logistic Companies", USER_TASK, "Secretary"),
        ("Select Logistic Company", USER_TASK, "Secretary"),
        
        # Small amount path (Secretary + Logistics Head)
        ("Write Package Label", USER_TASK, "Secretary"),
        ("Insurance Needed?", EXCLUSIVE_GW, "Secretary"),
        ("Take Parcel Insurance", USER_TASK, "Logistics Department Head"),
        
        # Parallel packaging (Warehousemen)
        ("Package Goods", USER_TASK, "Warehousemen"),
        
        # Convergence and end
        ("Join", PARALLEL_GW, "Secretary"),
        ("Prepare for Pickup", USER_TASK, "Secretary"),
        ("End", END, "Secretary"),
    ],
    
    "flows": [
        ("Start", "Clarify Shipping", ""),
        ("Clarify Shipping", "Fork", ""),
        
        # Parallel branches from Fork
        ("Fork", "Large Amount?", ""),
        ("Fork", "Package Goods", ""),
        
        # Large amount path (Yes)
        ("Large Amount?", "Invite Logistic Companies", "Yes"),
        ("Invite Logistic Companies", "Select Logistic Company", ""),
        ("Select Logistic Company", "Join", ""),
        
        # Small amount path (No)
        ("Large Amount?", "Write Package Label", "No"),
        ("Write Package Label", "Insurance Needed?", ""),
        ("Insurance Needed?", "Take Parcel Insurance", "Yes"),
        ("Insurance Needed?", "Join", "No"),
        ("Take Parcel Insurance", "Join", ""),
        
        # Packaging path
        ("Package Goods", "Join", ""),
        
        # Final steps
        ("Join", "Prepare for Pickup", ""),
        ("Prepare for Pickup", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Clarify Shipping": 1,
        "Fork": 2,
        "Large Amount?": 3,
        "Package Goods": 3,                    # Same column, different lane (parallel)
        "Invite Logistic Companies": (4, 0),   # Large path - top position
        "Write Package Label": (4, 90),       # Small path - below (stacked)
        "Select Logistic Company": (5, 0),    # Large path continuation - top
        "Insurance Needed?": (5, 90),          # Small path continuation - below
        "Take Parcel Insurance": 6,
        "Join": 7,
        "Prepare for Pickup": 8,
        "End": 9,
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
