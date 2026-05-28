#
# Contract.py
#
# Description: Contract parts ordering and building process with stock management
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Contract",
    
    "lanes": ["Purchaser", "Warehouse"],
    
    "elements": [
        # Query and order phase
        ("Start", START, "Purchaser"),
        ("Query Web Shops", SERVICE_TASK, "Purchaser"),
        ("Analyze Offers", BUSINESS_RULE_TASK, "Purchaser"),
        ("Single Shop OK?", EXCLUSIVE_GW, "Purchaser"),
        ("Order from Cheapest", SERVICE_TASK, "Purchaser"),
        ("Order from Multiple", SERVICE_TASK, "Purchaser"),
        ("Orders Merged", EXCLUSIVE_GW, "Purchaser"),
        
        # Building phase
        ("Wait for Parts", RECEIVE_TASK, "Warehouse"),
        ("Start Building", USER_TASK, "Warehouse"),
        ("Check Stock", SERVICE_TASK, "Warehouse"),
        ("Stock Level?", EXCLUSIVE_GW, "Warehouse"),
        
        # Stock actions
        ("Continue Building", USER_TASK, "Warehouse"),
        ("Reorder Cheapest", SERVICE_TASK, "Purchaser"),
        ("Reorder Fastest", SERVICE_TASK, "Purchaser"),
        ("Complain to Friends", SEND_TASK, "Purchaser"),
        
        # Completion
        ("Building Complete?", EXCLUSIVE_GW, "Warehouse"),
        ("End", END, "Warehouse"),
    ],
    
    "flows": [
        # Query and order flow
        ("Start", "Query Web Shops", ""),
        ("Query Web Shops", "Analyze Offers", ""),
        ("Analyze Offers", "Single Shop OK?", ""),
        ("Single Shop OK?", "Order from Cheapest", "Yes"),
        ("Single Shop OK?", "Order from Multiple", "No"),
        ("Order from Cheapest", "Orders Merged", ""),
        ("Order from Multiple", "Orders Merged", ""),
        ("Orders Merged", "Wait for Parts", ""),
        
        # Building flow
        ("Wait for Parts", "Start Building", ""),
        ("Start Building", "Check Stock", ""),
        ("Check Stock", "Stock Level?", ""),
        
        # Stock level decisions (priority order: most critical first)
        ("Stock Level?", "Complain to Friends", "= 0"),
        ("Stock Level?", "Reorder Fastest", "< 3"),
        ("Stock Level?", "Reorder Cheapest", "< 5"),
        ("Stock Level?", "Continue Building", ">= 5"),
        
        # Reorder loops back to waiting
        ("Reorder Cheapest", "Wait for Parts", ""),
        ("Reorder Fastest", "Wait for Parts", ""),
        ("Complain to Friends", "Wait for Parts", ""),
        
        # Building completion
        ("Continue Building", "Building Complete?", ""),
        ("Building Complete?", "End", "Yes"),
        ("Building Complete?", "Check Stock", "No"),
    ],
    
    "data_objects": [
        ("Parts List", "Purchaser", 2),
        ("Stock Status", "Warehouse", 8),
    ],
    
    "data_associations": [
        ("Query Web Shops", "Parts List"),
        ("Parts List", "Analyze Offers"),
        ("Check Stock", "Stock Status"),
    ],
    
    "layout": {
        "Start": 0,
        "Query Web Shops": 1,
        "Analyze Offers": 2,
        "Single Shop OK?": 3,
        "Order from Cheapest": 4,
        "Order from Multiple": 4,
        "Orders Merged": 5,
        "Wait for Parts": 6,
        "Start Building": 7,
        "Check Stock": 8,
        "Stock Level?": 9,
        "Continue Building": 10,
        "Reorder Cheapest": 10,
        "Reorder Fastest": 10,
        "Complain to Friends": 10,
        "Building Complete?": 11,
        "End": 12,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
