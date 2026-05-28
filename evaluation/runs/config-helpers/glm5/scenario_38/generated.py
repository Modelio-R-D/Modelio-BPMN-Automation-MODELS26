#
# BuildingHouse.py
#
# Description: BPMN process for building a tree house - from requirements to party
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "BuildingHouse",
    
    "lanes": ["You", "Architect", "Online Stores", "Friends"],
    
    "elements": [
        # You lane - main process flow
        ("Start", START, "You"),
        ("Collect Requirements", USER_TASK, "You"),
        ("Send Requirements", SEND_TASK, "You"),
        ("Refine Requirements", USER_TASK, "You"),
        ("Receive Draft", MESSAGE_CATCH, "You"),
        ("Review Draft", USER_TASK, "You"),
        ("Draft Complete?", EXCLUSIVE_GW, "You"),
        ("Create Material List", USER_TASK, "You"),
        ("Split Tasks", PARALLEL_GW, "You"),
        ("Order Materials", SEND_TASK, "You"),
        ("Invite Builders", SEND_TASK, "You"),
        ("Receive Materials", MESSAGE_CATCH, "You"),
        ("House Complete", MESSAGE_CATCH, "You"),
        ("Join Tasks", PARALLEL_GW, "You"),
        ("Send Party Invitations", SEND_TASK, "You"),
        ("Receive RSVPs", MESSAGE_CATCH, "You"),
        ("Create Attendee List", USER_TASK, "You"),
        ("Buy Snacks", USER_TASK, "You"),
        ("End", END, "You"),
        
        # Architect lane
        ("Receive Requirements", MESSAGE_CATCH, "Architect"),
        ("Create Draft", USER_TASK, "Architect"),
        ("Send Draft", SEND_TASK, "Architect"),
        
        # Online Stores lane
        ("Receive Order", MESSAGE_CATCH, "Online Stores"),
        ("Process Order", SERVICE_TASK, "Online Stores"),
        ("Send Confirmation", SEND_TASK, "Online Stores"),
        
        # Friends lane
        ("Receive Build Invitation", MESSAGE_CATCH, "Friends"),
        ("Build House", USER_TASK, "Friends"),
        ("Notify Complete", SEND_TASK, "Friends"),
        ("Receive Party Invitation", MESSAGE_CATCH, "Friends"),
        ("Send RSVP", SEND_TASK, "Friends"),
    ],
    
    "flows": [
        # You lane - main sequence
        ("Start", "Collect Requirements", ""),
        ("Collect Requirements", "Send Requirements", ""),
        ("Send Requirements", "Receive Draft", ""),
        ("Receive Draft", "Review Draft", ""),
        ("Review Draft", "Draft Complete?", ""),
        ("Draft Complete?", "Create Material List", "Yes"),
        ("Draft Complete?", "Refine Requirements", "No"),
        ("Refine Requirements", "Send Requirements", ""),
        ("Create Material List", "Split Tasks", ""),
        
        # Parallel paths from split
        ("Split Tasks", "Order Materials", ""),
        ("Split Tasks", "Invite Builders", ""),
        ("Order Materials", "Receive Materials", ""),
        ("Invite Builders", "House Complete", ""),
        
        # Converge at join
        ("Receive Materials", "Join Tasks", ""),
        ("House Complete", "Join Tasks", ""),
        
        # Party preparation
        ("Join Tasks", "Send Party Invitations", ""),
        ("Send Party Invitations", "Receive RSVPs", ""),
        ("Receive RSVPs", "Create Attendee List", ""),
        ("Create Attendee List", "Buy Snacks", ""),
        ("Buy Snacks", "End", ""),
        
        # Architect lane
        ("Receive Requirements", "Create Draft", ""),
        ("Create Draft", "Send Draft", ""),
        
        # Online Stores lane
        ("Receive Order", "Process Order", ""),
        ("Process Order", "Send Confirmation", ""),
        
        # Friends lane
        ("Receive Build Invitation", "Build House", ""),
        ("Build House", "Notify Complete", ""),
        ("Receive Party Invitation", "Send RSVP", ""),
    ],
    
    "layout": {
        # You lane
        "Start": 0,
        "Collect Requirements": 1,
        "Send Requirements": 2,
        "Refine Requirements": 3,
        "Receive Draft": 4,
        "Review Draft": 5,
        "Draft Complete?": 6,
        "Create Material List": 7,
        "Split Tasks": 8,
        "Order Materials": 9,
        "Invite Builders": 9,
        "Receive Materials": 13,
        "House Complete": 13,
        "Join Tasks": 14,
        "Send Party Invitations": 15,
        "Receive RSVPs": 16,
        "Create Attendee List": 17,
        "Buy Snacks": 18,
        "End": 19,
        
        # Architect lane
        "Receive Requirements": 2,
        "Create Draft": 3,
        "Send Draft": 4,
        
        # Online Stores lane
        "Receive Order": 10,
        "Process Order": 11,
        "Send Confirmation": 12,
        
        # Friends lane
        "Receive Build Invitation": 10,
        "Build House": 11,
        "Notify Complete": 12,
        "Receive Party Invitation": 15,
        "Send RSVP": 16,
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
