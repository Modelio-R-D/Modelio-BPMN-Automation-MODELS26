#
# FridgeServiceProcess.py
#
# Description: Fridge Service Process - Customer reports noise, service center assigns facility, 
#              facility repairs fridge, customer confirms and rates service.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Service for Your Fridge",
    
    "lanes": ["Customer", "Central Service Center", "Service Facility"],
    
    "elements": [
        # Customer lane
        ("Fridge Noise Detected", START, "Customer"),
        ("Describe Symptoms", USER_TASK, "Customer"),
        ("Send Symptoms & Fridge Type", SEND_TASK, "Customer"),
        ("Receive Appointment", RECEIVE_TASK, "Customer"),
        ("Confirm Fridge OK", USER_TASK, "Customer"),
        ("Rate Service Facility", USER_TASK, "Customer"),
        ("Process Complete", END, "Customer"),
        
        # Central Service Center lane
        ("Receive Service Request", RECEIVE_TASK, "Central Service Center"),
        ("Select Service Facility", USER_TASK, "Central Service Center"),
        ("Assign to Facility", SEND_TASK, "Central Service Center"),
        
        # Service Facility lane
        ("Receive Assignment", RECEIVE_TASK, "Service Facility"),
        ("Make Appointment", USER_TASK, "Service Facility"),
        ("Notify Customer", SEND_TASK, "Service Facility"),
        ("Arrive at Location", MANUAL_TASK, "Service Facility"),
        ("Parts Available?", EXCLUSIVE_GW, "Service Facility"),
        ("Repair Fridge", SERVICE_TASK, "Service Facility"),
        ("Order Parts", SERVICE_TASK, "Service Facility"),
        ("Reschedule Appointment", USER_TASK, "Service Facility"),
        ("Service Completed", END, "Service Facility"),
    ],
    
    "flows": [
        # Customer lane flows
        ("Fridge Noise Detected", "Describe Symptoms", ""),
        ("Describe Symptoms", "Send Symptoms & Fridge Type", ""),
        ("Receive Appointment", "Confirm Fridge OK", ""),
        ("Confirm Fridge OK", "Rate Service Facility", ""),
        ("Rate Service Facility", "Process Complete", ""),
        
        # Central Service Center flows
        ("Receive Service Request", "Select Service Facility", ""),
        ("Select Service Facility", "Assign to Facility", ""),
        
        # Service Facility flows
        ("Receive Assignment", "Make Appointment", ""),
        ("Make Appointment", "Notify Customer", ""),
        ("Notify Customer", "Arrive at Location", ""),
        ("Arrive at Location", "Parts Available?", ""),
        ("Parts Available?", "Repair Fridge", "Yes"),
        ("Parts Available?", "Order Parts", "No"),
        ("Order Parts", "Reschedule Appointment", ""),
        ("Reschedule Appointment", "Notify Customer", ""),
        ("Repair Fridge", "Service Completed", ""),
        
        # Message flows between lanes (modeled as sequence flows for simplicity)
        ("Send Symptoms & Fridge Type", "Receive Service Request", ""),
        ("Assign to Facility", "Receive Assignment", ""),
        ("Notify Customer", "Receive Appointment", ""),
    ],
    
    "layout": {
        # Customer lane (top)
        "Fridge Noise Detected": 0,
        "Describe Symptoms": 1,
        "Send Symptoms & Fridge Type": 2,
        "Receive Appointment": 4,
        "Confirm Fridge OK": 5,
        "Rate Service Facility": 6,
        "Process Complete": 7,
        
        # Central Service Center lane (middle)
        "Receive Service Request": 2,
        "Select Service Facility": 3,
        "Assign to Facility": 4,
        
        # Service Facility lane (bottom)
        "Receive Assignment": 4,
        "Make Appointment": 5,
        "Notify Customer": 6,
        "Arrive at Location": 7,
        "Parts Available?": 8,
        "Repair Fridge": 9,
        "Order Parts": 9,
        "Reschedule Appointment": 10,
        "Service Completed": 10,
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
