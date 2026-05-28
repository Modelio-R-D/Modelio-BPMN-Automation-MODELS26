#
# FridgeServiceProcess.py
#
# Description: Customer reports fridge issues, service center assigns local facility,
#              technician visits (may need parts), customer confirms repair and rates service.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "FridgeServiceProcess",
    
    "lanes": [
        "Customer",
        "Service Center",
        "Local Service Facility",
        "Technician"
    ],
    
    "elements": [
        # Customer lane
        ("Start",                    START,        "Customer"),
        ("Describe Symptoms",        USER_TASK,    "Customer"),
        ("Send Service Request",     SEND_TASK,    "Customer"),
        ("Receive Appointment",      RECEIVE_TASK, "Customer"),
        ("Wait for Technician",      USER_TASK,    "Customer"),
        ("Confirm Repair OK",        USER_TASK,    "Customer"),
        ("Rate Service Facility",    USER_TASK,    "Customer"),
        ("End",                      END,          "Customer"),
        
        # Service Center lane
        ("Receive Request",          RECEIVE_TASK, "Service Center"),
        ("Select Local Facility",    SERVICE_TASK, "Service Center"),
        ("Forward to Facility",      SEND_TASK,    "Service Center"),
        
        # Local Service Facility lane
        ("Receive Assignment",       RECEIVE_TASK, "Local Service Facility"),
        ("Schedule Appointment",     USER_TASK,    "Local Service Facility"),
        ("Send Appointment",         SEND_TASK,    "Local Service Facility"),
        ("Dispatch Technician",      MANUAL_TASK,  "Local Service Facility"),
        
        # Technician lane
        ("Arrive at Customer",       MANUAL_TASK,  "Technician"),
        ("Diagnose Problem",         MANUAL_TASK,  "Technician"),
        ("Parts Available?",         EXCLUSIVE_GW, "Technician"),
        ("Repair Fridge",            MANUAL_TASK,  "Technician"),
        ("Order Parts",              SEND_TASK,    "Technician"),
        ("Leave Without Repair",     MANUAL_TASK,  "Technician"),
        ("Reschedule Visit",         SEND_TASK,    "Technician"),
        ("Repair Complete",          EXCLUSIVE_GW, "Technician"),
    ],
    
    "data_objects": [
        ("Service Request",    "Customer",              2),
        ("Appointment Details", "Local Service Facility", 5),
    ],
    
    "data_associations": [
        ("Describe Symptoms",    "Service Request"),
        ("Service Request",      "Send Service Request"),
        ("Schedule Appointment", "Appointment Details"),
        ("Appointment Details",  "Send Appointment"),
    ],
    
    "flows": [
        # Customer initiates
        ("Start",                  "Describe Symptoms",     ""),
        ("Describe Symptoms",      "Send Service Request",  ""),
        
        # Service Center processing
        ("Send Service Request",   "Receive Request",       ""),
        ("Receive Request",        "Select Local Facility", ""),
        ("Select Local Facility",  "Forward to Facility",   ""),
        
        # Local Facility scheduling
        ("Forward to Facility",    "Receive Assignment",    ""),
        ("Receive Assignment",     "Schedule Appointment",  ""),
        ("Schedule Appointment",   "Send Appointment",      ""),
        ("Send Appointment",       "Receive Appointment",   ""),
        ("Send Appointment",       "Dispatch Technician",   ""),
        
        # Customer waiting
        ("Receive Appointment",    "Wait for Technician",   ""),
        
        # Technician visit
        ("Dispatch Technician",    "Arrive at Customer",    ""),
        ("Arrive at Customer",     "Diagnose Problem",      ""),
        ("Diagnose Problem",       "Parts Available?",      ""),
        
        # Parts decision
        ("Parts Available?",       "Repair Fridge",         "Yes"),
        ("Parts Available?",       "Order Parts",           "No"),
        ("Order Parts",            "Leave Without Repair",  ""),
        ("Leave Without Repair",   "Reschedule Visit",      ""),
        ("Reschedule Visit",       "Receive Appointment",   ""),
        
        # Repair completion
        ("Repair Fridge",          "Repair Complete",       ""),
        ("Repair Complete",        "Confirm Repair OK",     ""),
        
        # Customer confirmation and rating
        ("Confirm Repair OK",      "Rate Service Facility", ""),
        ("Rate Service Facility",  "End",                   ""),
    ],
    
    "layout": {
        # Customer lane
        "Start":                  0,
        "Describe Symptoms":      1,
        "Send Service Request":   2,
        "Receive Appointment":    6,
        "Wait for Technician":    7,
        "Confirm Repair OK":      12,
        "Rate Service Facility":  13,
        "End":                    14,
        
        # Service Center lane
        "Receive Request":        3,
        "Select Local Facility":  4,
        "Forward to Facility":    5,
        
        # Local Service Facility lane
        "Receive Assignment":     5,
        "Schedule Appointment":   5,
        "Send Appointment":       6,
        "Dispatch Technician":    7,
        
        # Technician lane
        "Arrive at Customer":     8,
        "Diagnose Problem":       9,
        "Parts Available?":       10,
        "Repair Fridge":          11,
        "Order Parts":            11,
        "Leave Without Repair":   12,
        "Reschedule Visit":       13,
        "Repair Complete":        12,
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
