#
# OrderFulfillmentProcess.py
#
# Description: Order fulfillment process from order placement to delivery
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Order Fulfillment Process",
    
    "lanes": ["Customer", "System", "Warehouse", "Logistics Provider"],
    
    "elements": [
        # Start event - triggered by customer order
        ("Order Placed", MESSAGE_START, "Customer"),
        
        # System automated tasks
        ("Generate Confirmation", SERVICE_TASK, "System"),
        ("Send Tracking Info", SEND_TASK, "System"),
        
        # Warehouse manual tasks
        ("Pick and Pack Items", USER_TASK, "Warehouse"),
        ("Hand Over to Carrier", SERVICE_TASK, "Warehouse"),
        
        # Logistics provider tasks
        ("Monitor Shipment", SERVICE_TASK, "Logistics Provider"),
        ("Deliver Package", SERVICE_TASK, "Logistics Provider"),
        
        # End event
        ("Order Complete", END, "Customer"),
    ],
    
    "flows": [
        ("Order Placed", "Generate Confirmation", ""),
        ("Generate Confirmation", "Pick and Pack Items", ""),
        ("Pick and Pack Items", "Send Tracking Info", ""),
        ("Send Tracking Info", "Hand Over to Carrier", ""),
        ("Hand Over to Carrier", "Monitor Shipment", ""),
        ("Monitor Shipment", "Deliver Package", ""),
        ("Deliver Package", "Order Complete", ""),
    ],
    
    "data_objects": [
        ("Order Confirmation", "System", 1),
        ("Tracking Number", "System", 3),
    ],
    
    "data_associations": [
        ("Generate Confirmation", "Order Confirmation"),
        ("Send Tracking Info", "Tracking Number"),
    ],
    
    "layout": {
        "Order Placed": 0,
        "Generate Confirmation": 1,
        "Pick and Pack Items": 2,
        "Send Tracking Info": 3,
        "Hand Over to Carrier": 4,
        "Monitor Shipment": 5,
        "Deliver Package": 6,
        "Order Complete": 7,
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
