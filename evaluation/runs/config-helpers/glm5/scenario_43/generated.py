#
# CarService.py
#
# Description: Police car service reminder and processing workflow
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Car Service",
    
    "lanes": ["System", "Customer", "Mechanic"],
    
    "elements": [
        # Start and registration check
        ("Service Due", TIMER_START, "System"),
        ("Check Registration", SERVICE_TASK, "System"),
        ("Registered?", EXCLUSIVE_GW, "System"),
        
        # Notification path (Yes first for proper stacking)
        ("Notify Customer", SEND_TASK, "System"),
        ("End - Not Registered", END, "System"),
        
        # Wait and arrival check
        ("Wait 30 Days", TIMER_CATCH, "System"),
        ("Went to Service?", EXCLUSIVE_GW, "System"),
        
        # Fine path
        ("Issue Fine", SERVICE_TASK, "System"),
        ("End - Fine Issued", END, "System"),
        
        # Service process
        ("Go to Service", USER_TASK, "Customer"),
        ("Enter Problems", USER_TASK, "Mechanic"),
        ("Wait for Repair", TIMER_CATCH, "Customer"),
        ("Send Status Update", SEND_TASK, "Mechanic"),
        ("Pay via App", USER_TASK, "Customer"),
        ("Confirm Repair", USER_TASK, "Mechanic"),
        ("Set Next Service", USER_TASK, "Mechanic"),
        ("End - Complete", END, "Mechanic"),
    ],
    
    "flows": [
        ("Service Due", "Check Registration", ""),
        ("Check Registration", "Registered?", ""),
        ("Registered?", "Notify Customer", "Yes"),
        ("Registered?", "End - Not Registered", "No"),
        ("Notify Customer", "Wait 30 Days", ""),
        ("Wait 30 Days", "Went to Service?", ""),
        ("Went to Service?", "Go to Service", "Yes"),
        ("Went to Service?", "Issue Fine", "No"),
        ("Issue Fine", "End - Fine Issued", ""),
        ("Go to Service", "Enter Problems", ""),
        ("Enter Problems", "Wait for Repair", ""),
        ("Wait for Repair", "Send Status Update", ""),
        ("Send Status Update", "Pay via App", ""),
        ("Pay via App", "Confirm Repair", ""),
        ("Confirm Repair", "Set Next Service", ""),
        ("Set Next Service", "End - Complete", ""),
    ],
    
    "data_objects": [
        ("Service Record", "Mechanic", 8),
        ("Pickerl", "Mechanic", 12),
        ("Next Service Date", "Mechanic", 13),
    ],
    
    "data_associations": [
        ("Enter Problems", "Service Record"),
        ("Confirm Repair", "Pickerl"),
        ("Set Next Service", "Next Service Date"),
    ],
    
    "layout": {
        "Service Due": 0,
        "Check Registration": 1,
        "Registered?": 2,
        "Notify Customer": 3,
        "End - Not Registered": 3,
        "Wait 30 Days": 4,
        "Went to Service?": 5,
        "Issue Fine": 6,
        "Go to Service": 6,
        "End - Fine Issued": 7,
        "Enter Problems": 7,
        "Wait for Repair": 8,
        "Send Status Update": 9,
        "Pay via App": 10,
        "Confirm Repair": 11,
        "Set Next Service": 12,
        "End - Complete": 13,
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
