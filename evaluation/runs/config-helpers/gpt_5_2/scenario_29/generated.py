#
# WorkAndLiveInAustria.py
#
# Description: Process to check requirements and complete key steps to work and live in Austria,
#              including visa / Rot-Weiss-Rot Card handling, accommodation and bank setup,
#              and periodic renewal preparation.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Work and Live in Austria",

    "lanes": [
        "Applicant",
        "Austrian Authorities",
        "Landlord/Bank",
    ],

    "elements": [
        ("Start",                                      START,          "Applicant"),

        ("Check eligibility and plan stay",            USER_TASK,      "Applicant"),
        ("Determine competent representation",         USER_TASK,      "Applicant"),

        ("Prepare visa application package",           USER_TASK,      "Applicant"),
        ("All required documents assembled?",          EXCLUSIVE_GW,   "Applicant"),
        ("Collect missing / other evidence",           USER_TASK,      "Applicant"),
        ("Update application package",                 USER_TASK,      "Applicant"),

        ("Submit application at representation",       USER_TASK,      "Applicant"),

        ("Review application",                         SERVICE_TASK,   "Austrian Authorities"),
        ("Additional documents needed?",               EXCLUSIVE_GW,   "Austrian Authorities"),
        ("Request additional documents",               SEND_TASK,      "Austrian Authorities"),
        ("Provide additional documents",               USER_TASK,      "Applicant"),
        ("Review additional documents",                SERVICE_TASK,   "Austrian Authorities"),

        ("Decision: approved?",                        EXCLUSIVE_GW,   "Austrian Authorities"),
        ("Issue entry visa / approval",                SERVICE_TASK,   "Austrian Authorities"),

        ("Travel to Austria",                          TASK,           "Applicant"),
        ("Register address (Meldezettel)",             USER_TASK,      "Applicant"),

        ("Settle basics in parallel",                  PARALLEL_GW,    "Applicant"),
        ("Negotiate accommodation",                    USER_TASK,      "Landlord/Bank"),
        ("Open bank account (negotiation)",            USER_TASK,      "Landlord/Bank"),
        ("Basics completed",                           PARALLEL_GW,    "Applicant"),

        ("Collect Rot-Weiss-Rot Card",                 USER_TASK,      "Austrian Authorities"),
        ("Start working and living in Austria",        TASK,           "Applicant"),

        ("Before expiry (every X months)",             TIMER_CATCH,    "Applicant"),
        ("Prepare renewal application",                USER_TASK,      "Applicant"),
        ("Submit renewal to authorities",              USER_TASK,      "Applicant"),
        ("Review renewal",                             SERVICE_TASK,   "Austrian Authorities"),
        ("Renewal approved?",                          EXCLUSIVE_GW,   "Austrian Authorities"),
        ("Issue renewed Rot-Weiss-Rot Card",           SERVICE_TASK,   "Austrian Authorities"),

        ("End: continue in Austria",                   END,            "Applicant"),
        ("End: refused / must leave",                  TERMINATE_END,  "Applicant"),
    ],

    "data_objects": [
        ("Visa application form",                                          "Applicant", 3),
        ("Passport (valid +3 months, 2 blank pages, issued <10y)",          "Applicant", 3),
        ("Passport photo 35x45",                                           "Applicant", 3),
        ("Travel health insurance (EUR 30000, Schengen)",                   "Applicant", 3),
        ("Proof of means of subsistence",                                   "Applicant", 3),
        ("Other evidence (reservations, invitation, return ticket, etc.)",  "Applicant", 5),

        ("Additional documents",                                           "Applicant", 11),

        ("Rot-Weiss-Rot Card",                                             "Applicant", 20),
        ("Renewal application package",                                    "Applicant", 23),
    ],

    "data_associations": [
        # Initial visa package (general principles / requirements)
        ("Prepare visa application package", "Visa application form"),
        ("Prepare visa application package", "Passport (valid +3 months, 2 blank pages, issued <10y)"),
        ("Prepare visa application package", "Passport photo 35x45"),
        ("Prepare visa application package", "Travel health insurance (EUR 30000, Schengen)"),
        ("Prepare visa application package", "Proof of means of subsistence"),

        # Other evidence may vary by location / authority request
        ("Collect missing / other evidence", "Other evidence (reservations, invitation, return ticket, etc.)"),

        # Submission uses the prepared documents
        ("Visa application form",                                         "Submit application at representation"),
        ("Passport (valid +3 months, 2 blank pages, issued <10y)",         "Submit application at representation"),
        ("Passport photo 35x45",                                          "Submit application at representation"),
        ("Travel health insurance (EUR 30000, Schengen)",                  "Submit application at representation"),
        ("Proof of means of subsistence",                                  "Submit application at representation"),
        ("Other evidence (reservations, invitation, return ticket, etc.)", "Submit application at representation"),

        # Additional documents cycle (if requested)
        ("Provide additional documents", "Additional documents"),
        ("Additional documents",         "Review additional documents"),

        # Card issuance and use
        ("Collect Rot-Weiss-Rot Card",     "Rot-Weiss-Rot Card"),
        ("Rot-Weiss-Rot Card",             "Start working and living in Austria"),

        # Renewal
        ("Prepare renewal application",    "Renewal application package"),
        ("Renewal application package",    "Submit renewal to authorities"),
    ],

    "flows": [
        ("Start",                                "Check eligibility and plan stay",         ""),
        ("Check eligibility and plan stay",      "Determine competent representation",      ""),

        ("Determine competent representation",   "Prepare visa application package",        ""),
        ("Prepare visa application package",     "All required documents assembled?",       ""),

        ("All required documents assembled?",    "Submit application at representation",    "Yes"),
        ("All required documents assembled?",    "Collect missing / other evidence",        "No"),
        ("Collect missing / other evidence",     "Update application package",              ""),
        ("Update application package",           "Submit application at representation",    ""),

        ("Submit application at representation", "Review application",                      ""),

        ("Review application",                   "Additional documents needed?",            ""),
        ("Additional documents needed?",         "Decision: approved?",                     "No"),
        ("Additional documents needed?",         "Request additional documents",            "Yes"),
        ("Request additional documents",         "Provide additional documents",            ""),
        ("Provide additional documents",         "Review additional documents",             ""),
        ("Review additional documents",          "Decision: approved?",                     ""),

        ("Decision: approved?",                  "Issue entry visa / approval",             "Yes"),
        ("Decision: approved?",                  "End: refused / must leave",               "No"),

        ("Issue entry visa / approval",          "Travel to Austria",                       ""),
        ("Travel to Austria",                    "Register address (Meldezettel)",          ""),
        ("Register address (Meldezettel)",       "Settle basics in parallel",               ""),

        ("Settle basics in parallel",            "Negotiate accommodation",                 ""),
        ("Settle basics in parallel",            "Open bank account (negotiation)",         ""),

        ("Negotiate accommodation",              "Basics completed",                        ""),
        ("Open bank account (negotiation)",      "Basics completed",                        ""),

        ("Basics completed",                     "Collect Rot-Weiss-Rot Card",              ""),
        ("Collect Rot-Weiss-Rot Card",           "Start working and living in Austria",     ""),

        # Renewal trigger (every X months, before expiry)
        ("Start working and living in Austria",  "Before expiry (every X months)",          ""),
        ("Before expiry (every X months)",       "Prepare renewal application",             ""),
        ("Prepare renewal application",          "Submit renewal to authorities",           ""),
        ("Submit renewal to authorities",        "Review renewal",                          ""),
        ("Review renewal",                       "Renewal approved?",                       ""),

        ("Renewal approved?",                    "Issue renewed Rot-Weiss-Rot Card",        "Yes"),
        ("Renewal approved?",                    "End: refused / must leave",               "No"),

        ("Issue renewed Rot-Weiss-Rot Card",     "End: continue in Austria",                ""),
    ],

    "layout": {
        "Start":                                     0,
        "Check eligibility and plan stay":           1,
        "Determine competent representation":        2,

        "Prepare visa application package":          3,
        "All required documents assembled?":         4,
        "Collect missing / other evidence":          5,
        "Update application package":                6,

        "Submit application at representation":      7,

        "Review application":                        8,
        "Additional documents needed?":              9,
        "Request additional documents":              10,
        "Provide additional documents":              11,
        "Review additional documents":               12,

        "Decision: approved?":                       13,
        "Issue entry visa / approval":               14,

        "Travel to Austria":                         15,
        "Register address (Meldezettel)":            16,

        "Settle basics in parallel":                 17,
        # Auto-stacked (same lane + same column) in Landlord/Bank lane:
        "Negotiate accommodation":                   18,
        "Open bank account (negotiation)":          18,
        "Basics completed":                          19,

        "Collect Rot-Weiss-Rot Card":                20,
        "Start working and living in Austria":       21,

        "Before expiry (every X months)":            22,
        "Prepare renewal application":               23,
        "Submit renewal to authorities":             24,
        "Review renewal":                            25,
        "Renewal approved?":                         26,
        "Issue renewed Rot-Weiss-Rot Card":          27,

        "End: continue in Austria":                  28,
        "End: refused / must leave":                 28,
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
