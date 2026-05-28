#
# InventoryReorderProcess.py
#
# Description: Inventory monitoring and reorder process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InventoryReorderProcess",
    
    "lanes": ["Inventory System", "Procurement Team", "Warehouse Staff"],
    
    "elements": [
        # Inventory System Lane
        ("Monitor Stock", TIMER_START, "Inventory System"),
        ("Check Threshold", EXCLUSIVE_GW, "Inventory System"),
        ("Update Expected Delivery", SERVICE_TASK, "Inventory System"),
        ("Record Receipt", SERVICE_TASK, "Inventory System"),
        ("Update Inventory Levels", SERVICE_TASK, "Inventory System"),
        ("Process Complete", END, "Inventory System"),
        
        # Procurement Team Lane
        ("Review Reorder Alert", USER_TASK, "Procurement Team"),
        ("Select Supplier", USER_TASK, "Procurement Team"),
        ("Place Order", USER_TASK, "Procurement Team"),
        
        # Warehouse Staff Lane
        ("Receive Stock", USER_TASK, "Warehouse Staff"),
        ("Inspect Quality", USER_TASK, "Warehouse Staff"),
        ("Store Items", USER_TASK, "Warehouse Staff"),
    ],
    
    "flows": [
        # Monitoring and threshold check
        ("Monitor Stock", "Check Threshold", ""),
        ("Check Threshold", "Review Reorder Alert", "Reorder Needed"),
        ("Check Threshold", "Monitor Stock", "Stock OK"),
        
        # Procurement flow
        ("Review Reorder Alert", "Select Supplier", ""),
        ("Select Supplier", "Place Order", ""),
        ("Place Order", "Update Expected Delivery", ""),
        
        # System update after order
        ("Update Expected Delivery", "Receive Stock", ""),
        
        # Warehouse receiving flow
        ("Receive Stock", "Inspect Quality", ""),
        ("Inspect Quality", "Record Receipt", ""),
        ("Record Receipt", "Store Items", ""),
        ("Store Items", "Update Inventory Levels", ""),
        ("Update Inventory Levels", "Process Complete", ""),
    ],
    
    "layout": {
        # Column 0-1: Start and threshold check
        "Monitor Stock": 0,
        "Check Threshold": 1,
        
        # Column 2: Procurement starts
        "Review Reorder Alert": 2,
        
        # Column 3: Supplier selection
        "Select Supplier": 3,
        
        # Column 4: Order placement
        "Place Order": 4,
        
        # Column 5: System update
        "Update Expected Delivery": 5,
        
        # Column 6: Receiving
        "Receive Stock": 6,
        
        # Column 7: Inspection
        "Inspect Quality": 7,
        
        # Column 8: Recording
        "Record Receipt": 8,
        
        # Column 9: Storage
        "Store Items": 9,
        
        # Column 10: Final update
        "Update Inventory Levels": 10,
        
        # Column 11: End
        "Process Complete": 11,
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
