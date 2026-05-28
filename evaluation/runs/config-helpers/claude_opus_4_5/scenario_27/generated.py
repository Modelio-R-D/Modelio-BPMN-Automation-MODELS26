#
# WorkAccidentProcess.py
#
# Description: Process for gathering information and reporting work accidents
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "WorkAccidentProcess",
    
    "lanes": [
        "Employee/Student",
        "Employer/Institution",
        "Insurance Provider"
    ],
    
    "elements": [
        # Employee/Student Lane
        ("Accident Occurs",           START,         "Employee/Student"),
        ("Assess Severity",           USER_TASK,     "Employee/Student"),
        ("Work Related?",             EXCLUSIVE_GW,  "Employee/Student"),
        ("Classify Accident Type",    USER_TASK,     "Employee/Student"),
        ("Notify Employer",           USER_TASK,     "Employee/Student"),
        ("Seek Medical Attention",    USER_TASK,     "Employee/Student"),
        ("Not Work Accident",         END,           "Employee/Student"),
        
        # Employer/Institution Lane
        ("Receive Notification",      USER_TASK,     "Employer/Institution"),
        ("Assess Incident",           USER_TASK,     "Employer/Institution"),
        ("Fatality or Serious?",      EXCLUSIVE_GW,  "Employer/Institution"),
        ("Report to Labour Inspect",  SEND_TASK,     "Employer/Institution"),
        ("Incapacity 3+ Days?",       EXCLUSIVE_GW,  "Employer/Institution"),
        ("Prepare Report",            USER_TASK,     "Employer/Institution"),
        ("Submit to Insurance",       SEND_TASK,     "Employer/Institution"),
        ("Document Internally",       USER_TASK,     "Employer/Institution"),
        ("Join Reports",              PARALLEL_GW,   "Employer/Institution"),
        
        # Insurance Provider Lane
        ("Receive Report",            RECEIVE_TASK,  "Insurance Provider"),
        ("Validate Claim",            SERVICE_TASK,  "Insurance Provider"),
        ("Claim Valid?",              EXCLUSIVE_GW,  "Insurance Provider"),
        ("Process Claim",             SERVICE_TASK,  "Insurance Provider"),
        ("Request More Info",         SEND_TASK,     "Insurance Provider"),
        ("Reject Claim",              SERVICE_TASK,  "Insurance Provider"),
        ("Notify Outcome",            SEND_TASK,     "Insurance Provider"),
        ("End Process",               END,           "Insurance Provider"),
    ],
    
    "data_objects": [
        ("Accident Details",    "Employee/Student",     2),
        ("Medical Records",     "Employee/Student",     5),
        ("Incident Report",     "Employer/Institution", 7),
        ("Insurance Claim",     "Insurance Provider",   9),
    ],
    
    "data_associations": [
        ("Classify Accident Type", "Accident Details"),
        ("Accident Details",       "Notify Employer"),
        ("Seek Medical Attention", "Medical Records"),
        ("Prepare Report",         "Incident Report"),
        ("Incident Report",        "Submit to Insurance"),
        ("Receive Report",         "Insurance Claim"),
        ("Insurance Claim",        "Validate Claim"),
    ],
    
    "flows": [
        # Employee flow
        ("Accident Occurs",         "Assess Severity",        ""),
        ("Assess Severity",         "Work Related?",          ""),
        ("Work Related?",           "Classify Accident Type", "Yes"),
        ("Work Related?",           "Not Work Accident",      "No"),
        ("Classify Accident Type",  "Notify Employer",        ""),
        ("Notify Employer",         "Seek Medical Attention", ""),
        
        # Cross-lane: Employee to Employer
        ("Notify Employer",         "Receive Notification",   ""),
        
        # Employer flow
        ("Receive Notification",    "Assess Incident",        ""),
        ("Assess Incident",         "Fatality or Serious?",   ""),
        ("Fatality or Serious?",    "Report to Labour Inspect", "Yes"),
        ("Fatality or Serious?",    "Incapacity 3+ Days?",    "No"),
        ("Report to Labour Inspect","Incapacity 3+ Days?",    ""),
        ("Incapacity 3+ Days?",     "Prepare Report",         "Yes"),
        ("Incapacity 3+ Days?",     "Document Internally",    "No"),
        ("Prepare Report",          "Submit to Insurance",    ""),
        ("Submit to Insurance",     "Join Reports",           ""),
        ("Document Internally",     "Join Reports",           ""),
        
        # Cross-lane: Employer to Insurance
        ("Submit to Insurance",     "Receive Report",         ""),
        
        # Insurance flow
        ("Receive Report",          "Validate Claim",         ""),
        ("Validate Claim",          "Claim Valid?",           ""),
        ("Claim Valid?",            "Process Claim",          "Yes"),
        ("Claim Valid?",            "Request More Info",      "Incomplete"),
        ("Claim Valid?",            "Reject Claim",           "Invalid"),
        ("Process Claim",           "Notify Outcome",         ""),
        ("Request More Info",       "Receive Report",         ""),
        ("Reject Claim",            "Notify Outcome",         ""),
        ("Notify Outcome",          "End Process",            ""),
    ],
    
    "layout": {
        # Employee/Student Lane (Row 1)
        "Accident Occurs":          0,
        "Assess Severity":          1,
        "Work Related?":            2,
        "Classify Accident Type":   3,
        "Notify Employer":          4,
        "Seek Medical Attention":   5,
        "Not Work Accident":        3,    # Auto-stacked below Work Related gateway path
        
        # Employer/Institution Lane (Row 2)
        "Receive Notification":     4,
        "Assess Incident":          5,
        "Fatality or Serious?":     6,
        "Report to Labour Inspect": 7,
        "Incapacity 3+ Days?":      8,
        "Prepare Report":           9,
        "Submit to Insurance":      10,
        "Document Internally":      9,    # Auto-stacked with Prepare Report
        "Join Reports":             11,
        
        # Insurance Provider Lane (Row 3)
        "Receive Report":           10,
        "Validate Claim":           11,
        "Claim Valid?":             12,
        "Process Claim":            13,
        "Request More Info":        13,   # Auto-stacked with Process Claim
        "Reject Claim":             13,   # Auto-stacked with above
        "Notify Outcome":           14,
        "End Process":              15,
    },
    
    "SPACING": 130,
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
