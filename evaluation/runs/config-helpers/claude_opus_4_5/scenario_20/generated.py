#
# EvanstonianRoomService.py
#
# Description: Room service process at The Evanstonian hotel
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "EvanstonianRoomService",
    
    "lanes": [
        "Room Service Manager",
        "Sommelier",
        "Kitchen",
        "Waiter"
    ],
    
    "elements": [
        # Room Service Manager
        ("Guest Calls",              START,        "Room Service Manager"),
        ("Take Down Order",          USER_TASK,    "Room Service Manager"),
        ("Distribute Tasks",         PARALLEL_GW,  "Room Service Manager"),
        
        # Kitchen
        ("Prepare Food",             MANUAL_TASK,  "Kitchen"),
        
        # Sommelier
        ("Alcohol Ordered?",         EXCLUSIVE_GW, "Sommelier"),
        ("Fetch Wine and Prepare Beverages", MANUAL_TASK, "Sommelier"),
        ("Skip Sommelier",           EXCLUSIVE_GW, "Sommelier"),
        
        # Waiter
        ("Ready Cart",               MANUAL_TASK,  "Waiter"),
        ("Prepare Non-Alcoholic Drinks", MANUAL_TASK, "Waiter"),
        ("All Ready",                PARALLEL_GW,  "Waiter"),
        ("Deliver to Room",          MANUAL_TASK,  "Waiter"),
        ("Return to Station",        MANUAL_TASK,  "Waiter"),
        ("Another Order Waiting?",   EXCLUSIVE_GW, "Waiter"),
        ("Debit Guest Account",      USER_TASK,    "Waiter"),
        ("End",                      END,          "Waiter"),
    ],
    
    "flows": [
        # Manager flow
        ("Guest Calls",              "Take Down Order",       ""),
        ("Take Down Order",          "Distribute Tasks",      ""),
        
        # Parallel split to kitchen, sommelier, and waiter
        ("Distribute Tasks",         "Prepare Food",          ""),
        ("Distribute Tasks",         "Alcohol Ordered?",      ""),
        ("Distribute Tasks",         "Ready Cart",            ""),
        
        # Sommelier path (80% have alcohol)
        ("Alcohol Ordered?",         "Fetch Wine and Prepare Beverages", "Yes (80%)"),
        ("Alcohol Ordered?",         "Skip Sommelier",        "No (20%)"),
        ("Fetch Wine and Prepare Beverages", "Skip Sommelier", ""),
        
        # Waiter prep
        ("Ready Cart",               "Prepare Non-Alcoholic Drinks", ""),
        
        # Synchronize all parallel paths
        ("Prepare Food",             "All Ready",             ""),
        ("Skip Sommelier",           "All Ready",             ""),
        ("Prepare Non-Alcoholic Drinks", "All Ready",         ""),
        
        # Delivery and billing
        ("All Ready",                "Deliver to Room",       ""),
        ("Deliver to Room",          "Return to Station",     ""),
        ("Return to Station",        "Another Order Waiting?", ""),
        ("Another Order Waiting?",   "Debit Guest Account",   "No"),
        ("Another Order Waiting?",   "End",                   "Yes - Bill Later"),
        ("Debit Guest Account",      "End",                   ""),
    ],
    
    "layout": {
        # Manager lane
        "Guest Calls":               0,
        "Take Down Order":           1,
        "Distribute Tasks":          2,
        
        # Kitchen lane
        "Prepare Food":              3,
        
        # Sommelier lane
        "Alcohol Ordered?":          3,
        "Fetch Wine and Prepare Beverages": 4,
        "Skip Sommelier":            5,
        
        # Waiter lane
        "Ready Cart":                3,
        "Prepare Non-Alcoholic Drinks": 4,
        "All Ready":                 6,
        "Deliver to Room":           7,
        "Return to Station":         8,
        "Another Order Waiting?":    9,
        "Debit Guest Account":       10,
        "End":                       11,
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
