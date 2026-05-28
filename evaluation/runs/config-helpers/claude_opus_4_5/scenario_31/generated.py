#
# BlizzardCharacterGenerator.py
#
# Description: WoW character creation process with parallel account setup and name brainstorming
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BlizzardCharacterGenerator",
    
    "lanes": [
        "Player",
        "Blizzard System"
    ],
    
    "elements": [
        # Start
        ("Start", START, "Player"),
        
        # Parallel split - do two things at once
        ("Split Activities", PARALLEL_GW, "Player"),
        
        # Upper path - Account Setup
        ("Has Battle.net?", EXCLUSIVE_GW, "Player"),
        ("Enter Account Info", USER_TASK, "Player"),
        ("Receive Confirmation Mail", MESSAGE_CATCH, "Player"),
        ("Click Confirmation Link", USER_TASK, "Player"),
        ("Account Ready", EXCLUSIVE_GW, "Player"),
        ("Has Active Subscription?", EXCLUSIVE_GW, "Player"),
        ("Select Payment Method", USER_TASK, "Player"),
        ("Payment Choice", EXCLUSIVE_GW, "Player"),
        ("Enter Credit Card Info", USER_TASK, "Player"),
        ("Enter IBAN and BIC", USER_TASK, "Player"),
        ("Payment Done", EXCLUSIVE_GW, "Player"),
        ("Subscription Ready", EXCLUSIVE_GW, "Player"),
        
        # Lower path - Name Brainstorming
        ("Brainstorm Character Names", USER_TASK, "Player"),
        
        # Synchronization
        ("Sync Before Creation", PARALLEL_GW, "Player"),
        
        # Character creation with name loop
        ("Log Into Game", USER_TASK, "Player"),
        ("Select Realm Race Class", USER_TASK, "Player"),
        ("Enter Character Name", USER_TASK, "Player"),
        ("Check Name Availability", SERVICE_TASK, "Blizzard System"),
        ("Name Available?", EXCLUSIVE_GW, "Blizzard System"),
        
        # Completion
        ("Send Confirmation and Selfies", SEND_TASK, "Blizzard System"),
        ("Receive Confirmation", MESSAGE_CATCH, "Player"),
        ("Wait for Expansion Release", TIMER_CATCH, "Blizzard System"),
        ("Send Expansion Message", SEND_TASK, "Blizzard System"),
        ("End", END, "Player"),
    ],
    
    "flows": [
        # Start to parallel split
        ("Start", "Split Activities", ""),
        
        # Parallel paths
        ("Split Activities", "Has Battle.net?", ""),
        ("Split Activities", "Brainstorm Character Names", ""),
        
        # Battle.net account check
        ("Has Battle.net?", "Account Ready", "Yes"),
        ("Has Battle.net?", "Enter Account Info", "No"),
        ("Enter Account Info", "Receive Confirmation Mail", ""),
        ("Receive Confirmation Mail", "Click Confirmation Link", ""),
        ("Click Confirmation Link", "Account Ready", ""),
        
        # Subscription check
        ("Account Ready", "Has Active Subscription?", ""),
        ("Has Active Subscription?", "Subscription Ready", "Yes"),
        ("Has Active Subscription?", "Select Payment Method", "No"),
        
        # Payment method choice
        ("Select Payment Method", "Payment Choice", ""),
        ("Payment Choice", "Enter Credit Card Info", "Credit Card"),
        ("Payment Choice", "Enter IBAN and BIC", "Bank Account"),
        ("Enter Credit Card Info", "Payment Done", ""),
        ("Enter IBAN and BIC", "Payment Done", ""),
        ("Payment Done", "Subscription Ready", ""),
        
        # Sync paths
        ("Subscription Ready", "Sync Before Creation", ""),
        ("Brainstorm Character Names", "Sync Before Creation", ""),
        
        # Character creation
        ("Sync Before Creation", "Log Into Game", ""),
        ("Log Into Game", "Select Realm Race Class", ""),
        ("Select Realm Race Class", "Enter Character Name", ""),
        ("Enter Character Name", "Check Name Availability", ""),
        ("Check Name Availability", "Name Available?", ""),
        
        # Name loop
        ("Name Available?", "Enter Character Name", "No"),
        ("Name Available?", "Send Confirmation and Selfies", "Yes"),
        
        # Completion
        ("Send Confirmation and Selfies", "Receive Confirmation", ""),
        ("Receive Confirmation", "Wait for Expansion Release", ""),
        ("Wait for Expansion Release", "Send Expansion Message", ""),
        ("Send Expansion Message", "End", ""),
    ],
    
    "layout": {
        # Column 0: Start
        "Start": 0,
        
        # Column 1: Parallel split
        "Split Activities": 1,
        
        # Column 2: First checks / brainstorm
        "Has Battle.net?": 2,
        "Brainstorm Character Names": 2,
        
        # Column 3: Account creation path
        "Enter Account Info": 3,
        "Account Ready": 3,
        
        # Column 4: Confirmation
        "Receive Confirmation Mail": 4,
        "Has Active Subscription?": 4,
        
        # Column 5: Click link / Payment
        "Click Confirmation Link": 5,
        "Select Payment Method": 5,
        "Subscription Ready": 5,
        
        # Column 6: Payment choice
        "Payment Choice": 6,
        "Sync Before Creation": 6,
        
        # Column 7: Payment entry (stacked)
        "Enter Credit Card Info": 7,
        "Enter IBAN and BIC": 7,
        "Log Into Game": 7,
        
        # Column 8: Payment done
        "Payment Done": 8,
        "Select Realm Race Class": 8,
        
        # Column 9: Enter name
        "Enter Character Name": 9,
        
        # Column 10: Check name
        "Check Name Availability": 10,
        
        # Column 11: Name available?
        "Name Available?": 11,
        
        # Column 12: Confirmation
        "Send Confirmation and Selfies": 12,
        
        # Column 13: Receive
        "Receive Confirmation": 13,
        
        # Column 14: Wait
        "Wait for Expansion Release": 14,
        
        # Column 15: Send expansion msg
        "Send Expansion Message": 15,
        
        # Column 16: End
        "End": 16,
    },
    
    # Layout settings for wider diagram
    "SPACING": 140,
    "TASK_WIDTH": 110,
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
