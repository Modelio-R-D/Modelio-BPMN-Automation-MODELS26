#
# FarmingBot.py
#
# Description: Custom farming bot process for resource gathering with parallel
#              collection, dependency management, and social features
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "FarmingBot",
    
    "lanes": [
        "Player",
        "Bot System",
        "Event Handler",
        "Social"
    ],
    
    "elements": [
        # Player lane - Setup and interaction
        ("Start",                    START,           "Player"),
        ("Select Resources",         USER_TASK,       "Player"),
        ("Set Priorities",           USER_TASK,       "Player"),
        ("Resources Valid?",         EXCLUSIVE_GW,    "Player"),
        ("Too Many Selected",        USER_TASK,       "Player"),
        ("Update Preferences",       USER_TASK,       "Player"),
        ("View Milestone",           USER_TASK,       "Player"),
        ("Continue Farming?",        EXCLUSIVE_GW,    "Player"),
        
        # Bot System lane - Core farming logic
        ("Check Dependencies",       SERVICE_TASK,    "Bot System"),
        ("Tools Needed?",            EXCLUSIVE_GW,    "Bot System"),
        ("Queue Tool Crafting",      SERVICE_TASK,    "Bot System"),
        ("Prepare Farming",          SERVICE_TASK,    "Bot System"),
        ("Fork Resources",           PARALLEL_GW,     "Bot System"),
        ("Farm Wood",                SERVICE_TASK,    "Bot System"),
        ("Farm Stone",               SERVICE_TASK,    "Bot System"),
        ("Farm Iron",                SERVICE_TASK,    "Bot System"),
        ("Farm Gold",                SERVICE_TASK,    "Bot System"),
        ("Farm Gems",                SERVICE_TASK,    "Bot System"),
        ("Join Resources",           PARALLEL_GW,     "Bot System"),
        ("Update Inventory",         SERVICE_TASK,    "Bot System"),
        ("All Complete?",            EXCLUSIVE_GW,    "Bot System"),
        ("Farming Complete",         END,             "Bot System"),
        
        # Event Handler lane - Interrupts and notifications
        ("Event Gateway",            EVENT_BASED_GW,  "Event Handler"),
        ("Disaster Strikes",         SIGNAL_CATCH,    "Event Handler"),
        ("Milestone Reached",        SIGNAL_CATCH,    "Event Handler"),
        ("Preference Update",        MESSAGE_CATCH,   "Event Handler"),
        ("Calculate Setback",        SERVICE_TASK,    "Event Handler"),
        ("Send Notification",        SEND_TASK,       "Event Handler"),
        ("Merge Events",             EXCLUSIVE_GW,    "Event Handler"),
        
        # Social lane - Sharing features
        ("Share Results?",           EXCLUSIVE_GW,    "Social"),
        ("Select Friends",           USER_TASK,       "Social"),
        ("Choose Share Type",        INCLUSIVE_GW,    "Social"),
        ("Post Achievement",         SEND_TASK,       "Social"),
        ("Send Materials",           SEND_TASK,       "Social"),
        ("Join Share",               INCLUSIVE_GW,    "Social"),
        ("End Process",              END,             "Social"),
        ("Skip Sharing",             END,             "Social"),
    ],
    
    "flows": [
        # Player setup flow
        ("Start",                "Select Resources",    ""),
        ("Select Resources",     "Set Priorities",      ""),
        ("Set Priorities",       "Resources Valid?",    ""),
        ("Resources Valid?",     "Too Many Selected",   "More than 10"),
        ("Resources Valid?",     "Check Dependencies",  "Valid"),
        ("Too Many Selected",    "Select Resources",    ""),
        
        # Bot dependency and preparation
        ("Check Dependencies",   "Tools Needed?",       ""),
        ("Tools Needed?",        "Queue Tool Crafting", "Yes"),
        ("Tools Needed?",        "Prepare Farming",     "No"),
        ("Queue Tool Crafting",  "Prepare Farming",     ""),
        
        # Parallel farming
        ("Prepare Farming",      "Fork Resources",      ""),
        ("Fork Resources",       "Farm Wood",           ""),
        ("Fork Resources",       "Farm Stone",          ""),
        ("Fork Resources",       "Farm Iron",           ""),
        ("Fork Resources",       "Farm Gold",           ""),
        ("Fork Resources",       "Farm Gems",           ""),
        ("Farm Wood",            "Join Resources",      ""),
        ("Farm Stone",           "Join Resources",      ""),
        ("Farm Iron",            "Join Resources",      ""),
        ("Farm Gold",            "Join Resources",      ""),
        ("Farm Gems",            "Join Resources",      ""),
        ("Join Resources",       "Update Inventory",    ""),
        ("Update Inventory",     "All Complete?",       ""),
        ("All Complete?",        "Fork Resources",      "More to farm"),
        ("All Complete?",        "Share Results?",      "Done"),
        
        # Event handling
        ("Prepare Farming",      "Event Gateway",       ""),
        ("Event Gateway",        "Disaster Strikes",    ""),
        ("Event Gateway",        "Milestone Reached",   ""),
        ("Event Gateway",        "Preference Update",   ""),
        ("Disaster Strikes",     "Calculate Setback",   ""),
        ("Calculate Setback",    "Merge Events",        ""),
        ("Milestone Reached",    "Send Notification",   ""),
        ("Send Notification",    "View Milestone",      ""),
        ("View Milestone",       "Continue Farming?",   ""),
        ("Continue Farming?",    "Merge Events",        "Continue"),
        ("Continue Farming?",    "Farming Complete",    "Stop"),
        ("Preference Update",    "Update Preferences",  ""),
        ("Update Preferences",   "Merge Events",        ""),
        ("Merge Events",         "Event Gateway",       ""),
        
        # Social sharing
        ("Share Results?",       "Select Friends",      "Yes"),
        ("Share Results?",       "Skip Sharing",        "No"),
        ("Select Friends",       "Choose Share Type",   ""),
        ("Choose Share Type",    "Post Achievement",    "Brag"),
        ("Choose Share Type",    "Send Materials",      "Gift"),
        ("Post Achievement",     "Join Share",          ""),
        ("Send Materials",       "Join Share",          ""),
        ("Join Share",           "End Process",         ""),
    ],
    
    "data_objects": [
        ("Resource List",        "Player",        1),
        ("Priority Queue",       "Player",        2),
        ("Tool Requirements",    "Bot System",    4),
        ("Inventory",            "Bot System",    11),
        ("Friend List",          "Social",        14),
    ],
    
    "data_associations": [
        ("Select Resources",     "Resource List"),
        ("Resource List",        "Set Priorities"),
        ("Set Priorities",       "Priority Queue"),
        ("Priority Queue",       "Check Dependencies"),
        ("Check Dependencies",   "Tool Requirements"),
        ("Tool Requirements",    "Queue Tool Crafting"),
        ("Update Inventory",     "Inventory"),
        ("Inventory",            "Send Materials"),
        ("Select Friends",       "Friend List"),
        ("Friend List",          "Post Achievement"),
        ("Friend List",          "Send Materials"),
    ],
    
    "layout": {
        # Player lane (row 0)
        "Start":                 0,
        "Select Resources":      1,
        "Set Priorities":        2,
        "Resources Valid?":      3,
        "Too Many Selected":     3,      # Auto-stacked below Resources Valid?
        "Update Preferences":    8,
        "View Milestone":        9,
        "Continue Farming?":     10,
        
        # Bot System lane (row 1)
        "Check Dependencies":    4,
        "Tools Needed?":         5,
        "Queue Tool Crafting":   5,      # Auto-stacked below Tools Needed?
        "Prepare Farming":       6,
        "Fork Resources":        7,
        "Farm Wood":             8,
        "Farm Stone":            8,      # Auto-stacked
        "Farm Iron":             8,      # Auto-stacked
        "Farm Gold":             8,      # Auto-stacked
        "Farm Gems":             8,      # Auto-stacked
        "Join Resources":        9,
        "Update Inventory":      10,
        "All Complete?":         11,
        "Farming Complete":      12,
        
        # Event Handler lane (row 2)
        "Event Gateway":         7,
        "Disaster Strikes":      8,
        "Milestone Reached":     8,      # Auto-stacked
        "Preference Update":     8,      # Auto-stacked
        "Calculate Setback":     9,
        "Send Notification":     9,      # Auto-stacked
        "Merge Events":          10,
        
        # Social lane (row 3)
        "Share Results?":        13,
        "Select Friends":        14,
        "Choose Share Type":     15,
        "Post Achievement":      16,
        "Send Materials":        16,     # Auto-stacked
        "Join Share":            17,
        "End Process":           18,
        "Skip Sharing":          14,     # Auto-stacked below Select Friends
    },
    
    # Custom spacing for wider diagram
    "SPACING": 130,
    "START_X": 60,
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
