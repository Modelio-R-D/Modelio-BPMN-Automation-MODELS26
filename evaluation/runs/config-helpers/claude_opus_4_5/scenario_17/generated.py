#
# OrderFulfillment.py
#
# Description: E-commerce order fulfillment process with payment, inventory,
#              shipping, and returns handling
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderFulfillment",
    
    "lanes": [
        "Order Management",
        "Payment",
        "Inventory",
        "Warehouse",
        "Quality Control",
        "Packaging",
        "Shipping",
        "Customer Service",
        "Returns"
    ],
    
    "elements": [
        # Order Management
        ("Order Placed",              START,        "Order Management"),
        ("Record Order Details",      SERVICE_TASK, "Order Management"),
        
        # Payment
        ("Process Payment",           SERVICE_TASK, "Payment"),
        ("Payment OK?",               EXCLUSIVE_GW, "Payment"),
        ("Notify Payment Failed",     SEND_TASK,    "Payment"),
        ("End Payment Failed",        END,          "Payment"),
        
        # Inventory
        ("Check Stock",               SERVICE_TASK, "Inventory"),
        ("In Stock?",                 EXCLUSIVE_GW, "Inventory"),
        ("Initiate Back-Order",       SERVICE_TASK, "Inventory"),
        ("Notify Delay",              SEND_TASK,    "Inventory"),
        ("Receive Back-Order",        RECEIVE_TASK, "Inventory"),
        ("Update Inventory",          SERVICE_TASK, "Inventory"),
        
        # Warehouse
        ("Pick Items",                MANUAL_TASK,  "Warehouse"),
        
        # Quality Control
        ("QC Check",                  USER_TASK,    "Quality Control"),
        
        # Packaging
        ("Gift Wrap?",                EXCLUSIVE_GW, "Packaging"),
        ("Standard Packaging",        MANUAL_TASK,  "Packaging"),
        ("Gift Wrap Packaging",       MANUAL_TASK,  "Packaging"),
        ("Packaging Complete",        EXCLUSIVE_GW, "Packaging"),
        
        # Shipping
        ("Prepare Shipping Docs",     USER_TASK,    "Shipping"),
        ("International?",            EXCLUSIVE_GW, "Shipping"),
        ("Prepare Customs Docs",      USER_TASK,    "Shipping"),
        ("Docs Ready",                EXCLUSIVE_GW, "Shipping"),
        ("Sync Pack and Ship",        PARALLEL_GW,  "Shipping"),
        ("Dispatch Order",            MANUAL_TASK,  "Shipping"),
        ("Send Shipping Confirmation", SEND_TASK,   "Shipping"),
        
        # Customer Service
        ("Confirm Delivery",          RECEIVE_TASK, "Customer Service"),
        ("Issues Reported?",          EXCLUSIVE_GW, "Customer Service"),
        ("Send Feedback Request",     SEND_TASK,    "Customer Service"),
        ("End Success",               END,          "Customer Service"),
        
        # Returns
        ("Send Return Label",         SEND_TASK,    "Returns"),
        ("Receive Returned Items",    RECEIVE_TASK, "Returns"),
        ("Inspect Returns",           USER_TASK,    "Returns"),
        ("Process Refund or Replace", SERVICE_TASK, "Returns"),
        ("End Returns",               END,          "Returns"),
    ],
    
    "flows": [
        # Order start
        ("Order Placed",              "Record Order Details",      ""),
        ("Record Order Details",      "Process Payment",           ""),
        
        # Payment flow
        ("Process Payment",           "Payment OK?",               ""),
        ("Payment OK?",               "Notify Payment Failed",     "No"),
        ("Notify Payment Failed",     "End Payment Failed",        ""),
        ("Payment OK?",               "Check Stock",               "Yes"),
        
        # Inventory flow
        ("Check Stock",               "In Stock?",                 ""),
        ("In Stock?",                 "Initiate Back-Order",       "No"),
        ("Initiate Back-Order",       "Notify Delay",              ""),
        ("Notify Delay",              "Receive Back-Order",        ""),
        ("Receive Back-Order",        "Pick Items",                ""),
        ("In Stock?",                 "Pick Items",                "Yes"),
        
        # Warehouse and QC
        ("Pick Items",                "QC Check",                  ""),
        
        # Parallel split - packaging and shipping docs
        ("QC Check",                  "Gift Wrap?",                ""),
        ("QC Check",                  "Prepare Shipping Docs",     ""),
        
        # Packaging branch
        ("Gift Wrap?",                "Gift Wrap Packaging",       "Yes"),
        ("Gift Wrap?",                "Standard Packaging",        "No"),
        ("Gift Wrap Packaging",       "Packaging Complete",        ""),
        ("Standard Packaging",        "Packaging Complete",        ""),
        
        # Shipping docs branch
        ("Prepare Shipping Docs",     "International?",            ""),
        ("International?",            "Prepare Customs Docs",      "Yes"),
        ("International?",            "Docs Ready",                "No"),
        ("Prepare Customs Docs",      "Docs Ready",                ""),
        
        # Sync and dispatch
        ("Packaging Complete",        "Sync Pack and Ship",        ""),
        ("Docs Ready",                "Sync Pack and Ship",        ""),
        ("Sync Pack and Ship",        "Dispatch Order",            ""),
        ("Dispatch Order",            "Send Shipping Confirmation", ""),
        ("Dispatch Order",            "Update Inventory",          ""),
        
        # Delivery and feedback
        ("Send Shipping Confirmation", "Confirm Delivery",         ""),
        ("Confirm Delivery",          "Issues Reported?",          ""),
        ("Issues Reported?",          "Send Feedback Request",     "No"),
        ("Send Feedback Request",     "End Success",               ""),
        
        # Returns flow
        ("Issues Reported?",          "Send Return Label",         "Yes"),
        ("Send Return Label",         "Receive Returned Items",    ""),
        ("Receive Returned Items",    "Inspect Returns",           ""),
        ("Inspect Returns",           "Process Refund or Replace", ""),
        ("Process Refund or Replace", "End Returns",               ""),
    ],
    
    "data_objects": [
        ("Order Details",      "Order Management", 1),
        ("Payment Record",     "Payment",          2),
        ("Stock Report",       "Inventory",        4),
        ("Back-Order Request", "Inventory",        5),
        ("Picked Items List",  "Warehouse",        8),
        ("QC Report",          "Quality Control",  9),
        ("Shipping Label",     "Shipping",         10),
        ("Customs Forms",      "Shipping",         12),
        ("Return Label",       "Returns",          17),
        ("Inspection Report",  "Returns",          19),
    ],
    
    "data_associations": [
        ("Record Order Details",      "Order Details"),
        ("Order Details",             "Process Payment"),
        ("Process Payment",           "Payment Record"),
        ("Check Stock",               "Stock Report"),
        ("Initiate Back-Order",       "Back-Order Request"),
        ("Pick Items",                "Picked Items List"),
        ("Picked Items List",         "QC Check"),
        ("QC Check",                  "QC Report"),
        ("Prepare Shipping Docs",     "Shipping Label"),
        ("Prepare Customs Docs",      "Customs Forms"),
        ("Send Return Label",         "Return Label"),
        ("Inspect Returns",           "Inspection Report"),
        ("Inspection Report",         "Process Refund or Replace"),
    ],
    
    "layout": {
        # Order start
        "Order Placed":               0,
        "Record Order Details":       1,
        
        # Payment
        "Process Payment":            2,
        "Payment OK?":                3,
        "Notify Payment Failed":      4,
        "End Payment Failed":         5,
        
        # Inventory
        "Check Stock":                4,
        "In Stock?":                  5,
        "Initiate Back-Order":        6,
        "Notify Delay":               7,
        "Receive Back-Order":         8,
        "Update Inventory":           15,
        
        # Warehouse
        "Pick Items":                 9,
        
        # QC
        "QC Check":                   10,
        
        # Packaging (stacked)
        "Gift Wrap?":                 11,
        "Standard Packaging":         12,
        "Gift Wrap Packaging":        12,
        "Packaging Complete":         13,
        
        # Shipping docs (stacked)
        "Prepare Shipping Docs":      11,
        "International?":             12,
        "Prepare Customs Docs":       13,
        "Docs Ready":                 14,
        
        # Sync and dispatch
        "Sync Pack and Ship":         14,
        "Dispatch Order":             15,
        "Send Shipping Confirmation": 16,
        
        # Customer service
        "Confirm Delivery":           17,
        "Issues Reported?":           18,
        "Send Feedback Request":      19,
        "End Success":                20,
        
        # Returns
        "Send Return Label":          19,
        "Receive Returned Items":     20,
        "Inspect Returns":            21,
        "Process Refund or Replace":  22,
        "End Returns":                23,
    },
    
    "SPACING": 130,
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
