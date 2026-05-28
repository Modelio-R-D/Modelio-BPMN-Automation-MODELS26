#
# HiringProcess.py
#
# Description: End-to-end hiring process from job posting to employee onboarding
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "HiringProcess",
    
    "lanes": ["Department", "HR", "Hiring Manager", "New Hire"],
    
    "elements": [
        # Department lane
        ("Identify Hiring Need",     USER_TASK,     "Department"),
        ("Start",                    START,         "Department"),
        
        # HR lane
        ("Create Job Description",   USER_TASK,     "HR"),
        ("Post on Job Boards",       USER_TASK,     "HR"),
        ("Collect Resumes",          USER_TASK,     "HR"),
        ("Screen Resumes",           USER_TASK,     "HR"),
        ("Conduct Phone Interviews", USER_TASK,     "HR"),
        ("Prepare Offer",            USER_TASK,     "HR"),
        ("Extend Offer",             SEND_TASK,     "HR"),
        ("Negotiate Salary",         USER_TASK,     "HR"),
        ("Prepare Onboarding",       USER_TASK,     "HR"),
        ("Conduct Orientation",      USER_TASK,     "HR"),
        ("Arrange Training",         USER_TASK,     "HR"),
        ("End",                      END,           "HR"),
        
        # Hiring Manager lane
        ("Interview Preference?",    EXCLUSIVE_GW,  "Hiring Manager"),
        ("In-Person Interview",      USER_TASK,     "Hiring Manager"),
        ("Virtual Interview",        USER_TASK,     "Hiring Manager"),
        ("Evaluate Candidates",      USER_TASK,     "Hiring Manager"),
        ("Select Candidate?",        EXCLUSIVE_GW,  "Hiring Manager"),
        ("Confirm Integration",      USER_TASK,     "Hiring Manager"),
        
        # New Hire lane
        ("Review Offer",             USER_TASK,     "New Hire"),
        ("Offer Accepted?",          EXCLUSIVE_GW,  "New Hire"),
        ("Complete Paperwork",       USER_TASK,     "New Hire"),
        ("Attend Orientation",       USER_TASK,     "New Hire"),
        ("Complete Training",        USER_TASK,     "New Hire"),
    ],
    
    "flows": [
        # Initial flow
        ("Start",                    "Identify Hiring Need",     ""),
        ("Identify Hiring Need",     "Create Job Description",   ""),
        ("Create Job Description",   "Post on Job Boards",       ""),
        ("Post on Job Boards",       "Collect Resumes",          ""),
        ("Collect Resumes",          "Screen Resumes",           ""),
        ("Screen Resumes",           "Conduct Phone Interviews", ""),
        ("Conduct Phone Interviews", "Interview Preference?",    ""),
        
        # Interview type split
        ("Interview Preference?",    "In-Person Interview",      "In-Person"),
        ("Interview Preference?",    "Virtual Interview",        "Virtual"),
        ("In-Person Interview",      "Evaluate Candidates",      ""),
        ("Virtual Interview",        "Evaluate Candidates",      ""),
        
        # Candidate selection
        ("Evaluate Candidates",      "Select Candidate?",        ""),
        ("Select Candidate?",        "Conduct Phone Interviews", "No - Continue Search"),
        ("Select Candidate?",        "Prepare Offer",            "Yes"),
        
        # Offer process
        ("Prepare Offer",            "Extend Offer",             ""),
        ("Extend Offer",             "Review Offer",             ""),
        ("Review Offer",             "Offer Accepted?",          ""),
        ("Offer Accepted?",          "Negotiate Salary",         "Negotiate"),
        ("Negotiate Salary",         "Extend Offer",             ""),
        ("Offer Accepted?",          "Prepare Onboarding",       "Accepted"),
        
        # Onboarding process
        ("Prepare Onboarding",       "Complete Paperwork",       ""),
        ("Complete Paperwork",       "Conduct Orientation",      ""),
        ("Conduct Orientation",      "Attend Orientation",       ""),
        ("Attend Orientation",       "Arrange Training",         ""),
        ("Arrange Training",         "Complete Training",        ""),
        ("Complete Training",        "Confirm Integration",      ""),
        ("Confirm Integration",      "End",                      ""),
    ],
    
    "layout": {
        # Column 0
        "Start":                     0,
        
        # Column 1
        "Identify Hiring Need":      1,
        
        # Column 2
        "Create Job Description":    2,
        
        # Column 3
        "Post on Job Boards":        3,
        
        # Column 4
        "Collect Resumes":           4,
        
        # Column 5
        "Screen Resumes":            5,
        
        # Column 6
        "Conduct Phone Interviews":  6,
        
        # Column 7
        "Interview Preference?":     7,
        
        # Column 8 - Interview types auto-stacked
        "In-Person Interview":       8,
        "Virtual Interview":         8,
        
        # Column 9
        "Evaluate Candidates":       9,
        
        # Column 10
        "Select Candidate?":         10,
        
        # Column 11
        "Prepare Offer":             11,
        
        # Column 12
        "Extend Offer":              12,
        
        # Column 13
        "Review Offer":              13,
        
        # Column 14
        "Offer Accepted?":           14,
        
        # Column 15
        "Negotiate Salary":          15,
        "Prepare Onboarding":        15,
        
        # Column 16
        "Complete Paperwork":        16,
        
        # Column 17
        "Conduct Orientation":       17,
        
        # Column 18
        "Attend Orientation":        18,
        
        # Column 19
        "Arrange Training":          19,
        
        # Column 20
        "Complete Training":         20,
        
        # Column 21
        "Confirm Integration":       21,
        
        # Column 22
        "End":                       22,
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
