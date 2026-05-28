#
# OrderFulfillment.py
#
# Description: End-to-end order fulfillment process from order placement to delivery
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OrderFulfillment",
    
    "lanes": ["Customer", "System", "Warehouse", "Logistics"],
    
    "elements": [
        # Customer lane
        ("Order Placed",           START,        "Customer"),
        ("Receive Confirmation",   RECEIVE_TASK, "Customer"),
        ("Receive Tracking",       RECEIVE_TASK, "Customer"),
        ("Delivery Received",      USER_TASK,    "Customer"),
        ("Feedback Decision",      EXCLUSIVE_GW, "Customer"),
        ("Submit Feedback",        USER_TASK,    "Customer"),
        ("Request Return",         USER_TASK,    "Customer"),
        ("Process Complete",       END,          "Customer"),
        
        # System lane
        ("Generate Confirmation",  SERVICE_TASK, "System"),
        ("Send Confirmation",      SEND_TASK,    "System"),
        ("Generate Shipping Label",SERVICE_TASK, "System"),
        ("Send Tracking Info",     SEND_TASK,    "System"),
        
        # Warehouse lane
        ("Pick Items",             MANUAL_TASK,  "Warehouse"),
        ("Pack Order",             MANUAL_TASK,  "Warehouse"),
        ("Handover to Logistics",  MANUAL_TASK,  "Warehouse"),
        
        # Logistics lane
        ("Receive Shipment",       MANUAL_TASK,  "Logistics"),
        ("Monitor Shipment",       SERVICE_TASK, "Logistics"),
        ("Deliver to Customer",    MANUAL_TASK,  "Logistics"),
    ],
    
    "data_objects": [
        ("Order Details",      "Customer",  0),
        ("Order Confirmation", "System",    2),
        ("Shipping Label",     "System",    5),
        ("Tracking Info",      "System",    7),
    ],
    
    "data_associations": [
        ("Order Placed",           "Order Details"),
        ("Order Details",          "Generate Confirmation"),
        ("Generate Confirmation",  "Order Confirmation"),
        ("Order Confirmation",     "Send Confirmation"),
        ("Generate Shipping Label","Shipping Label"),
        ("Shipping Label",         "Handover to Logistics"),
        ("Send Tracking Info",     "Tracking Info"),
        ("Tracking Info",          "Receive Tracking"),
    ],
    
    "flows": [
        # Order placement and confirmation
        ("Order Placed",           "Generate Confirmation",   ""),
        ("Generate Confirmation",  "Send Confirmation",       ""),
        ("Send Confirmation",      "Receive Confirmation",    ""),
        
        # Warehouse processing
        ("Receive Confirmation",   "Pick Items",              ""),
        ("Pick Items",             "Pack Order",              ""),
        ("Pack Order",             "Generate Shipping Label", ""),
        ("Generate Shipping Label","Handover to Logistics",   ""),
        
        # Logistics and tracking
        ("Handover to Logistics",  "Receive Shipment",        ""),
        ("Receive Shipment",       "Send Tracking Info",      ""),
        ("Send Tracking Info",     "Receive Tracking",        ""),
        ("Receive Tracking",       "Monitor Shipment",        ""),
        ("Monitor Shipment",       "Deliver to Customer",     ""),
        ("Deliver to Customer",    "Delivery Received",       ""),
        
        # Post-delivery
        ("Delivery Received",      "Feedback Decision",       ""),
        ("Feedback Decision",      "Submit Feedback",         "Feedback"),
        ("Feedback Decision",      "Request Return",          "Return"),
        ("Feedback Decision",      "Process Complete",        "No Action"),
        ("Submit Feedback",        "Process Complete",        ""),
        ("Request Return",         "Process Complete",        ""),
    ],
    
    "layout": {
        # Customer lane
        "Order Placed":            0,
        "Receive Confirmation":    3,
        "Receive Tracking":        8,
        "Delivery Received":       11,
        "Feedback Decision":       12,
        "Submit Feedback":         13,
        "Request Return":          13,
        "Process Complete":        14,
        
        # System lane
        "Generate Confirmation":   1,
        "Send Confirmation":       2,
        "Generate Shipping Label": 5,
        "Send Tracking Info":      7,
        
        # Warehouse lane
        "Pick Items":              4,
        "Pack Order":              5,
        "Handover to Logistics":   6,
        
        # Logistics lane
        "Receive Shipment":        7,
        "Monitor Shipment":        9,
        "Deliver to Customer":     10,
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
