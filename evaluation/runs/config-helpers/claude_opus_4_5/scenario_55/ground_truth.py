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
        ("Prepare implements", USER_TASK, "Process 1"),
        ("Hand washing", USER_TASK, "Process 1"),
        ("Get in sterile clothes", USER_TASK, "Process 1"),
        ("Clean puncture area", USER_TASK, "Process 1"),
        ("Drap puncture zone", USER_TASK, "Process 1"),
        ("Ultrasound configuration", USER_TASK, "Process 1"),
        ("Gel in probe", USER_TASK, "Process 1"),
        ("Cover probe", USER_TASK, "Process 1"),
        ("Put sterile gel", USER_TASK, "Process 1"),
        ("Position probe", USER_TASK, "Process 1"),
        ("Position patient", USER_TASK, "Process 1"),
        ("Doppler identification", USER_TASK, "Process 1"),
        ("Anatomic identification", USER_TASK, "Process 1"),
        ("Compression identification", USER_TASK, "Process 1"),
        ("Anesthetize patient", USER_TASK, "Process 1"),
        ("Puncture patient", USER_TASK, "Process 1"),
        ("Check blood return", USER_TASK, "Process 1"),
        ("Drop probe", USER_TASK, "Process 1"),
        ("Remove syringe", USER_TASK, "Process 1"),
        ("Guidewire install", USER_TASK, "Process 1"),
        ("Remove trocar", USER_TASK, "Process 1"),
        ("Check wire in long axis", USER_TASK, "Process 1"),
        ("Check wire in short axis", USER_TASK, "Process 1"),
        ("Check wire position", USER_TASK, "Process 1"),
        ("Widen pathway", USER_TASK, "Process 1"),
        ("Advance catheter", USER_TASK, "Process 1"),
        ("Remove guidewire", USER_TASK, "Process 1"),
        ("Check flow and reflow", USER_TASK, "Process 1"),
        ("Check catheter position", USER_TASK, "Process 1"),
        ("Vein identification method", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Blood return correct ?", EXCLUSIVE_GW, "Process 1"),
        ("Wire in good position ?", EXCLUSIVE_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "Prepare implements", ""),
        ("Prepare implements", "Hand washing", ""),
        ("Hand washing", "Get in sterile clothes", ""),
        ("Get in sterile clothes", "Clean puncture area", ""),
        ("Clean puncture area", "Drap puncture zone", ""),
        ("Drap puncture zone", "Ultrasound configuration", ""),
        ("Ultrasound configuration", "Gel in probe", ""),
        ("Gel in probe", "Cover probe", ""),
        ("Cover probe", "Put sterile gel", ""),
        ("Put sterile gel", "Position probe", ""),
        ("Position probe", "Position patient", ""),
        ("Position patient", "Vein identification method", ""),
        ("Vein identification method", "Doppler identification", ""),
        ("Vein identification method", "Anatomic identification", ""),
        ("Vein identification method", "Compression identification", ""),
        ("Doppler identification", "ExclusiveGateway_2", ""),
        ("Anatomic identification", "ExclusiveGateway_2", ""),
        ("Compression identification", "ExclusiveGateway_2", ""),
        ("Anesthetize patient", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "Puncture patient", ""),
        ("Puncture patient", "Check blood return", ""),
        ("ExclusiveGateway_2", "Anesthetize patient", ""),
        ("Drop probe", "Remove syringe", ""),
        ("Remove syringe", "Guidewire install", ""),
        ("Guidewire install", "Remove trocar", ""),
        ("Remove trocar", "ExclusiveGateway_4", ""),
        ("ExclusiveGateway_4", "Check wire in long axis", ""),
        ("ExclusiveGateway_4", "Check wire in short axis", ""),
        ("Check wire in long axis", "ExclusiveGateway_5", ""),
        ("Check wire in short axis", "ExclusiveGateway_5", ""),
        ("ExclusiveGateway_5", "Check wire position", ""),
        ("Check blood return", "Blood return correct ?", ""),
        ("Check wire position", "Wire in good position ?", ""),
        ("Blood return correct ?", "ExclusiveGateway_3", "No"),
        ("Wire in good position ?", "ExclusiveGateway_3", "No"),
        ("Blood return correct ?", "Drop probe", "Yes"),
        ("Wire in good position ?", "Widen pathway", "Yes"),
        ("Widen pathway", "Advance catheter", ""),
        ("Advance catheter", "Remove guidewire", ""),
        ("Remove guidewire", "Check flow and reflow", ""),
        ("Check flow and reflow", "Check catheter position", ""),
        ("Check catheter position", "EndEvent_1", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Prepare implements": 1,
        "Hand washing": 2,
        "Get in sterile clothes": 3,
        "Clean puncture area": 4,
        "Drap puncture zone": 5,
        "Ultrasound configuration": 6,
        "Gel in probe": 7,
        "Cover probe": 8,
        "Put sterile gel": 9,
        "Position probe": 10,
        "Position patient": 11,
        "Vein identification method": 12,
        "Doppler identification": 13,
        "Anatomic identification": 13,
        "Compression identification": 13,
        "ExclusiveGateway_2": 14,
        "Anesthetize patient": 15,
        "Puncture patient": 17,
        "Check blood return": 18,
        "Blood return correct ?": 19,
        "Drop probe": 20,
        "Remove syringe": 21,
        "Guidewire install": 22,
        "Remove trocar": 23,
        "ExclusiveGateway_4": 24,
        "Check wire in long axis": 25,
        "Check wire in short axis": 25,
        "ExclusiveGateway_5": 26,
        "Check wire position": 27,
        "Wire in good position ?": 28,
        "ExclusiveGateway_3": 29,
        "Widen pathway": 29,
        "Advance catheter": 30,
        "Remove guidewire": 31,
        "Check flow and reflow": 32,
        "Check catheter position": 33,
        "EndEvent_1": 34,
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
