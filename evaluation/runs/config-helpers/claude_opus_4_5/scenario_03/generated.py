#
# InventoryRestockProcess.py
#
# Description: Inventory monitoring and restocking process from threshold detection to stock replenishment
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InventoryRestockProcess",
    
    "lanes": ["Warehouse", "Procurement", "Receiving"],
    
    "elements": [
        # Warehouse Lane - Monitoring
        ("Start",                    START,           "Warehouse"),
        ("Monitor Inventory Levels", SERVICE_TASK,    "Warehouse"),
        ("Threshold Reached?",       EXCLUSIVE_GW,    "Warehouse"),
        ("Continue Monitoring",      TIMER_CATCH,     "Warehouse"),
        
        # Procurement Lane - Ordering
        ("Evaluate Suppliers",       USER_TASK,       "Procurement"),
        ("Place Order",              SEND_TASK,       "Procurement"),
        ("Update Expected Delivery", SERVICE_TASK,    "Procurement"),
        
        # Receiving Lane - Stock Receipt
        ("Receive Stock",            MANUAL_TASK,     "Receiving"),
        ("Inspect Quality",          USER_TASK,       "Receiving"),
        ("Quality OK?",              EXCLUSIVE_GW,    "Receiving"),
        ("Record in System",         SERVICE_TASK,    "Receiving"),
        ("Return to Supplier",       SEND_TASK,       "Receiving"),
        ("Place on Shelves",         MANUAL_TASK,     "Receiving"),
        ("Update Inventory Levels",  SERVICE_TASK,    "Receiving"),
        ("End",                      END,             "Receiving"),
    ],
    
    "data_objects": [
        ("Inventory Data",    "Warehouse",   1),
        ("Purchase Order",    "Procurement", 4),
        ("Delivery Schedule", "Procurement", 5),
        ("Stock Record",      "Receiving",   8),
    ],
    
    "data_associations": [
        ("Monitor Inventory Levels", "Inventory Data"),
        ("Inventory Data",           "Evaluate Suppliers"),
        ("Place Order",              "Purchase Order"),
        ("Purchase Order",           "Update Expected Delivery"),
        ("Update Expected Delivery", "Delivery Schedule"),
        ("Record in System",         "Stock Record"),
        ("Stock Record",             "Update Inventory Levels"),
    ],
    
    "flows": [
        ("Start",                    "Monitor Inventory Levels", ""),
        ("Monitor Inventory Levels", "Threshold Reached?",       ""),
        ("Threshold Reached?",       "Continue Monitoring",      "No"),
        ("Continue Monitoring",      "Monitor Inventory Levels", ""),
        ("Threshold Reached?",       "Evaluate Suppliers",       "Yes"),
        ("Evaluate Suppliers",       "Place Order",              ""),
        ("Place Order",              "Update Expected Delivery", ""),
        ("Update Expected Delivery", "Receive Stock",            ""),
        ("Receive Stock",            "Inspect Quality",          ""),
        ("Inspect Quality",          "Quality OK?",              ""),
        ("Quality OK?",              "Record in System",         "Passed"),
        ("Quality OK?",              "Return to Supplier",       "Failed"),
        ("Return to Supplier",       "Receive Stock",            ""),
        ("Record in System",         "Place on Shelves",         ""),
        ("Place on Shelves",         "Update Inventory Levels",  ""),
        ("Update Inventory Levels",  "End",                      ""),
    ],
    
    "layout": {
        "Start":                    0,
        "Monitor Inventory Levels": 1,
        "Threshold Reached?":       2,
        "Continue Monitoring":      3,
        "Evaluate Suppliers":       3,
        "Place Order":              4,
        "Update Expected Delivery": 5,
        "Receive Stock":            6,
        "Inspect Quality":          7,
        "Quality OK?":              8,
        "Record in System":         9,
        "Return to Supplier":       9,
        "Place on Shelves":         10,
        "Update Inventory Levels":  11,
        "End":                      12,
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
