#
# USI_Course_Registration.py
#
# Description: Process for registering for a USI (University Sports Institute) course
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "USI_Course_Registration",
    
    "lanes": ["Applicant", "USI System", "Twitter"],
    
    "elements": [
        # Start
        ("Start",                      START,        "Applicant"),
        
        # Course Selection
        ("Select Course",              USER_TASK,    "Applicant"),
        ("Check Availability",         SERVICE_TASK, "USI System"),
        ("Slots Available?",           EXCLUSIVE_GW, "USI System"),
        ("Display Courses and Dates",  SERVICE_TASK, "USI System"),
        ("Choose Course and Date",     USER_TASK,    "Applicant"),
        
        # Account Check
        ("Has Account?",               EXCLUSIVE_GW, "USI System"),
        
        # No Account Path
        ("Registered at University?",  EXCLUSIVE_GW, "USI System"),
        ("Register Account",           USER_TASK,    "Applicant"),
        ("Request Activation",         USER_TASK,    "Applicant"),
        ("Wait for Response",          INTERMEDIATE_CATCH, "Applicant"),
        
        # Merge accounts path
        ("Account Ready",              EXCLUSIVE_GW, "Applicant"),
        
        # Login and Complete
        ("Log Into Account",           USER_TASK,    "Applicant"),
        
        # Parallel: Tweet and Registration
        ("Split",                      PARALLEL_GW,  "Applicant"),
        ("Tweet to Friends",           SEND_TASK,    "Twitter"),
        ("Complete Registration",      USER_TASK,    "Applicant"),
        ("Provide Payment Info",       USER_TASK,    "Applicant"),
        ("Join",                       PARALLEL_GW,  "Applicant"),
        
        # End
        ("Receive Course Ticket",      RECEIVE_TASK, "Applicant"),
        ("End",                        END,          "Applicant"),
    ],
    
    "flows": [
        # Course Selection
        ("Start",                     "Select Course",             ""),
        ("Select Course",             "Check Availability",        ""),
        ("Check Availability",        "Slots Available?",          ""),
        ("Slots Available?",          "Display Courses and Dates", "Yes"),
        ("Slots Available?",          "End",                       "No"),
        ("Display Courses and Dates", "Choose Course and Date",    ""),
        
        # Account Check
        ("Choose Course and Date",    "Has Account?",              ""),
        ("Has Account?",              "Log Into Account",          "Yes"),
        ("Has Account?",              "Registered at University?", "No"),
        
        # University Registration Path
        ("Registered at University?", "Register Account",          "Yes"),
        ("Registered at University?", "Request Activation",        "No"),
        ("Request Activation",        "Wait for Response",         ""),
        ("Wait for Response",         "Account Ready",             ""),
        ("Register Account",          "Account Ready",             ""),
        
        # Account Ready merges to Login
        ("Account Ready",             "Log Into Account",          ""),
        
        # Parallel activities
        ("Log Into Account",          "Split",                     ""),
        ("Split",                     "Tweet to Friends",          ""),
        ("Split",                     "Complete Registration",     ""),
        ("Tweet to Friends",          "Join",                      ""),
        ("Complete Registration",     "Provide Payment Info",      ""),
        ("Provide Payment Info",      "Join",                      ""),
        
        # End
        ("Join",                      "Receive Course Ticket",     ""),
        ("Receive Course Ticket",     "End",                       ""),
    ],
    
    "layout": {
        "Start":                      0,
        "Select Course":              1,
        "Check Availability":         2,
        "Slots Available?":           3,
        "Display Courses and Dates":  4,
        "Choose Course and Date":     5,
        "Has Account?":               6,
        "Log Into Account":           7,
        "Registered at University?":  7,    # Auto-stacked below Has Account? path
        "Register Account":           8,    # Auto-stacked with Request Activation
        "Request Activation":         8,
        "Wait for Response":          9,
        "Account Ready":              10,
        "Split":                      11,
        "Tweet to Friends":           12,
        "Complete Registration":      12,   # Auto-stacked with Tweet
        "Provide Payment Info":       13,
        "Join":                       14,
        "Receive Course Ticket":      15,
        "End":                        16,
    },
    
    # Data Objects
    "data_objects": [
        ("Course Ticket", "Applicant", 15),
    ],
    
    "data_associations": [
        ("Receive Course Ticket", "Course Ticket"),
    ],
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
