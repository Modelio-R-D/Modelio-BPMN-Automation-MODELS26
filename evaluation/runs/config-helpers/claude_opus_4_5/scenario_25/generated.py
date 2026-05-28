#
# FindAJob.py
#
# Description: Job search process from application to permanent employment
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "FindAJob",
    
    "lanes": ["Job Seeker", "Job Platform", "Company"],
    
    "elements": [
        # Job Seeker Lane
        ("Start",                   START,          "Job Seeker"),
        ("Submit Applications",     USER_TASK,      "Job Seeker"),
        ("Report Applications",     USER_TASK,      "Job Seeker"),
        ("Receive Job Offers",      RECEIVE_TASK,   "Job Seeker"),
        ("Review Offers",           USER_TASK,      "Job Seeker"),
        ("Interested?",             EXCLUSIVE_GW,   "Job Seeker"),
        ("Negotiate Interview",     USER_TASK,      "Job Seeker"),
        ("Attend Interview",        USER_TASK,      "Job Seeker"),
        ("Offer Received?",         EXCLUSIVE_GW,   "Job Seeker"),
        ("Start Probation",         USER_TASK,      "Job Seeker"),
        ("Complete Probation",      USER_TASK,      "Job Seeker"),
        ("Rate Company",            USER_TASK,      "Job Seeker"),
        ("Permanent?",              EXCLUSIVE_GW,   "Job Seeker"),
        ("Rating C or Less?",       EXCLUSIVE_GW,   "Job Seeker"),
        ("End Employed",            END,            "Job Seeker"),
        ("Continue No Report",      USER_TASK,      "Job Seeker"),
        
        # Job Platform Lane
        ("Process Reports",         SERVICE_TASK,   "Job Platform"),
        ("Match Job Offers",        SERVICE_TASK,   "Job Platform"),
        ("Send Offers",             SEND_TASK,      "Job Platform"),
        ("Store Seeker Rating",     SERVICE_TASK,   "Job Platform"),
        ("Store Company Rating",    SERVICE_TASK,   "Job Platform"),
        ("Wait 1 Year",             TIMER_CATCH,    "Job Platform"),
        ("Publish Review",          SERVICE_TASK,   "Job Platform"),
        
        # Company Lane
        ("Receive Application",     RECEIVE_TASK,   "Company"),
        ("Confirm Receipt",         SEND_TASK,      "Company"),
        ("Rate Application",        USER_TASK,      "Company"),
        ("Schedule Interview",      USER_TASK,      "Company"),
        ("Conduct Interview",       USER_TASK,      "Company"),
        ("Make Decision",           EXCLUSIVE_GW,   "Company"),
        ("Send Offer",              SEND_TASK,      "Company"),
        ("Reject Candidate",        SEND_TASK,      "Company"),
        ("Manage Probation",        USER_TASK,      "Company"),
        ("Rate Employee",           USER_TASK,      "Company"),
        ("Confirm Permanent",       SEND_TASK,      "Company"),
    ],
    
    "flows": [
        # Job Seeker flow
        ("Start",                 "Submit Applications",   ""),
        ("Submit Applications",   "Report Applications",   ""),
        ("Report Applications",   "Receive Job Offers",    ""),
        ("Receive Job Offers",    "Review Offers",         ""),
        ("Review Offers",         "Interested?",           ""),
        ("Interested?",           "Negotiate Interview",   "Yes"),
        ("Interested?",           "Receive Job Offers",    "No"),
        ("Negotiate Interview",   "Attend Interview",      ""),
        ("Attend Interview",      "Offer Received?",       ""),
        ("Offer Received?",       "Start Probation",       "Yes"),
        ("Offer Received?",       "Report Applications",   "No"),
        ("Start Probation",       "Complete Probation",    ""),
        ("Complete Probation",    "Rate Company",          ""),
        ("Rate Company",          "Permanent?",            ""),
        ("Permanent?",            "Rating C or Less?",     "Yes"),
        ("Permanent?",            "Report Applications",   "No"),
        ("Rating C or Less?",     "End Employed",          "No"),
        ("Rating C or Less?",     "Continue No Report",    "Yes"),
        ("Continue No Report",    "Receive Job Offers",    ""),
        
        # Job Platform flow
        ("Report Applications",   "Process Reports",       ""),
        ("Process Reports",       "Match Job Offers",      ""),
        ("Match Job Offers",      "Send Offers",           ""),
        ("Send Offers",           "Receive Job Offers",    ""),
        ("Rate Company",          "Store Company Rating",  ""),
        ("Store Company Rating",  "Wait 1 Year",           ""),
        ("Wait 1 Year",           "Publish Review",        ""),
        ("Rate Employee",         "Store Seeker Rating",   ""),
        
        # Company flow
        ("Submit Applications",   "Receive Application",   ""),
        ("Receive Application",   "Confirm Receipt",       ""),
        ("Confirm Receipt",       "Rate Application",      ""),
        ("Rate Application",      "Schedule Interview",    ""),
        ("Negotiate Interview",   "Schedule Interview",    ""),
        ("Schedule Interview",    "Conduct Interview",     ""),
        ("Conduct Interview",     "Make Decision",         ""),
        ("Make Decision",         "Send Offer",            "Accept"),
        ("Make Decision",         "Reject Candidate",      "Reject"),
        ("Send Offer",            "Offer Received?",       ""),
        ("Reject Candidate",      "Offer Received?",       ""),
        ("Start Probation",       "Manage Probation",      ""),
        ("Manage Probation",      "Rate Employee",         ""),
        ("Complete Probation",    "Confirm Permanent",     ""),
        ("Confirm Permanent",     "Permanent?",            ""),
    ],
    
    "data_objects": [
        ("Application Report",    "Job Seeker",    2),
        ("Job Offers List",       "Job Platform",  4),
        ("Application Record",    "Company",       1),
        ("Company Review",        "Job Seeker",    12),
        ("Employee Review",       "Company",       13),
    ],
    
    "data_associations": [
        ("Report Applications",   "Application Report"),
        ("Application Report",    "Process Reports"),
        ("Match Job Offers",      "Job Offers List"),
        ("Job Offers List",       "Send Offers"),
        ("Submit Applications",   "Application Record"),
        ("Application Record",    "Receive Application"),
        ("Rate Company",          "Company Review"),
        ("Company Review",        "Store Company Rating"),
        ("Rate Employee",         "Employee Review"),
        ("Employee Review",       "Store Seeker Rating"),
    ],
    
    "layout": {
        # Job Seeker Lane
        "Start":                  0,
        "Submit Applications":    1,
        "Report Applications":    2,
        "Receive Job Offers":     4,
        "Review Offers":          5,
        "Interested?":            6,
        "Negotiate Interview":    7,
        "Attend Interview":       8,
        "Offer Received?":        9,
        "Start Probation":        10,
        "Complete Probation":     11,
        "Rate Company":           12,
        "Permanent?":             13,
        "Rating C or Less?":      14,
        "End Employed":           15,
        "Continue No Report":     15,
        
        # Job Platform Lane
        "Process Reports":        2,
        "Match Job Offers":       3,
        "Send Offers":            4,
        "Store Company Rating":   13,
        "Wait 1 Year":            14,
        "Publish Review":         15,
        "Store Seeker Rating":    14,
        
        # Company Lane
        "Receive Application":    1,
        "Confirm Receipt":        2,
        "Rate Application":       3,
        "Schedule Interview":     7,
        "Conduct Interview":      8,
        "Make Decision":          9,
        "Send Offer":             9,
        "Reject Candidate":       9,
        "Manage Probation":       11,
        "Rate Employee":          13,
        "Confirm Permanent":      12,
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
