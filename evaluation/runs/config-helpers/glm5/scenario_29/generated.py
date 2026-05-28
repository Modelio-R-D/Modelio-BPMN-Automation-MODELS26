#
# WorkLiveAustria.py
#
# Description: BPMN process for working and living in Austria
#              - Rot-Weiss-Rot Card visa application
#              - Accommodation and bank account negotiation
#              - Residence registration
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "WorkLiveAustria",
    
    "lanes": ["Applicant", "Austrian Embassy", "Service Provider", "Municipal Authority"],
    
    "elements": [
        # === PHASE 1: DOCUMENT PREPARATION ===
        ("Start", START, "Applicant"),
        ("Gather Required Documents", USER_TASK, "Applicant"),
        ("Documents Complete?", EXCLUSIVE_GW, "Applicant"),
        ("Obtain Missing Documents", USER_TASK, "Applicant"),
        ("Purchase Travel Insurance", USER_TASK, "Applicant"),
        
        # === PHASE 2: ACCOMMODATION (Negotiation) ===
        ("Search Accommodation", USER_TASK, "Applicant"),
        ("Negotiate Terms", USER_TASK, "Service Provider"),
        ("Accommodation Available?", EXCLUSIVE_GW, "Service Provider"),
        ("Sign Rental Contract", USER_TASK, "Service Provider"),
        
        # === PHASE 3: BANK ACCOUNT ===
        ("Open Bank Account", USER_TASK, "Service Provider"),
        
        # === PHASE 4: VISA APPLICATION ===
        ("Submit Visa Application", USER_TASK, "Applicant"),
        ("Review Application", SERVICE_TASK, "Austrian Embassy"),
        ("Application Complete?", EXCLUSIVE_GW, "Austrian Embassy"),
        ("Request Additional Documents", SERVICE_TASK, "Austrian Embassy"),
        ("Provide Additional Documents", USER_TASK, "Applicant"),
        ("Process Application", SERVICE_TASK, "Austrian Embassy"),
        ("Visa Approved?", EXCLUSIVE_GW, "Austrian Embassy"),
        ("Issue Rot-Weiss-Rot Card", SERVICE_TASK, "Austrian Embassy"),
        ("Application Rejected", END, "Austrian Embassy"),
        
        # === PHASE 5: POST-ARRIVAL ===
        ("Receive Card", USER_TASK, "Applicant"),
        ("Enter Austria", USER_TASK, "Applicant"),
        ("Register Residence", USER_TASK, "Municipal Authority"),
        
        # === END ===
        ("Live and Work in Austria", END, "Applicant"),
    ],
    
    "data_objects": [
        ("Valid Passport", "Applicant", 1),
        ("Passport Photo", "Applicant", 1),
        ("Application Form", "Applicant", 8),
        ("Health Insurance", "Applicant", 4),
        ("Rental Contract", "Service Provider", 7),
        ("Bank Account Details", "Service Provider", 8),
        ("Proof of Means", "Applicant", 8),
        ("Rot-Weiss-Rot Card", "Austrian Embassy", 14),
        ("Residence Registration", "Municipal Authority", 17),
    ],
    
    "data_associations": [
        # Documents prepared by applicant
        ("Gather Required Documents", "Valid Passport"),
        ("Gather Required Documents", "Passport Photo"),
        ("Purchase Travel Insurance", "Health Insurance"),
        
        # Documents from service providers
        ("Sign Rental Contract", "Rental Contract"),
        ("Open Bank Account", "Bank Account Details"),
        
        # Visa card issuance
        ("Issue Rot-Weiss-Rot Card", "Rot-Weiss-Rot Card"),
        
        # Documents submitted with visa application
        ("Valid Passport", "Submit Visa Application"),
        ("Passport Photo", "Submit Visa Application"),
        ("Application Form", "Submit Visa Application"),
        ("Health Insurance", "Submit Visa Application"),
        ("Rental Contract", "Submit Visa Application"),
        ("Bank Account Details", "Proof of Means"),
        ("Proof of Means", "Submit Visa Application"),
        
        # Post-arrival
        ("Register Residence", "Residence Registration"),
    ],
    
    "flows": [
        # Phase 1: Document Preparation
        ("Start", "Gather Required Documents", ""),
        ("Gather Required Documents", "Documents Complete?", ""),
        ("Documents Complete?", "Obtain Missing Documents", "No"),
        ("Obtain Missing Documents", "Gather Required Documents", ""),
        ("Documents Complete?", "Purchase Travel Insurance", "Yes"),
        
        # Phase 2: Accommodation (Negotiation)
        ("Purchase Travel Insurance", "Search Accommodation", ""),
        ("Search Accommodation", "Negotiate Terms", ""),
        ("Negotiate Terms", "Accommodation Available?", ""),
        ("Accommodation Available?", "Search Accommodation", "No"),
        ("Accommodation Available?", "Sign Rental Contract", "Yes"),
        
        # Phase 3: Bank Account
        ("Sign Rental Contract", "Open Bank Account", ""),
        
        # Phase 4: Visa Application
        ("Open Bank Account", "Submit Visa Application", ""),
        ("Submit Visa Application", "Review Application", ""),
        ("Review Application", "Application Complete?", ""),
        ("Application Complete?", "Request Additional Documents", "No"),
        ("Request Additional Documents", "Provide Additional Documents", ""),
        ("Provide Additional Documents", "Review Application", ""),
        ("Application Complete?", "Process Application", "Yes"),
        ("Process Application", "Visa Approved?", ""),
        ("Visa Approved?", "Application Rejected", "No"),
        ("Visa Approved?", "Issue Rot-Weiss-Rot Card", "Yes"),
        
        # Phase 5: Post-Arrival
        ("Issue Rot-Weiss-Rot Card", "Receive Card", ""),
        ("Receive Card", "Enter Austria", ""),
        ("Enter Austria", "Register Residence", ""),
        ("Register Residence", "Live and Work in Austria", ""),
    ],
    
    "layout": {
        "Start": 0,
        "Gather Required Documents": 1,
        "Documents Complete?": 2,
        "Obtain Missing Documents": 3,
        "Purchase Travel Insurance": 4,
        "Search Accommodation": 5,
        "Negotiate Terms": 6,
        "Accommodation Available?": 7,
        "Sign Rental Contract": 8,
        "Open Bank Account": 9,
        "Submit Visa Application": 10,
        "Review Application": 11,
        "Application Complete?": 12,
        "Request Additional Documents": 13,
        "Provide Additional Documents": 13,
        "Process Application": 14,
        "Visa Approved?": 15,
        "Issue Rot-Weiss-Rot Card": 16,
        "Application Rejected": 16,
        "Receive Card": 17,
        "Enter Austria": 18,
        "Register Residence": 19,
        "Live and Work in Austria": 20,
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
