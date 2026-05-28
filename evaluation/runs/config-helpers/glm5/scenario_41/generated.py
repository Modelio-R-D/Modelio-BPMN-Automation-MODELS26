#
# InspectionEnergyDrinkBottlingMachine.py
#
# Description: BPMN process for inspection of an energy drink bottling machine
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "InspectionEnergyDrinkBottlingMachine",
    
    "lanes": ["Inspector", "Application"],
    
    "elements": [
        ("Start", START, "Inspector"),
        ("Enter Machine Details", USER_TASK, "Inspector"),
        ("Display Inspection Questions", SERVICE_TASK, "Application"),
        ("Answer Questions", USER_TASK, "Inspector"),
        ("Collect Machine Values", SERVICE_TASK, "Application"),
        ("Results Satisfactory?", EXCLUSIVE_GW, "Application"),
        ("Ask Additional Questions", USER_TASK, "Inspector"),
        ("Complete Inspection", SERVICE_TASK, "Application"),
        ("End", END, "Inspector"),
    ],
    
    "flows": [
        ("Start", "Enter Machine Details", ""),
        ("Enter Machine Details", "Display Inspection Questions", ""),
        ("Display Inspection Questions", "Answer Questions", ""),
        ("Answer Questions", "Collect Machine Values", ""),
        ("Collect Machine Values", "Results Satisfactory?", ""),
        ("Results Satisfactory?", "Complete Inspection", "Yes"),
        ("Results Satisfactory?", "Ask Additional Questions", "No"),
        ("Ask Additional Questions", "Complete Inspection", ""),
        ("Complete Inspection", "End", ""),
    ],
    
    "data_objects": [
        ("Machine Info", "Inspector", 1),
        ("Inspection Data", "Application", 4),
        ("Inspection Report", "Application", 7),
    ],
    
    "data_associations": [
        ("Enter Machine Details", "Machine Info"),
        ("Machine Info", "Display Inspection Questions"),
        ("Collect Machine Values", "Inspection Data"),
        ("Inspection Data", "Complete Inspection"),
        ("Complete Inspection", "Inspection Report"),
    ],
    
    "layout": {
        "Start": 0,
        "Enter Machine Details": 1,
        "Display Inspection Questions": 2,
        "Answer Questions": 3,
        "Collect Machine Values": 4,
        "Results Satisfactory?": 5,
        "Ask Additional Questions": 6,
        "Complete Inspection": 7,
        "End": 8,
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
