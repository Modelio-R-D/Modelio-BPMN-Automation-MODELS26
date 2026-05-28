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
        ("Check if passport is up to date", USER_TASK, "Process 1"),
        ("Prepare Documents for r-w-r card", USER_TASK, "Process 1"),
        ("Send documentation to relevant agency", SERVICE_TASK, "Process 1"),
        ("Rules engine automaticly checks if documentations fullfilles requirements", SERVICE_TASK, "Process 1"),
        ("Bank Systems creates bank account and sends E-Mail confirmation", SERVICE_TASK, "Process 1"),
        ("Check requirements and point for particularly highly qualified people", MANUAL_TASK, "Process 1"),
        ("Check requirements for independent key employees", MANUAL_TASK, "Process 1"),
        ("Check requirements and point for start-up founders", MANUAL_TASK, "Process 1"),
        ("Check requirements for Graduates of an Austrian higher education institution", MANUAL_TASK, "Process 1"),
        ("Check requirements and point for other key employees", MANUAL_TASK, "Process 1"),
        ("Check requirements and point for skilled workers in shortage occupations", MANUAL_TASK, "Process 1"),
        ("Request new passport", MANUAL_TASK, "Process 1"),
        ("Make passport photo", MANUAL_TASK, "Process 1"),
        ("Prepare birth certificate", MANUAL_TASK, "Process 1"),
        ("Search and find suited apartment", MANUAL_TASK, "Process 1"),
        ("Negotiate rent with landlord", MANUAL_TASK, "Process 1"),
        ("Sign contract", MANUAL_TASK, "Process 1"),
        ("Request Austrian health insurance coverage incl. documentation", MANUAL_TASK, "Process 1"),
        ("Gather documentation to prove financial indepence", MANUAL_TASK, "Process 1"),
        ("Application for a residence permit", MANUAL_TASK, "Process 1"),
        ("Request Bank Account on Bank website", MANUAL_TASK, "Process 1"),
        ("ExclusiveGateway_1", EXCLUSIVE_GW, "Process 1"),
        ("Fullfiles the requirements or point?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_3", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_4", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_5", EXCLUSIVE_GW, "Process 1"),
        ("Negotitation successful?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_7", EXCLUSIVE_GW, "Process 1"),
        ("Additional documentation needed?", EXCLUSIVE_GW, "Process 1"),
        ("ExclusiveGateway_9", EXCLUSIVE_GW, "Process 1"),
        ("Agency approves right to stay?", EXCLUSIVE_GW, "Process 1"),
        ("ParallelGateway_1", PARALLEL_GW, "Process 1"),
        ("ParallelGateway_2", PARALLEL_GW, "Process 1"),
        ("StartEvent_1", START, "Process 1"),
        ("EndEvent_1", END, "Process 1"),
    ],

    "flows": [
        ("StartEvent_1", "ExclusiveGateway_1", ""),
        ("ExclusiveGateway_1", "Check requirements and point for skilled workers in shortage occupations", ""),
        ("ExclusiveGateway_1", "Check requirements and point for particularly highly qualified people", ""),
        ("ExclusiveGateway_1", "Check requirements and point for other key employees", ""),
        ("ExclusiveGateway_1", "Check requirements and point for start-up founders", ""),
        ("Check requirements and point for skilled workers in shortage occupations", "Fullfiles the requirements or point?", ""),
        ("Check requirements and point for particularly highly qualified people", "Fullfiles the requirements or point?", ""),
        ("Check requirements and point for other key employees", "Fullfiles the requirements or point?", ""),
        ("Check requirements and point for start-up founders", "Fullfiles the requirements or point?", ""),
        ("Check requirements for independent key employees", "Fullfiles the requirements or point?", ""),
        ("Fullfiles the requirements or point?", "ExclusiveGateway_1", "No"),
        ("Check if passport is up to date", "ExclusiveGateway_3", ""),
        ("ExclusiveGateway_3", "ExclusiveGateway_4", "Yes"),
        ("Request new passport", "ExclusiveGateway_4", ""),
        ("Prepare Documents for r-w-r card", "ParallelGateway_1", ""),
        ("ParallelGateway_1", "Check if passport is up to date", ""),
        ("ParallelGateway_1", "Make passport photo", ""),
        ("ParallelGateway_1", "Prepare birth certificate", ""),
        ("Search and find suited apartment", "Negotiate rent with landlord", ""),
        ("ExclusiveGateway_5", "Search and find suited apartment", ""),
        ("ParallelGateway_1", "ExclusiveGateway_5", ""),
        ("Negotiate rent with landlord", "Negotitation successful?", ""),
        ("Negotitation successful?", "ExclusiveGateway_5", "No"),
        ("Negotitation successful?", "Sign contract", "Yes"),
        ("ParallelGateway_1", "Gather documentation to prove financial indepence", ""),
        ("ParallelGateway_1", "Application for a residence permit", ""),
        ("Make passport photo", "ParallelGateway_2", ""),
        ("ExclusiveGateway_4", "ParallelGateway_2", ""),
        ("Prepare birth certificate", "ParallelGateway_2", ""),
        ("Gather documentation to prove financial indepence", "ParallelGateway_2", ""),
        ("Application for a residence permit", "ParallelGateway_2", ""),
        ("Sign contract", "ParallelGateway_2", ""),
        ("ExclusiveGateway_7", "Prepare Documents for r-w-r card", ""),
        ("ExclusiveGateway_3", "Request new passport", "No"),
        ("ParallelGateway_1", "Request Austrian health insurance coverage incl. documentation", ""),
        ("Request Austrian health insurance coverage incl. documentation", "ParallelGateway_2", ""),
        ("Send documentation to relevant agency", "Rules engine automaticly checks if documentations fullfilles requirements", ""),
        ("Rules engine automaticly checks if documentations fullfilles requirements", "Additional documentation needed?", ""),
        ("Bank Systems creates bank account and sends E-Mail confirmation", "ExclusiveGateway_9", ""),
        ("ExclusiveGateway_9", "EndEvent_1", ""),
        ("ParallelGateway_2", "Send documentation to relevant agency", ""),
        ("Additional documentation needed?", "Agency approves right to stay?", "No"),
        ("Additional documentation needed?", "ExclusiveGateway_7", "Yes"),
        ("Request Bank Account on Bank website", "Bank Systems creates bank account and sends E-Mail confirmation", ""),
        ("Agency approves right to stay?", "Request Bank Account on Bank website", "Yes"),
        ("Agency approves right to stay?", "ExclusiveGateway_9", "No"),
        ("Fullfiles the requirements or point?", "ExclusiveGateway_7", "Yes"),
        ("ExclusiveGateway_1", "Check requirements for independent key employees", ""),
        ("ExclusiveGateway_1", "Check requirements for Graduates of an Austrian higher education institution", ""),
        ("Check requirements for Graduates of an Austrian higher education institution", "Fullfiles the requirements or point?", ""),
    ],

    "layout": {
        "StartEvent_1": 0,
        "Check requirements and point for skilled workers in shortage occupations": 2,
        "Check requirements and point for particularly highly qualified people": 2,
        "Check requirements and point for other key employees": 2,
        "Check requirements and point for start-up founders": 2,
        "Check requirements for independent key employees": 2,
        "Check requirements for Graduates of an Austrian higher education institution": 2,
        "Fullfiles the requirements or point?": 3,
        "ExclusiveGateway_1": 4,
        "Prepare Documents for r-w-r card": 5,
        "ParallelGateway_1": 6,
        "Check if passport is up to date": 7,
        "Make passport photo": 7,
        "Prepare birth certificate": 7,
        "Gather documentation to prove financial indepence": 7,
        "Application for a residence permit": 7,
        "Request Austrian health insurance coverage incl. documentation": 7,
        "ExclusiveGateway_3": 8,
        "Search and find suited apartment": 8,
        "Request new passport": 9,
        "Send documentation to relevant agency": 9,
        "Negotiate rent with landlord": 9,
        "ExclusiveGateway_4": 10,
        "Rules engine automaticly checks if documentations fullfilles requirements": 10,
        "Negotitation successful?": 10,
        "ExclusiveGateway_5": 11,
        "Additional documentation needed?": 11,
        "Sign contract": 11,
        "ExclusiveGateway_7": 12,
        "ParallelGateway_2": 12,
        "Agency approves right to stay?": 12,
        "Request Bank Account on Bank website": 13,
        "Bank Systems creates bank account and sends E-Mail confirmation": 14,
        "EndEvent_1": 14,
        "ExclusiveGateway_9": 15,
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
