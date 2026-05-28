#
# MarketingCampaignProcess.py
#
# Description: Marketing Campaign Management Process - from objective definition 
#              through campaign execution, lead collection, and performance analysis
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "MarketingCampaign",
    
    "lanes": ["Marketing Team", "Sales Team"],
    
    "elements": [
        # Start
        ("Start", START, "Marketing Team"),
        
        # Marketing Team Activities
        ("Define Campaign Objectives", USER_TASK, "Marketing Team"),
        ("Create Content", USER_TASK, "Marketing Team"),
        ("Design Visuals", USER_TASK, "Marketing Team"),
        ("Select Channels", USER_TASK, "Marketing Team"),
        ("Launch Campaign", SERVICE_TASK, "Marketing Team"),
        ("Track Performance", SERVICE_TASK, "Marketing Team"),
        ("Analyze Performance", USER_TASK, "Marketing Team"),
        
        # Sales Team Activities
        ("Collect Leads in CRM", SERVICE_TASK, "Sales Team"),
        ("Follow Up Leads", USER_TASK, "Sales Team"),
        
        # End
        ("End", END, "Marketing Team"),
    ],
    
    "flows": [
        ("Start", "Define Campaign Objectives", ""),
        ("Define Campaign Objectives", "Create Content", ""),
        ("Create Content", "Design Visuals", ""),
        ("Design Visuals", "Select Channels", ""),
        ("Select Channels", "Launch Campaign", ""),
        ("Launch Campaign", "Track Performance", ""),
        ("Track Performance", "Collect Leads in CRM", ""),
        ("Collect Leads in CRM", "Follow Up Leads", ""),
        ("Follow Up Leads", "Analyze Performance", ""),
        ("Analyze Performance", "End", ""),
    ],
    
    "data_objects": [
        ("Campaign Brief", "Marketing Team", 1),
        ("Content Assets", "Marketing Team", 3),
        ("Performance Metrics", "Marketing Team", 6),
        ("Lead Records", "Sales Team", 7),
    ],
    
    "data_associations": [
        ("Define Campaign Objectives", "Campaign Brief"),
        ("Campaign Brief", "Create Content"),
        ("Design Visuals", "Content Assets"),
        ("Content Assets", "Select Channels"),
        ("Track Performance", "Performance Metrics"),
        ("Performance Metrics", "Analyze Performance"),
        ("Collect Leads in CRM", "Lead Records"),
        ("Lead Records", "Follow Up Leads"),
    ],
    
    "layout": {
        "Start": 0,
        "Define Campaign Objectives": 1,
        "Create Content": 2,
        "Design Visuals": 3,
        "Select Channels": 4,
        "Launch Campaign": 5,
        "Track Performance": 6,
        "Collect Leads in CRM": 7,
        "Follow Up Leads": 8,
        "Analyze Performance": 9,
        "End": 10,
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
