#
# Chainsaw.py
#
# Description: Custom chainsaw production process - Customer specifies 5 properties
#              (guide bar length, chain width, power type, handle type, safety features),
#              parts are ordered in parallel, inspected, assembled, and delivered.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Chainsaw Production",
    
    "lanes": ["Customer", "Production"],
    
    "elements": [
        # Customer lane
        ("Start", START, "Customer"),
        ("Specify Properties", USER_TASK, "Customer"),
        ("Evaluate First Saw", USER_TASK, "Customer"),
        ("Satisfied?", EXCLUSIVE_GW, "Customer"),
        ("End", END, "Customer"),
        
        # Production lane - Parallel ordering of 5 parts
        ("Order Parts", PARALLEL_GW, "Production"),
        ("Order Guide Bar", SERVICE_TASK, "Production"),
        ("Order Chain", SERVICE_TASK, "Production"),
        ("Order Engine", SERVICE_TASK, "Production"),
        ("Order Handle", SERVICE_TASK, "Production"),
        ("Order Safety Guard", SERVICE_TASK, "Production"),
        
        # Production lane - Assembly and delivery
        ("Parts Arrived", PARALLEL_GW, "Production"),
        ("Inspect Parts", MANUAL_TASK, "Production"),
        ("Assemble First Saw", MANUAL_TASK, "Production"),
        ("Send Update", SERVICE_TASK, "Production"),
        ("Ship First Saw", SEND_TASK, "Production"),
        
        # Production lane - Order completion or rework
        ("Produce Remaining", MANUAL_TASK, "Production"),
        ("Ship Final Order", SEND_TASK, "Production"),
        ("Handle Rejection", USER_TASK, "Production"),
    ],
    
    "flows": [
        # Start and specification
        ("Start", "Specify Properties", ""),
        ("Specify Properties", "Order Parts", ""),
        
        # Parallel ordering (fork)
        ("Order Parts", "Order Guide Bar", ""),
        ("Order Parts", "Order Chain", ""),
        ("Order Parts", "Order Engine", ""),
        ("Order Parts", "Order Handle", ""),
        ("Order Parts", "Order Safety Guard", ""),
        
        # Parallel arrival (join)
        ("Order Guide Bar", "Parts Arrived", ""),
        ("Order Chain", "Parts Arrived", ""),
        ("Order Engine", "Parts Arrived", ""),
        ("Order Handle", "Parts Arrived", ""),
        ("Order Safety Guard", "Parts Arrived", ""),
        
        # Assembly and first delivery
        ("Parts Arrived", "Inspect Parts", ""),
        ("Inspect Parts", "Assemble First Saw", ""),
        ("Assemble First Saw", "Send Update", ""),
        ("Send Update", "Ship First Saw", ""),
        ("Ship First Saw", "Evaluate First Saw", ""),
        
        # Customer decision
        ("Evaluate First Saw", "Satisfied?", ""),
        ("Satisfied?", "Produce Remaining", "Yes"),
        ("Satisfied?", "Handle Rejection", "No"),
        
        # Complete order or rework
        ("Produce Remaining", "Ship Final Order", ""),
        ("Ship Final Order", "End", ""),
        ("Handle Rejection", "Inspect Parts", ""),
    ],
    
    "data_objects": [
        ("Saw Specifications", "Customer", 1),
        ("Quality Report", "Production", 5),
        ("First Chainsaw", "Production", 6),
        ("Customer Feedback", "Customer", 9),
        ("Final Order", "Production", 11),
    ],
    
    "data_associations": [
        ("Specify Properties", "Saw Specifications"),
        ("Inspect Parts", "Quality Report"),
        ("Quality Report", "Assemble First Saw"),
        ("Assemble First Saw", "First Chainsaw"),
        ("First Chainsaw", "Ship First Saw"),
        ("Evaluate First Saw", "Customer Feedback"),
        ("Customer Feedback", "Handle Rejection"),
        ("Produce Remaining", "Final Order"),
        ("Final Order", "Ship Final Order"),
    ],
    
    "layout": {
        # Customer lane
        "Start": 0,
        "Specify Properties": 1,
        "Evaluate First Saw": 9,
        "Satisfied?": 10,
        "End": 13,
        
        # Production lane - ordering (auto-stacked in column 3)
        "Order Parts": 2,
        "Order Guide Bar": 3,
        "Order Chain": 3,
        "Order Engine": 3,
        "Order Handle": 3,
        "Order Safety Guard": 3,
        
        # Production lane - assembly
        "Parts Arrived": 4,
        "Inspect Parts": 5,
        "Assemble First Saw": 6,
        "Send Update": 7,
        "Ship First Saw": 8,
        
        # Production lane - completion (auto-stacked in column 11)
        "Produce Remaining": 11,
        "Handle Rejection": 11,
        "Ship Final Order": 12,
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
