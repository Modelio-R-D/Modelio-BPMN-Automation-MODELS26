#
# Process_1.py
#
# Auto-generated from BPMN XML: Process_1
# Compatible with BPMN_Helpers.py v3.2
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Send sketches to an artist", USER_TASK, "Process 1"),
        ("Tell artist to change", USER_TASK, "Process 1"),
        ("Choose the color", USER_TASK, "Process 1"),
        ("Check color level", USER_TASK, "Process 1"),
        ("Order color", USER_TASK, "Process 1"),
        ("Turn on the printer", USER_TASK, "Process 1"),
        ("Generate gcode file", USER_TASK, "Process 1"),
        ("Print the model", USER_TASK, "Process 1"),
        ("Receive result", RECEIVE_TASK, "Process 1"),
        ("Receive status", RECEIVE_TASK, "Process 1"),
        ("Receive order confirmation", RECEIVE_TASK, "Process 1"),
        ("Put it on shopping list", MANUAL_TASK, "Process 1"),
        ("Color received", MANUAL_TASK, "Process 1"),
        ("Satisfied with result?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("In stock?", EXCLUSIVE_GW, "Process 1"),
        ("Under 100g?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("Heated?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Create a 3D model", START, "Process 1"),
        ("Model printed", END, "Process 1"),
    ],

    "flows": [
        ("Send sketches to an artist", "Receive result", ""),
        ("Receive result", "Satisfied with result?", ""),
        ("Tell artist to change", "ExclusiveGateway_2", ""),
        ("ExclusiveGateway_2", "Send sketches to an artist", ""),
        ("Create a 3D model", "ExclusiveGateway_2", ""),
        ("Satisfied with result?", "Choose the color", "Yes"),
        ("Choose the color", "In stock?", ""),
        ("In stock?", "Check color level", "Yes"),
        ("Check color level", "Under 100g?", ""),
        ("Under 100g?", "Put it on shopping list", "Yes"),
        ("Under 100g?", "ExclusiveGateway_5", "No"),
        ("Put it on shopping list", "ExclusiveGateway_5", ""),
        ("In stock?", "Order color", "No"),
        ("ExclusiveGateway_5", "ExclusiveGateway_6", ""),
        ("Order color", "Receive order confirmation", ""),
        ("ExclusiveGateway_6", "Turn on the printer", ""),
        ("Turn on the printer", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Generate gcode file", ""),
        ("Receive status", "Heated?", ""),
        ("ParallelGateway_1", "ExclusiveGateway_8", ""),
        ("ExclusiveGateway_8", "Receive status", ""),
        ("Heated?", "ParallelGateway_2", "Yes"),
        ("Generate gcode file", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Print the model", ""),
        ("Print the model", "Model printed", ""),
        ("Heated?", "ExclusiveGateway_8", "No"),
        ("Receive order confirmation", "Color received", ""),
        ("Color received", "ExclusiveGateway_6", ""),
        ("Satisfied with result?", "Tell artist to change", "No"),
    ],

    "layout": {
        "Create a 3D model": 0,
        "Send sketches to an artist": 2,
        "Receive result": 3,
        "Satisfied with result?": 4,
        "Choose the color": 5,
        "Tell artist to change": 5,
        "ExclusiveGateway_2": 6,
        "In stock?": 6,
        "Check color level": 7,
        "Order color": 7,
        "Under 100g?": 8,
        "Receive order confirmation": 8,
        "Put it on shopping list": 9,
        "Color received": 9,
        "ExclusiveGateway_5": 10,
        "ExclusiveGateway_6": 11,
        "Turn on the printer": 12,
        "ParallelGateway_1": 13,
        "Generate gcode file": 14,
        "Receive status": 15,
        "Print the model": 16,
        "Heated?": 16,
        "ExclusiveGateway_8": 17,
        "ParallelGateway_2": 17,
        "Model printed": 17,
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
