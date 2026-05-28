#
# StorageManagement.py
#
# Description: Storage management process for handling orders, stock checking,
#              reordering with penalty handling, and parallel shipping.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "StorageManagement",
    
    "lanes": ["Order Management", "Warehouse", "Shipping"],
    
    "elements": [
        # Order Management lane
        ("Start", START, "Order Management"),
        ("Read Order", SERVICE_TASK, "Order Management"),
        ("Product in Stock?", EXCLUSIVE_GW, "Order Management"),
        ("Reorder from Wholesaler", SEND_TASK, "Order Management"),
        ("Wait for Product", RECEIVE_TASK, "Order Management"),
        ("Penalty Needed?", EXCLUSIVE_GW, "Order Management"),
        ("Demand Penalty", SERVICE_TASK, "Order Management"),
        ("Register in Stock", SERVICE_TASK, "Order Management"),
        ("Order Ready?", EXCLUSIVE_GW, "Order Management"),
        ("Select Next Product", SERVICE_TASK, "Order Management"),
        ("Parallel Fork", PARALLEL_GW, "Order Management"),
        ("Parallel Join", PARALLEL_GW, "Order Management"),
        
        # Warehouse lane
        ("Withdraw from Warehouse", MANUAL_TASK, "Warehouse"),
        ("Pack Products", MANUAL_TASK, "Warehouse"),
        
        # Shipping lane
        ("Request Courier", SERVICE_TASK, "Shipping"),
        ("Ship", SEND_TASK, "Shipping"),
        ("End", END, "Shipping"),
    ],
    
    "flows": [
        # Main process flow
        ("Start", "Read Order", ""),
        ("Read Order", "Product in Stock?", ""),
        
        # Stock availability decision
        ("Product in Stock?", "Withdraw from Warehouse", "In Stock"),
        ("Product in Stock?", "Reorder from Wholesaler", "Not in Stock"),
        
        # In stock path - direct to order ready check
        ("Withdraw from Warehouse", "Order Ready?", ""),
        
        # Not in stock path - reorder and wait
        ("Reorder from Wholesaler", "Wait for Product", ""),
        ("Wait for Product", "Penalty Needed?", ""),
        ("Penalty Needed?", "Demand Penalty", ">10 days"),
        ("Penalty Needed?", "Register in Stock", "<=10 days"),
        ("Demand Penalty", "Register in Stock", ""),
        ("Register in Stock", "Order Ready?", ""),
        
        # Order completion decision
        ("Order Ready?", "Select Next Product", "Not Ready"),
        ("Order Ready?", "Parallel Fork", "Ready"),
        
        # Loop back for next product
        ("Select Next Product", "Product in Stock?", ""),
        
        # Parallel shipping activities
        ("Parallel Fork", "Request Courier", ""),
        ("Parallel Fork", "Pack Products", ""),
        ("Request Courier", "Parallel Join", ""),
        ("Pack Products", "Parallel Join", ""),
        ("Parallel Join", "Ship", ""),
        ("Ship", "End", ""),
    ],
    
    "layout": {
        # Order Management lane
        "Start": 0,
        "Read Order": 1,
        "Product in Stock?": 2,
        "Reorder from Wholesaler": 3,
        "Wait for Product": 4,
        "Penalty Needed?": 5,
        "Demand Penalty": 6,
        "Register in Stock": 7,
        "Order Ready?": 8,
        "Select Next Product": 9,
        "Parallel Fork": 10,
        "Parallel Join": 12,
        
        # Warehouse lane
        "Withdraw from Warehouse": 3,
        "Pack Products": 11,
        
        # Shipping lane
        "Request Courier": 11,
        "Ship": 13,
        "End": 14,
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
