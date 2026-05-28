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
        ("Run diagnostics/find problems", SERVICE_TASK, "Process 1"),
        ("Notify labor inspectorate", SERVICE_TASK, "Process 1"),
        ("Notify insurance", SERVICE_TASK, "Process 1"),
        ("Notify insurance about the death", SERVICE_TASK, "Process 1"),
        ("Schedule safety training", MANUAL_TASK, "Process 1"),
        ("Inform employer", MANUAL_TASK, "Process 1"),
        ("Stay informed about the person's condition", MANUAL_TASK, "Process 1"),
        ("Fix the problem", MANUAL_TASK, "Process 1"),
        ("Identify potential issues", MANUAL_TASK, "Process 1"),
        ("Inform relatives", MANUAL_TASK, "Process 1"),
        ("Fix the threat", MANUAL_TASK, "Process 1"),
        ("Type of event?", EXCLUSIVE_GW, "Process 1"),
        ("Death or serious injury?", EXCLUSIVE_GW, "Process 1"),
        ("Safety authorities informed?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Person insured?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("Is the person dead? (Death as a result of an accident)", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_10", EXCLUSIVE_GW, "Process 1"),
        ("Did the person die and was insured?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_12", EXCLUSIVE_GW, "Process 1"),
        ("Employee training reqired?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_14", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_15", EXCLUSIVE_GW, "Process 1"),
        ("More issues?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_17", EXCLUSIVE_GW, "Process 1"),
        ("More issues?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("Issue occurs", START, "Process 1"),
        ("Issue resolved", END, "Process 1"),
    ],

    "flows": [
        ("Issue occurs", "Inform employer", ""),
        ("Death or serious injury?", "ExclusiveGateway_5", "No"),
        ("Death or serious injury?", "Inform relatives", "Yes"),
        ("Notify labor inspectorate", "ExclusiveGateway_4", ""),
        ("Safety authorities informed?", "Notify labor inspectorate", "No"),
        ("Safety authorities informed?", "ExclusiveGateway_4", "Yes"),
        ("ParallelGateway_1", "Person insured?", ""),
        ("Notify insurance", "ExclusiveGateway_7", ""),
        ("ParallelGateway_1", "Safety authorities informed?", ""),
        ("ExclusiveGateway_4", "ParallelGateway_2", ""),
        ("ExclusiveGateway_7", "ParallelGateway_2", ""),
        ("Person insured?", "Notify insurance", "Yes"),
        ("Inform employer", "Type of event?", ""),
        ("ExclusiveGateway_8", "Issue resolved", ""),
        ("ExclusiveGateway_5", "ExclusiveGateway_8", ""),
        ("ParallelGateway_2", "Is the person dead? (Death as a result of an accident)", ""),
        ("ExclusiveGateway_10", "ExclusiveGateway_5", ""),
        ("Is the person dead? (Death as a result of an accident)", "ExclusiveGateway_10", "Yes"),
        ("Stay informed about the person's condition", "Did the person die and was insured?", ""),
        ("ExclusiveGateway_12", "ExclusiveGateway_10", ""),
        ("Notify insurance about the death", "ExclusiveGateway_12", ""),
        ("Did the person die and was insured?", "Notify insurance about the death", "Yes"),
        ("Schedule safety training", "ExclusiveGateway_14", ""),
        ("Employee training reqired?", "ExclusiveGateway_14", "No"),
        ("Employee training reqired?", "Schedule safety training", "Yes"),
        ("Type of event?", "Death or serious injury?", "Event that almost led to an accident"),
        ("ExclusiveGateway_14", "ExclusiveGateway_8", ""),
        ("Run diagnostics/find problems", "ExclusiveGateway_15", ""),
        ("ExclusiveGateway_15", "Fix the problem", ""),
        ("Fix the problem", "More issues?", ""),
        ("More issues?", "ExclusiveGateway_8", "No"),
        ("More issues?", "ExclusiveGateway_15", "Yes"),
        ("ExclusiveGateway_17", "Fix the threat", ""),
        ("Fix the threat", "More issues?", ""),
        ("More issues?", "ExclusiveGateway_17", "Yes"),
        ("Identify potential issues", "ExclusiveGateway_17", ""),
        ("Is the person dead? (Death as a result of an accident)", "Stay informed about the person's condition", "No"),
        ("Type of event?", "Employee training reqired?", "Defect in protective system"),
        ("Person insured?", "ExclusiveGateway_7", "No"),
        ("Type of event?", "Run diagnostics/find problems", "Accident at work"),
        ("Type of event?", "Identify potential issues", "Serious/imminent threat to safety"),
        ("Inform relatives", "ParallelGateway_1", ""),
        ("More issues?", "ExclusiveGateway_8", ""),
        ("Did the person die and was insured?", "ExclusiveGateway_12", "No"),
    ],

    "layout": {
        "Issue occurs": 0,
        "Inform employer": 1,
        "Type of event?": 2,
        "Death or serious injury?": 3,
        "Employee training reqired?": 3,
        "Run diagnostics/find problems": 3,
        "Identify potential issues": 3,
        "Inform relatives": 4,
        "Schedule safety training": 4,
        "ExclusiveGateway_14": 5,
        "ParallelGateway_1": 5,
        "Fix the problem": 5,
        "Fix the threat": 5,
        "Issue resolved": 6,
        "Person insured?": 6,
        "Safety authorities informed?": 6,
        "More issues?": 6,
        "ExclusiveGateway_15": 7,
        "ExclusiveGateway_17": 7,
        "ExclusiveGateway_8": 7,
        "Notify insurance": 7,
        "Notify labor inspectorate": 7,
        "ExclusiveGateway_7": 8,
        "ExclusiveGateway_4": 8,
        "ParallelGateway_2": 9,
        "Is the person dead? (Death as a result of an accident)": 10,
        "Stay informed about the person's condition": 11,
        "ExclusiveGateway_5": 12,
        "Did the person die and was insured?": 12,
        "Notify insurance about the death": 13,
        "ExclusiveGateway_12": 14,
        "ExclusiveGateway_10": 15,
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
