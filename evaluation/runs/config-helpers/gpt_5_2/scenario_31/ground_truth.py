#
# Process_1.py
#
# Auto-generated from BPMN XML: Process_1
# Compatible with BPMN_Helpers.py v3.2
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Create character names", USER_TASK, "Process 1"),
        ("Create battle.net account", USER_TASK, "Process 1"),
        ("Confirm registration via email link", USER_TASK, "Process 1"),
        ("Enter credit card information", USER_TASK, "Process 1"),
        ("Enter IBAN", USER_TASK, "Process 1"),
        ("Enter BIC", USER_TASK, "Process 1"),
        ("Log into the game", USER_TASK, "Process 1"),
        ("Select realm", USER_TASK, "Process 1"),
        ("Select race", USER_TASK, "Process 1"),
        ("Select class", USER_TASK, "Process 1"),
        ("Enter character name", USER_TASK, "Process 1"),
        ("Check if battle.net account exists", SERVICE_TASK, "Process 1"),
        ("Check if active WoW subscription exists", SERVICE_TASK, "Process 1"),
        ("Recieve confirmation", SERVICE_TASK, "Process 1"),
        ("Recieve character selfies", SERVICE_TASK, "Process 1"),
        ("Does an account exist?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("Does a subscription exist?", EXCLUSIVE_GW, "Process 1"),
        ("Select payment method", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Name available?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_5", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_6", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_7", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_8", PARALLEL_GW, "Process 1"),
        ("Account is set up", START, "Process 1"),
        ("Character created", END, "Process 1"),
    ],

    "flows": [
        ("Account is set up", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Create character names", ""),
        ("Check if battle.net account exists", "Does an account exist?", ""),
        ("Does an account exist?", "Create battle.net account", "No"),
        ("Create battle.net account", "Confirm registration via email link", ""),
        ("Confirm registration via email link", "ExclusiveGateway_2", ""),
        ("ParallelGateway_1", "Check if battle.net account exists", ""),
        ("ExclusiveGateway_2", "Check if active WoW subscription exists", ""),
        ("Check if active WoW subscription exists", "Does a subscription exist?", ""),
        ("Does a subscription exist?", "Select payment method", "No"),
        ("ParallelGateway_2", "Enter IBAN", ""),
        ("ParallelGateway_2", "Enter BIC", ""),
        ("Enter IBAN", "ParallelGateway_3", ""),
        ("Enter credit card information", "ExclusiveGateway_5", ""),
        ("ParallelGateway_3", "ExclusiveGateway_5", ""),
        ("Does an account exist?", "ExclusiveGateway_2", "Yes"),
        ("Enter BIC", "ParallelGateway_3", ""),
        ("Select payment method", "Enter credit card information", "Credit card"),
        ("ExclusiveGateway_5", "Log into the game", ""),
        ("Log into the game", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "Select realm", ""),
        ("ParallelGateway_4", "Select race", ""),
        ("ParallelGateway_4", "Select class", ""),
        ("Select race", "ParallelGateway_8", ""),
        ("Select realm", "ParallelGateway_8", ""),
        ("Select class", "ParallelGateway_8", ""),
        ("ParallelGateway_8", "ParallelGateway_5", ""),
        ("Create character names", "ParallelGateway_5", ""),
        ("Enter character name", "Name available?", ""),
        ("ParallelGateway_5", "ExclusiveGateway_7", ""),
        ("ExclusiveGateway_7", "Enter character name", ""),
        ("Name available?", "ExclusiveGateway_7", "No"),
        ("Name available?", "ParallelGateway_6", "Yes"),
        ("ParallelGateway_6", "Recieve character selfies", ""),
        ("ParallelGateway_6", "Recieve confirmation", ""),
        ("Recieve confirmation", "ParallelGateway_7", ""),
        ("ParallelGateway_7", "Character created", ""),
        ("Select payment method", "ParallelGateway_2", "Bank account"),
        ("Does a subscription exist?", "ExclusiveGateway_5", "Yes"),
        ("Recieve character selfies", "ParallelGateway_7", ""),
    ],

    "layout": {
        "Account is set up": 0,
        "ParallelGateway_1": 1,
        "Create character names": 2,
        "Check if battle.net account exists": 2,
        "Does an account exist?": 3,
        "Create battle.net account": 4,
        "Enter character name": 5,
        "Confirm registration via email link": 5,
        "Check if active WoW subscription exists": 5,
        "ExclusiveGateway_2": 6,
        "Name available?": 6,
        "Does a subscription exist?": 6,
        "ExclusiveGateway_7": 7,
        "ParallelGateway_6": 7,
        "Select payment method": 7,
        "Recieve character selfies": 8,
        "Recieve confirmation": 8,
        "Enter credit card information": 8,
        "ParallelGateway_2": 8,
        "Log into the game": 8,
        "ParallelGateway_7": 9,
        "Enter IBAN": 9,
        "Enter BIC": 9,
        "ParallelGateway_4": 9,
        "Character created": 10,
        "ParallelGateway_3": 10,
        "Select realm": 10,
        "Select race": 10,
        "Select class": 10,
        "ExclusiveGateway_5": 11,
        "ParallelGateway_8": 11,
        "ParallelGateway_5": 12,
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
