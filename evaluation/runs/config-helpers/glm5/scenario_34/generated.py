#
# LegoMachineBuilder.py
#
# Description: Building a custom machine out of Lego bricks
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "LegoMachineBuilder",
    
    "lanes": ["Engineer", "Children"],
    
    "elements": [
        ("Start", START, "Engineer"),
        ("Develop Design", USER_TASK, "Engineer"),
        ("Order Brick Sets", SERVICE_TASK, "Engineer"),
        ("Sort Parts", USER_TASK, "Children"),
        ("Build Subcomponent", USER_TASK, "Engineer"),
        ("Parts Available?", EXCLUSIVE_GW, "Engineer"),
        ("Reorder Parts", SERVICE_TASK, "Engineer"),
        ("Test Subcomponent", USER_TASK, "Engineer"),
        ("Test OK?", EXCLUSIVE_GW, "Engineer"),
        ("Redesign Subcomponent", USER_TASK, "Engineer"),
        ("Rebuild Subcomponent", USER_TASK, "Engineer"),
        ("More Subcomponents?", EXCLUSIVE_GW, "Engineer"),
        ("Assemble Machine", USER_TASK, "Engineer"),
        ("End", END, "Engineer"),
    ],
    
    "flows": [
        ("Start", "Develop Design", ""),
        ("Develop Design", "Order Brick Sets", ""),
        ("Order Brick Sets", "Sort Parts", ""),
        ("Sort Parts", "Build Subcomponent", ""),
        ("Build Subcomponent", "Parts Available?", ""),
        ("Parts Available?", "Reorder Parts", "No"),
        ("Reorder Parts", "Build Subcomponent", ""),
        ("Parts Available?", "Test Subcomponent", "Yes"),
        ("Test Subcomponent", "Test OK?", ""),
        ("Test OK?", "Redesign Subcomponent", "No"),
        ("Redesign Subcomponent", "Rebuild Subcomponent", ""),
        ("Rebuild Subcomponent", "Test Subcomponent", ""),
        ("Test OK?", "More Subcomponents?", "Yes"),
        ("More Subcomponents?", "Build Subcomponent", "Yes"),
        ("More Subcomponents?", "Assemble Machine", "No"),
        ("Assemble Machine", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Develop Design": 1,
        "Order Brick Sets": 2,
        "Sort Parts": 3,
        "Build Subcomponent": 4,
        "Parts Available?": 5,
        "Test Subcomponent": 6,
        "Reorder Parts": 6,
        "Test OK?": 7,
        "More Subcomponents?": 8,
        "Redesign Subcomponent": 8,
        "Rebuild Subcomponent": 9,
        "Assemble Machine": 10,
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
