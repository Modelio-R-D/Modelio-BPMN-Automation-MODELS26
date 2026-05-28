#
# UniversityEnrollment.py
#
# Description: University enrollment system from application to graduation
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "UniversityEnrollment",
    
    "lanes": [
        "Applicant/Student",
        "Admissions Office",
        "Finance Department",
        "IT Department",
        "International Office",
        "Academic Services"
    ],
    
    "elements": [
        # Application Phase
        ("Start",                    START,          "Applicant/Student"),
        ("Submit Application",       USER_TASK,      "Applicant/Student"),
        ("Review Application",       USER_TASK,      "Admissions Office"),
        ("Documents Complete?",      EXCLUSIVE_GW,   "Admissions Office"),
        ("Notify Missing Docs",      SEND_TASK,      "Admissions Office"),
        ("Provide Missing Docs",     USER_TASK,      "Applicant/Student"),
        
        # Evaluation Phase - Parallel
        ("All Docs Received",        PARALLEL_GW,    "Admissions Office"),
        ("Evaluate Application",     USER_TASK,      "Admissions Office"),
        ("Process Fees",             SERVICE_TASK,   "Finance Department"),
        ("Sync After Eval",          PARALLEL_GW,    "Admissions Office"),
        
        # Decision Phase
        ("Accepted?",                EXCLUSIVE_GW,   "Admissions Office"),
        ("Send Rejection",           SEND_TASK,      "Admissions Office"),
        ("End Rejected",             END,            "Admissions Office"),
        ("Send Acceptance",          SEND_TASK,      "Admissions Office"),
        
        # Confirmation Phase
        ("Wait Confirmation",        TIMER_CATCH,    "Applicant/Student"),
        ("Confirmed?",               EXCLUSIVE_GW,   "Applicant/Student"),
        ("Cancel Application",       SERVICE_TASK,   "Admissions Office"),
        ("End Cancelled",            END,            "Admissions Office"),
        ("Confirm Enrollment",       USER_TASK,      "Applicant/Student"),
        
        # Onboarding - Parallel
        ("Start Onboarding",         PARALLEL_GW,    "Applicant/Student"),
        ("Send Orientation",         SEND_TASK,      "Admissions Office"),
        ("Setup Accounts",           SERVICE_TASK,   "IT Department"),
        ("International?",           EXCLUSIVE_GW,   "Applicant/Student"),
        ("Process Visa",             USER_TASK,      "International Office"),
        ("Skip Visa",                TASK,           "Applicant/Student"),
        ("Sync Onboarding",          PARALLEL_GW,    "Applicant/Student"),
        ("Get Student ID",           USER_TASK,      "Applicant/Student"),
        
        # Study Plan Sub-process
        ("Create Study Plan",        USER_TASK,      "Applicant/Student"),
        ("Meet Advisor",             USER_TASK,      "Academic Services"),
        ("Select Courses",           USER_TASK,      "Applicant/Student"),
        ("Conflicts?",               EXCLUSIVE_GW,   "Academic Services"),
        ("Resolve Conflicts",        USER_TASK,      "Academic Services"),
        ("Plan Complete",            TASK,           "Applicant/Student"),
        
        # Semester Cycle
        ("Attend Classes",           USER_TASK,      "Applicant/Student"),
        ("Add Drop Period",          TIMER_CATCH,    "Applicant/Student"),
        ("Modify Courses?",          EXCLUSIVE_GW,   "Applicant/Student"),
        ("Add Drop Courses",         USER_TASK,      "Applicant/Student"),
        ("Continue Semester",        TASK,           "Applicant/Student"),
        ("Post Grades",              SERVICE_TASK,   "Academic Services"),
        ("Review Grades",            USER_TASK,      "Applicant/Student"),
        
        # Appeals Process
        ("Has Grievance?",           EXCLUSIVE_GW,   "Applicant/Student"),
        ("Submit Appeal",            USER_TASK,      "Applicant/Student"),
        ("Meet Appeals Committee",   USER_TASK,      "Academic Services"),
        ("Await Decision",           RECEIVE_TASK,   "Applicant/Student"),
        ("No Appeal",                TASK,           "Applicant/Student"),
        ("Sync After Appeals",       EXCLUSIVE_GW,   "Applicant/Student"),
        
        # Graduation Check
        ("Graduate or Continue?",    EXCLUSIVE_GW,   "Applicant/Student"),
        ("End Graduated",            END,            "Applicant/Student"),
    ],
    
    "flows": [
        # Application Phase
        ("Start",                "Submit Application",    ""),
        ("Submit Application",   "Review Application",    ""),
        ("Review Application",   "Documents Complete?",   ""),
        ("Documents Complete?",  "Notify Missing Docs",   "No"),
        ("Notify Missing Docs",  "Provide Missing Docs",  ""),
        ("Provide Missing Docs", "Review Application",    ""),
        ("Documents Complete?",  "All Docs Received",     "Yes"),
        
        # Parallel Evaluation
        ("All Docs Received",    "Evaluate Application",  ""),
        ("All Docs Received",    "Process Fees",          ""),
        ("Evaluate Application", "Sync After Eval",       ""),
        ("Process Fees",         "Sync After Eval",       ""),
        ("Sync After Eval",      "Accepted?",             ""),
        
        # Decision
        ("Accepted?",            "Send Rejection",        "No"),
        ("Send Rejection",       "End Rejected",          ""),
        ("Accepted?",            "Send Acceptance",       "Yes"),
        
        # Confirmation
        ("Send Acceptance",      "Wait Confirmation",     ""),
        ("Wait Confirmation",    "Confirmed?",            ""),
        ("Confirmed?",           "Cancel Application",    "Timeout"),
        ("Cancel Application",   "End Cancelled",         ""),
        ("Confirmed?",           "Confirm Enrollment",    "Yes"),
        
        # Onboarding
        ("Confirm Enrollment",   "Start Onboarding",      ""),
        ("Start Onboarding",     "Send Orientation",      ""),
        ("Start Onboarding",     "Setup Accounts",        ""),
        ("Start Onboarding",     "International?",        ""),
        ("International?",       "Process Visa",          "Yes"),
        ("International?",       "Skip Visa",             "No"),
        ("Send Orientation",     "Sync Onboarding",       ""),
        ("Setup Accounts",       "Sync Onboarding",       ""),
        ("Process Visa",         "Sync Onboarding",       ""),
        ("Skip Visa",            "Sync Onboarding",       ""),
        ("Sync Onboarding",      "Get Student ID",        ""),
        
        # Study Plan
        ("Get Student ID",       "Create Study Plan",     ""),
        ("Create Study Plan",    "Meet Advisor",          ""),
        ("Meet Advisor",         "Select Courses",        ""),
        ("Select Courses",       "Conflicts?",            ""),
        ("Conflicts?",           "Resolve Conflicts",     "Yes"),
        ("Resolve Conflicts",    "Select Courses",        ""),
        ("Conflicts?",           "Plan Complete",         "No"),
        
        # Semester
        ("Plan Complete",        "Attend Classes",        ""),
        ("Attend Classes",       "Add Drop Period",       ""),
        ("Add Drop Period",      "Modify Courses?",       ""),
        ("Modify Courses?",      "Add Drop Courses",      "Yes"),
        ("Modify Courses?",      "Continue Semester",     "No"),
        ("Add Drop Courses",     "Continue Semester",     ""),
        ("Continue Semester",    "Post Grades",           ""),
        ("Post Grades",          "Review Grades",         ""),
        
        # Appeals
        ("Review Grades",        "Has Grievance?",        ""),
        ("Has Grievance?",       "Submit Appeal",         "Yes"),
        ("Submit Appeal",        "Meet Appeals Committee",""),
        ("Meet Appeals Committee","Await Decision",       ""),
        ("Await Decision",       "Sync After Appeals",    ""),
        ("Has Grievance?",       "No Appeal",             "No"),
        ("No Appeal",            "Sync After Appeals",    ""),
        
        # Loop or End
        ("Sync After Appeals",   "Graduate or Continue?", ""),
        ("Graduate or Continue?","End Graduated",         "Graduate"),
        ("Graduate or Continue?","Attend Classes",        "Continue"),
    ],
    
    "layout": {
        # Column 0 - Start
        "Start":                 0,
        
        # Column 1 - Submit
        "Submit Application":    1,
        
        # Column 2 - Review
        "Review Application":    2,
        
        # Column 3 - Doc Check
        "Documents Complete?":   3,
        
        # Column 4 - Missing docs handling
        "Notify Missing Docs":   4,
        "Provide Missing Docs":  4,
        
        # Column 5 - Parallel split
        "All Docs Received":     5,
        
        # Column 6 - Parallel work
        "Evaluate Application":  6,
        "Process Fees":          6,
        
        # Column 7 - Sync
        "Sync After Eval":       7,
        
        # Column 8 - Decision
        "Accepted?":             8,
        
        # Column 9 - Decision outcomes
        "Send Rejection":        9,
        "Send Acceptance":       9,
        
        # Column 10 - End rejected / Wait
        "End Rejected":          10,
        "Wait Confirmation":     10,
        
        # Column 11 - Confirmation check
        "Confirmed?":            11,
        
        # Column 12 - Confirm outcomes
        "Cancel Application":    12,
        "Confirm Enrollment":    12,
        
        # Column 13 - End cancelled / Start onboarding
        "End Cancelled":         13,
        "Start Onboarding":      13,
        
        # Column 14 - Parallel onboarding
        "Send Orientation":      14,
        "Setup Accounts":        14,
        "International?":        14,
        
        # Column 15 - Visa handling
        "Process Visa":          15,
        "Skip Visa":             15,
        
        # Column 16 - Sync onboarding
        "Sync Onboarding":       16,
        
        # Column 17 - Student ID
        "Get Student ID":        17,
        
        # Column 18 - Study plan
        "Create Study Plan":     18,
        
        # Column 19 - Advisor
        "Meet Advisor":          19,
        
        # Column 20 - Course selection
        "Select Courses":        20,
        
        # Column 21 - Conflict check
        "Conflicts?":            21,
        
        # Column 22 - Resolve / Complete
        "Resolve Conflicts":     (22, 0),
        "Plan Complete":         (22, 120),
        
        # Column 23 - Attend
        "Attend Classes":        23,
        
        # Column 24 - Add/Drop timer
        "Add Drop Period":       24,
        
        # Column 25 - Modify check
        "Modify Courses?":       25,
        
        # Column 26 - Modify outcomes
        "Add Drop Courses":      26,
        "Continue Semester":     26,
        
        # Column 27 - Grades
        "Post Grades":           27,
        
        # Column 28 - Review
        "Review Grades":         28,
        
        # Column 29 - Grievance check
        "Has Grievance?":        29,
        
        # Column 30 - Appeal outcomes
        "Submit Appeal":         30,
        "No Appeal":             30,
        
        # Column 31 - Committee
        "Meet Appeals Committee":31,
        
        # Column 32 - Await
        "Await Decision":        32,
        
        # Column 33 - Sync appeals
        "Sync After Appeals":    33,
        
        # Column 34 - Graduate check
        "Graduate or Continue?": 34,
        
        # Column 35 - End
        "End Graduated":         35,
    },
    
    "data_objects": [
        ("Application Form",     "Applicant/Student",  1),
        ("Supporting Docs",      "Applicant/Student",  2),
        ("Acceptance Letter",    "Admissions Office",  9),
        ("Student Account",      "IT Department",      14),
        ("Study Plan Doc",       "Applicant/Student",  18),
        ("Grade Report",         "Academic Services",  27),
        ("Appeal Form",          "Applicant/Student",  30),
    ],
    
    "data_associations": [
        ("Submit Application",   "Application Form"),
        ("Application Form",     "Review Application"),
        ("Review Application",   "Supporting Docs"),
        ("Send Acceptance",      "Acceptance Letter"),
        ("Setup Accounts",       "Student Account"),
        ("Create Study Plan",    "Study Plan Doc"),
        ("Study Plan Doc",       "Meet Advisor"),
        ("Post Grades",          "Grade Report"),
        ("Grade Report",         "Review Grades"),
        ("Submit Appeal",        "Appeal Form"),
        ("Appeal Form",          "Meet Appeals Committee"),
    ],
    
    # Wider spacing for this large diagram
    "SPACING": 130,
    "TASK_WIDTH": 110,
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
