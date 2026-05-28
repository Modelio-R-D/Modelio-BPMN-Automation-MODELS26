#
# ContractPartsProcurement.py
#
# Description: Process for procuring parts from multiple web shops, managing inventory,
#              and building while handling reorders based on stock levels.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ContractPartsProcurement",
    
    "lanes": [
        "Procurement",
        "Inventory",
        "Building",
        "Communication"
    ],
    
    "elements": [
        # Procurement Lane - Query and Order
        ("Start",                    START,           "Procurement"),
        ("Query All Web Shops",      SERVICE_TASK,    "Procurement"),
        ("Collect Quotes",           USER_TASK,       "Procurement"),
        ("Analyze Availability",     USER_TASK,       "Procurement"),
        ("Create Order Lists",       USER_TASK,       "Procurement"),
        ("Place Orders",             SERVICE_TASK,    "Procurement"),
        
        # Inventory Lane - Receiving and Stock Management
        ("Wait for Delivery",        TIMER_CATCH,     "Inventory"),
        ("Receive Batch",            USER_TASK,       "Inventory"),
        ("Update Stock",             SERVICE_TASK,    "Inventory"),
        ("Check Stock Level",        EXCLUSIVE_GW,    "Inventory"),
        ("Stock OK",                 TASK,            "Inventory"),
        ("Below 5 - Reorder Cheap",  SERVICE_TASK,    "Inventory"),
        ("Below 3 - Reorder Fast",   SERVICE_TASK,    "Inventory"),
        ("Zero Stock",               TASK,            "Inventory"),
        ("More Deliveries?",         EXCLUSIVE_GW,    "Inventory"),
        
        # Building Lane
        ("First Parts Arrived?",     EXCLUSIVE_GW,    "Building"),
        ("Start Building",           MANUAL_TASK,     "Building"),
        ("Continue Building",        MANUAL_TASK,     "Building"),
        ("Building Complete?",       EXCLUSIVE_GW,    "Building"),
        ("Project Complete",         END,             "Building"),
        
        # Communication Lane
        ("Complain to Friends",      SEND_TASK,       "Communication"),
    ],
    
    "data_objects": [
        ("Parts List",         "Procurement", 0),
        ("Quotes",             "Procurement", 2),
        ("Order Lists",        "Procurement", 4),
        ("Stock Register",     "Inventory",   8),
        ("Complaint Email",    "Communication", 11),
    ],
    
    "data_associations": [
        # Procurement data flow
        ("Start",                "Parts List"),
        ("Parts List",           "Query All Web Shops"),
        ("Collect Quotes",       "Quotes"),
        ("Quotes",               "Analyze Availability"),
        ("Create Order Lists",   "Order Lists"),
        ("Order Lists",          "Place Orders"),
        
        # Inventory data flow
        ("Update Stock",         "Stock Register"),
        ("Stock Register",       "Check Stock Level"),
        
        # Communication data flow
        ("Complain to Friends",  "Complaint Email"),
    ],
    
    "flows": [
        # Procurement flow
        ("Start",                   "Query All Web Shops",    ""),
        ("Query All Web Shops",     "Collect Quotes",         ""),
        ("Collect Quotes",          "Analyze Availability",   ""),
        ("Analyze Availability",    "Create Order Lists",     ""),
        ("Create Order Lists",      "Place Orders",           ""),
        ("Place Orders",            "Wait for Delivery",      ""),
        
        # Inventory flow - receiving
        ("Wait for Delivery",       "Receive Batch",          ""),
        ("Receive Batch",           "Update Stock",           ""),
        ("Update Stock",            "Check Stock Level",      ""),
        
        # Stock level checks (auto-stacked branches)
        ("Check Stock Level",       "Stock OK",               ">=5"),
        ("Check Stock Level",       "Below 5 - Reorder Cheap","<5"),
        ("Check Stock Level",       "Below 3 - Reorder Fast", "<3"),
        ("Check Stock Level",       "Zero Stock",             "=0"),
        
        # After stock actions - check for more deliveries
        ("Stock OK",                "More Deliveries?",       ""),
        ("Below 5 - Reorder Cheap", "More Deliveries?",       ""),
        ("Below 3 - Reorder Fast",  "More Deliveries?",       ""),
        ("Zero Stock",              "Complain to Friends",    ""),
        ("Complain to Friends",     "More Deliveries?",       ""),
        
        # More deliveries loop
        ("More Deliveries?",        "Wait for Delivery",      "Yes"),
        ("More Deliveries?",        "First Parts Arrived?",   "No"),
        
        # Building flow
        ("First Parts Arrived?",    "Start Building",         "Yes"),
        ("First Parts Arrived?",    "Wait for Delivery",      "No"),
        ("Start Building",          "Continue Building",      ""),
        ("Continue Building",       "Building Complete?",     ""),
        ("Building Complete?",      "Continue Building",      "No"),
        ("Building Complete?",      "Project Complete",       "Yes"),
    ],
    
    "layout": {
        # Procurement Lane (columns 0-5)
        "Start":                    0,
        "Query All Web Shops":      1,
        "Collect Quotes":           2,
        "Analyze Availability":     3,
        "Create Order Lists":       4,
        "Place Orders":             5,
        
        # Inventory Lane (columns 6-12)
        "Wait for Delivery":        6,
        "Receive Batch":            7,
        "Update Stock":             8,
        "Check Stock Level":        9,
        "Stock OK":                 10,    # Auto-stacked with others in col 10
        "Below 5 - Reorder Cheap":  10,
        "Below 3 - Reorder Fast":   10,
        "Zero Stock":               10,
        "More Deliveries?":         12,
        
        # Building Lane (columns 13-17)
        "First Parts Arrived?":     13,
        "Start Building":           14,
        "Continue Building":        15,
        "Building Complete?":       16,
        "Project Complete":         17,
        
        # Communication Lane (column 11)
        "Complain to Friends":      11,
    },
    
    # Wider spacing for readability
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
