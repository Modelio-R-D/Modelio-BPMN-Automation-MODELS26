#
# Test_03_ParallelGateway.py
#
# Description:
#   Test Case 3: Process with parallel gateway (fork and join)
#   Tests: PARALLEL_GW, parallel execution paths
#
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Test03_ParallelGateway",
    
    "lanes": ["Worker"],
    
    "elements": [
        ("Start",          START,       "Worker"),
        ("Receive Order",  USER_TASK,   "Worker"),
        ("Fork",           PARALLEL_GW, "Worker"),
        ("Prepare Docs",   USER_TASK,   "Worker"),
        ("Prepare Goods",  USER_TASK,   "Worker"),
        ("Notify Customer", SERVICE_TASK, "Worker"),
        ("Join",           PARALLEL_GW, "Worker"),
        ("Ship Order",     USER_TASK,   "Worker"),
        ("End",            END,         "Worker"),
    ],
    
    "flows": [
        ("Start",          "Receive Order",   ""),
        ("Receive Order",  "Fork",            ""),
        ("Fork",           "Prepare Docs",    ""),
        ("Fork",           "Prepare Goods",   ""),
        ("Fork",           "Notify Customer", ""),
        ("Prepare Docs",   "Join",            ""),
        ("Prepare Goods",  "Join",            ""),
        ("Notify Customer", "Join",           ""),
        ("Join",           "Ship Order",      ""),
        ("Ship Order",     "End",             ""),
    ],
    
    "layout": {
        "Start":          0,
        "Receive Order":  1,
        "Fork":           2,
        "Prepare Docs":   3,
        "Prepare Goods":  3,
        "Notify Customer": 3,
        "Join":           4,
        "Ship Order":     5,
        "End":            6,
    },
}

if (selectedElements.size > 0):
    element = selectedElements.get(0)
    if (isinstance(element, Package)):
        createBPMNFromConfig(element, CONFIG)
    else:
        print "ERROR: Please select a Package."
else:
    print "ERROR: Please select a Package first."
