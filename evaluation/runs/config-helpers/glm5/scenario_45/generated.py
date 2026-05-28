#
# OnlineShopOrdering.py
#
# Description: BPMN process for ordering in an online shop, including login,
#              product selection loop, parallel payment/shipping, and order finalization.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OnlineShopOrdering",
    
    "lanes": ["Customer", "E-Shop System"],
    
    "elements": [
        # Start and Login
        ("Start", START, "Customer"),
        ("Login", USER_TASK, "Customer"),
        ("Check Credentials", SERVICE_TASK, "E-Shop System"),
        ("Login Successful?", EXCLUSIVE_GW, "E-Shop System"),
        ("End Login Failed", END, "Customer"),
        
        # Product selection loop
        ("Select Product", USER_TASK, "Customer"),
        ("Add to Cart", USER_TASK, "Customer"),
        ("Save Product", SERVICE_TASK, "E-Shop System"),
        ("All Selected?", EXCLUSIVE_GW, "Customer"),
        
        # Parallel split
        ("Split", PARALLEL_GW, "Customer"),
        
        # System branch
        ("Prepare Order", SERVICE_TASK, "E-Shop System"),
        
        # Payment path
        ("Enter Payment Data", USER_TASK, "Customer"),
        ("Bank Confirmation", MESSAGE_CATCH, "Customer"),
        
        # Shipping path
        ("Enter Shipping Address", USER_TASK, "Customer"),
        ("Different Billing?", EXCLUSIVE_GW, "Customer"),
        ("Enter Billing Address", USER_TASK, "Customer"),
        ("Shipping Merge", EXCLUSIVE_GW, "Customer"),
        
        # Parallel join and end
        ("Join", PARALLEL_GW, "Customer"),
        ("Finish Order", SERVICE_TASK, "E-Shop System"),
        ("End", END, "Customer"),
    ],
    
    "flows": [
        # Login flow
        ("Start", "Login", ""),
        ("Login", "Check Credentials", ""),
        ("Check Credentials", "Login Successful?", ""),
        ("Login Successful?", "Select Product", "Yes"),
        ("Login Successful?", "End Login Failed", "No"),
        
        # Product selection loop
        ("Select Product", "Add to Cart", ""),
        ("Add to Cart", "Save Product", ""),
        ("Save Product", "All Selected?", ""),
        ("All Selected?", "Select Product", "No"),
        ("All Selected?", "Split", "Yes"),
        
        # Parallel paths (3 branches)
        ("Split", "Prepare Order", ""),
        ("Split", "Enter Payment Data", ""),
        ("Split", "Enter Shipping Address", ""),
        
        # System branch
        ("Prepare Order", "Join", ""),
        
        # Payment path
        ("Enter Payment Data", "Bank Confirmation", ""),
        ("Bank Confirmation", "Join", ""),
        
        # Shipping path
        ("Enter Shipping Address", "Different Billing?", ""),
        ("Different Billing?", "Enter Billing Address", "Yes"),
        ("Different Billing?", "Shipping Merge", "No"),
        ("Enter Billing Address", "Shipping Merge", ""),
        ("Shipping Merge", "Join", ""),
        
        # End
        ("Join", "Finish Order", ""),
        ("Finish Order", "End", ""),
    ],
    
    "layout": {
        # Start and Login
        "Start": 0,
        "Login": 1,
        "Check Credentials": 2,
        "Login Successful?": 3,
        "End Login Failed": 4,
        
        # Product selection loop
        "Select Product": 5,
        "Add to Cart": 6,
        "Save Product": 7,
        "All Selected?": 8,
        
        # Parallel split
        "Split": 9,
        
        # Three parallel branches (auto-stacked in Customer lane)
        "Prepare Order": 10,
        "Enter Payment Data": 10,
        "Enter Shipping Address": 10,
        
        # Continue paths (auto-stacked)
        "Bank Confirmation": 11,
        "Different Billing?": 11,
        
        # Shipping conditional path
        "Enter Billing Address": 12,
        "Shipping Merge": 13,
        
        # Join and end
        "Join": 14,
        "Finish Order": 15,
        "End": 16,
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
