#
# OnlineShopPurchase.py
#
# Description: BPMN process for purchasing items from an online shop with parallel activities,
#              payment options, reward selection, and return handling
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OnlineShopPurchase",
    
    "lanes": ["Customer"],
    
    "elements": [
        # Process start
        ("Start", START, "Customer"),
        ("Login", USER_TASK, "Customer"),
        
        # Parallel fork - items and payment happen simultaneously
        ("Fork", PARALLEL_GW, "Customer"),
        
        # Branch 1: Items selection and reward
        ("Select Items", USER_TASK, "Customer"),
        ("Select Reward", USER_TASK, "Customer"),
        
        # Branch 2: Payment method and payment options
        ("Set Payment Method", USER_TASK, "Customer"),
        ("Payment Choice", EXCLUSIVE_GW, "Customer"),
        ("Pay", SERVICE_TASK, "Customer"),
        ("Installment Agreement", USER_TASK, "Customer"),
        ("Payment Merge", EXCLUSIVE_GW, "Customer"),
        
        # Synchronization point
        ("Join", PARALLEL_GW, "Customer"),
        
        # Delivery and return loop
        ("Delivery", SERVICE_TASK, "Customer"),
        ("Return?", EXCLUSIVE_GW, "Customer"),
        ("Return Items", USER_TASK, "Customer"),
        
        # Process end
        ("End", END, "Customer"),
    ],
    
    "flows": [
        # Start and fork
        ("Start", "Login", ""),
        ("Login", "Fork", ""),
        
        # Fork to parallel branches
        ("Fork", "Select Items", ""),
        ("Fork", "Set Payment Method", ""),
        
        # Branch 1: Items -> Reward -> Join
        ("Select Items", "Select Reward", ""),
        ("Select Reward", "Join", ""),
        
        # Branch 2: Payment method -> Payment choice -> Pay/Installment -> Merge -> Join
        ("Set Payment Method", "Payment Choice", ""),
        ("Payment Choice", "Pay", "Direct Payment"),
        ("Payment Choice", "Installment Agreement", "Installment Plan"),
        ("Pay", "Payment Merge", ""),
        ("Installment Agreement", "Payment Merge", ""),
        ("Payment Merge", "Join", ""),
        
        # After both branches complete
        ("Join", "Delivery", ""),
        
        # Return decision and loop
        ("Delivery", "Return?", ""),
        ("Return?", "End", "No"),
        ("Return?", "Return Items", "Yes"),
        ("Return Items", "Delivery", ""),
    ],
    
    "layout": {
        # Sequential start
        "Start": 0,
        "Login": 1,
        "Fork": 2,
        
        # Parallel branches (auto-stacked in same column)
        "Select Items": 3,
        "Set Payment Method": 3,
        
        "Select Reward": 4,
        "Payment Choice": 4,
        
        # Payment options (auto-stacked)
        "Pay": 5,
        "Installment Agreement": 5,
        
        # Merge paths
        "Payment Merge": 6,
        "Join": 7,
        
        # Delivery and return
        "Delivery": 8,
        "Return?": 9,
        
        # End options (auto-stacked)
        "End": 10,
        "Return Items": 10,
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
