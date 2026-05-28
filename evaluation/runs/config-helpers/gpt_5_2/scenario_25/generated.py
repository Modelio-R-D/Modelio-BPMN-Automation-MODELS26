#
# Find_a_Job.py
#
# Description: Job search process with regular reporting, company confirmation/rating, interview negotiation,
#              probation, mutual reviews with 1-year visibility delay, and conditional continuation after permanent hire.
# Applicable on: Package
#

from org.modelio.metamodel.uml.statik import Package

# Load helper library
execfile(".modelio/5.4/macros/BPMN_Helpers.py")

CONFIG = {
    "name": "Find a Job",

    "lanes": ["Applicant", "Company", "Employment Office", "Review Portal"],

    "elements": [
        # Applicant
        ("Reporting Cycle",                    TIMER_START,     "Applicant"),
        ("Receive Job Offers",                 MESSAGE_CATCH,   "Applicant"),
        ("Review Job Offers",                  USER_TASK,       "Applicant"),
        ("Apply?",                             EXCLUSIVE_GW,    "Applicant"),
        ("Prepare Application",                USER_TASK,       "Applicant"),
        ("Send Application",                   SEND_TASK,       "Applicant"),
        ("Report Required?",                   EXCLUSIVE_GW,    "Applicant"),
        ("Report Applications",                USER_TASK,       "Applicant"),
        ("Negotiate Interview",                USER_TASK,       "Applicant"),
        ("Receive Rejection",                  MESSAGE_CATCH,   "Applicant"),
        ("Attend Interview",                   USER_TASK,       "Applicant"),
        ("Probation Work",                     USER_TASK,       "Applicant"),
        ("Receive Interview Outcome",          MESSAGE_CATCH,   "Applicant"),
        ("Receive Probation Result",           MESSAGE_CATCH,   "Applicant"),
        ("Rate Company",                       USER_TASK,       "Applicant"),
        ("Rating <= C?",                       EXCLUSIVE_GW,    "Applicant"),
        ("Continue Receiving Offers (No Reporting)", TASK,      "Applicant"),
        ("End",                                END,            "Applicant"),

        # Company
        ("Receive Application",                RECEIVE_TASK,    "Company"),
        ("Confirm Receipt",                    USER_TASK,       "Company"),
        ("Rate Application",                   USER_TASK,       "Company"),
        ("Invite Interview?",                  EXCLUSIVE_GW,    "Company"),
        ("Propose Interview",                  SEND_TASK,       "Company"),
        ("Send Rejection",                     SEND_TASK,       "Company"),
        ("Offer Job?",                         EXCLUSIVE_GW,    "Company"),
        ("Hire on Probation",                  USER_TASK,       "Company"),
        ("Reject After Interview",             SEND_TASK,       "Company"),
        ("Permanent?",                         EXCLUSIVE_GW,    "Company"),
        ("Notify Not Permanent",               SEND_TASK,       "Company"),
        ("Rate Applicant",                     USER_TASK,       "Company"),

        # Employment Office
        ("Receive Report",                     RECEIVE_TASK,    "Employment Office"),
        ("Archive Report",                     SERVICE_TASK,    "Employment Office"),

        # Review Portal
        ("Record Reviews",                     SERVICE_TASK,    "Review Portal"),
        ("Wait 1 Year",                        TIMER_CATCH,     "Review Portal"),
        ("Publish Company Reviews",            SERVICE_TASK,    "Review Portal"),
    ],

    "flows": [
        # Start and offers cycle
        ("Reporting Cycle",        "Receive Job Offers",                 ""),
        ("Receive Job Offers",     "Review Job Offers",                  ""),
        ("Review Job Offers",      "Apply?",                             ""),

        # Decide to apply
        ("Apply?",                 "Prepare Application",                "Yes"),
        ("Apply?",                 "Receive Job Offers",                 "No"),

        # Application
        ("Prepare Application",    "Send Application",                   ""),
        ("Send Application",       "Report Required?",                   ""),

        # Reporting (conditional)
        ("Report Required?",       "Report Applications",                "Yes"),
        ("Report Required?",       "Receive Application",                "No"),

        ("Report Applications",    "Receive Report",                     ""),
        ("Receive Report",         "Archive Report",                     ""),
        ("Archive Report",         "Receive Application",                ""),

        # Company handling
        ("Receive Application",    "Confirm Receipt",                    ""),
        ("Confirm Receipt",        "Rate Application",                   ""),
        ("Rate Application",       "Invite Interview?",                  ""),

        ("Invite Interview?",      "Propose Interview",                  "Yes"),
        ("Invite Interview?",      "Send Rejection",                     "No"),

        # Rejection before interview
        ("Send Rejection",         "Receive Rejection",                  ""),
        ("Receive Rejection",      "Receive Job Offers",                 ""),

        # Interview negotiation and interview
        ("Propose Interview",      "Negotiate Interview",                ""),
        ("Negotiate Interview",    "Attend Interview",                   ""),
        ("Attend Interview",       "Offer Job?",                         ""),

        # Offer decision
        ("Offer Job?",             "Hire on Probation",                  "Yes"),
        ("Offer Job?",             "Reject After Interview",             "No"),

        ("Reject After Interview", "Receive Interview Outcome",          ""),
        ("Receive Interview Outcome", "Receive Job Offers",              ""),

        # Probation and permanence decision
        ("Hire on Probation",      "Probation Work",                     ""),
        ("Probation Work",         "Permanent?",                         ""),

        ("Permanent?",             "Notify Not Permanent",               "No"),
        ("Notify Not Permanent",   "Receive Probation Result",           ""),
        ("Receive Probation Result", "Receive Job Offers",               ""),

        # Permanent: mutual rating and review visibility after 1 year
        ("Permanent?",             "Rate Company",                       "Yes"),
        ("Rate Company",           "Rate Applicant",                     ""),
        ("Rate Applicant",         "Record Reviews",                     ""),
        ("Record Reviews",         "Wait 1 Year",                        ""),
        ("Wait 1 Year",            "Publish Company Reviews",            ""),
        ("Publish Company Reviews","Rating <= C?",                       ""),

        # End or continue (no reporting) based on applicant rating
        ("Rating <= C?",           "Continue Receiving Offers (No Reporting)", "Yes"),
        ("Rating <= C?",           "End",                                "No"),
        ("Continue Receiving Offers (No Reporting)", "Receive Job Offers", ""),
    ],

    "layout": {
        # Applicant
        "Reporting Cycle":                         0,
        "Receive Job Offers":                      1,
        "Review Job Offers":                       2,
        "Apply?":                                  3,
        "Prepare Application":                     4,
        "Send Application":                        5,
        "Report Required?":                        6,
        "Report Applications":                     7,
        "Negotiate Interview":                    15,
        "Receive Rejection":                      15,   # auto-stacked under "Negotiate Interview"
        "Attend Interview":                       16,
        "Probation Work":                         19,
        "Receive Interview Outcome":              19,   # auto-stacked under "Probation Work"
        "Receive Probation Result":               22,
        "Rate Company":                           21,
        "Rating <= C?":                           26,
        "Continue Receiving Offers (No Reporting)": 27,
        "End":                                    28,

        # Company
        "Receive Application":                    10,
        "Confirm Receipt":                        11,
        "Rate Application":                       12,
        "Invite Interview?":                      13,
        "Propose Interview":                      14,
        "Send Rejection":                         14,   # auto-stacked
        "Offer Job?":                             17,
        "Hire on Probation":                      18,
        "Reject After Interview":                 18,   # auto-stacked
        "Permanent?":                             20,
        "Notify Not Permanent":                   21,
        "Rate Applicant":                         22,

        # Employment Office
        "Receive Report":                          8,
        "Archive Report":                          9,

        # Review Portal
        "Record Reviews":                         23,
        "Wait 1 Year":                            24,
        "Publish Company Reviews":                25,
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
