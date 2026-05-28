#
# LANParty.py
#
# Description: Planning process for organizing a LAN party with 10 friends
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LANParty",
    
    "lanes": ["Organizer"],
    
    "elements": [
        ("Start", START, "Organizer"),
        ("Send Invitations", SEND_TASK, "Organizer"),
        ("Find Out Games", USER_TASK, "Organizer"),
        ("Split", PARALLEL_GW, "Organizer"),
        ("Appoint Date", USER_TASK, "Organizer"),
        ("8+ Agree?", EXCLUSIVE_GW, "Organizer"),
        ("Check Games Available", USER_TASK, "Organizer"),
        ("Games Missing?", EXCLUSIVE_GW, "Organizer"),
        ("Download Games", SERVICE_TASK, "Organizer"),
        ("Join", PARALLEL_GW, "Organizer"),
        ("Find Out Beer Needed", USER_TASK, "Organizer"),
        ("Enough Beer?", EXCLUSIVE_GW, "Organizer"),
        ("Buy Beer", MANUAL_TASK, "Organizer"),
        ("Merge Beer", EXCLUSIVE_GW, "Organizer"),
        ("Enjoy LAN Party", USER_TASK, "Organizer"),
        ("End", END, "Organizer"),
    ],
    
    "flows": [
        ("Start", "Send Invitations", ""),
        ("Send Invitations", "Find Out Games", ""),
        ("Find Out Games", "Split", ""),
        ("Split", "Appoint Date", ""),
        ("Split", "Check Games Available", ""),
        ("Appoint Date", "8+ Agree?", ""),
        ("8+ Agree?", "Join", "Yes"),
        ("8+ Agree?", "Appoint Date", "No"),
        ("Check Games Available", "Games Missing?", ""),
        ("Games Missing?", "Download Games", "Yes"),
        ("Games Missing?", "Join", "No"),
        ("Download Games", "Join", ""),
        ("Join", "Find Out Beer Needed", ""),
        ("Find Out Beer Needed", "Enough Beer?", ""),
        ("Enough Beer?", "Buy Beer", "No"),
        ("Enough Beer?", "Merge Beer", "Yes"),
        ("Buy Beer", "Merge Beer", ""),
        ("Merge Beer", "Enjoy LAN Party", ""),
        ("Enjoy LAN Party", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Send Invitations": 1,
        "Find Out Games": 2,
        "Split": 3,
        "Appoint Date": 4,
        "Check Games Available": (4, 120),
        "8+ Agree?": 5,
        "Games Missing?": (5, 120),
        "Download Games": (6, 120),
        "Join": 7,
        "Find Out Beer Needed": 8,
        "Enough Beer?": 9,
        "Buy Beer": (10, 90),
        "Merge Beer": 11,
        "Enjoy LAN Party": 12,
        "End": 13,
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
