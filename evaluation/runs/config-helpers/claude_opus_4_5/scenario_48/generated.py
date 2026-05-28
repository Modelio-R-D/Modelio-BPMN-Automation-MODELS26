#
# ViennaNightRunApp.py
#
# Description: Process for participating at the Vienna Night Run
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ViennaNightRunApp",
    
    "lanes": ["Runner", "App/System", "Fitness Gadget"],
    
    "elements": [
        # Start
        ("Start", START, "Runner"),
        
        # Preparation phase
        ("Select Starting Block", USER_TASK, "Runner"),
        
        # Training loop
        ("Run 5km", MANUAL_TASK, "Runner"),
        ("Measure Time", SERVICE_TASK, "Fitness Gadget"),
        ("Under 25 min?", EXCLUSIVE_GW, "App/System"),
        ("Train More", MANUAL_TASK, "Runner"),
        
        # Registration
        ("Get Starting Number", SERVICE_TASK, "App/System"),
        
        # Travel decision
        ("Check Time Buffer", SERVICE_TASK, "App/System"),
        ("More than 1 hour?", EXCLUSIVE_GW, "App/System"),
        ("Go from Home", MANUAL_TASK, "Runner"),
        ("Leave from Work", MANUAL_TASK, "Runner"),
        ("Arrive at Event", MANUAL_TASK, "Runner"),
        
        # Race - parallel activities
        ("Race Start", PARALLEL_GW, "Runner"),
        ("Run Race", MANUAL_TASK, "Runner"),
        ("Drink Water", MANUAL_TASK, "Runner"),
        ("Race End", PARALLEL_GW, "Runner"),
        
        # Finish
        ("Record Final Time", SERVICE_TASK, "Fitness Gadget"),
        ("Receive Final Time", USER_TASK, "Runner"),
        ("End", END, "Runner"),
    ],
    
    "data_objects": [
        ("Starting Block", "App/System", 1),
        ("Training Time", "Fitness Gadget", 3),
        ("Starting Number", "App/System", 6),
        ("Work Schedule", "App/System", 7),
        ("Final Time", "Fitness Gadget", 14),
    ],
    
    "data_associations": [
        ("Select Starting Block", "Starting Block"),
        ("Starting Block", "Get Starting Number"),
        ("Measure Time", "Training Time"),
        ("Training Time", "Check Time Buffer"),
        ("Get Starting Number", "Starting Number"),
        ("Check Time Buffer", "Work Schedule"),
        ("Record Final Time", "Final Time"),
        ("Final Time", "Receive Final Time"),
    ],
    
    "flows": [
        ("Start", "Select Starting Block", ""),
        ("Select Starting Block", "Run 5km", ""),
        ("Run 5km", "Measure Time", ""),
        ("Measure Time", "Under 25 min?", ""),
        ("Under 25 min?", "Train More", "No"),
        ("Train More", "Run 5km", ""),
        ("Under 25 min?", "Get Starting Number", "Yes"),
        ("Get Starting Number", "Check Time Buffer", ""),
        ("Check Time Buffer", "More than 1 hour?", ""),
        ("More than 1 hour?", "Go from Home", "Yes"),
        ("More than 1 hour?", "Leave from Work", "No"),
        ("Go from Home", "Arrive at Event", ""),
        ("Leave from Work", "Arrive at Event", ""),
        ("Arrive at Event", "Race Start", ""),
        ("Race Start", "Run Race", ""),
        ("Race Start", "Drink Water", ""),
        ("Run Race", "Race End", ""),
        ("Drink Water", "Race End", ""),
        ("Race End", "Record Final Time", ""),
        ("Record Final Time", "Receive Final Time", ""),
        ("Receive Final Time", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Select Starting Block": 1,
        "Run 5km": 2,
        "Measure Time": 3,
        "Under 25 min?": 4,
        "Train More": 5,
        "Get Starting Number": 6,
        "Check Time Buffer": 7,
        "More than 1 hour?": 8,
        "Go from Home": 9,
        "Leave from Work": 9,
        "Arrive at Event": 10,
        "Race Start": 11,
        "Run Race": 12,
        "Drink Water": 12,
        "Race End": 13,
        "Record Final Time": 14,
        "Receive Final Time": 15,
        "End": 16,
    },
    
    "SPACING": 140,
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
