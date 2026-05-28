#
# LuxuryAirplaneProcess.py
#
# Description: Luxury airplane customization with multiple manufacturing teams,
#              assembly, test flight, and customer delivery confirmation.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LuxuryAirplaneProcess",
    
    "lanes": [
        "Customer",
        "Sales",
        "Russian Team",
        "Irish Team",
        "Scottish Team",
        "Japanese Team",
        "German Team",
        "Assembly",
        "Test Pilot"
    ],
    
    "elements": [
        # Customer lane
        ("Order Request",           START,        "Customer"),
        ("Select Bar Type",         USER_TASK,    "Customer"),
        ("Configure Seats",         USER_TASK,    "Customer"),
        ("Choose Extras",           USER_TASK,    "Customer"),
        ("Submit Configuration",    USER_TASK,    "Customer"),
        ("Receive Test Protocol",   USER_TASK,    "Customer"),
        ("Receive Airplane",        USER_TASK,    "Customer"),
        ("Confirm Delivery",        USER_TASK,    "Customer"),
        ("Order Complete",          END,          "Customer"),
        
        # Sales lane
        ("Receive Specs",           SERVICE_TASK, "Sales"),
        ("Which Bar?",              EXCLUSIVE_GW, "Sales"),
        ("Dispatch to Teams",       PARALLEL_GW,  "Sales"),
        ("Collect All Parts",       PARALLEL_GW,  "Sales"),
        ("Forward to Assembly",     SERVICE_TASK, "Sales"),
        ("Send Protocol",           SEND_TASK,    "Sales"),
        
        # Manufacturing teams
        ("Make Vodka Bar",          MANUAL_TASK,  "Russian Team"),
        ("Make Whiskey Bar",        MANUAL_TASK,  "Irish Team"),
        ("Make Scotch Bar",         MANUAL_TASK,  "Scottish Team"),
        ("Make Sake Bar",           MANUAL_TASK,  "Japanese Team"),
        ("Make Beer Bar",           MANUAL_TASK,  "German Team"),
        ("Make Seats",              MANUAL_TASK,  "German Team"),
        ("Make Toilet System",      MANUAL_TASK,  "Japanese Team"),
        ("Make Entertainment",      MANUAL_TASK,  "Japanese Team"),
        
        # Assembly lane
        ("Assemble Interior",       MANUAL_TASK,  "Assembly"),
        ("Quality Check",           USER_TASK,    "Assembly"),
        ("Prepare for Test",        SERVICE_TASK, "Assembly"),
        ("Deliver to Customer",     SEND_TASK,    "Assembly"),
        
        # Test Pilot lane
        ("Conduct Test Flight",     MANUAL_TASK,  "Test Pilot"),
        ("Create Test Protocol",    USER_TASK,    "Test Pilot"),
    ],
    
    "data_objects": [
        ("Specifications",    "Sales",      2),
        ("Test Protocol",     "Test Pilot", 10),
    ],
    
    "data_associations": [
        ("Receive Specs",        "Specifications"),
        ("Specifications",       "Which Bar?"),
        ("Create Test Protocol", "Test Protocol"),
        ("Test Protocol",        "Send Protocol"),
    ],
    
    "flows": [
        # Customer configuration flow
        ("Order Request",         "Select Bar Type",      ""),
        ("Select Bar Type",       "Configure Seats",      ""),
        ("Configure Seats",       "Choose Extras",        ""),
        ("Choose Extras",         "Submit Configuration", ""),
        ("Submit Configuration",  "Receive Specs",        ""),
        
        # Sales processing
        ("Receive Specs",         "Which Bar?",           ""),
        ("Which Bar?",            "Dispatch to Teams",    ""),
        
        # Bar selection (exclusive - only one bar type)
        ("Dispatch to Teams",     "Make Vodka Bar",       "Vodka"),
        ("Dispatch to Teams",     "Make Whiskey Bar",     "Whiskey"),
        ("Dispatch to Teams",     "Make Scotch Bar",      "Scotch"),
        ("Dispatch to Teams",     "Make Sake Bar",        "Sake"),
        ("Dispatch to Teams",     "Make Beer Bar",        "Beer"),
        
        # Parallel work on seats, toilets, entertainment
        ("Dispatch to Teams",     "Make Seats",           ""),
        ("Dispatch to Teams",     "Make Toilet System",   ""),
        ("Dispatch to Teams",     "Make Entertainment",   ""),
        
        # All parts converge
        ("Make Vodka Bar",        "Collect All Parts",    ""),
        ("Make Whiskey Bar",      "Collect All Parts",    ""),
        ("Make Scotch Bar",       "Collect All Parts",    ""),
        ("Make Sake Bar",         "Collect All Parts",    ""),
        ("Make Beer Bar",         "Collect All Parts",    ""),
        ("Make Seats",            "Collect All Parts",    ""),
        ("Make Toilet System",    "Collect All Parts",    ""),
        ("Make Entertainment",    "Collect All Parts",    ""),
        
        # Assembly phase
        ("Collect All Parts",     "Forward to Assembly",  ""),
        ("Forward to Assembly",   "Assemble Interior",    ""),
        ("Assemble Interior",     "Quality Check",        ""),
        ("Quality Check",         "Prepare for Test",     ""),
        
        # Test flight
        ("Prepare for Test",      "Conduct Test Flight",  ""),
        ("Conduct Test Flight",   "Create Test Protocol", ""),
        ("Create Test Protocol",  "Send Protocol",        ""),
        
        # Protocol distribution and delivery
        ("Send Protocol",         "Receive Test Protocol", ""),
        ("Send Protocol",         "Deliver to Customer",   ""),
        ("Deliver to Customer",   "Receive Airplane",      ""),
        
        # Customer confirmation
        ("Receive Test Protocol", "Confirm Delivery",      ""),
        ("Receive Airplane",      "Confirm Delivery",      ""),
        ("Confirm Delivery",      "Order Complete",        ""),
    ],
    
    "layout": {
        # Customer lane
        "Order Request":          0,
        "Select Bar Type":        1,
        "Configure Seats":        2,
        "Choose Extras":          3,
        "Submit Configuration":   4,
        "Receive Test Protocol":  11,
        "Receive Airplane":       12,
        "Confirm Delivery":       13,
        "Order Complete":         14,
        
        # Sales lane
        "Receive Specs":          5,
        "Which Bar?":             6,
        "Dispatch to Teams":      7,
        "Collect All Parts":      8,
        "Forward to Assembly":    9,
        "Send Protocol":          11,
        
        # Manufacturing teams - all in column 8 (auto-stacked per lane)
        "Make Vodka Bar":         8,
        "Make Whiskey Bar":       8,
        "Make Scotch Bar":        8,
        "Make Sake Bar":          8,
        "Make Beer Bar":          8,
        "Make Seats":             (8, 90),
        "Make Toilet System":     (8, 90),
        "Make Entertainment":     (8, 180),
        
        # Assembly lane
        "Assemble Interior":      9,
        "Quality Check":          10,
        "Prepare for Test":       11,
        "Deliver to Customer":    12,
        
        # Test Pilot lane
        "Conduct Test Flight":    9,
        "Create Test Protocol":   10,
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
