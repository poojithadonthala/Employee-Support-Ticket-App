# PRODUCT PROMPT
# Employee Support Ticket Management Application

## 1. PROJECT OVERVIEW

Build a web-based Employee Support Ticket Management Application that allows employees to raise workplace and technical support requests, monitor their status and update their requests.

Support staff should be able to view all submitted employee tickets and manage their status until resolution.

The application must provide secure authentication, role-based access, ticket management, data validation and a simple, professional user interface.

The initial implementation must contain only the core ticket management functionality. Ticket commenting must be introduced later as a separate feature enhancement.

---

## 2. PROBLEM STATEMENT

Employees frequently encounter technical and workplace-related problems, such as laptop issues, network connectivity failures, software crashes and access requests.

Without a centralized support ticket system, employees may find it difficult to report problems, monitor progress and know whether their requests have been resolved.

Support staff also need an organized platform to view, manage and update employee support requests.

The proposed application provides a centralized system where employees can submit and track support tickets, while support staff can manage requests and update their resolution status.

---

## 3. OBJECTIVES

1. Provide employees with a simple platform to submit support requests.
2. Allow employees to monitor their own ticket status.
3. Allow employees to update their requests when permitted.
4. Enable support staff to view and manage all submitted tickets.
5. Ensure only authorized support staff can change ticket status.
6. Protect employee ticket information using role-based access control.
7. Maintain accurate ticket creation and modification information.
8. Provide persistent storage and reliable ticket management.

---

## 4. USER ROLES

The application must support exactly two user roles.

### 4.1 Employee

Employees must be able to:

- Register through a public registration page.
- Log in using their email and password.
- Access their employee dashboard.
- Create support tickets.
- View only their own submitted tickets.
- View individual ticket details.
- Track the current ticket status.
- Update their own ticket information when permitted.
- View ticket creation and last updated dates.
- Log out securely.

Employees must NOT be able to:

- View another employee's tickets.
- Access the support staff dashboard.
- Change ticket status.
- Register themselves as Support Staff.
- Change their assigned role.
- Modify automatically generated ticket information.
- Access restricted support staff APIs.

### 4.2 Support Staff

Support staff must be able to:

- Log in using an authorized support staff account.
- Access the support staff dashboard.
- View all employee tickets.
- View individual ticket details.
- Search and filter tickets.
- Update ticket status.
- View the employee who created each ticket.
- View ticket creation and last updated information.
- Log out securely.

Support staff can manage ticket status but must not modify the original creator or creation date.

---

## 5. AUTHENTICATION AND ROLE ASSIGNMENT

Implement a secure authentication system with backend-controlled role assignment.

### 5.1 Common Login Page

Use one common login page for both user roles.

Login fields:
- Email
- Password

Do not provide an Employee or Support Staff role selector during login.

After successful login:

1. The backend verifies the user's email and password.
2. The backend retrieves the user's actual role from the database.
3. The backend creates a secure authenticated session or token.
4. The frontend redirects the user according to the verified role.

Redirection:
- Employee → Employee Dashboard.
- Support Staff → Support Staff Dashboard.

The frontend must never decide or assign the authenticated user's role.

### 5.2 Employee Registration

Provide a public employee registration page.

Registration fields:
- Full name
- Email
- Password
- Confirm password

Rules:
- Public registration must create Employee accounts only.
- The backend must automatically assign the Employee role.
- Do not provide a role selection field.
- Ignore or reject any role value submitted by the client.
- Prevent duplicate email registrations.
- Validate all registration fields.
- Store passwords using secure password hashing.

### 5.3 Support Staff Account Creation

Support Staff accounts must not be created through public registration.

Provide a secure backend initialization or authorized administrator-only process to create support staff accounts.

For the lab demonstration:
- Support an initial Support Staff account through a controlled initialization process.
- Do not expose support staff registration publicly.
- Do not hardcode support staff passwords in source code.
- Use environment variables or secure interactive initialization for credentials.
- Prevent ordinary employees from promoting themselves to Support Staff.

### 5.4 Authentication Security

- Implement secure password hashing.
- Never store plain-text passwords.
- Never expose password hashes through API responses.
- Protect authenticated routes and API endpoints.
- Verify sessions or tokens on the backend.
- Implement appropriate logout and session/token invalidation.
- Store sensitive configuration in environment variables.
- Add secret-containing files to .gitignore.
- Never commit passwords, API keys or secret values to Git.

---

## 6. TICKET MANAGEMENT

### 6.1 Ticket Creation

Employees must be able to create tickets by providing:

- Title
- Description
- Category
- Priority

The application must validate these fields before saving a ticket.

### 6.2 Detailed Ticket Data Structure

Every ticket must store exactly the following required information:

| Detail | Example | Who fills it |
|---|---|---|
| Title (required, maximum 100 characters) | Laptop not charging | Employee |
| Description (required) | My laptop shows 0% even when plugged in | Employee |
| Category | Hardware | Employee selects from a list |
| Priority | High | Employee selects from a list |
| Status | Open | Application assigns automatically; Support Staff can change it |
| Created by | Ravi | Application fills automatically |
| Created date | 18 Nov 2026 | Application fills automatically |
| Last updated date | 18 Nov 2026 | Application updates on every change |

### 6.3 Field-Level Validation and Behavior

#### Title
- Required.
- Maximum 100 characters.
- Must not be empty or contain only whitespace.
- Entered by the employee.

#### Description
- Required.
- Must not be empty or contain only whitespace.
- Entered by the employee.

#### Category
The employee must select one predefined option:

- Hardware
- Software
- Network
- Access
- Other

Do not accept arbitrary category values.

#### Priority
The employee must select one predefined option:

- Low
- Medium
- High

Do not accept arbitrary priority values.

#### Status
Supported statuses:

1. Open
2. In Progress
3. Resolved
4. Closed

Rules:
- Every newly created ticket must automatically receive Open status.
- Employees can view status but cannot change it.
- Only authenticated Support Staff can change ticket status.
- Status must not be accepted as an editable field during employee ticket creation or editing.
- The backend must validate every status update.

#### Created By
- Automatically retrieve the authenticated user's identity.
- Do not allow employees to enter or modify this field.
- Link the ticket to the actual user record.
- Keep the creator unchanged throughout the ticket lifecycle.

#### Created Date
- Automatically generate when the ticket is created.
- Do not allow manual entry or editing.
- Keep the original creation date unchanged after updates.
- Display in a readable format, such as 18 Nov 2026.

#### Last Updated Date
- Automatically generate when the ticket is created.
- Update whenever ticket information or status changes successfully.
- Generate the timestamp on the backend.
- Do not allow manual editing.
- Display in a readable format, such as 18 Nov 2026.

### 6.4 Ticket Data Integrity

- Every ticket must have a unique identifier.
- All eight required fields must be stored and associated with the correct ticket.
- The Created By field must reference the authenticated user.
- Created Date and Created By must remain unchanged.
- Last Updated Date must change after every successful modification.
- Failed or unauthorized operations must not modify ticket information or timestamps.
- Store timestamps consistently in UTC and display them in a readable local format.

---

## 7. TICKET VIEWING

### Employee

- Display only tickets belonging to the authenticated employee.
- Provide a ticket list.
- Display title, category, priority, status and created date.
- Allow the employee to open individual ticket details.
- Display all eight ticket fields in the ticket detail view.

### Support Staff

- Display tickets from all employees.
- Show the creator's name.
- Display title, category, priority, status and dates.
- Allow support staff to open individual ticket details.
- Display all eight ticket fields.

The backend must enforce ticket ownership and access restrictions.

---

## 8. TICKET UPDATING

### Employee Ticket Updates

Employees may update their own tickets when the status is not Closed.

Permitted fields:
- Title
- Description
- Category
- Priority

Restrictions:
- Employees cannot change status.
- Employees cannot edit another employee's ticket.
- Employees cannot modify Created By.
- Employees cannot modify Created Date.
- Employees cannot manually modify Last Updated Date.
- Closed tickets cannot be edited.

### Support Staff Ticket Updates

Support staff can change the status of tickets.

- Support staff can update status for any ticket.
- Support staff cannot change the original creator or creation date.
- Support staff cannot use the normal ticket-editing operation to modify employee-submitted ticket content.
- Last Updated Date must update after a successful status change.

---

## 9. TICKET STATUS MANAGEMENT

The ticket lifecycle must follow the specified sequence:

Open → In Progress → Resolved → Closed

Status responsibilities:

| Status | Meaning |
|---|---|
| Open | Newly submitted ticket awaiting attention |
| In Progress | Support staff is working on the ticket |
| Resolved | The reported issue has been resolved |
| Closed | Ticket processing is complete |

Rules:
- Initial status is Open.
- Only Support Staff can change status.
- Employees can only view status.
- Status changes must be stored in the database.
- Last Updated Date must update after a successful status change.
- Closed tickets cannot be edited.

Do not introduce additional statuses without approval.

---

## 10. BUSINESS RULES AND ACCESS CONTROL

The following rules are mandatory:

1. Only authenticated users can access protected application features.
2. Employees can access only their own tickets.
3. Support Staff can view all employee tickets.
4. Only Support Staff can change ticket status.
5. Employees cannot register as Support Staff.
6. Users cannot modify their own assigned roles.
7. Closed tickets cannot be edited.
8. Ticket title cannot be empty and must not exceed 100 characters.
9. Ticket description cannot be empty.
10. Category must belong to the predefined category list.
11. Priority must belong to the predefined priority list.
12. Every new ticket must start with Open status.
13. Created By must be automatically assigned.
14. Created Date must be automatically generated and remain unchanged.
15. Last Updated Date must be automatically maintained.
16. Frontend access restrictions must also be enforced by backend authorization.
17. Direct API requests must not bypass role restrictions.
18. Unauthorized actions must be rejected.
19. Invalid input must not be stored.
20. Failed operations must not produce false success messages or update timestamps.

### Backend Authorization Examples

If an employee tries to access another employee's ticket, reject the request.

If an employee directly calls the ticket status-update API, reject the request with HTTP 403 Forbidden.

If an unauthenticated user tries to access a protected endpoint, return HTTP 401 Unauthorized.

If an employee attempts to access the support dashboard, deny access.

Never depend only on hidden frontend buttons for security.

---

## 11. SAMPLE DATA

Use only the fictional sample data supplied below for development and demonstration.

### 11.1 Sample Users

Employee:
- Name: Ravi
- Email: ravi@company.com
- Role: Employee

Support Staff:
- Name: Support Admin
- Email: support@company.com
- Role: Support Staff

These are demonstration identities, not actual credentials.

Create sample accounts through a controlled database seed or initialization process. Do not embed known passwords in source code.

### 11.2 Sample Tickets

| No. | Title | Category | Priority | Status |
|---|---|---|---|---|
| 1 | Laptop not charging | Hardware | High | Open |
| 2 | Cannot log in to VPN | Network | High | In Progress |
| 3 | Need access to the shared project folder | Access | Medium | Open |
| 4 | Excel keeps crashing on startup | Software | Medium | Resolved |
| 5 | Request a second monitor | Hardware | Low | Closed |

### 11.3 Sample Ticket Details

Title: Laptop not charging

Description: My laptop shows 0% even when plugged in.

Category: Hardware

Priority: High

Status: Open

Created By: Ravi

Created Date: 18 Nov 2026

Last Updated Date: 18 Nov 2026

The application must support all five sample tickets and their specified statuses.

Sample tickets must be inserted through a controlled seeding process, not hardcoded as fake frontend records.

---

## 12. DASHBOARD REQUIREMENTS

### 12.1 Employee Dashboard

Display:
- Total tickets submitted by the employee.
- Open tickets.
- In Progress tickets.
- Resolved tickets.
- Closed tickets.
- Recent tickets.
- Ticket creation option.

Provide clear ticket status and priority indicators.

All dashboard information must come from the authenticated employee's actual database records.

### 12.2 Support Staff Dashboard

Display:
- Total employee tickets.
- Open tickets.
- In Progress tickets.
- Resolved tickets.
- Closed tickets.
- All submitted tickets.
- Employee names.
- Ticket management options.

Provide filtering by:
- Status
- Category
- Priority

Provide search functionality for tickets using appropriate ticket information.

Dashboard statistics must be calculated from actual database records.

---

## 13. NON-FUNCTIONAL REQUIREMENTS

### Usability
- Clean, professional and user-friendly interface.
- Separate employee and support staff dashboards.
- Responsive layout.
- Consistent navigation.
- Clear status and priority indicators.
- Appropriate success and error messages.

### Security
- Secure authentication.
- Password hashing.
- Role-based access control.
- Backend authorization.
- Ticket ownership verification.
- Input validation.
- Secure secret management.
- Protection against unauthorized data access.

### Reliability
- Persistent database storage.
- Appropriate error handling.
- Accurate ticket timestamps.
- No false success messages.
- Consistent database operations.

### Maintainability
- Organized project structure.
- Reusable frontend components.
- Separation of frontend, backend, business logic and database responsibilities.
- Readable code.
- Meaningful variable and function names.

### Performance
- Efficient database queries.
- Avoid unnecessary API requests.
- Support smooth ticket listing and filtering for the lab's expected data volume.

---

## 14. PROPOSED TECHNOLOGY STACK

Frontend:
- React
- Vite
- CSS

Backend:
- Python
- FastAPI

Database:
- SQLite

Communication:
- REST APIs

Version Control:
- Git and GitHub

Configuration:
- Environment variables.

These are proposed technologies. Confirm the architecture and implementation choices in PLAN.md before generating code.

---

## 15. PROJECT LIMITATIONS AND OUT-OF-SCOPE FEATURES

The initial implementation must remain focused on employee support ticket management.

Do not implement the following in the initial version:

1. Ticket comments.
2. AI-based ticket classification.
3. AI chatbots.
4. Email notifications.
5. SMS notifications.
6. Payment functionality.
7. Unnecessary enterprise-level functionality.
8. Additional user roles.
9. Unapproved ticket statuses or categories.

Ticket commenting will be implemented later as a separate feature enhancement during the lab exercise.

The initial version must be completed and tested before adding comments.

---

## 16. ACCEPTANCE CRITERIA

The application will be considered functionally complete when the following conditions are satisfied:

### Authentication
- An employee can register and log in.
- A support staff account can be initialized securely.
- Both roles use a common login page.
- The backend identifies the actual role.
- Users reach the correct dashboard.
- An employee cannot become Support Staff through public registration.

### Ticket Creation
- An employee can create a ticket with valid information.
- Empty title and description are rejected.
- Titles longer than 100 characters are rejected.
- Category and priority are restricted to permitted values.
- Status is automatically set to Open.
- Created By and dates are automatically generated.

### Ticket Viewing
- Employees see only their own tickets.
- Support Staff see all tickets.
- Both roles can view ticket details.

### Ticket Updating
- Employees can update permitted fields on their own non-Closed tickets.
- Employees cannot change status.
- Employees cannot edit Closed tickets.
- Support Staff can change ticket status.
- Created By and Created Date remain unchanged.
- Last Updated Date changes after successful updates.

### Security
- An employee cannot access the support dashboard.
- An employee cannot access another employee's ticket.
- An employee cannot change status through direct API requests.
- Unauthenticated requests to protected APIs are rejected.
- Passwords and secrets are not exposed.

### Persistence
- Tickets are stored in the database.
- Tickets remain available after restarting the application.
- Sample tickets can be inserted using the seed process.

### User Interface
- Both dashboards display correct information.
- Navigation works.
- Forms provide validation feedback.
- Application is responsive.
- Visible buttons perform their intended actions.

---

## 17. EXPECTED FINAL DELIVERABLE

Deliver a working Employee Support Ticket Management Application with:

- Employee registration and login.
- Secure Support Staff account initialization.
- Role-based dashboards.
- Employee ticket creation.
- Employee ticket viewing and permitted updating.
- Support Staff ticket viewing and status management.
- Correct storage of all eight ticket fields.
- Backend authorization and validation.
- SQLite database persistence.
- Sample demonstration data.
- Organized source code.
- A clear README with installation and execution instructions.

The project must be runnable locally and suitable for a live demonstration.

---

## 18. INSTRUCTIONS TO AI

First read and understand this entire product prompt.

Do not generate application code.

Your immediate task is to create a detailed Software Requirements Specification.

Save it as SPEC.md.

The specification must include:

1. Project overview.
2. Problem statement and objectives.
3. User roles and permissions.
4. Functional requirements with unique IDs.
5. Non-functional requirements.
6. Detailed eight-field ticket data structure.
7. Field ownership and validation rules.
8. Authentication and role assignment.
9. Ticket creation, viewing and updating workflows.
10. Ticket status management.
11. Business rules and authorization.
12. Database entities and relationships.
13. API requirements.
14. Error handling.
15. Security requirements.
16. Acceptance criteria.
17. Out-of-scope features.
18. Assumptions and unresolved technical decisions.

Clearly distinguish confirmed requirements from assumptions.

Do not silently invent functionality or change the supplied sample data.

Do not include ticket commenting in the initial implementation scope.

Do not generate code or modify application files.

Wait for my review and explicit approval of SPEC.md before generating PLAN.md.