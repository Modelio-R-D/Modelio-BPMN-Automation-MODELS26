#
# WorkAndLiveInAustria.py
#
# Description: Process for obtaining Rot-Weiss-Rot Card and settling in Austria
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile("C:/Users/lchlih/.modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "WorkAndLiveInAustria",
    
    "lanes": [
        "Applicant",
        "Austrian Representation",
        "Immigration Authority (MA35)",
        "Service Providers"
    ],
    
    "elements": [
        # Start
        ("Start", START, "Applicant"),
        
        # Initial Preparation Phase
        ("Research Requirements", USER_TASK, "Applicant"),
        ("Identify Competent Representation", USER_TASK, "Applicant"),
        
        # Document Collection - Parallel
        ("Prepare Documents", PARALLEL_GW, "Applicant"),
        ("Complete Visa Application Form", USER_TASK, "Applicant"),
        ("Obtain Passport Photo 35x45mm", USER_TASK, "Applicant"),
        ("Arrange Travel Health Insurance", USER_TASK, "Applicant"),
        ("Gather Financial Proof", USER_TASK, "Applicant"),
        ("Obtain Employment Contract", USER_TASK, "Applicant"),
        ("Check Passport Validity", USER_TASK, "Applicant"),
        ("Documents Ready", PARALLEL_GW, "Applicant"),
        
        # Passport Check
        ("Passport Valid?", EXCLUSIVE_GW, "Applicant"),
        ("Renew Passport", USER_TASK, "Applicant"),
        
        # Type D Visa Application
        ("Submit RWR Card Application", USER_TASK, "Applicant"),
        ("Receive Application", USER_TASK, "Austrian Representation"),
        ("Verify Documents Complete?", EXCLUSIVE_GW, "Austrian Representation"),
        ("Request Additional Documents", SEND_TASK, "Austrian Representation"),
        ("Provide Additional Documents", USER_TASK, "Applicant"),
        ("Forward to MA35", SEND_TASK, "Austrian Representation"),
        
        # Immigration Processing
        ("Process Application", SERVICE_TASK, "Immigration Authority (MA35)"),
        ("Check Eligibility Criteria", SERVICE_TASK, "Immigration Authority (MA35)"),
        ("Application Approved?", EXCLUSIVE_GW, "Immigration Authority (MA35)"),
        ("Issue Rejection Notice", SEND_TASK, "Immigration Authority (MA35)"),
        ("Issue RWR Card", SERVICE_TASK, "Immigration Authority (MA35)"),
        ("Notify Applicant", SEND_TASK, "Immigration Authority (MA35)"),
        
        # Settlement in Austria - Parallel Activities
        ("Arrive in Austria", USER_TASK, "Applicant"),
        ("Begin Settlement Tasks", PARALLEL_GW, "Applicant"),
        
        # Accommodation
        ("Search Accommodation", USER_TASK, "Applicant"),
        ("Negotiate Rental Terms", USER_TASK, "Applicant"),
        ("Sign Rental Contract", USER_TASK, "Applicant"),
        ("Register Residence Meldezettel", USER_TASK, "Applicant"),
        
        # Banking
        ("Research Banks", USER_TASK, "Applicant"),
        ("Schedule Bank Appointment", USER_TASK, "Applicant"),
        ("Open Bank Account", USER_TASK, "Service Providers"),
        ("Receive Bank Details", RECEIVE_TASK, "Applicant"),
        
        # Completion
        ("Settlement Complete", PARALLEL_GW, "Applicant"),
        
        # Renewal Reminder
        ("Set Renewal Reminder", SERVICE_TASK, "Applicant"),
        ("Wait for Renewal Period", TIMER_CATCH, "Applicant"),
        ("Renewal Required?", EXCLUSIVE_GW, "Applicant"),
        
        # End Events
        ("End Success", END, "Applicant"),
        ("End Rejected", TERMINATE_END, "Immigration Authority (MA35)"),
    ],
    
    "data_objects": [
        ("Visa Application Form", "Applicant", 3),
        ("Passport Photo", "Applicant", 3),
        ("Health Insurance Policy", "Applicant", 3),
        ("Financial Documents", "Applicant", 3),
        ("Employment Contract", "Applicant", 3),
        ("Valid Passport", "Applicant", 5),
        ("Application Package", "Austrian Representation", 8),
        ("RWR Card", "Immigration Authority (MA35)", 13),
        ("Rental Contract", "Applicant", 18),
        ("Meldezettel", "Applicant", 19),
        ("Bank Account Details", "Service Providers", 21),
    ],
    
    "data_associations": [
        ("Complete Visa Application Form", "Visa Application Form"),
        ("Obtain Passport Photo 35x45mm", "Passport Photo"),
        ("Arrange Travel Health Insurance", "Health Insurance Policy"),
        ("Gather Financial Proof", "Financial Documents"),
        ("Obtain Employment Contract", "Employment Contract"),
        ("Check Passport Validity", "Valid Passport"),
        ("Valid Passport", "Submit RWR Card Application"),
        ("Receive Application", "Application Package"),
        ("Application Package", "Process Application"),
        ("Issue RWR Card", "RWR Card"),
        ("RWR Card", "Arrive in Austria"),
        ("Sign Rental Contract", "Rental Contract"),
        ("Rental Contract", "Register Residence Meldezettel"),
        ("Register Residence Meldezettel", "Meldezettel"),
        ("Open Bank Account", "Bank Account Details"),
        ("Bank Account Details", "Receive Bank Details"),
    ],
    
    "flows": [
        # Initial Phase
        ("Start", "Research Requirements", ""),
        ("Research Requirements", "Identify Competent Representation", ""),
        ("Identify Competent Representation", "Prepare Documents", ""),
        
        # Parallel Document Preparation
        ("Prepare Documents", "Complete Visa Application Form", ""),
        ("Prepare Documents", "Obtain Passport Photo 35x45mm", ""),
        ("Prepare Documents", "Arrange Travel Health Insurance", ""),
        ("Prepare Documents", "Gather Financial Proof", ""),
        ("Prepare Documents", "Obtain Employment Contract", ""),
        ("Prepare Documents", "Check Passport Validity", ""),
        
        # Passport Check Loop
        ("Check Passport Validity", "Passport Valid?", ""),
        ("Passport Valid?", "Renew Passport", "No - Less than 3 months validity"),
        ("Renew Passport", "Check Passport Validity", ""),
        ("Passport Valid?", "Documents Ready", "Yes"),
        
        # Converge Documents
        ("Complete Visa Application Form", "Documents Ready", ""),
        ("Obtain Passport Photo 35x45mm", "Documents Ready", ""),
        ("Arrange Travel Health Insurance", "Documents Ready", ""),
        ("Gather Financial Proof", "Documents Ready", ""),
        ("Obtain Employment Contract", "Documents Ready", ""),
        
        # Application Submission
        ("Documents Ready", "Submit RWR Card Application", ""),
        ("Submit RWR Card Application", "Receive Application", ""),
        ("Receive Application", "Verify Documents Complete?", ""),
        ("Verify Documents Complete?", "Request Additional Documents", "No"),
        ("Request Additional Documents", "Provide Additional Documents", ""),
        ("Provide Additional Documents", "Receive Application", ""),
        ("Verify Documents Complete?", "Forward to MA35", "Yes"),
        
        # Immigration Processing
        ("Forward to MA35", "Process Application", ""),
        ("Process Application", "Check Eligibility Criteria", ""),
        ("Check Eligibility Criteria", "Application Approved?", ""),
        ("Application Approved?", "Issue Rejection Notice", "No"),
        ("Issue Rejection Notice", "End Rejected", ""),
        ("Application Approved?", "Issue RWR Card", "Yes"),
        ("Issue RWR Card", "Notify Applicant", ""),
        
        # Arrival and Settlement
        ("Notify Applicant", "Arrive in Austria", ""),
        ("Arrive in Austria", "Begin Settlement Tasks", ""),
        
        # Parallel Settlement - Accommodation Branch
        ("Begin Settlement Tasks", "Search Accommodation", ""),
        ("Search Accommodation", "Negotiate Rental Terms", ""),
        ("Negotiate Rental Terms", "Sign Rental Contract", ""),
        ("Sign Rental Contract", "Register Residence Meldezettel", ""),
        ("Register Residence Meldezettel", "Settlement Complete", ""),
        
        # Parallel Settlement - Banking Branch
        ("Begin Settlement Tasks", "Research Banks", ""),
        ("Research Banks", "Schedule Bank Appointment", ""),
        ("Schedule Bank Appointment", "Open Bank Account", ""),
        ("Open Bank Account", "Receive Bank Details", ""),
        ("Receive Bank Details", "Settlement Complete", ""),
        
        # Renewal Cycle
        ("Settlement Complete", "Set Renewal Reminder", ""),
        ("Set Renewal Reminder", "Wait for Renewal Period", ""),
        ("Wait for Renewal Period", "Renewal Required?", "12-24 months"),
        ("Renewal Required?", "Research Requirements", "Yes - Renew RWR Card"),
        ("Renewal Required?", "End Success", "No - Permanent Residence"),
    ],
    
    "layout": {
        # Initial Phase
        "Start": 0,
        "Research Requirements": 1,
        "Identify Competent Representation": 2,
        "Prepare Documents": 3,
        
        # Parallel Document Tasks (Column 4 - auto-stacked)
        "Complete Visa Application Form": 4,
        "Obtain Passport Photo 35x45mm": 4,
        "Arrange Travel Health Insurance": 4,
        "Gather Financial Proof": 4,
        "Obtain Employment Contract": 4,
        "Check Passport Validity": 4,
        
        # Passport Validation
        "Passport Valid?": 5,
        "Renew Passport": (5, 90),
        
        # Document Convergence
        "Documents Ready": 6,
        
        # Application Submission
        "Submit RWR Card Application": 7,
        "Receive Application": 8,
        "Verify Documents Complete?": 9,
        "Request Additional Documents": (9, 90),
        "Provide Additional Documents": (8, 90),
        "Forward to MA35": 10,
        
        # Immigration Processing
        "Process Application": 11,
        "Check Eligibility Criteria": 12,
        "Application Approved?": 13,
        "Issue Rejection Notice": (13, 90),
        "End Rejected": (14, 90),
        "Issue RWR Card": 14,
        "Notify Applicant": 15,
        
        # Arrival
        "Arrive in Austria": 16,
        "Begin Settlement Tasks": 17,
        
        # Accommodation Branch (auto-stacked in column 18-20)
        "Search Accommodation": 18,
        "Negotiate Rental Terms": 19,
        "Sign Rental Contract": 20,
        "Register Residence Meldezettel": 21,
        
        # Banking Branch (auto-stacked with accommodation tasks)
        "Research Banks": 18,
        "Schedule Bank Appointment": 19,
        "Open Bank Account": 20,
        "Receive Bank Details": 21,
        
        # Completion
        "Settlement Complete": 22,
        "Set Renewal Reminder": 23,
        "Wait for Renewal Period": 24,
        "Renewal Required?": 25,
        "End Success": 26,
    },
    
    # Wider spacing for readability
    "SPACING": 160,
    "START_X": 60,
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
