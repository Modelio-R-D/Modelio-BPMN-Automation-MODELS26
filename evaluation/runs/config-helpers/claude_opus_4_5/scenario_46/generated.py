#
# StorageManagement.py
#
# Description: Order fulfillment process with stock checking, reordering, and shipment
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "StorageManagement",
    
    "lanes": ["Warehouse", "Procurement", "Shipping"],
    
    "elements": [
        # Start
        ("Start",                    START,           "Warehouse"),
        
        # Initial read
        ("Read Order",               SERVICE_TASK,    "Warehouse"),
        
        # Stock check loop
        ("In Stock?",                EXCLUSIVE_GW,    "Warehouse"),
        ("Withdraw from Warehouse",  MANUAL_TASK,     "Warehouse"),
        
        # Reorder path
        ("Reorder from Wholesaler",  SEND_TASK,       "Procurement"),
        ("Wait for Delivery",        TIMER_CATCH,     "Procurement"),
        ("Delivery > 10 days?",      EXCLUSIVE_GW,    "Procurement"),
        ("Demand Penalty",           SERVICE_TASK,    "Procurement"),
        ("Merge After Penalty",      EXCLUSIVE_GW,    "Procurement"),
        ("Register in Stock",        SERVICE_TASK,    "Warehouse"),
        
        # Merge after stock/reorder
        ("Merge Product Ready",      EXCLUSIVE_GW,    "Warehouse"),
        
        # Order complete check
        ("Order Ready?",             EXCLUSIVE_GW,    "Warehouse"),
        ("Select Next Product",      SERVICE_TASK,    "Warehouse"),
        
        # Shipping
        ("Fork Shipping",            PARALLEL_GW,     "Shipping"),
        ("Request Courier",          SEND_TASK,       "Shipping"),
        ("Pack Products",            MANUAL_TASK,     "Shipping"),
        ("Join Shipping",            PARALLEL_GW,     "Shipping"),
        ("Ship Order",               MANUAL_TASK,     "Shipping"),
        
        # End
        ("End",                      END,             "Shipping"),
    ],
    
    "flows": [
        # Start to read order
        ("Start",                   "Read Order",              ""),
        ("Read Order",              "In Stock?",               ""),
        
        # Stock check
        ("In Stock?",               "Withdraw from Warehouse", "Yes"),
        ("In Stock?",               "Reorder from Wholesaler", "No"),
        
        # Withdraw path
        ("Withdraw from Warehouse", "Merge Product Ready",     ""),
        
        # Reorder path
        ("Reorder from Wholesaler", "Wait for Delivery",       ""),
        ("Wait for Delivery",       "Delivery > 10 days?",     ""),
        ("Delivery > 10 days?",     "Demand Penalty",          "Yes"),
        ("Delivery > 10 days?",     "Merge After Penalty",     "No"),
        ("Demand Penalty",          "Merge After Penalty",     ""),
        ("Merge After Penalty",     "Register in Stock",       ""),
        ("Register in Stock",       "Merge Product Ready",     ""),
        
        # Order complete check
        ("Merge Product Ready",     "Order Ready?",            ""),
        ("Order Ready?",            "Fork Shipping",           "Yes"),
        ("Order Ready?",            "Select Next Product",     "No"),
        ("Select Next Product",     "In Stock?",               ""),
        
        # Parallel shipping
        ("Fork Shipping",           "Request Courier",         ""),
        ("Fork Shipping",           "Pack Products",           ""),
        ("Request Courier",         "Join Shipping",           ""),
        ("Pack Products",           "Join Shipping",           ""),
        ("Join Shipping",           "Ship Order",              ""),
        ("Ship Order",              "End",                     ""),
    ],
    
    "layout": {
        # Column 0
        "Start":                    0,
        
        # Column 1
        "Read Order":               1,
        
        # Column 2 - Stock check
        "In Stock?":                2,
        
        # Column 3 - Stock/Reorder paths
        "Withdraw from Warehouse":  3,
        "Reorder from Wholesaler":  3,
        
        # Column 4 - Reorder continuation
        "Wait for Delivery":        4,
        
        # Column 5 - Delay check
        "Delivery > 10 days?":      5,
        
        # Column 6 - Penalty path
        "Demand Penalty":           6,
        "Merge After Penalty":      6,
        
        # Column 7 - Register
        "Register in Stock":        7,
        
        # Column 8 - Merge and check
        "Merge Product Ready":      8,
        
        # Column 9 - Order ready check
        "Order Ready?":             9,
        "Select Next Product":      9,
        
        # Column 10 - Parallel fork
        "Fork Shipping":            10,
        
        # Column 11 - Parallel tasks
        "Request Courier":          11,
        "Pack Products":            11,
        
        # Column 12 - Join
        "Join Shipping":            12,
        
        # Column 13 - Ship
        "Ship Order":               13,
        
        # Column 14 - End
        "End":                      14,
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
