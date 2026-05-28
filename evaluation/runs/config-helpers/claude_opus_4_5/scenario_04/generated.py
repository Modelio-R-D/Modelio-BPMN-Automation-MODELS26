#
# MarketingCampaignProcess.py
#
# Description: Marketing campaign lifecycle from objective definition through execution and analysis
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "MarketingCampaignProcess",
    
    "lanes": ["Marketing Team", "Sales Team"],
    
    "elements": [
        # Marketing Team activities
        ("Start", START, "Marketing Team"),
        ("Define Campaign Objectives", USER_TASK, "Marketing Team"),
        ("Identify Target Audience", USER_TASK, "Marketing Team"),
        ("Set Campaign Goals", USER_TASK, "Marketing Team"),
        ("Create Content", USER_TASK, "Marketing Team"),
        ("Design Visuals", USER_TASK, "Marketing Team"),
        ("Select Promotion Channels", USER_TASK, "Marketing Team"),
        ("Launch Campaign", USER_TASK, "Marketing Team"),
        ("Track Performance Metrics", SERVICE_TASK, "Marketing Team"),
        ("Campaign Active?", EXCLUSIVE_GW, "Marketing Team"),
        ("Continue Monitoring", SERVICE_TASK, "Marketing Team"),
        ("Analyze Campaign Results", USER_TASK, "Marketing Team"),
        ("Document Learnings", USER_TASK, "Marketing Team"),
        ("End", END, "Marketing Team"),
        
        # Sales Team activities
        ("Collect Leads in CRM", SERVICE_TASK, "Sales Team"),
        ("Follow Up with Leads", USER_TASK, "Sales Team"),
    ],
    
    "data_objects": [
        ("Campaign Brief", "Marketing Team", 1),
        ("Content Assets", "Marketing Team", 4),
        ("Performance Data", "Marketing Team", 8),
        ("Lead List", "Sales Team", 9),
        ("Campaign Report", "Marketing Team", 11),
    ],
    
    "data_associations": [
        ("Define Campaign Objectives", "Campaign Brief"),
        ("Campaign Brief", "Identify Target Audience"),
        ("Create Content", "Content Assets"),
        ("Content Assets", "Design Visuals"),
        ("Track Performance Metrics", "Performance Data"),
        ("Performance Data", "Collect Leads in CRM"),
        ("Collect Leads in CRM", "Lead List"),
        ("Lead List", "Follow Up with Leads"),
        ("Analyze Campaign Results", "Campaign Report"),
    ],
    
    "flows": [
        ("Start", "Define Campaign Objectives", ""),
        ("Define Campaign Objectives", "Identify Target Audience", ""),
        ("Identify Target Audience", "Set Campaign Goals", ""),
        ("Set Campaign Goals", "Create Content", ""),
        ("Create Content", "Design Visuals", ""),
        ("Design Visuals", "Select Promotion Channels", ""),
        ("Select Promotion Channels", "Launch Campaign", ""),
        ("Launch Campaign", "Track Performance Metrics", ""),
        ("Track Performance Metrics", "Collect Leads in CRM", ""),
        ("Collect Leads in CRM", "Follow Up with Leads", ""),
        ("Track Performance Metrics", "Campaign Active?", ""),
        ("Campaign Active?", "Continue Monitoring", "Yes"),
        ("Continue Monitoring", "Track Performance Metrics", ""),
        ("Campaign Active?", "Analyze Campaign Results", "No - Campaign Ended"),
        ("Analyze Campaign Results", "Document Learnings", ""),
        ("Document Learnings", "End", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Define Campaign Objectives": 1,
        "Identify Target Audience": 2,
        "Set Campaign Goals": 3,
        "Create Content": 4,
        "Design Visuals": 5,
        "Select Promotion Channels": 6,
        "Launch Campaign": 7,
        "Track Performance Metrics": 8,
        "Collect Leads in CRM": 9,
        "Follow Up with Leads": 10,
        "Campaign Active?": 9,
        "Continue Monitoring": 10,
        "Analyze Campaign Results": 11,
        "Document Learnings": 12,
        "End": 13,
    },
    
    "SPACING": 160,
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
