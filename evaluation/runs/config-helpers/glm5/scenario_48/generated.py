#
# ViennaNightRun.py
#
# Description: BPMN for Vienna Night Run app participation process
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "ViennaNightRun",
    
    "lanes": ["App User", "Fitness Gadget"],
    
    "elements": [
        # Start and initial flow
        ("Start", START, "App User"),
        ("Select Starting Block", USER_TASK, "App User"),
        ("Run 5km", USER_TASK, "App User"),
        ("Measure Time", SERVICE_TASK, "Fitness Gadget"),
        
        # Training validation decision
        ("Time < 25 min?", EXCLUSIVE_GW, "App User"),
        ("Train More", USER_TASK, "App User"),
        ("Get Starting Number", USER_TASK, "App User"),
        
        # Work schedule decision
        ("Check Work Schedule", USER_TASK, "App User"),
        ("Work > 1hr Before Start?", EXCLUSIVE_GW, "App User"),
        ("Go from Home", USER_TASK, "App User"),
        ("Go from Work", USER_TASK, "App User"),
        
        # Parallel execution at event (run + drink)
        ("Fork", PARALLEL_GW, "App User"),
        ("Run Night Run", USER_TASK, "App User"),
        ("Drink Water", USER_TASK, "App User"),
        ("Join", PARALLEL_GW, "App User"),
        
        # End
        ("Record Final Time", SERVICE_TASK, "Fitness Gadget"),
        ("End", END, "App User"),
    ],
    
    "flows": [
        ("Start", "Select Starting Block", ""),
        ("Select Starting Block", "Run 5km", ""),
        ("Run 5km", "Measure Time", ""),
        ("Measure Time", "Time < 25 min?", ""),
        ("Time < 25 min?", "Train More", "No"),
        ("Train More", "Run 5km", ""),
        ("Time < 25 min?", "Get Starting Number", "Yes"),
        ("Get Starting Number", "Check Work Schedule", ""),
        ("Check Work Schedule", "Work > 1hr Before Start?", ""),
        ("Work > 1hr Before Start?", "Go from Home", "Yes"),
        ("Work > 1hr Before Start?", "Go from Work", "No"),
        ("Go from Home", "Fork", ""),
        ("Go from Work", "Fork", ""),
        ("Fork", "Run Night Run", ""),
        ("Fork", "Drink Water", ""),
        ("Run Night Run", "Join", ""),
        ("Drink Water", "Join", ""),
        ("Join", "Record Final Time", ""),
        ("Record Final Time", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Select Starting Block": 1,
        "Run 5km": 2,
        "Measure Time": 3,
        "Time < 25 min?": 4,
        "Train More": 4,           # Auto-stacked below gateway
        "Get Starting Number": 5,
        "Check Work Schedule": 6,
        "Work > 1hr Before Start?": 7,
        "Go from Home": 8,
        "Go from Work": 8,         # Auto-stacked below Go from Home
        "Fork": 9,
        "Run Night Run": 10,
        "Drink Water": 10,          # Auto-stacked below Run Night Run
        "Join": 11,
        "Record Final Time": 12,
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
