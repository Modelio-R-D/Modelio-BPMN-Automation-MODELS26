#
# WoWCharacterGenerator.py
#
# Description: Blizzard Online Character Generator for WoW expansion
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "WoWCharacterGenerator",
    
    "lanes": ["User", "Blizzard System"],
    
    "elements": [
        # Start with parallel split
        ("Start", START, "User"),
        ("Fork", PARALLEL_GW, "User"),
        
        # === ACCOUNT PATH ===
        ("Has Battle.net Account?", EXCLUSIVE_GW, "User"),
        ("Enter Account Info", USER_TASK, "User"),
        ("Send Confirmation Email", SERVICE_TASK, "Blizzard System"),
        ("Click Confirmation Link", USER_TASK, "User"),
        ("Has WoW Subscription?", EXCLUSIVE_GW, "User"),
        ("Select Payment Method", EXCLUSIVE_GW, "User"),
        ("Enter Credit Card Info", USER_TASK, "User"),
        ("Enter IBAN/BIC", USER_TASK, "User"),
        ("Process Payment", SERVICE_TASK, "Blizzard System"),
        
        # === NAMES PATH (parallel) ===
        ("Brainstorm Names", USER_TASK, "User"),
        
        # === SYNC POINT ===
        ("Join", PARALLEL_GW, "User"),
        
        # === CHARACTER CREATION ===
        ("Log Into Game", USER_TASK, "User"),
        ("Select Character Options", USER_TASK, "User"),
        ("Enter Character Name", USER_TASK, "User"),
        ("Name Available?", EXCLUSIVE_GW, "Blizzard System"),
        
        # === COMPLETION ===
        ("Send Confirmation", SERVICE_TASK, "Blizzard System"),
        ("Generate Selfies", SERVICE_TASK, "Blizzard System"),
        ("Wait for Expansion Release", TIMER_CATCH, "Blizzard System"),
        ("Send Expansion Message", SERVICE_TASK, "Blizzard System"),
        ("End", END, "User"),
    ],
    
    "flows": [
        # Start and parallel fork
        ("Start", "Fork", ""),
        ("Fork", "Has Battle.net Account?", ""),
        ("Fork", "Brainstorm Names", ""),
        
        # No Battle.net account - create one
        ("Has Battle.net Account?", "Enter Account Info", "No"),
        ("Enter Account Info", "Send Confirmation Email", ""),
        ("Send Confirmation Email", "Click Confirmation Link", ""),
        ("Click Confirmation Link", "Has WoW Subscription?", ""),
        
        # Has Battle.net account - skip to subscription check
        ("Has Battle.net Account?", "Has WoW Subscription?", "Yes"),
        
        # No subscription - payment options
        ("Has WoW Subscription?", "Select Payment Method", "No"),
        ("Select Payment Method", "Enter Credit Card Info", "Credit Card"),
        ("Select Payment Method", "Enter IBAN/BIC", "Bank Account"),
        ("Enter Credit Card Info", "Process Payment", ""),
        ("Enter IBAN/BIC", "Process Payment", ""),
        ("Process Payment", "Join", ""),
        
        # Has subscription - proceed directly
        ("Has WoW Subscription?", "Join", "Yes"),
        
        # Names path joins
        ("Brainstorm Names", "Join", ""),
        
        # After both paths complete
        ("Join", "Log Into Game", ""),
        ("Log Into Game", "Select Character Options", ""),
        ("Select Character Options", "Enter Character Name", ""),
        ("Enter Character Name", "Name Available?", ""),
        
        # Name availability loop
        ("Name Available?", "Enter Character Name", "No"),
        ("Name Available?", "Send Confirmation", "Yes"),
        
        # Final steps
        ("Send Confirmation", "Generate Selfies", ""),
        ("Generate Selfies", "Wait for Expansion Release", ""),
        ("Wait for Expansion Release", "Send Expansion Message", ""),
        ("Send Expansion Message", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Fork": 1,
        
        # Account path
        "Has Battle.net Account?": 2,
        "Enter Account Info": 3,
        "Send Confirmation Email": 4,
        "Click Confirmation Link": 5,
        "Has WoW Subscription?": 6,
        "Select Payment Method": 7,
        "Enter Credit Card Info": 8,
        "Enter IBAN/BIC": 8,
        "Process Payment": 9,
        
        # Parallel names path
        "Brainstorm Names": 4,
        
        # Sync and continue
        "Join": 10,
        "Log Into Game": 11,
        "Select Character Options": 12,
        "Enter Character Name": 13,
        "Name Available?": 14,
        "Send Confirmation": 15,
        "Generate Selfies": 16,
        "Wait for Expansion Release": 17,
        "Send Expansion Message": 18,
        "End": 19,
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
