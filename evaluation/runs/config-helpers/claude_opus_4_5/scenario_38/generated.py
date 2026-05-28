#
# BuildingAHouse.py
#
# Description: Tree house building process - from requirements to party
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BuildingAHouse",
    
    "lanes": ["You", "Architect", "Friends"],
    
    "elements": [
        # Start
        ("Start",                    START,           "You"),
        
        # Requirements and Design phase
        ("Collect Requirements",     USER_TASK,       "You"),
        ("Send to Architect",        SEND_TASK,       "You"),
        ("Receive Requirements",     RECEIVE_TASK,    "Architect"),
        ("Create Draft",             USER_TASK,       "Architect"),
        ("Send Draft",               SEND_TASK,       "Architect"),
        ("Receive Draft",            RECEIVE_TASK,    "You"),
        ("Review Draft",             USER_TASK,       "You"),
        ("Refinement Needed?",       EXCLUSIVE_GW,    "You"),
        ("Add Requirements",         USER_TASK,       "You"),
        
        # Materials phase
        ("Create Materials List",    USER_TASK,       "You"),
        ("Categorize Materials",     USER_TASK,       "You"),
        ("Order from Stores",        SEND_TASK,       "You"),
        
        # Building phase (parallel)
        ("Wait and Build",           PARALLEL_GW,     "You"),
        ("Wait for Delivery",        RECEIVE_TASK,    "You"),
        ("Send Build Invites",       SEND_TASK,       "You"),
        ("Receive Build Invite",     RECEIVE_TASK,    "Friends"),
        ("Build Tree House",         MANUAL_TASK,     "Friends"),
        ("Sync After Build",         PARALLEL_GW,     "You"),
        
        # Party phase
        ("Send Party Invitations",   SEND_TASK,       "You"),
        ("Receive Party Invite",     RECEIVE_TASK,    "Friends"),
        ("Respond to Invite",        USER_TASK,       "Friends"),
        ("Create Attendee List",     USER_TASK,       "You"),
        ("Buy Party Snacks",         MANUAL_TASK,     "You"),
        
        # End
        ("End",                      END,             "You"),
    ],
    
    "data_objects": [
        ("Requirements",      "You",       1),
        ("Draft Plan",        "Architect", 4),
        ("Final Plan",        "You",       8),
        ("Materials List",    "You",       9),
        ("Attendee List",     "You",       17),
    ],
    
    "data_associations": [
        ("Collect Requirements",  "Requirements"),
        ("Requirements",          "Send to Architect"),
        ("Create Draft",          "Draft Plan"),
        ("Draft Plan",            "Send Draft"),
        ("Review Draft",          "Final Plan"),
        ("Final Plan",            "Create Materials List"),
        ("Create Materials List", "Materials List"),
        ("Materials List",        "Categorize Materials"),
        ("Create Attendee List",  "Attendee List"),
        ("Attendee List",         "Buy Party Snacks"),
    ],
    
    "flows": [
        # Start to requirements
        ("Start",                  "Collect Requirements",   ""),
        ("Collect Requirements",   "Send to Architect",      ""),
        
        # Architect work
        ("Send to Architect",      "Receive Requirements",   ""),
        ("Receive Requirements",   "Create Draft",           ""),
        ("Create Draft",           "Send Draft",             ""),
        ("Send Draft",             "Receive Draft",          ""),
        
        # Review loop
        ("Receive Draft",          "Review Draft",           ""),
        ("Review Draft",           "Refinement Needed?",     ""),
        ("Refinement Needed?",     "Add Requirements",       "Yes"),
        ("Add Requirements",       "Send to Architect",      ""),
        ("Refinement Needed?",     "Create Materials List",  "No"),
        
        # Materials
        ("Create Materials List",  "Categorize Materials",   ""),
        ("Categorize Materials",   "Order from Stores",      ""),
        ("Order from Stores",      "Wait and Build",         ""),
        
        # Parallel: Wait for delivery AND invite friends to build
        ("Wait and Build",         "Wait for Delivery",      ""),
        ("Wait and Build",         "Send Build Invites",     ""),
        ("Send Build Invites",     "Receive Build Invite",   ""),
        ("Receive Build Invite",   "Build Tree House",       ""),
        ("Wait for Delivery",      "Sync After Build",       ""),
        ("Build Tree House",       "Sync After Build",       ""),
        
        # Party phase
        ("Sync After Build",       "Send Party Invitations", ""),
        ("Send Party Invitations", "Receive Party Invite",   ""),
        ("Receive Party Invite",   "Respond to Invite",      ""),
        ("Respond to Invite",      "Create Attendee List",   ""),
        ("Create Attendee List",   "Buy Party Snacks",       ""),
        ("Buy Party Snacks",       "End",                    ""),
    ],
    
    "layout": {
        # Start
        "Start":                   0,
        
        # Requirements gathering
        "Collect Requirements":    1,
        "Send to Architect":       2,
        "Receive Requirements":    3,
        "Create Draft":            4,
        "Send Draft":              5,
        "Receive Draft":           6,
        "Review Draft":            7,
        "Refinement Needed?":      8,
        "Add Requirements":        (8, 100),
        
        # Materials
        "Create Materials List":   9,
        "Categorize Materials":    10,
        "Order from Stores":       11,
        
        # Parallel building phase
        "Wait and Build":          12,
        "Wait for Delivery":       13,
        "Send Build Invites":      13,
        "Receive Build Invite":    14,
        "Build Tree House":        15,
        "Sync After Build":        16,
        
        # Party phase
        "Send Party Invitations":  17,
        "Receive Party Invite":    18,
        "Respond to Invite":       19,
        "Create Attendee List":    20,
        "Buy Party Snacks":        21,
        
        # End
        "End":                     22,
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
