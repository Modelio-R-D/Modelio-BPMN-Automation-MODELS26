#
# OEE_Monitoring.py
#
# Description: OEE monitoring process - collects machine data, calculates OEE,
#              stops machine and notifies engineer if OEE falls below threshold.
#              Resumes on restart, ends on disconnection.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "OEE",
    
    "lanes": ["Machine", "System", "Engineer"],
    
    "elements": [
        # Start - periodic timer triggers data collection
        ("Start", TIMER_START, "System"),
        
        # Collect data from machine
        ("Collect Machine Data", SERVICE_TASK, "Machine"),
        
        # Check if machine is still connected
        ("Machine Connected?", EXCLUSIVE_GW, "System"),
        
        # Calculate OEE from collected data
        ("Calculate OEE", SERVICE_TASK, "System"),
        
        # End process when machine disconnects
        ("End Process", TERMINATE_END, "System"),
        
        # Check if OEE is below threshold
        ("OEE Below Threshold?", EXCLUSIVE_GW, "System"),
        
        # Stop the machine if OEE is low
        ("Stop Machine", SERVICE_TASK, "Machine"),
        
        # Notify engineer via email
        ("Notify Engineer", SEND_TASK, "System"),
        
        # Wait for machine restart signal
        ("Wait for Restart", SIGNAL_CATCH, "Machine"),
    ],
    
    "flows": [
        # Timer triggers data collection
        ("Start", "Collect Machine Data", ""),
        
        # After collecting, check connection
        ("Collect Machine Data", "Machine Connected?", ""),
        
        # If connected, calculate OEE
        ("Machine Connected?", "Calculate OEE", "Yes"),
        
        # If disconnected, end process
        ("Machine Connected?", "End Process", "No"),
        
        # After calculation, check threshold
        ("Calculate OEE", "OEE Below Threshold?", ""),
        
        # If OEE is low, stop machine
        ("OEE Below Threshold?", "Stop Machine", "Yes"),
        
        # If OEE is OK, continue monitoring (loop back)
        ("OEE Below Threshold?", "Collect Machine Data", "No"),
        
        # After stopping, notify engineer
        ("Stop Machine", "Notify Engineer", ""),
        
        # After notification, wait for restart
        ("Notify Engineer", "Wait for Restart", ""),
        
        # After restart, resume monitoring
        ("Wait for Restart", "Collect Machine Data", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Collect Machine Data": 1,
        "Machine Connected?": 2,
        "Calculate OEE": 3,
        "End Process": 3,
        "OEE Below Threshold?": 4,
        "Stop Machine": 5,
        "Notify Engineer": 6,
        "Wait for Restart": 7,
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
