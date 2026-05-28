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
execfile(".modelio/5.4/macros/BPMN_Helpers.py")


CONFIG = {
    "name": "Process_1",

    "lanes": ["Process 1"],

    "elements": [
        ("Submit documents", USER_TASK, "Process 1"),
        ("Approve report", USER_TASK, "Process 1"),
        ("Archive report", USER_TASK, "Process 1"),
        ("Send notification", USER_TASK, "Process 1"),
        ("Launch detailed investigation", USER_TASK, "Process 1"),
        ("Close audit process", USER_TASK, "Process 1"),
        ("Gather necessary documents", USER_TASK, "Process 1"),
        ("Send report for revision", USER_TASK, "Process 1"),
        ("Compile audit report", USER_TASK, "Process 1"),
        ("Conduct interviews", USER_TASK, "Process 1"),
        ("Check regulatory updates", USER_TASK, "Process 1"),
        ("Update and resubmit report", USER_TASK, "Process 1"),
        ("Evaluate compliance risks", USER_TASK, "Process 1"),
        ("Evaluate financial risks", USER_TASK, "Process 1"),
        ("Review submission", USER_TASK, "Process 1"),
        ("Receive clarifications", USER_TASK, "Process 1"),
        ("Prepare financial statements", USER_TASK, "Process 1"),
        ("Complete risk assessment/mitigation", USER_TASK, "Process 1"),
        ("Perform site visits", USER_TASK, "Process 1"),
        ("Review report by audit director", USER_TASK, "Process 1"),
        ("Distribute final report", USER_TASK, "Process 1"),
        ("Conduct data analysis", USER_TASK, "Process 1"),
        ("Request clarifications of discrepancies", USER_TASK, "Process 1"),
        ("Evaluate operational risks", USER_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_2", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_6", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_8", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_3", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_4", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_5", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_6", PARALLEL_GW, "Process 1"),
        ("Start", START, "Process 1"),
        ("End", END, "Process 1"),
    ],

    "flows": [
        ("ExclusiveGateway_5", "ExclusiveGateway_8", ""),
        ("Approve report", "Distribute final report", ""),
        ("ExclusiveGateway_4", "ParallelGateway_1", ""),
        ("ParallelGateway_6", "Check regulatory updates", ""),
        ("Check regulatory updates", "ParallelGateway_2", ""),
        ("Request clarifications of discrepancies", "Receive clarifications", ""),
        ("Evaluate financial risks", "ParallelGateway_3", ""),
        ("Prepare financial statements", "ParallelGateway_2", ""),
        ("ExclusiveGateway_5", "Launch detailed investigation", ""),
        ("ParallelGateway_4", "ExclusiveGateway_7", ""),
        ("Launch detailed investigation", "ParallelGateway_4", ""),
        ("ParallelGateway_4", "Conduct interviews", ""),
        ("ParallelGateway_5", "ExclusiveGateway_8", ""),
        ("Evaluate operational risks", "ParallelGateway_3", ""),
        ("ExclusiveGateway_7", "Perform site visits", ""),
        ("ParallelGateway_6", "Prepare financial statements", ""),
        ("ParallelGateway_4", "Conduct data analysis", ""),
        ("Evaluate compliance risks", "ParallelGateway_3", ""),
        ("Receive clarifications", "ExclusiveGateway_4", ""),
        ("Start", "Send notification", ""),
        ("Gather necessary documents", "ParallelGateway_2", ""),
        ("ExclusiveGateway_1", "ParallelGateway_5", ""),
        ("ParallelGateway_6", "Gather necessary documents", ""),
        ("Conduct data analysis", "ParallelGateway_5", ""),
        ("ExclusiveGateway_7", "ExclusiveGateway_1", ""),
        ("Conduct interviews", "ParallelGateway_5", ""),
        ("ExclusiveGateway_3", "Approve report", ""),
        ("ExclusiveGateway_8", "Complete risk assessment/mitigation", ""),
        ("ParallelGateway_1", "Evaluate financial risks", ""),
        ("Send report for revision", "Update and resubmit report", ""),
        ("ParallelGateway_1", "Evaluate compliance risks", ""),
        ("ExclusiveGateway_6", "Request clarifications of discrepancies", ""),
        ("Send notification", "ParallelGateway_6", ""),
        ("ParallelGateway_1", "Evaluate operational risks", ""),
        ("Close audit process", "End", ""),
        ("ExclusiveGateway_6", "ExclusiveGateway_4", ""),
        ("ParallelGateway_2", "Submit documents", ""),
        ("Distribute final report", "Archive report", ""),
        ("ExclusiveGateway_3", "Send report for revision", ""),
        ("Perform site visits", "ExclusiveGateway_1", ""),
        ("Archive report", "Close audit process", ""),
        ("ExclusiveGateway_2", "Review report by audit director", ""),
        ("Review submission", "ExclusiveGateway_6", ""),
        ("Complete risk assessment/mitigation", "Compile audit report", ""),
        ("ParallelGateway_3", "ExclusiveGateway_5", ""),
        ("Review report by audit director", "ExclusiveGateway_3", ""),
        ("Submit documents", "Review submission", ""),
        ("Compile audit report", "ExclusiveGateway_2", ""),
        ("Update and resubmit report", "ExclusiveGateway_2", ""),
    ],

    "layout": {
        "Start": 0,
        "Send notification": 1,
        "ParallelGateway_6": 2,
        "Check regulatory updates": 3,
        "Prepare financial statements": 3,
        "Gather necessary documents": 3,
        "ParallelGateway_2": 4,
        "Submit documents": 5,
        "Review submission": 6,
        "ExclusiveGateway_6": 7,
        "Request clarifications of discrepancies": 8,
        "Receive clarifications": 9,
        "ParallelGateway_1": 9,
        "ExclusiveGateway_4": 10,
        "Evaluate financial risks": 10,
        "Evaluate compliance risks": 10,
        "Evaluate operational risks": 10,
        "ParallelGateway_3": 11,
        "ExclusiveGateway_5": 12,
        "Launch detailed investigation": 13,
        "Complete risk assessment/mitigation": 14,
        "ParallelGateway_4": 14,
        "Compile audit report": 15,
        "ExclusiveGateway_7": 15,
        "Conduct interviews": 15,
        "Conduct data analysis": 15,
        "Perform site visits": 16,
        "ExclusiveGateway_1": 17,
        "Review report by audit director": 17,
        "ParallelGateway_5": 18,
        "ExclusiveGateway_3": 18,
        "ExclusiveGateway_8": 19,
        "Approve report": 19,
        "Send report for revision": 19,
        "Distribute final report": 20,
        "Update and resubmit report": 20,
        "ExclusiveGateway_2": 21,
        "Archive report": 21,
        "Close audit process": 22,
        "End": 23,
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
