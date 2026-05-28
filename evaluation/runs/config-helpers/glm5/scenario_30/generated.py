#
# LAN_Party.py
#
# Description: LAN Party Planning Process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LAN_Party",
    
    "lanes": ["Organizer"],
    
    "elements": [
        ("Start", START, "Organizer"),
        ("Send Invitations", SEND_TASK, "Organizer"),
        ("Get Game Preferences", RECEIVE_TASK, "Organizer"),
        ("Appoint Date", USER_TASK, "Organizer"),
        ("8+ Confirmed?", EXCLUSIVE_GW, "Organizer"),
        ("Find New Date", USER_TASK, "Organizer"),
        ("Games Available?", EXCLUSIVE_GW, "Organizer"),
        ("Download Games", SERVICE_TASK, "Organizer"),
        ("Get Beer Requirements", USER_TASK, "Organizer"),
        ("Enough Beer?", EXCLUSIVE_GW, "Organizer"),
        ("Buy Beer", USER_TASK, "Organizer"),
        ("Enjoy LAN Party", USER_TASK, "Organizer"),
        ("End", END, "Organizer"),
    ],
    
    "flows": [
        ("Start", "Send Invitations", ""),
        ("Send Invitations", "Get Game Preferences", ""),
        ("Get Game Preferences", "Appoint Date", ""),
        ("Appoint Date", "8+ Confirmed?", ""),
        ("8+ Confirmed?", "Find New Date", "No"),
        ("Find New Date", "Appoint Date", ""),
        ("8+ Confirmed?", "Games Available?", "Yes"),
        ("Games Available?", "Get Beer Requirements", "Yes"),
        ("Games Available?", "Download Games", "No"),
        ("Download Games", "Get Beer Requirements", ""),
        ("Get Beer Requirements", "Enough Beer?", ""),
        ("Enough Beer?", "Enjoy LAN Party", "Yes"),
        ("Enough Beer?", "Buy Beer", "No"),
        ("Buy Beer", "Enjoy LAN Party", ""),
        ("Enjoy LAN Party", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Send Invitations": 1,
        "Get Game Preferences": 2,
        "Appoint Date": 3,
        "8+ Confirmed?": 4,
        "Find New Date": 4,
        "Games Available?": 5,
        "Download Games": 6,
        "Get Beer Requirements": 7,
        "Enough Beer?": 8,
        "Buy Beer": 9,
        "Enjoy LAN Party": 10,
        "End": 11,
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
