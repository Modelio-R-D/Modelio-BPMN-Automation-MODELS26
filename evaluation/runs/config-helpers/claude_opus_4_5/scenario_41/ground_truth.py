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
        ("Turn on bluetooth", USER_TASK, "Process 1"),
        ("Enter type of Machine", USER_TASK, "Process 1"),
        ("Enter serial number of machine", USER_TASK, "Process 1"),
        ("Run 'Inspect-App'", USER_TASK, "Process 1"),
        ("Check the fill capacity", USER_TASK, "Process 1"),
        ("Leave short Feedback", USER_TASK, "Process 1"),
        ("Press 'Produce' button", USER_TASK, "Process 1"),
        ("Press button 'Abort process'", USER_TASK, "Process 1"),
        ("Connecting to device", SERVICE_TASK, "Process 1"),
        ("Save Answers", SERVICE_TASK, "Process 1"),
        ("Auto collect values", SERVICE_TASK, "Process 1"),
        ("Show data", SERVICE_TASK, "Process 1"),
        ("Present results", SERVICE_TASK, "Process 1"),
        ("Connected?", EXCLUSIVE_GW, "Process 1"),
        ("Is the fill level in the bootle ok?", EXCLUSIVE_GW, "Process 1"),
        ("Is the cap position straight?", EXCLUSIVE_GW, "Process 1"),
        ("Are the right bottles in the pack?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("Enter type of Machine", "Enter serial number of machine", ""),
        ("Enter serial number of machine", "Connecting to device", ""),
        ("StartEvent_1", "Turn on bluetooth", ""),
        ("Turn on bluetooth", "Run 'Inspect-App'", ""),
        ("Run 'Inspect-App'", "Enter type of Machine", ""),
        ("Connecting to device", "Connected?", ""),
        ("Connected?", "Check the fill capacity", "yes"),
        ("Check the fill capacity", "Is the fill level in the bootle ok?", ""),
        ("Save Answers", "Press 'Produce' button", ""),
        ("Press 'Produce' button", "Are the right bottles in the pack?", ""),
        ("Press button 'Abort process'", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Auto collect values", ""),
        ("ParallelGateway_1", "Show data", ""),
        ("Show data", "ParallelGateway_2", ""),
        ("Auto collect values", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Present results", ""),
        ("Present results", "EndEvent_1", ""),
        ("Connected?", "Run 'Inspect-App'", "no"),
        ("Is the cap position straight?", "Leave short Feedback", "no"),
        ("Are the right bottles in the pack?", "Press button 'Abort process'", "no"),
        ("Is the fill level in the bootle ok?", "Leave short Feedback", "no"),
        ("Leave short Feedback", "Press button 'Abort process'", ""),
        ("Is the fill level in the bootle ok?", "Is the cap position straight?", "yes"),
        ("Is the cap position straight?", "Save Answers", "yes"),
        ("Are the right bottles in the pack?", "Present results", "yes"),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Turn on bluetooth": 1,
        "Enter type of Machine": 3,
        "Enter serial number of machine": 4,
        "Connecting to device": 5,
        "Connected?": 6,
        "Run 'Inspect-App'": 7,
        "Check the fill capacity": 7,
        "Is the fill level in the bootle ok?": 8,
        "Is the cap position straight?": 9,
        "Leave short Feedback": 10,
        "Save Answers": 10,
        "ParallelGateway_1": 11,
        "Press 'Produce' button": 11,
        "Auto collect values": 12,
        "Show data": 12,
        "Are the right bottles in the pack?": 12,
        "Press button 'Abort process'": 13,
        "ParallelGateway_2": 13,
        "Present results": 14,
        "EndEvent_1": 15,
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
