# Test Prompts for Modelio BPMN Generation

Use these prompts to validate macro generation quality across increasing complexity.

---

## Level 1: Simple Process
**Test 1.1 – Leave Request**  
Prompt:
> Create a BPMN process for "Leave Request" with 2 lanes: Employee, Manager.  
> Employee: Start -> Submit Leave Request.  
> Manager: Review -> Approve/Reject gateway.  
> If approved: End (Approved) in Manager lane.  
> If rejected: End (Rejected) in Employee lane.

---

## Level 2: Complex Process
**Test 2.1 – Invoice Processing**  
Prompt:
> Create a BPMN process for "Invoice Processing" with 3 lanes: Vendor, Accounts Payable, Finance Manager.  
> Vendor submits invoice.  
> Accounts Payable validates invoice (gateway: valid/invalid).  
> If invalid: return to vendor, end.  
> If valid: Finance Manager approves (gateway: approve/reject).  
> If approved: Accounts Payable processes payment -> End.  
> If rejected: notify vendor -> End.

---

## Level 3: Medium (Multiple Tasks per Lane)
**Test 3.1 – Hiring Process**  
Prompt:
> Create a BPMN process for "Job Application" with 2 lanes: Candidate, HR.  
> Candidate submits application.  
> HR reviews application (gateway: Qualified/Unqualified).  
> If Unqualified: End Rejected.  
> If Qualified: HR schedules interview -> HR conducts interview -> End Complete.

**Test 3.2 – Order Processing**  
Prompt:
> Create a BPMN process for "Online Order" with 2 lanes: Customer, Warehouse.  
> Customer places order.  
> Warehouse checks stock (gateway: InStock/OutOfStock).  
> If OutOfStock: End Cancelled.  
> If InStock: Warehouse picks items -> Warehouse ships order -> End Shipped.

---

## Level 4: Three Lanes
**Test 4.1 – Expense Claim**  
Prompt:
> Create a BPMN process for "Expense Claim" with 3 lanes: Employee, Manager, Finance.  
> Employee submits expense.  
> Manager approves (gateway: Approved/Rejected).  
> If Rejected: End Rejected.  
> If Approved: Finance processes payment -> End Paid.

**Test 4.2 – Bug Report**  
Prompt:
> Create a BPMN process for "Bug Report" with 3 lanes: User, Developer, QA.  
> User reports bug.  
> Developer fixes bug.  
> QA tests fix (gateway: Pass/Fail).  
> If Fail: End Reopen.  
> If Pass: End Closed.

---

## Level 5: Multiple Gateways
**Test 5.1 – Loan Application**  
Prompt:
> Create a BPMN process for "Loan Application" with 3 lanes: Customer, Bank Clerk, Manager.  
> Customer submits application.  
> Bank Clerk checks documents (gateway: Complete/Incomplete).  
> If Incomplete: End Incomplete.  
> If Complete: Manager reviews (gateway: Approved/Rejected).  
> If Rejected: End Rejected.  
> If Approved: Bank Clerk issues loan -> End Approved.

**Test 5.2 – Invoice Processing (Reference)**  
Prompt:
> Create a BPMN process for "Invoice Processing" with 3 lanes: Vendor, Accounts Payable, Finance Manager.  
> Vendor submits invoice.  
> Accounts Payable validates (gateway: Valid/Invalid).  
> If Invalid: End Invalid.  
> If Valid: Finance Manager approves (gateway: Approved/Rejected).  
> If Approved: Accounts Payable processes payment -> End Paid.  
> If Rejected: Accounts Payable notifies vendor -> End Rejected.

---

## Level 6: Service Tasks (Automated)
**Test 6.1 – Email Notification**  
Prompt:
> Create a BPMN process for "Password Reset" with 2 lanes: User, System.  
> User requests reset (UserTask).  
> System generates token (ServiceTask).  
> System sends email (ServiceTask).  
> User sets new password (UserTask).  
> End.

**Test 6.2 – Mixed Tasks**  
Prompt:
> Create a BPMN process for "Order Confirmation" with 2 lanes: Customer, System.  
> Customer places order (UserTask).  
> System validates payment (ServiceTask) - gateway: Success/Failed.  
> If Failed: End Failed.  
> If Success: System sends confirmation (ServiceTask) -> End Complete.

---

## Level 7: Data Objects (Documents/Data)
**Test 7.1 – Document Review**  
Prompt:
> Create a BPMN process for "Document Review" with 2 lanes: Author, Reviewer.  
> Author writes document (produces "Draft Document" data object).  
> Reviewer reviews document (consumes "Draft Document").  
> Reviewer adds comments (produces "Review Comments" data object).  
> Author revises document (consumes "Review Comments", produces "Final Document").  
> End.

**Test 7.2 – Contract Approval**  
Prompt:
> Create a BPMN process for "Contract Approval" with 3 lanes: Sales, Legal, Customer.  
> Sales creates contract (produces "Draft Contract" data object).  
> Legal reviews contract (consumes "Draft Contract").  
> Legal approves (gateway: Approved/NeedsRevision).  
> If NeedsRevision: Sales revises -> loop back to Legal.  
> If Approved: Legal produces "Approved Contract" data object.  
> Customer signs contract (consumes "Approved Contract", produces "Signed Contract").  
> End.

**Test 7.3 – Invoice with Documents**  
Prompt:
> Create a BPMN process for "Invoice Processing" with 3 lanes: Vendor, Accounts Payable, Finance.  
> Vendor submits invoice (produces "Invoice" data object).  
> Accounts Payable validates invoice (consumes "Invoice").  
> Gateway: Valid/Invalid.  
> If Invalid: End.  
> If Valid: Finance approves (gateway: Approved/Rejected).  
> If Approved: Accounts Payable creates payment (produces "Payment Record") -> End.  
> If Rejected: End.

**Test 7.4 – Report Generation**  
Prompt:
> Create a BPMN process for "Monthly Report" with 2 lanes: Analyst, Manager.  
> Analyst gathers data (produces "Raw Data" data object).  
> Analyst creates report (consumes "Raw Data", produces "Draft Report").  
> Manager reviews report (consumes "Draft Report").  
> Gateway: Approved/Revise.  
> If Revise: back to Analyst.  
> If Approved: Manager publishes (produces "Final Report") -> End.

---

## Level 8: Open-Ended Creative Prompts

These prompts test the LLM's ability to design complete processes from minimal guidance. The AI should determine appropriate lanes, tasks, gateways, and data objects.

**Test 8.1 – Office Furniture Order**  
Prompt:
> Design a BPMN process for ordering office furniture. Include approval workflow and delivery tracking.

**Test 8.2 – Employee Onboarding**  
Prompt:
> Create a BPMN process for onboarding a new employee. Consider IT setup, HR paperwork, and team introduction.

**Test 8.3 – Product Return**  
Prompt:
> Design a BPMN process for handling product returns in an e-commerce company. Include quality inspection and refund processing.

**Test 8.4 – Conference Room Booking**  
Prompt:
> Create a BPMN process for booking a conference room with equipment requests and catering.

**Test 8.5 – Software Release**  
Prompt:
> Design a BPMN process for releasing a software update. Include code review, testing, and deployment stages.

**Test 8.6 – Travel Request**  
Prompt:
> Create a BPMN process for requesting business travel. Include budget approval, booking, and expense reporting.

**Test 8.7 – Customer Complaint**  
Prompt:
> Design a BPMN process for handling customer complaints. Include investigation, resolution, and follow-up.

**Test 8.8 – Inventory Reorder**  
Prompt:
> Create a BPMN process for automatic inventory reordering when stock falls below threshold.

**Test 8.9 – Job Posting**  
Prompt:
> Design a BPMN process for creating and publishing a job posting. Include drafting, approval, and multi-channel publication.

**Test 8.10 – Maintenance Request**  
Prompt:
> Create a BPMN process for facility maintenance requests. Include priority assessment and technician dispatch.

---

## Level 9: Complex Open-Ended (Advanced)

These prompts require the AI to handle multiple decision points, parallel work, and data flow.

**Test 9.1 – Procurement Process**  
Prompt:
> Design a complete procurement process from purchase request to delivery. Include vendor selection, quotes comparison, approval hierarchy, and goods receipt.

**Test 9.2 – Insurance Claim**  
Prompt:
> Create a BPMN process for processing an insurance claim. Include initial filing, documentation review, investigation if needed, approval/denial, and payment.

**Test 9.3 – Project Kickoff**  
Prompt:
> Design a BPMN process for starting a new project. Include stakeholder identification, resource allocation, kickoff meeting, and project charter creation.

**Test 9.4 – Audit Process**  
Prompt:
> Create a BPMN process for conducting an internal audit. Include planning, fieldwork, findings documentation, and report issuance.

**Test 9.5 – Vendor Onboarding**  
Prompt:
> Design a BPMN process for onboarding a new vendor. Include due diligence, contract negotiation, system setup, and first order.

---

## Testing Checklist

### Basic Rules
- Functions: Only `createUserTask(process, name)` — no extra params
- Gateways: Short names, e.g., "Valid?" not "Validation: Valid/Invalid"
- End events: No outgoing flows from End events
- Name matching: `flowDefs` names must equal `elementRefs` keys
- Guards: Simple labels, e.g., "Approved" not "(Guard: Approved)"

### Data Objects (v2.1+)
- Data objects placed in correct lane
- Position is "above" or "below" (lowercase)
- Column aligns with producing task
- Associations use "input" or "output" (lowercase)
- "output": Task produces data (Task → Data)
- "input": Task consumes data (Data → Task)

### Open-Ended Prompts
- AI should determine reasonable lanes (2-4 typical)
- Process should have clear start and end
- Decision points should have meaningful guards
- Data objects should represent real documents/data when appropriate

---

## Recommended Test Order

### Structured Tests
1. Test 1.1 (simplest)
2. Test 2.1 (adds gateway)
3. Test 4.1 (adds third lane)
4. Test 5.1 (multiple gateways)
5. Test 6.1 (service tasks)
6. Test 7.1 (data objects)
7. Test 7.3 (data objects with gateways)

### Open-Ended Tests
1. Test 8.1 (office furniture - simple creative)
2. Test 8.2 (onboarding - multiple lanes)
3. Test 8.5 (software release - technical)
4. Test 9.1 (procurement - complex)

---

## Expected Quality Indicators

### Good Output
- Logical lane assignments (actors/departments)
- Appropriate task types (User vs Service vs Manual)
- Clear decision points with Yes/No or specific outcomes
- Data objects for important documents
- Reasonable column layout (left to right flow)

### Common Issues
- Too many lanes (keep to 2-4)
- Overly complex gateway names
- Missing flows between elements
- Data objects without associations
- Quoted element types ("USER_TASK" instead of USER_TASK)