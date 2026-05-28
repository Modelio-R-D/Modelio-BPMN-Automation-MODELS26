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
        ("Stop the machine", SERVICE_TASK, "Process 1"),
        ("Send email to an engineer", SERVICE_TASK, "Process 1"),
        ("Get availability data", SERVICE_TASK, "Process 1"),
        ("Get quality data", SERVICE_TASK, "Process 1"),
        ("Get performance data", SERVICE_TASK, "Process 1"),
        ("Calculate OEE", SERVICE_TASK, "Process 1"),
        ("Continue measuring", MANUAL_TASK, "Process 1"),
        ("Repair the issue", MANUAL_TASK, "Process 1"),
        ("Restart the machine", MANUAL_TASK, "Process 1"),
        ("Disconnect the machine", MANUAL_TASK, "Process 1"),
        ("OEE below 50%?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("Machine worth repairing?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("Remaining issues?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("OEE data required", START, "Process 1"),
        ("Machine operating normally / Machine disconnected", END, "Process 1"),
    ],

    "flows": [
        ("ParallelGateway_1", "Get quality data", ""),
        ("ParallelGateway_1", "Get availability data", ""),
        ("ParallelGateway_1", "Get performance data", ""),
        ("Get quality data", "ParallelGateway_2", ""),
        ("Get availability data", "ParallelGateway_2", ""),
        ("Get performance data", "ParallelGateway_2", ""),
        ("ParallelGateway_2", "Calculate OEE", ""),
        ("OEE below 50%?", "Stop the machine", "Yes"),
        ("Stop the machine", "Send email to an engineer", ""),
        ("OEE data required", "ParallelGateway_1", ""),
        ("Send email to an engineer", "Machine worth repairing?", ""),
        ("Repair the issue", "Remaining issues?", ""),
        ("Restart the machine", "Continue measuring", ""),
        ("ExclusiveGateway_2", "Machine operating normally / Machine disconnected", ""),
        ("Calculate OEE", "OEE below 50%?", ""),
        ("Machine worth repairing?", "Disconnect the machine", "No"),
        ("ExclusiveGateway_4", "ExclusiveGateway_2", ""),
        ("Disconnect the machine", "ExclusiveGateway_4", ""),
        ("Continue measuring", "ExclusiveGateway_4", ""),
        ("Machine worth repairing?", "ExclusiveGateway_6", "Yes"),
        ("Remaining issues?", "Restart the machine", "No"),
        ("ExclusiveGateway_6", "Repair the issue", ""),
        ("Remaining issues?", "ExclusiveGateway_6", "Yes"),
        ("OEE below 50%?", "ExclusiveGateway_2", "No"),
    ],

    "layout": {
        "OEE data required": 0,
        "ParallelGateway_1": 1,
        "Get quality data": 2,
        "Get availability data": 2,
        "Get performance data": 2,
        "ParallelGateway_2": 3,
        "Calculate OEE": 4,
        "OEE below 50%?": 5,
        "Stop the machine": 6,
        "Send email to an engineer": 7,
        "Machine operating normally / Machine disconnected": 7,
        "Machine worth repairing?": 8,
        "Disconnect the machine": 9,
        "Repair the issue": 10,
        "ExclusiveGateway_2": 11,
        "Remaining issues?": 11,
        "ExclusiveGateway_6": 12,
        "Restart the machine": 12,
        "Continue measuring": 13,
        "ExclusiveGateway_4": 14,
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
