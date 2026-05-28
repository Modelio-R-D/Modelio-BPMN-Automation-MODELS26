#
# LuxuryAirplane.py
#
# Description: Luxury airplane manufacturing with customizable interior
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LuxuryAirplane",
    
    "lanes": [
        "Customer",
        "Manufacturer", 
        "Russian Team",
        "Irish Team",
        "Interior Team"
    ],
    
    "elements": [
        # Customer lane
        ("Start", START, "Customer"),
        ("Select Options", USER_TASK, "Customer"),
        ("Review Protocol", USER_TASK, "Customer"),
        ("Confirm Delivery", USER_TASK, "Customer"),
        ("End", END, "Customer"),
        
        # Manufacturer lane
        ("Receive Order", RECEIVE_TASK, "Manufacturer"),
        ("Fork", PARALLEL_GW, "Manufacturer"),
        ("Bar Type?", EXCLUSIVE_GW, "Manufacturer"),
        ("Bar Done", EXCLUSIVE_GW, "Manufacturer"),
        ("Join", PARALLEL_GW, "Manufacturer"),
        ("Assemble Interior", SERVICE_TASK, "Manufacturer"),
        ("Test Flight", SERVICE_TASK, "Manufacturer"),
        ("Create Protocol", SERVICE_TASK, "Manufacturer"),
        ("Send Protocol", SEND_TASK, "Manufacturer"),
        ("Deliver Plane", SEND_TASK, "Manufacturer"),
        
        # Russian Team lane
        ("Build Vodka Bar", SERVICE_TASK, "Russian Team"),
        
        # Irish Team lane
        ("Build Whiskey Bar", SERVICE_TASK, "Irish Team"),
        
        # Interior Team lane - bar options + other components
        ("Build Champagne Bar", SERVICE_TASK, "Interior Team"),
        ("Build Seats", SERVICE_TASK, "Interior Team"),
        ("Apply Color", SERVICE_TASK, "Interior Team"),
        ("Install Water System", SERVICE_TASK, "Interior Team"),
    ],
    
    "flows": [
        # Main flow
        ("Start", "Select Options", ""),
        ("Select Options", "Receive Order", ""),
        ("Receive Order", "Fork", ""),
        
        # Parallel split - all branches from Fork
        ("Fork", "Bar Type?", ""),
        ("Fork", "Build Seats", ""),
        ("Fork", "Apply Color", ""),
        ("Fork", "Install Water System", ""),
        
        # Exclusive gateway - bar type selection (5 options shown)
        ("Bar Type?", "Build Vodka Bar", "Vodka"),
        ("Bar Type?", "Build Whiskey Bar", "Whiskey"),
        ("Bar Type?", "Build Champagne Bar", "Champagne"),
        
        # Bar paths converge at XOR join
        ("Build Vodka Bar", "Bar Done", ""),
        ("Build Whiskey Bar", "Bar Done", ""),
        ("Build Champagne Bar", "Bar Done", ""),
        
        # All paths converge at parallel join
        ("Bar Done", "Join", ""),
        ("Build Seats", "Join", ""),
        ("Apply Color", "Join", ""),
        ("Install Water System", "Join", ""),
        
        # Assembly and testing
        ("Join", "Assemble Interior", ""),
        ("Assemble Interior", "Test Flight", ""),
        ("Test Flight", "Create Protocol", ""),
        ("Create Protocol", "Send Protocol", ""),
        
        # Parallel: protocol review + plane delivery
        ("Send Protocol", "Review Protocol", ""),
        ("Send Protocol", "Deliver Plane", ""),
        
        # Customer confirmation
        ("Deliver Plane", "Confirm Delivery", ""),
        ("Review Protocol", "Confirm Delivery", ""),
        ("Confirm Delivery", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Select Options": 1,
        "Receive Order": 2,
        "Fork": 3,
        "Bar Type?": 4,
        "Build Seats": 4,
        "Apply Color": 4,
        "Install Water System": 4,
        "Build Vodka Bar": 5,
        "Build Whiskey Bar": 5,
        "Build Champagne Bar": 5,
        "Bar Done": 6,
        "Join": 7,
        "Assemble Interior": 8,
        "Test Flight": 9,
        "Create Protocol": 10,
        "Send Protocol": 11,
        "Review Protocol": 12,
        "Deliver Plane": 12,
        "Confirm Delivery": 13,
        "End": 14,
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
