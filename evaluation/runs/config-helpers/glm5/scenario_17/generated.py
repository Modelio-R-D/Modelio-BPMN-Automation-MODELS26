#
# OrderFulfillment.py
#
# Description: E-commerce order fulfillment process with payment, inventory, 
#              shipping, and returns handling
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderFulfillment",
    
    "lanes": ["Customer", "Order System", "Warehouse", "Shipping", "Returns"],
    
    "elements": [
        # Customer Lane
        ("Order Placed", START, "Customer"),
        
        # Order System Lane
        ("Record Order Details", SERVICE_TASK, "Order System"),
        ("Process Payment", SERVICE_TASK, "Order System"),
        ("Payment OK?", EXCLUSIVE_GW, "Order System"),
        ("Notify Payment Failed", SERVICE_TASK, "Order System"),
        ("Payment Failed End", TERMINATE_END, "Order System"),
        ("Inform Customer of Delay", SERVICE_TASK, "Order System"),
        ("Send Shipping Confirmation", SERVICE_TASK, "Order System"),
        ("Wait for Delivery", MESSAGE_CATCH, "Order System"),
        ("Send Feedback Email", SERVICE_TASK, "Order System"),
        ("Issues Reported?", EXCLUSIVE_GW, "Order System"),
        ("Process Complete", END, "Order System"),
        
        # Warehouse Lane
        ("Check Stock Availability", SERVICE_TASK, "Warehouse"),
        ("In Stock?", EXCLUSIVE_GW, "Warehouse"),
        ("Pick Items", USER_TASK, "Warehouse"),
        ("Quality Control", USER_TASK, "Warehouse"),
        ("Packaging Split", PARALLEL_GW, "Warehouse"),
        ("Package Items", USER_TASK, "Warehouse"),
        ("Initiate Back-Order", SERVICE_TASK, "Warehouse"),
        ("Wait for Back-Order", TIMER_CATCH, "Warehouse"),
        ("Update Inventory", SERVICE_TASK, "Warehouse"),
        
        # Shipping Lane
        ("Prepare Shipping Documents", SERVICE_TASK, "Shipping"),
        ("International Order?", EXCLUSIVE_GW, "Shipping"),
        ("Prepare Customs Docs", SERVICE_TASK, "Shipping"),
        ("Documents Ready", PARALLEL_GW, "Shipping"),
        ("Dispatch Order", SERVICE_TASK, "Shipping"),
        
        # Returns Lane
        ("Initiate Returns", SERVICE_TASK, "Returns"),
        ("Send Return Label", SERVICE_TASK, "Returns"),
        ("Receive Returned Items", SERVICE_TASK, "Returns"),
        ("Inspect Items", USER_TASK, "Returns"),
        ("Refund or Replace?", EXCLUSIVE_GW, "Returns"),
        ("Process Refund", SERVICE_TASK, "Returns"),
        ("Process Replacement", SERVICE_TASK, "Returns"),
        ("Returns Complete", END, "Returns"),
    ],
    
    "flows": [
        # Order intake
        ("Order Placed", "Record Order Details", ""),
        ("Record Order Details", "Process Payment", ""),
        ("Process Payment", "Payment OK?", ""),
        
        # Payment failed path
        ("Payment OK?", "Notify Payment Failed", "No"),
        ("Notify Payment Failed", "Payment Failed End", ""),
        
        # Payment success path
        ("Payment OK?", "Check Stock Availability", "Yes"),
        
        # Stock check
        ("Check Stock Availability", "In Stock?", ""),
        
        # In stock path (happy path)
        ("In Stock?", "Pick Items", "Yes"),
        
        # Back-order path (exception)
        ("In Stock?", "Initiate Back-Order", "No"),
        ("Initiate Back-Order", "Inform Customer of Delay", ""),
        ("Inform Customer of Delay", "Wait for Back-Order", ""),
        ("Wait for Back-Order", "Pick Items", ""),
        
        # Warehouse operations
        ("Pick Items", "Quality Control", ""),
        ("Quality Control", "Packaging Split", ""),
        
        # Parallel packaging split
        ("Packaging Split", "Package Items", ""),
        ("Packaging Split", "Prepare Shipping Documents", ""),
        
        # Packaging path to join
        ("Package Items", "Documents Ready", ""),
        
        # Shipping documents path
        ("Prepare Shipping Documents", "International Order?", ""),
        ("International Order?", "Prepare Customs Docs", "Yes"),
        ("International Order?", "Documents Ready", "No"),
        ("Prepare Customs Docs", "Documents Ready", ""),
        
        # Dispatch and post-dispatch
        ("Documents Ready", "Dispatch Order", ""),
        ("Dispatch Order", "Send Shipping Confirmation", ""),
        ("Send Shipping Confirmation", "Update Inventory", ""),
        ("Update Inventory", "Wait for Delivery", ""),
        ("Wait for Delivery", "Send Feedback Email", ""),
        ("Send Feedback Email", "Issues Reported?", ""),
        
        # No issues reported
        ("Issues Reported?", "Process Complete", "No"),
        
        # Returns process
        ("Issues Reported?", "Initiate Returns", "Yes"),
        ("Initiate Returns", "Send Return Label", ""),
        ("Send Return Label", "Receive Returned Items", ""),
        ("Receive Returned Items", "Inspect Items", ""),
        ("Inspect Items", "Refund or Replace?", ""),
        ("Refund or Replace?", "Process Refund", "Refund"),
        ("Refund or Replace?", "Process Replacement", "Replace"),
        ("Process Refund", "Returns Complete", ""),
        ("Process Replacement", "Returns Complete", ""),
    ],
    
    "layout": {
        # Start
        "Order Placed": 0,
        
        # Order processing
        "Record Order Details": 1,
        "Process Payment": 2,
        "Payment OK?": 3,
        
        # Payment branches (different lanes)
        "Notify Payment Failed": 4,
        "Payment Failed End": 5,
        "Check Stock Availability": 4,
        
        # Stock check
        "In Stock?": 5,
        
        # Stock branches - manual offset for clear separation
        "Pick Items": (6, 0),
        "Initiate Back-Order": (6, 100),
        
        # Back-order continuation
        "Inform Customer of Delay": 7,
        "Wait for Back-Order": (8, 100),
        
        # Main warehouse flow
        "Quality Control": 7,
        "Packaging Split": (8, 0),
        "Package Items": 9,
        
        # Parallel shipping path
        "Prepare Shipping Documents": 9,
        "International Order?": 10,
        "Prepare Customs Docs": 11,
        "Documents Ready": 12,
        "Dispatch Order": 13,
        
        # Post-dispatch
        "Send Shipping Confirmation": 14,
        "Update Inventory": 15,
        "Wait for Delivery": 16,
        "Send Feedback Email": 17,
        "Issues Reported?": 18,
        
        # Issues branches (different lanes)
        "Process Complete": 19,
        "Initiate Returns": 19,
        
        # Returns flow
        "Send Return Label": 20,
        "Receive Returned Items": 21,
        "Inspect Items": 22,
        "Refund or Replace?": 23,
        "Process Refund": (24, 0),
        "Process Replacement": (24, 100),
        "Returns Complete": 25,
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
