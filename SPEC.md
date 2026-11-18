# Software Requirements Specification

## Employee Support Ticket Management Application

| Item | Detail |
|---|---|
| Document | SPEC.md |
| Status | Final draft — awaiting implementation approval |
| Source | Product prompt in this project (`PRODUCT_PROMPT.md`), plus review decisions in section 1.5 |
| Audience | Beginner-level implementation and lab demonstration |
| Date | 18 Nov 2026 |
| Revision | Review decisions RD-01 through RD-16 applied. All product open questions resolved in section 20. |

This specification contains two kinds of statements:

- **Original requirement:** behavior stated in the product prompt. Statements that are not marked as a review decision are original requirements.
- **Review decision:** a choice added during review. Each review decision resolves a gap in the product prompt or adds an approved requirement. Review decisions are now requirements. They are marked **Review decision RD-xx** where they change behavior, and they are collected in section 1.5.

All product open questions have now been resolved; section 20 records that no product questions remain. Technical choices the prompt defers to a later plan are listed in section 19, Unresolved Technical Decisions.

No application code is authorized by this document. Implementation starts only after this specification is reviewed and explicitly approved, and only after a separate plan document is approved.

---

## 1. Project Overview

The project is a web-based Employee Support Ticket Management Application. Employees use it to raise workplace and technical support requests, monitor status, and update their own requests when the rules allow. Support staff use it to view all submitted tickets and manage status until resolution.

The application provides:

- Secure authentication
- Role-based access for exactly two roles
- Ticket management
- Data validation
- A simple, professional user interface
- Persistent storage

The first version contains only core ticket management. Ticket commenting is a later, separate enhancement. The finished application must run locally and be suitable for a live demonstration.

### 1.1 Problem Statement

Employees often face technical and workplace problems, including laptop issues, network connectivity failures, software crashes, and access requests. Without a centralized support ticket system, employees have difficulty reporting problems, monitoring progress, and knowing whether a request has been resolved. Support staff also need an organized way to view, manage, and update those requests.

The application is that centralized system.

### 1.2 Objectives

1. Provide employees with a simple platform to submit support requests.
2. Allow employees to monitor their own ticket status.
3. Allow employees to update their requests when permitted.
4. Enable support staff to view and manage all submitted tickets.
5. Ensure only authorized support staff can change ticket status.
6. Protect employee ticket information using role-based access control.
7. Maintain accurate ticket creation and modification information.
8. Provide persistent storage and reliable ticket management.

### 1.3 In-Scope Summary

The initial version includes:

- Public employee registration and a common login page
- Secure initialization of support staff accounts
- Employee and support staff dashboards
- Employee ticket creation, viewing, and permitted updates
- Support staff viewing of all tickets, search, filter, and status updates
- Storage of all eight ticket fields, plus a unique ticket identifier
- Backend authorization and validation
- Persistent database storage
- Fictional sample data loaded by a controlled seed or initialization process
- A README with installation and execution instructions

Ticket comments are not part of this initial version. Section 16 records that exclusion. Reopening a Closed ticket is also outside the initial version.

### 1.4 How to tell the two kinds of requirements apart

| Mark in this document | Meaning |
|---|---|
| No review-decision mark | Original requirement from the product prompt. |
| **Review decision RD-xx** | Added or made definite during this review. The original requirement remains in place. The review decision fills the gap or resolves the conflict. |

A review decision does not delete an original requirement. Where the two meet, the review decision states the rule that implementation must follow.

### 1.5 Review Decisions

These decisions were requested in review. They are requirements of this revised specification.

| ID | Resolved question | Decision |
|---|---|---|
| RD-01 | Former OQ-01, status transitions | The only legal status path is Open → In Progress → Resolved → Closed, one step at a time. Closed is final. Support staff cannot reopen a Closed ticket unless a future approved feature allows it. |
| RD-02 | Former OQ-02, registration validation | Confirm password must match password. Email must use the format in section 3.2. Password minimum length is 8 characters. Full name must not be empty. |
| RD-03 | Former OQ-03, HTTP responses | Authentication failures return HTTP 401. Authorization failures return HTTP 403. Invalid input returns HTTP 400. A missing ticket returns HTTP 404. Section 12.3 states the situations and the check order. |
| RD-04 | Former OQ-05 and OQ-06, timestamp display | Timestamps are stored in UTC. Created Date and Last Updated Date are displayed as a date and a time in the Asia/Kolkata time zone. |
| RD-05 | Former OQ-08, support staff search | Search covers ticket title, description, and creator name. Filters remain status, category, and priority. |
| RD-06 | Former OQ-09, sample tickets | Section 14 completes the five sample tickets. Values the product prompt did not supply are labelled as fictional demonstration values. Supplied titles, categories, priorities, and statuses are unchanged. |
| RD-07 | Edit permissions, clarified in review | An employee can edit their own ticket only when it is not Closed, and only the employee-submitted fields. Support Staff can update status only. They cannot change employee-submitted ticket content. |
| RD-08 | Ticket comments, confirmed in review | Ticket comments stay completely out of the initial implementation. They are a later, separate enhancement. |
| RD-09 | Former OQ-04, description length | Ticket description has a maximum of 2,000 characters. The limit is applied after surrounding whitespace is trimmed. |
| RD-10 | Former OQ-07, recent tickets | The employee dashboard shows the latest 5 tickets by Created Date, newest first. If the employee has fewer than 5 tickets, all of them are shown. |
| RD-11 | Former OQ-10, whitespace handling | Surrounding whitespace is trimmed from full names, emails, ticket titles, and ticket descriptions before validation and storage. Passwords are never trimmed, and confirm password is compared exactly with the password as submitted. |
| RD-12 | Former OQ-11, email case handling | Email uniqueness checks and login email comparisons are case-insensitive. Emails are stored in a consistently normalized format: trimmed and converted to lowercase. |
| RD-13 | User capacity and support staff creation | There is no arbitrary fixed maximum on the number of registered Employee accounts. Support Staff accounts are created only through the approved secure initialization process or an authorized administrative process. There is no public Support Staff registration option. |
| RD-14 | User interface quality | The interface is attractive, modern, clean, and professional. It uses large, readable fonts, clear visual hierarchy, consistent spacing, alignment, colors, and component styling. Layouts adapt properly to desktop, tablet, and mobile screens, use available screen space effectively, and avoid unwanted horizontal scrolling, clipped content, and overlapping elements. Forms, tables, dashboards, navigation, and feedback messages are easy to understand and use. Duplicate information and unnecessary UI elements are avoided. |
| RD-15 | Database reliability | Database configuration and connection management are clearly defined and organized. Connection failures and transaction errors are handled safely so partial or inconsistent changes are not saved. Successful changes are persisted. Appropriate relationships, constraints, and validation maintain data integrity and prevent accidental data loss. Database access is organized rather than scattered through the application, and database credentials or secrets are never exposed in source code. |
| RD-16 | Functional completeness | Every visible button, form, link, filter, and navigation control performs its intended action. Clear success, validation, and error feedback is provided. Placeholder functionality and decorative controls that appear operational but do nothing are not included. All implemented features work with the backend and database as specified. |

---

## 2. User Roles and Permissions

The application supports exactly two roles: **Employee** and **Support Staff**.

The backend stores and assigns each user’s role. A user cannot change their own role. Public registration cannot create a Support Staff account or assign any role other than Employee.

### 2.1 Employee

An employee can:

- Register on a public registration page
- Log in with email and password
- Open the employee dashboard
- Create support tickets
- View only tickets they submitted
- Open an individual ticket and see all eight ticket fields
- Track the current status
- Update title, description, category, and priority on their own ticket only when that ticket is not Closed
- View the created date and the last updated date
- Log out securely

An employee cannot:

- View another employee’s tickets
- Open the support staff dashboard
- Change ticket status
- Register as Support Staff
- Change their assigned role
- Modify automatically generated ticket information
- Call restricted support staff APIs successfully

### 2.2 Support Staff

A support staff user can:

- Log in with an authorized support staff account
- Open the support staff dashboard
- View all employee tickets
- Open an individual ticket and see all eight ticket fields
- Search and filter tickets
- Update ticket status
- See the employee who created each ticket
- View creation and last updated information
- Log out securely

A support staff user manages status. They do not modify the original creator or the creation date. They do not modify employee-submitted ticket content. Employee-submitted content is the title, description, category, and priority.

**Review decision RD-07.** Support Staff update status only. They have no operation that changes title, description, category, or priority. An employee can edit those four fields only on a ticket they created, and only while its status is not Closed.

Support staff accounts are not created on the public registration page. The product prompt does not give support staff permission to create tickets.

**Review decision RD-13.** There is no arbitrary fixed maximum on the number of registered Employee accounts. Support Staff accounts are created only through the approved secure initialization process or an authorized administrative process. No public Support Staff registration option is provided.

### 2.3 Permission Matrix

| Action | Unauthenticated visitor | Employee | Support Staff |
|---|---|---|---|
| Open the public registration page | Yes | Not required | Not required |
| Register an Employee account | Yes | No self-service role change | No public staff registration |
| Register a Support Staff account | No | No | No |
| Log in on the common login page | Yes | Yes | Yes |
| Open the employee dashboard | No | Yes | No |
| Open the support staff dashboard | No | No | Yes |
| Create a ticket | No | Yes | No |
| List own tickets | No | Yes | Not a separate duty; staff list all tickets |
| List every employee ticket | No | No | Yes |
| View a ticket’s full details | No | Own tickets only | Any ticket |
| Edit title, description, category, and priority | No | Own ticket, and only when status is not Closed | No. Status update does not change these fields (Review decision RD-07). |
| Change status | No | No | Yes, but only one step forward along Open → In Progress → Resolved → Closed. A Closed ticket cannot be reopened (Review decision RD-01). |
| Change Created By or Created Date | No | No | No |
| Change Last Updated Date manually | No | No | No |
| Change own role | No | No | No |
| Log out | No | Yes | Yes |

---

## 3. Authentication and Role-Based Access Control

Authentication is secure, and role assignment is controlled by the backend.

### 3.1 Common Login

Both roles use one login page. The page has two fields:

- Email
- Password

The login page has no Employee or Support Staff selector.

**Review decision RD-12.** Login emails are compared case-insensitively by normalizing the submitted email to trimmed lowercase before lookup. **Review decision RD-11.** Passwords are compared exactly as submitted and are never trimmed.

After a successful login, the system behaves in this order:

1. The backend verifies the email and password.
2. The backend reads the user’s actual role from the database.
3. The backend creates a secure authenticated session or token.
4. The frontend redirects the user according to that verified role.

Redirection:

- Employee → Employee Dashboard
- Support Staff → Support Staff Dashboard

The frontend never decides or assigns the authenticated user’s role.

Whether the authenticated state is a server session or a token is an unresolved technical decision (section 19). Either approach must be verified on the backend and invalidated on logout.

### 3.2 Employee Registration

The registration page is public and contains:

- Full name
- Email
- Password
- Confirm password

Confirmed registration rules:

- Public registration creates Employee accounts only.
- The backend assigns the Employee role automatically.
- The form has no role selection field.
- If the client submits a role value, the backend ignores or rejects it. The submitted role is never applied.
- Duplicate email registrations are prevented.
- All registration fields are validated.
- Passwords are stored with secure password hashing.

The product prompt requires those checks and does not define the field rules. **Review decision RD-02** defines them as follows:

- Full name is required. It must contain at least one character that is not whitespace.
- Email is required and must have a valid format, defined below.
- Password is required and must contain at least 8 characters.
- Confirm password is required and must match password exactly.
- This review does not add password complexity rules, a maximum password length, or a maximum full-name length. Those limits are not requirements.
- **Review decision RD-11.** Surrounding whitespace is trimmed from the full name and email before validation and storage. Passwords are never trimmed. Password length and confirm-password comparison use the submitted characters exactly.
- **Review decision RD-12.** Email uniqueness checks and login comparisons are case-insensitive. The stored email is normalized to trimmed lowercase.

A valid email format, for this project, means all of the following:

- The value contains exactly one `@`.
- The text before `@` is not empty and contains no spaces.
- The text after `@` is not empty, contains no spaces, and contains at least one `.`.
- The text after `@` does not start or end with `.`.
- Each side of that `.` contains at least one character.

This is a simple project rule for beginners. It is not a claim that the check implements every detail of the email standards.

### 3.3 Support Staff Account Creation

Support Staff accounts are created only through a secure backend initialization process or an authorized administrator-only process.

For the lab demonstration:

- An initial Support Staff account is created through a controlled initialization process.
- Support staff registration is not public.
- Support staff passwords are not hardcoded in source code.
- Credentials come from environment variables or from secure interactive initialization.
- An ordinary employee cannot promote themselves to Support Staff.

The sample identities in section 14 are demonstration identities, not credentials, and they are not known passwords.

### 3.4 Session Protection

- Authenticated routes and API endpoints are protected.
- The backend verifies the session or token.
- Logout invalidates the session or token.
- Sensitive configuration is stored in environment variables.
- Files that contain secrets are listed in `.gitignore`.
- Passwords, API keys, and secret values are never committed to Git.

### 3.5 Authorization Principle

Frontend restrictions and backend authorization both apply. Hiding a button is not sufficient. A direct API request must not bypass role restrictions.

Original HTTP results from the product prompt:

- An unauthenticated request to a protected endpoint returns **HTTP 401 Unauthorized**.
- An employee who calls the ticket status-update API is rejected with **HTTP 403 Forbidden**.
- An employee who requests another employee’s ticket is rejected.
- An employee who attempts to open the support dashboard is denied access.

**Review decision RD-03** assigns the remaining refusal codes. The full list and the order of checks are in section 12.3. In short:

- Authentication failure: HTTP 401 Unauthorized.
- Authorization failure, including another employee’s ticket and the support dashboard API: HTTP 403 Forbidden.
- Invalid input: HTTP 400 Bad Request.
- A ticket identifier that does not exist: HTTP 404 Not Found.

---

## 4. Ticket Fields

Every ticket stores exactly these eight required details, plus a unique identifier required by the data-integrity rules. The identifier is system data. It is not a ninth business field and it is not entered by the user.

| # | Field | Required | Who sets it | Who may change it |
|---|---|---|---|---|
| 1 | Title | Yes | Employee | The creating employee, only while the ticket is not Closed |
| 2 | Description | Yes | Employee | The creating employee, only while the ticket is not Closed |
| 3 | Category | Yes | Employee, from a fixed list | The creating employee, only while the ticket is not Closed |
| 4 | Priority | Yes | Employee, from a fixed list | The creating employee, only while the ticket is not Closed |
| 5 | Status | Yes | Application sets Open on creation | Support Staff only, and only by the transitions in section 4.5 (Review decision RD-01) |
| 6 | Created By | Yes | Application, from the authenticated user | Nobody |
| 7 | Created Date | Yes | Application, at creation | Nobody |
| 8 | Last Updated Date | Yes | Application, at creation and after each successful change | Nobody manually; the backend updates it |

### 4.1 Title

- Required.
- Maximum 100 characters, measured after surrounding whitespace is trimmed.
- Must not be empty or contain only whitespace after surrounding whitespace is trimmed.
- Entered by the employee.
- **Review decision RD-11.** Surrounding whitespace is trimmed before validation and storage.

### 4.2 Description

- Required.
- Must not be empty or contain only whitespace after surrounding whitespace is trimmed.
- Entered by the employee.
- The product prompt did not set a maximum length. **Review decision RD-09** sets the maximum to 2,000 characters, measured after trimming.
- **Review decision RD-11.** Surrounding whitespace is trimmed before validation and storage.

### 4.3 Category

The employee selects one of these values:

- Hardware
- Software
- Network
- Access
- Other

Any other category value is rejected.

### 4.4 Priority

The employee selects one of these values:

- Low
- Medium
- High

Any other priority value is rejected.

### 4.5 Status

The only supported statuses are:

1. Open — newly submitted and awaiting attention
2. In Progress — support staff is working on the ticket
3. Resolved — the reported issue has been resolved
4. Closed — ticket processing is complete

Confirmed status rules:

- A newly created ticket receives Open automatically.
- Employees can view status and cannot change it.
- Status is not an editable field during employee ticket creation or employee ticket editing.
- Only an authenticated Support Staff user can change status.
- The backend validates every status update.
- A successful status change is stored in the database.
- A successful status change updates Last Updated Date.
- No additional status may be introduced without approval.

The product prompt states the lifecycle sequence as:

**Open → In Progress → Resolved → Closed**

The prompt also says support staff can update status, and that closed tickets cannot be edited. It does not list each allowed transition. **Review decision RD-01** resolves that conflict.

The only successful status changes are:

| Current status | The only status support staff may set next |
|---|---|
| Open | In Progress |
| In Progress | Resolved |
| Resolved | Closed |
| Closed | None. Closed is final. |

These changes are rejected:

- Skipping a step, such as Open directly to Resolved or Open directly to Closed.
- Moving backward, such as In Progress back to Open.
- Submitting the status the ticket already has.
- Any status change when the ticket is already Closed, including an attempt to reopen it.

Support staff cannot reopen a Closed ticket unless a future approved feature allows it. That feature is out of scope for the initial version (section 16). A rejected status change does not modify the ticket and does not change Last Updated Date.

### 4.6 Created By

- The backend sets this from the authenticated user’s identity.
- The employee cannot enter or modify it.
- The ticket is linked to the actual user record.
- The creator stays the same for the life of the ticket.
- Support staff can see the creator’s name. The product prompt’s display example is the name “Ravi”.

### 4.7 Created Date

- The backend generates it when the ticket is created.
- Manual entry and editing are not allowed.
- The original creation date stays the same after later updates.
- The product prompt’s display example for the date portion is `18 Nov 2026`.

### 4.8 Last Updated Date

- The backend sets it when the ticket is created.
- The backend updates it whenever ticket information or status changes successfully.
- The timestamp is generated on the backend.
- Manual editing is not allowed.
- The product prompt’s display example for the date portion is `18 Nov 2026`.

### 4.8.1 Timestamp storage and display

Original requirement: timestamps are stored consistently in UTC and displayed in a readable local format.

**Review decision RD-04.** Display uses the date and the time, in the Asia/Kolkata time zone (Indian Standard Time, UTC+5:30). This applies everywhere Created Date or Last Updated Date is shown, including lists, ticket details, and both dashboards.

The readable display form keeps the prompt’s date style and adds the time:

`18 Nov 2026, 09:15 AM`

The stored value remains the corresponding UTC timestamp. The screen does not show the raw UTC value.

### 4.9 Identifier and Integrity

- Every ticket has a unique identifier.
- All eight fields are stored and associated with the correct ticket.
- Created By references the authenticated user.
- Created Date and Created By remain unchanged after updates.
- Last Updated Date changes after every successful modification.
- A failed or unauthorized operation does not modify ticket information or timestamps.
- Timestamps are stored consistently in UTC and displayed as a date and time in Asia/Kolkata (Review decision RD-04).

The prompt does not define the identifier format. That remains unresolved technical decision TD-04 in section 19.

---

## 5. Ticket Workflows

### 5.1 Creation

An authenticated employee creates a ticket by providing:

- Title
- Description
- Category
- Priority

The application validates these fields before saving. **Review decision RD-11.** The backend trims surrounding whitespace from title and description before validation and storage. On success, the backend:

- Stores the four submitted fields
- Sets Status to Open
- Sets Created By to the authenticated user
- Sets Created Date
- Sets Last Updated Date
- Assigns a unique identifier

Invalid input is not stored. A failed create does not show a success message.

### 5.2 Viewing

**Employee**

- The list contains only tickets belonging to the authenticated employee.
- The list shows title, category, priority, status, and created date and time (Review decision RD-04).
- The employee can open one ticket.
- The detail view shows all eight fields.
- The backend enforces ownership. A request for another employee’s ticket is rejected.

**Support Staff**

- The list contains tickets from all employees.
- The list shows the creator’s name, title, category, priority, status, and created and last updated date and time (Review decision RD-04).
- Support staff can open one ticket.
- The detail view shows all eight fields.

### 5.3 Employee Update

An employee may update their own ticket when its status is not Closed.

Permitted fields:

- Title
- Description
- Category
- Priority

The same validation rules used at creation apply to these fields.

The employee cannot:

- Change status
- Edit another employee’s ticket
- Modify Created By
- Modify Created Date
- Manually modify Last Updated Date
- Edit a Closed ticket

A successful update refreshes Last Updated Date. Created By and Created Date stay unchanged. A rejected update does not change the ticket or its timestamps and does not report success.

The original rule allows content edits while status is Open, In Progress, or Resolved, because the restriction is “when the status is not Closed.” **Review decision RD-07** confirms that reading. Closed is the only status that blocks an employee’s content edit. A Resolved ticket can still be edited by its creator. The employee still cannot change status.

### 5.4 Support Staff Update

Support staff can change the status of a ticket.

- The status update follows Review decision RD-01. It is not available for a Closed ticket, and it cannot skip or reverse a step.
- Support staff cannot change the original creator or the creation date.
- Support staff cannot modify employee-submitted content: title, description, category, or priority. **Review decision RD-07** confirms that support staff have no other operation that changes those fields.
- A successful status change updates Last Updated Date.
- The backend validates every status update against the four supported statuses and against the transition table in section 4.5.

### 5.5 Status Management

Confirmed behavior:

- New tickets start at Open.
- Only Support Staff can change status.
- Employees can only view status.
- Status changes are stored.
- Last Updated Date updates after a successful status change.
- Employees cannot edit a Closed ticket.
- The lifecycle order is Open, then In Progress, then Resolved, then Closed.
- Additional statuses are out of scope unless later approved.
- **Review decision RD-01.** Only the next step in that order can be saved. Closed is final. Support staff cannot reopen a Closed ticket in this version.
- **Review decision RD-07.** Employee content edits and support staff status updates remain separate operations. A status update does not change title, description, category, or priority. An employee content update does not change status.

---

## 6. Dashboards

Dashboard numbers come from the database for the relevant set of tickets. They are not hardcoded.

### 6.1 Employee Dashboard

The employee dashboard shows:

- Total tickets submitted by that employee
- Count of that employee’s Open tickets
- Count of that employee’s In Progress tickets
- Count of that employee’s Resolved tickets
- Count of that employee’s Closed tickets
- Recent tickets
- A way to create a ticket

It also provides clear status and priority indicators.

All of this information comes from the authenticated employee’s own ticket records.

**Review decision RD-10.** The prompt did not define how many tickets are “recent” or how they are ordered. The employee dashboard displays the latest 5 tickets by Created Date, newest first. If the employee has fewer than 5 tickets, all of them are displayed in that section.

### 6.2 Support Staff Dashboard

The support staff dashboard shows:

- Total employee tickets
- Count of Open tickets
- Count of In Progress tickets
- Count of Resolved tickets
- Count of Closed tickets
- All submitted tickets
- Employee names
- Ticket management options, meaning the ability to open tickets and update status

Support staff can filter by:

- Status
- Category
- Priority

The product prompt requires search and does not name the fields. **Review decision RD-05** defines them:

- Search text is compared with ticket title, description, and creator name.
- The comparison is a case-insensitive substring match. A ticket matches when the search text appears in any one of those three fields.
- Status, category, and priority filters remain available and are separate from search.
- When more than one filter is selected, a ticket must match every selected filter.
- Search and filters apply together. A ticket must match the search text and every selected filter.
- An empty search does not add a text condition. The selected filters still apply.

The employee dashboard requirements do not include search or these filters. This specification does not add them for employees.

---

## 7. Business Rules and Access Restrictions

These rules are mandatory:

1. Only authenticated users can access protected application features.
2. Employees can access only their own tickets.
3. Support Staff can view all employee tickets.
4. Only Support Staff can change ticket status.
5. Employees cannot register as Support Staff.
6. Users cannot modify their own assigned roles.
7. Closed tickets cannot be edited. An employee cannot change title, description, category, or priority on a Closed ticket. **Review decision RD-01:** support staff also cannot change the status of a Closed ticket. Closed is final unless a future approved feature allows reopening.
8. Ticket title cannot be empty and must not exceed 100 characters after surrounding whitespace is trimmed. A title that contains only whitespace is invalid. Surrounding whitespace is trimmed before validation and storage (Review decision RD-11).
9. Ticket description cannot be empty and must not exceed 2,000 characters after surrounding whitespace is trimmed. A description that contains only whitespace is invalid. Surrounding whitespace is trimmed before validation and storage (Review decisions RD-09 and RD-11).
10. Category must belong to the predefined category list.
11. Priority must belong to the predefined priority list.
12. Every new ticket starts with Open status.
13. Created By is assigned automatically from the authenticated user and does not change.
14. Created Date is generated automatically and does not change.
15. Last Updated Date is maintained automatically by the backend.
16. Frontend access restrictions are also enforced by backend authorization.
17. Direct API requests must not bypass role restrictions.
18. Unauthorized actions are rejected.
19. Invalid input is not stored.
20. Failed operations do not produce false success messages and do not update timestamps.
21. **Review decision RD-01.** Status changes only from Open to In Progress, from In Progress to Resolved, and from Resolved to Closed.
22. **Review decision RD-02.** Registration requires a non-empty full name, a valid email format, a password of at least 8 characters, and a confirm password that matches the password.
23. **Review decision RD-04.** Created Date and Last Updated Date are stored in UTC and shown as a date and time in Asia/Kolkata.
24. **Review decision RD-05.** Support staff search covers title, description, and creator name, together with the existing status, category, and priority filters.
25. **Review decision RD-08.** The initial version has no ticket comments.
26. **Review decision RD-09.** Ticket description is limited to 2,000 characters after trimming.
27. **Review decision RD-10.** The employee dashboard shows the latest 5 tickets by Created Date, newest first.
28. **Review decision RD-11.** Full names, emails, ticket titles, and ticket descriptions are trimmed before validation and storage. Passwords are never trimmed, and confirm password is compared exactly.
29. **Review decision RD-12.** Email uniqueness and login email comparisons are case-insensitive. Stored emails are normalized to trimmed lowercase.
30. **Review decision RD-13.** There is no arbitrary fixed maximum on Employee registrations. Support Staff accounts are created only through the approved secure initialization process or an authorized administrative process, never through public registration.
31. **Review decision RD-14.** The interface is attractive, modern, clean, professional, readable, visually well organized, consistent, responsive, and free of horizontal scrolling, clipped content, overlapping elements, duplicate information, and unnecessary UI elements.
32. **Review decision RD-15.** Database configuration and connection management are clear and organized. Connection and transaction errors are handled safely, successful changes are persisted, data integrity is protected by relationships and constraints, and database credentials are not exposed in source code.
33. **Review decision RD-16.** Every visible button, form, link, filter, and navigation control works as intended; feedback is clear; no placeholder or decorative controls appear operational without doing work.

---

## 8. Functional Requirements

Each requirement below is an original requirement unless the row cites a review decision. Review decisions are defined in section 1.5.

### 8.1 Authentication and Accounts

| ID | Requirement |
|---|---|
| FR-01 | The system provides a public employee registration page with full name, email, password, and confirm password. |
| FR-02 | Public registration creates an Employee account only. The backend assigns the Employee role. A client-supplied role is ignored or rejected and is never stored as the account role. |
| FR-03 | The system prevents registration with an email that is already registered. **Review decision RD-12:** uniqueness is case-insensitive and the stored email is normalized to trimmed lowercase. |
| FR-04 | The system validates every registration field before creating an account. **Review decision RD-02:** full name must contain a non-whitespace character; email must match the format in section 3.2; password must be at least 8 characters; confirm password must match password exactly. **Review decision RD-11:** full name and email are trimmed before validation and storage; passwords are never trimmed and confirmation is compared exactly. Invalid registration input is not stored and returns HTTP 400. |
| FR-05 | The system stores passwords only as secure hashes. Plain-text passwords are not stored. Password hashes are not returned in API responses. |
| FR-06 | The system provides one login page for both roles, with email and password, and without a role selector. |
| FR-07 | On successful login, the backend verifies the credentials, reads the stored role, creates an authenticated session or token, and the frontend redirects Employee users to the employee dashboard and Support Staff users to the support staff dashboard. **Review decisions RD-11 and RD-12:** the submitted email is normalized to trimmed lowercase for comparison, while the password is compared exactly as submitted. |
| FR-08 | The frontend does not decide or assign the authenticated user’s role. |
| FR-09 | Support Staff accounts are created only by a controlled initialization process or an authorized administrator-only process. Public registration cannot create them. |
| FR-10 | The lab setup can create the initial Support Staff account without hardcoding the password in source code. Credentials are supplied through environment variables or secure interactive initialization. |
| FR-11 | A user cannot change their own role, and an employee cannot promote themselves to Support Staff. |
| FR-12 | An authenticated user can log out. Logout invalidates the session or token. |
| FR-13 | Protected pages and APIs require a verified session or token. Missing or invalid authentication returns HTTP 401 Unauthorized. **Review decision RD-03:** a login attempt that does not match a stored account also returns HTTP 401. |

### 8.2 Ticket Creation

| ID | Requirement |
|---|---|
| FR-14 | An authenticated employee can create a ticket by submitting title, description, category, and priority. |
| FR-15 | The system validates title, description, category, and priority before saving a ticket. Invalid values are not stored. |
| FR-16 | Title is required, contains non-whitespace text after trimming, and is at most 100 characters after trimming. **Review decision RD-11:** surrounding whitespace is trimmed before validation and storage. |
| FR-17 | Description is required and contains non-whitespace text after trimming. **Review decision RD-09:** it is at most 2,000 characters after trimming. **Review decision RD-11:** surrounding whitespace is trimmed before validation and storage. |
| FR-18 | Category is one of: Hardware, Software, Network, Access, Other. |
| FR-19 | Priority is one of: Low, Medium, High. |
| FR-20 | The backend sets Status to Open. A status value submitted by the employee during creation is not accepted as the stored status. |
| FR-21 | The backend sets Created By from the authenticated user and links the ticket to that user record. |
| FR-22 | The backend sets Created Date and Last Updated Date at creation. The user cannot supply these values. |
| FR-23 | The system assigns each ticket a unique identifier. |

### 8.3 Ticket Viewing

| ID | Requirement |
|---|---|
| FR-24 | An employee ticket list contains only tickets linked to that authenticated employee. |
| FR-25 | The employee list shows title, category, priority, status, and created date and time, and the employee can open a detail view of all eight fields. **Review decision RD-04** adds the time and the Asia/Kolkata zone. |
| FR-26 | Support staff can list tickets from all employees, including each creator’s name, title, category, priority, status, and created and last updated date and time, and can open a detail view of all eight fields. |
| FR-27 | The backend enforces ticket ownership and role restrictions for list and detail requests. |

### 8.4 Ticket Updating

| ID | Requirement |
|---|---|
| FR-28 | An employee can update title, description, category, and priority on their own ticket when the status is not Closed, including when the status is Open, In Progress, or Resolved. The field rules in FR-16 through FR-19 apply. **Review decision RD-07** confirms that this is the only employee edit and that Closed blocks it. |
| FR-29 | An employee cannot change status, Created By, Created Date, or Last Updated Date. |
| FR-30 | An employee cannot edit another employee’s ticket. |
| FR-31 | An employee cannot edit a ticket whose status is Closed. |
| FR-32 | Support staff can submit a status change. The backend accepts only Open, In Progress, Resolved, and Closed. **Review decision RD-01:** the only stored changes are Open to In Progress, In Progress to Resolved, and Resolved to Closed. A Closed ticket cannot change status. Any other transition returns HTTP 400 and is not stored. |
| FR-33 | Support staff cannot change Created By, Created Date, title, description, category, or priority. **Review decision RD-07:** status update is their only ticket-changing operation. An attempt to change employee-submitted content returns HTTP 403 and does not change the ticket. |
| FR-34 | After a successful content update or status update, the backend sets a new Last Updated Date and leaves Created By and Created Date unchanged. |
| FR-35 | A failed or unauthorized update does not change ticket fields or timestamps and does not return a success result. |

### 8.5 Dashboards, Search, and Filter

| ID | Requirement |
|---|---|
| FR-36 | The employee dashboard shows that employee’s total ticket count, counts for Open, In Progress, Resolved, and Closed, recent tickets, and a ticket creation option. Counts and lists come from that employee’s database records. **Review decision RD-10:** recent tickets means the latest 5 tickets by Created Date, newest first. |
| FR-37 | The employee dashboard shows clear status and priority indicators. |
| FR-38 | The support staff dashboard shows the total ticket count, counts for Open, In Progress, Resolved, and Closed, all submitted tickets, employee names, and ticket management options. Counts come from actual database records. |
| FR-39 | Support staff can filter tickets by status, category, and priority. |
| FR-40 | Support staff can search tickets. **Review decision RD-05:** search matches title, description, and creator name, case-insensitive, and combines with the status, category, and priority filters as defined in section 6.2. |

### 8.6 Sample Data and Persistence

| ID | Requirement |
|---|---|
| FR-41 | Tickets and users are stored in a persistent database and remain available after the application restarts. **Review decision RD-15:** the database reliability requirements in section 9.3 and FR-51 also apply. |
| FR-42 | Timestamps are stored in UTC. **Review decision RD-04:** the display is a date and time in Asia/Kolkata, in the form `18 Nov 2026, 09:15 AM`. The date portion keeps the product prompt’s example style. |
| FR-43 | Sample users and sample tickets are inserted through a controlled database seed or initialization process. They are not hardcoded as fake frontend records. |
| FR-44 | The seed supports the sample users and all five sample tickets in section 14, including each supplied title, category, priority, and status. **Review decision RD-06:** the seed also stores the labelled demonstration descriptions, creators, and timestamps in that section. |

### 8.7 Delivery

| ID | Requirement |
|---|---|
| FR-45 | The project includes a README with installation and execution instructions, and the application can be run locally for a demonstration. |
| FR-46 | **Review decision RD-08.** The initial version does not implement ticket comments. It has no comment field, comment storage, comment API, comment form, or comment display. Comments are a later enhancement, after this version is complete and tested. |
| FR-47 | **Review decision RD-03.** Refused API calls use the HTTP status codes and check order in section 12.3. |

### 8.8 Additional Approved Requirements

| ID | Requirement |
|---|---|
| FR-48 | **Review decision RD-13.** The system does not impose an arbitrary fixed maximum on the number of registered Employee accounts. Support Staff accounts are created only through the approved secure initialization process or an authorized administrative process, and no public Support Staff registration option is provided. |
| FR-49 | **Review decision RD-14.** The application provides the interface quality and responsive behavior defined in NFR-U-01 through NFR-U-11. |
| FR-50 | **Review decision RD-16.** Every visible button, form, link, filter, and navigation control performs its intended action with the backend and database. Clear success, validation, and error feedback is provided. No placeholder functionality or decorative controls that appear operational but do nothing are included. |
| FR-51 | **Review decision RD-15.** Database configuration and connection management are clearly defined and organized. Connection failures and transaction errors are handled safely, successful changes are persisted, data integrity is maintained through appropriate relationships, constraints, and validation, accidental data loss and inconsistent records are prevented, database access is organized, and database credentials or secrets are never exposed in source code. |

---

## 9. Non-Functional Requirements

### 9.1 Usability

| ID | Requirement |
|---|---|
| NFR-U-01 | The interface is attractive, modern, clean, professional, and user-friendly. **Review decision RD-14.** |
| NFR-U-02 | Employees and support staff have separate dashboards. |
| NFR-U-03 | The layout is responsive and adapts properly to desktop, tablet, and mobile screens. It uses available screen space effectively and avoids unwanted horizontal scrolling, clipped content, and overlapping elements. **Review decision RD-14.** |
| NFR-U-04 | Navigation is consistent. |
| NFR-U-05 | Status and priority indicators are clear. |
| NFR-U-06 | The interface shows appropriate success and error messages. |
| NFR-U-07 | Forms provide validation feedback. |
| NFR-U-08 | Every visible button, form, link, filter, and navigation control performs its intended action. No placeholder or decorative controls appear operational without doing work. **Review decision RD-16.** |
| NFR-U-09 | The interface uses large, readable fonts and clear visual hierarchy. **Review decision RD-14.** |
| NFR-U-10 | Spacing, alignment, colors, and component styling are consistent. Duplicate information and unnecessary UI elements are avoided. **Review decision RD-14.** |
| NFR-U-11 | Forms, tables, dashboards, navigation, and feedback messages are easy to understand and use, with clear success, validation, and error feedback. **Review decisions RD-14 and RD-16.** |

### 9.2 Security

| ID | Requirement |
|---|---|
| NFR-S-01 | Authentication is secure, and passwords are hashed. Plain-text passwords and password hashes are not exposed. |
| NFR-S-02 | Role-based access control is enforced on the backend for pages and APIs, including direct API calls. |
| NFR-S-03 | Ticket ownership is verified on the backend before an employee reads or updates a ticket. |
| NFR-S-04 | Input is validated on the backend before it is stored. |
| NFR-S-05 | Secrets are managed through environment variables or secure interactive initialization, and secret-bearing files are excluded from Git. |
| NFR-S-06 | Unauthorized users cannot access other employees’ tickets, the support dashboard, or support-only operations. |

### 9.3 Reliability

| ID | Requirement |
|---|---|
| NFR-R-01 | Ticket and user data is stored persistently. |
| NFR-R-02 | Errors are handled so a failed operation does not appear to succeed. |
| NFR-R-03 | Created Date, Last Updated Date, and Created By stay accurate under the rules in section 4. |
| NFR-R-04 | Database operations leave stored tickets consistent when an operation fails or is unauthorized. |
| NFR-R-05 | Database configuration and connection management are clearly defined and organized rather than scattered through the application. **Review decision RD-15.** |
| NFR-R-06 | Database connection failures and transaction errors are handled safely. Failed operations do not leave partial or inconsistent changes, and successful changes are persisted. **Review decision RD-15.** |
| NFR-R-07 | Appropriate database relationships, constraints, and validation maintain data integrity and prevent accidental data loss or inconsistent records. **Review decision RD-15.** |
| NFR-R-08 | Database credentials and secrets are not exposed in source code. **Review decision RD-15.** |

### 9.4 Maintainability

| ID | Requirement |
|---|---|
| NFR-M-01 | The project structure is organized. |
| NFR-M-02 | Frontend components are reusable where the interface repeats. |
| NFR-M-03 | Frontend, backend, business logic, and database responsibilities are separated. |
| NFR-M-04 | Code is readable, with meaningful variable and function names. |
| NFR-M-05 | Database access is organized in a defined layer rather than scattered through frontend, business logic, or unrelated backend code. **Review decision RD-15.** |

### 9.5 Performance

| ID | Requirement |
|---|---|
| NFR-P-01 | Database queries used for ticket lists, filters, and dashboard counts are efficient for the lab’s expected data volume. |
| NFR-P-02 | The application avoids unnecessary API requests. |
| NFR-P-03 | Ticket listing and filtering remain smooth for the lab’s expected data volume. |

The prompt defines that volume through the sample data: two demonstration users and five tickets. It does not require a larger capacity target.

---

## 10. Data Requirements

### 10.1 Entities

The product prompt requires two stored concepts: users and tickets. This specification does not add further entities.

**User**

| Attribute | Rule |
|---|---|
| Full name | Collected at employee registration. **Review decision RD-02:** it must contain a non-whitespace character. The sample support staff identity also has a name. |
| Email | Used for login. Duplicate registration emails are prevented. **Review decision RD-02:** registration requires the email format in section 3.2. |
| Password | Stored only as a secure hash. **Review decision RD-02:** registration requires at least 8 characters and a matching confirm password. |
| Role | Exactly one of Employee or Support Staff. Assigned by the backend. |

A user record must be identifiable so a ticket can link to it. The identifier format is unresolved (section 19).

**Ticket**

| Attribute | Rule |
|---|---|
| Unique identifier | Required. Format is unresolved (section 19). |
| Title | Section 4.1 |
| Description | Section 4.2 |
| Category | Section 4.3 |
| Priority | Section 4.4 |
| Status | Section 4.5 |
| Created By | Reference to the user record, displayed by the creator’s name |
| Created Date | Backend timestamp, stored in UTC, displayed as date and time in Asia/Kolkata (Review decision RD-04) |
| Last Updated Date | Backend timestamp, stored in UTC, displayed as date and time in Asia/Kolkata (Review decision RD-04) |

### 10.2 Relationships

- A ticket is created by exactly one user.
- A user may be the creator of zero, one, or many tickets.
- The creator link does not change after the ticket is saved.
- Support Staff users are user records with the Support Staff role. The prompt does not allow them to create tickets through the application.

No comment, attachment, notification, or audit-log entity is in scope. **Review decision RD-08:** a comment must not be added as a field on the ticket, as a related record, or as sample data in the initial version.

---

## 11. API Requirements

The application uses REST APIs. The prompt requires the following capabilities and authorization results. It does not require specific URL paths or request-body shapes. Those designs belong in the later plan (section 19).

### 11.1 Required Capabilities

| Capability | Who may succeed | Confirmed result when refused |
|---|---|---|
| Register an employee | Unauthenticated visitor, subject to validation | Duplicate email is prevented. A submitted role is ignored or rejected. Invalid input is not stored and returns HTTP 400 (Review decision RD-03). |
| Log in | Employee or Support Staff with valid credentials | The backend, not the client, supplies the role after success. Unsuccessful credentials return HTTP 401 (Review decision RD-03). |
| Log out | Authenticated user | The session or token is invalidated. |
| Create a ticket | Authenticated employee | Unauthenticated calls return HTTP 401. Invalid fields return HTTP 400 and are not stored. Status is stored as Open. |
| List and read own tickets | Authenticated employee | Another employee’s ticket returns HTTP 403. An unknown ticket identifier returns HTTP 404 (Review decision RD-03). |
| List and read all tickets | Authenticated Support Staff | An employee receives HTTP 403. Unauthenticated calls return HTTP 401. An unknown ticket identifier returns HTTP 404. |
| Update own ticket content | Authenticated employee, own ticket, status not Closed | Another employee’s ticket, or a Closed ticket, returns HTTP 403. Invalid fields return HTTP 400. The ticket and its timestamps stay unchanged. |
| Update ticket status | Authenticated Support Staff, and only for a legal next step (Review decision RD-01) | An employee call returns HTTP 403 Forbidden. An illegal transition returns HTTP 400. A missing ticket returns HTTP 404. |
| Dashboard figures | The matching authenticated role | Figures are calculated from database records in that role’s allowed scope. An employee request for support-dashboard data returns HTTP 403. |
| Filter and search tickets | Authenticated Support Staff | Search covers title, description, and creator name (Review decision RD-05). Employees are not given this capability by the prompt. |

### 11.2 Authorization Rules for APIs

- The backend verifies the session or token on protected endpoints.
- The backend reads the role from the authenticated user record.
- The backend checks ticket ownership before an employee read or content update.
- Hidden frontend controls are not the only protection.
- API responses do not include password hashes or secrets.
- A failed operation does not return a success message.
- **Review decision RD-03.** Refusal codes are the codes in section 12.3. Success response codes and URL paths remain technical decision TD-03.

---

## 12. Error Handling and Validation

### 12.1 Validation

The backend validates input before storage.

| Input | Validation |
|---|---|
| Full name | Original requirement: the field is required and validated. **Review decision RD-02:** it must contain at least one non-whitespace character. **Review decision RD-11:** surrounding whitespace is trimmed before validation and storage. |
| Email on registration | Original requirement: duplicates are prevented. **Review decision RD-02:** the value must match the format in section 3.2. **Review decision RD-11:** surrounding whitespace is trimmed before validation and storage. **Review decision RD-12:** uniqueness is case-insensitive; the stored email is normalized to trimmed lowercase. |
| Password | **Review decision RD-02:** at least 8 characters. No complexity rule was added. **Review decision RD-11:** the password is never trimmed; length is measured on the submitted characters. |
| Confirm password | **Review decision RD-02:** required, and it must match password exactly. **Review decision RD-11:** the comparison uses the submitted characters exactly and never trims either value. |
| Registration role | Ignored or rejected. Never applied. |
| Title | Required, not empty, not whitespace only, maximum 100 characters after trimming. **Review decision RD-11:** surrounding whitespace is trimmed before validation and storage. |
| Description | Required, not empty, not whitespace only, maximum 2,000 characters after trimming. **Review decisions RD-09 and RD-11:** the limit applies after trimming, and trimmed text is stored. |
| Category | One of the five listed values. |
| Priority | One of the three listed values. |
| Status on employee create or edit | Not accepted from the employee as the stored or updated status. |
| Status on support update | Must be one of the four listed statuses and must be the next step in section 4.5 (Review decision RD-01). |
| Created By, Created Date, Last Updated Date | Not accepted as client-authored values. |

### 12.2 Failure Behavior

- Invalid input is not stored.
- Unauthorized actions are rejected.
- A failed or unauthorized ticket operation does not modify ticket information.
- A failed or unauthorized ticket operation does not update Last Updated Date or Created Date.
- The user interface does not show a success message for a failed operation.
- Forms show validation feedback.
- Success and error messages are appropriate and clear.

### 12.3 HTTP Responses

The product prompt fixes two codes: HTTP 401 for an unauthenticated protected request, and HTTP 403 when an employee calls the status-update API. **Review decision RD-03** assigns codes to the other refusal cases and sets the order of checks.

When a request can fail for more than one reason, the backend checks in this order and returns the first matching result:

1. Authentication, if the operation is protected.
2. Missing ticket, if the operation names a ticket identifier.
3. Authorization, using the authenticated user’s role and ticket ownership.
4. Invalid input, including an illegal status transition.

| Situation | HTTP response | Source |
|---|---|---|
| A protected endpoint is called with no session or token, or with a session or token that is missing, expired, or otherwise invalid | 401 Unauthorized | Original requirement for a missing authenticated user. Review decision RD-03 covers an invalid session or token in the same way. |
| Login email and password do not match an account | 401 Unauthorized | Review decision RD-03 |
| Login is missing the email or the password | 400 Bad Request | Review decision RD-03. This is invalid input, before the credential check. |
| Employee calls the status-update API | 403 Forbidden | Original requirement |
| Employee reads or updates another employee’s ticket | 403 Forbidden | Original requirement to reject the request. Review decision RD-03 assigns 403. The ticket exists, so this is not 404. |
| Employee requests the support dashboard or a support-only API | 403 Forbidden | Original requirement to deny access. Review decision RD-03 assigns 403 for the API. The support dashboard is not shown. |
| Employee edits a Closed ticket | 403 Forbidden | Original requirement to reject the edit. Review decision RD-03 assigns 403. The ticket is not changed. |
| Support staff attempts to modify title, description, category, priority, creator, or creation date | 403 Forbidden | Original requirement to reject that modification. Review decision RD-03 assigns 403. |
| Registration or ticket field validation fails, including a duplicate registration email, a title over 100 characters, a bad category, or a bad priority | 400 Bad Request | Original requirement that invalid input is not stored. Review decision RD-03 assigns 400. |
| Support staff submits a status that is not the next step, including any change to a Closed ticket, a skipped step, a backward step, or the same status | 400 Bad Request | Review decision RD-01 and RD-03. The ticket and Last Updated Date stay unchanged. |
| The ticket identifier does not exist | 404 Not Found | Review decision RD-03 |

A 401, 403, 400, or 404 ticket operation must not change stored ticket fields or timestamps, and it must not be presented as a success. The response should say what went wrong in plain language without exposing password hashes, secrets, or another employee’s ticket contents.

---

## 13. Security Requirements

Security requirements are the combination of section 3, NFR-S-01 through NFR-S-06, and the authorization rows in section 11.

In summary, the implementation must provide:

- Secure authentication and backend verification of each protected request
- Hashed passwords, with no plain-text passwords and no hashes in responses
- Backend role assignment and backend role checks
- Ticket ownership checks
- Rejection of direct API attempts that bypass the user interface
- Secret storage outside source code, with secret files ignored by Git. Database credentials and other secrets are not exposed in source code (Review decision RD-15).
- No hardcoded support staff passwords

---

## 14. Sample Data

Use the fictional sample data in this section. Do not replace the names, emails, titles, categories, priorities, or statuses that the product prompt supplied.

**Review decision RD-06.** The prompt fully specified description, creator, and dates for ticket 1 only. This review completes tickets 2 through 5 with fictional demonstration values so the seed can store every required field. Each completed value is labelled **Demonstration value**. Ticket 1 keeps the supplied description, creator, and calendar date. Clock times were added to every ticket so the Asia/Kolkata date-and-time display in Review decision RD-04 can be seeded. Those clock times are also demonstration values.

All five tickets are created by Ravi. The prompt names Ravi on ticket 1 and provides only one sample employee. Assigning Ravi to tickets 2 through 5 does not add a new user. That assignment is a demonstration value except on ticket 1, where the prompt already names Ravi.

Sample accounts are created by the controlled seed or initialization process. Known passwords must not be embedded in source code. The seed stores the UTC instants below. The application displays the Asia/Kolkata date and time.

### 14.1 Sample Users

| Name | Email | Role |
|---|---|---|
| Ravi | ravi@company.com | Employee |
| Support Admin | support@company.com | Support Staff |

These rows are demonstration identities, not credentials.

### 14.2 Sample Tickets

| No. | Title | Category | Priority | Status |
|---|---|---|---|---|
| 1 | Laptop not charging | Hardware | High | Open |
| 2 | Cannot log in to VPN | Network | High | In Progress |
| 3 | Need access to the shared project folder | Access | Medium | Open |
| 4 | Excel keeps crashing on startup | Software | Medium | Resolved |
| 5 | Request a second monitor | Hardware | Low | Closed |

### 14.3 Sample Ticket 1

| Field | Value | Source |
|---|---|---|
| Title | Laptop not charging | Original requirement |
| Description | My laptop shows 0% even when plugged in. | Original requirement |
| Category | Hardware | Original requirement |
| Priority | High | Original requirement |
| Status | Open | Original requirement |
| Created By | Ravi | Original requirement |
| Created Date | 18 Nov 2026, 09:15 AM Asia/Kolkata | Calendar date is original. The time 09:15 AM is a demonstration value. |
| Created Date stored in UTC | 18 Nov 2026, 03:45 AM UTC | Demonstration value, equal to the display time above |
| Last Updated Date | 18 Nov 2026, 09:15 AM Asia/Kolkata | Calendar date is original. The time 09:15 AM is a demonstration value. |
| Last Updated Date stored in UTC | 18 Nov 2026, 03:45 AM UTC | Demonstration value |

### 14.4 Sample Ticket 2

| Field | Value | Source |
|---|---|---|
| Title | Cannot log in to VPN | Original requirement |
| Description | The VPN client connects and then disconnects before the office network opens. | Demonstration value |
| Category | Network | Original requirement |
| Priority | High | Original requirement |
| Status | In Progress | Original requirement |
| Created By | Ravi | Demonstration value |
| Created Date | 17 Nov 2026, 11:00 AM Asia/Kolkata | Demonstration value |
| Created Date stored in UTC | 17 Nov 2026, 05:30 AM UTC | Demonstration value |
| Last Updated Date | 18 Nov 2026, 09:40 AM Asia/Kolkata | Demonstration value |
| Last Updated Date stored in UTC | 18 Nov 2026, 04:10 AM UTC | Demonstration value |

### 14.5 Sample Ticket 3

| Field | Value | Source |
|---|---|---|
| Title | Need access to the shared project folder | Original requirement |
| Description | I need read access to the shared project folder so I can open the onboarding documents. | Demonstration value |
| Category | Access | Original requirement |
| Priority | Medium | Original requirement |
| Status | Open | Original requirement |
| Created By | Ravi | Demonstration value |
| Created Date | 18 Nov 2026, 10:05 AM Asia/Kolkata | Demonstration value |
| Created Date stored in UTC | 18 Nov 2026, 04:35 AM UTC | Demonstration value |
| Last Updated Date | 18 Nov 2026, 10:05 AM Asia/Kolkata | Demonstration value |
| Last Updated Date stored in UTC | 18 Nov 2026, 04:35 AM UTC | Demonstration value |

### 14.6 Sample Ticket 4

| Field | Value | Source |
|---|---|---|
| Title | Excel keeps crashing on startup | Original requirement |
| Description | Excel closes immediately after it opens, before any workbook appears. | Demonstration value |
| Category | Software | Original requirement |
| Priority | Medium | Original requirement |
| Status | Resolved | Original requirement |
| Created By | Ravi | Demonstration value |
| Created Date | 16 Nov 2026, 02:30 PM Asia/Kolkata | Demonstration value |
| Created Date stored in UTC | 16 Nov 2026, 09:00 AM UTC | Demonstration value |
| Last Updated Date | 18 Nov 2026, 11:20 AM Asia/Kolkata | Demonstration value |
| Last Updated Date stored in UTC | 18 Nov 2026, 05:50 AM UTC | Demonstration value |

### 14.7 Sample Ticket 5

| Field | Value | Source |
|---|---|---|
| Title | Request a second monitor | Original requirement |
| Description | I am requesting a second monitor so I can keep a spreadsheet and the ticket page open together. | Demonstration value |
| Category | Hardware | Original requirement |
| Priority | Low | Original requirement |
| Status | Closed | Original requirement |
| Created By | Ravi | Demonstration value |
| Created Date | 15 Nov 2026, 09:00 AM Asia/Kolkata | Demonstration value |
| Created Date stored in UTC | 15 Nov 2026, 03:30 AM UTC | Demonstration value |
| Last Updated Date | 17 Nov 2026, 04:45 PM Asia/Kolkata | Demonstration value |
| Last Updated Date stored in UTC | 17 Nov 2026, 11:15 AM UTC | Demonstration value |

The application must support all five sample tickets, the original titles, categories, priorities, and statuses, and the demonstration values in sections 14.3 through 14.7. None of these rows is a ticket comment.

---

## 15. Acceptance Criteria

The application is functionally complete for the initial version when every criterion in this section passes. No criterion depends on an open question because no product open questions remain. Review decisions in this section are testable now.

### 15.1 Registration

Related requirements: FR-01, FR-02, FR-03, FR-04, FR-05.

- A visitor can open the public registration page and submit full name, email, password, and confirm password.
- A successful registration creates an Employee account.
- The new user cannot choose or submit a role that becomes Support Staff.
- A second registration with the same email is rejected, no duplicate account is created, and the API returns HTTP 400.
- The stored password is a hash. The hash is not shown in the interface or in API responses.
- **Review decision RD-02.** An empty or whitespace-only full name is rejected with HTTP 400, and no account is created.
- **Review decision RD-02.** An email that does not match the format in section 3.2 is rejected with HTTP 400.
- **Review decision RD-02.** A password shorter than 8 characters is rejected with HTTP 400.
- **Review decision RD-02.** A confirm password that differs from the password is rejected with HTTP 400.
- **Review decision RD-02.** A password of exactly 8 characters is accepted when the other fields are valid. No extra complexity rule is required. Letters alone are enough.
- **Review decision RD-11.** Full names and emails are stored without leading or trailing whitespace. A name or email submitted with surrounding spaces is validated and stored in trimmed form.
- **Review decision RD-11.** Passwords are never trimmed. A password with leading or trailing spaces keeps those spaces for length checking, hashing, and confirmation comparison; a confirmation that differs by spacing is rejected.
- **Review decision RD-12.** Registrations using the same email with different letter case are treated as duplicates. The second registration is rejected with HTTP 400 and no duplicate account is created.
- **Review decision RD-12.** Stored emails use trimmed lowercase, such as `ravi@company.com`.

### 15.2 Login and Role Routing

Related requirements: FR-06, FR-07, FR-08, FR-13.

- Employee and Support Staff use the same login page.
- The login page does not offer a role selector.
- After a successful employee login, the user reaches the employee dashboard.
- After a successful support staff login, the user reaches the support staff dashboard.
- The role used for that redirect comes from the backend database check.
- A protected API call without authentication returns HTTP 401.
- **Review decision RD-03.** A login with the wrong password returns HTTP 401 and does not open a dashboard.
- **Review decision RD-03.** A login request that omits the email or the password returns HTTP 400.
- **Review decision RD-12.** Login succeeds when the email differs only in letter case from the stored email, because the submitted email is normalized before comparison.
- **Review decision RD-11.** Login fails when the password differs by leading or trailing whitespace, because passwords are never trimmed.

### 15.3 Support Staff Initialization

Related requirements: FR-09, FR-10, FR-11.

- The demonstration Support Staff account can be created through controlled initialization.
- There is no public support staff registration page.
- The support staff password is not hardcoded in source code.
- An employee registration cannot produce a Support Staff user.
- A logged-in user cannot change their role to Support Staff.

### 15.4 Logout

Related requirements: FR-12.

- An employee can log out, and the previous session or token no longer authorizes protected requests.
- A support staff user can log out, and the previous session or token no longer authorizes protected requests.

### 15.5 Ticket Creation

Related requirements: FR-14 through FR-23, FR-35.

- An employee can create a ticket with a valid title, description, category, and priority.
- The saved status is Open.
- Created By is the logged-in employee, and both timestamps are set by the backend.
- **Review decision RD-04.** The created and last updated values display as a date and time in Asia/Kolkata.
- **Review decision RD-03.** Each rejected create in this section returns HTTP 400.
- An empty title, a whitespace-only title, an empty description, and a whitespace-only description are rejected and not stored.
- A title longer than 100 characters after trimming is rejected and not stored.
- **Review decision RD-09.** A description longer than 2,000 characters after trimming is rejected with HTTP 400 and not stored.
- **Review decision RD-09.** A description of exactly 2,000 characters after trimming is accepted when the other fields are valid.
- **Review decision RD-11.** Title and description are trimmed before validation and storage. Surrounding spaces in an otherwise valid title or description are not stored.
- A category outside the five allowed values is rejected and not stored.
- A priority outside the three allowed values is rejected and not stored.
- Submitting a status during creation does not let the employee store a status other than Open.
- A rejected create does not show a success message.

### 15.6 Ticket Viewing

Related requirements: FR-24, FR-25, FR-26, FR-27.

- An employee sees only their own tickets in the list.
- An employee can open one of their tickets and see all eight fields.
- Support staff see tickets from all employees, including the creator’s name.
- Support staff can open a ticket and see all eight fields.
- **Review decision RD-04.** Created Date and Last Updated Date are shown as a date and time in Asia/Kolkata, in the form illustrated by `18 Nov 2026, 09:15 AM`.
- **Review decision RD-03.** A request for a ticket identifier that does not exist returns HTTP 404.
- **Review decision RD-03.** An employee request for a ticket that belongs to someone else returns HTTP 403, and the ticket contents are not returned.

### 15.7 Employee Ticket Update

Related requirements: FR-28, FR-29, FR-30, FR-31, FR-34, FR-35.

- An employee can change title, description, category, and priority on their own ticket while it is Open, In Progress, or Resolved.
- The same field validation used for creation applies to the update.
- After a successful update, Last Updated Date changes and Created By and Created Date do not.
- An employee cannot change status. A direct status-update call returns HTTP 403.
- An employee cannot save edits to a Closed ticket. That request returns HTTP 403, including for sample ticket 5, “Request a second monitor.”
- An employee cannot save edits to another employee’s ticket. That request returns HTTP 403.
- **Review decision RD-07.** The employee edit form and the employee update API accept only title, description, category, and priority.
- A rejected update does not change stored fields, does not change timestamps, and does not show success.

### 15.8 Status Management

Related requirements: FR-20, FR-32, FR-33, FR-34, FR-35.

- A new ticket is Open.
- **Review decision RD-01.** Support staff can change Open to In Progress, In Progress to Resolved, and Resolved to Closed.
- The new status is stored in the database.
- Last Updated Date changes after a successful status change.
- Created By and Created Date do not change.
- Title, description, category, and priority do not change because of a status update.
- **Review decision RD-07.** Support staff have no successful way to change title, description, category, or priority. That attempt returns HTTP 403.
- An employee who calls the status-update API receives HTTP 403, and the status stays unchanged.
- **Review decision RD-01.** Skipping a step, moving backward, submitting the current status, or changing a Closed ticket returns HTTP 400. Sample ticket 5 remains Closed.
- A status update for a ticket identifier that does not exist returns HTTP 404.

### 15.9 Dashboards

Related requirements: FR-36, FR-37, FR-38.

- The employee dashboard totals match that employee’s stored tickets, including separate counts for Open, In Progress, Resolved, and Closed.
- The employee dashboard shows recent tickets and a working way to create a ticket.
- **Review decision RD-10.** The recent tickets section shows at most 5 of that employee’s tickets, ordered by Created Date with the newest ticket first. If the employee has fewer than 5 tickets, all of them are shown in that order.
- The support dashboard totals match all stored tickets, including the four status counts.
- The support dashboard lists submitted tickets and shows employee names.
- Status and priority indicators are visible.
- Changing a ticket’s status or creating a ticket changes the related dashboard counts after the data is loaded again from the database.

### 15.10 Search and Filter

Related requirements: FR-39, FR-40.

- Support staff can filter the ticket list by status, by category, and by priority.
- Each filter shows only tickets that match the selected allowed value.
- When more than one filter is selected, every selected filter applies.
- **Review decision RD-05.** Searching `laptop` matches “Laptop not charging” through the title. The match does not depend on letter case.
- **Review decision RD-05.** Searching `workbook` matches “Excel keeps crashing on startup” through the demonstration description.
- **Review decision RD-05.** Searching `Ravi` matches tickets whose creator name is Ravi.
- **Review decision RD-05.** A search combined with a status filter returns only tickets that match both.
- The employee dashboard does not add this search or these filters.

### 15.11 Security and Authorization

Related requirements: FR-08, FR-13, FR-27, FR-30, FR-32, NFR-S-01 through NFR-S-06.

- An employee cannot open the support dashboard. A direct request for support-dashboard data returns HTTP 403.
- An employee cannot retrieve another employee’s ticket through the interface or a direct API request. The direct request returns HTTP 403.
- An employee cannot change status through a direct API request. The response is HTTP 403.
- An unauthenticated request to a protected API is rejected with HTTP 401.
- A request for a missing ticket returns HTTP 404.
- Passwords, password hashes, and secrets are not exposed in responses, the interface, or committed source files.

### 15.12 Persistence and Sample Data

Related requirements: FR-41, FR-43, FR-44.

- Created tickets are present in the database.
- After a restart, previously stored tickets are still available.
- The seed process can insert the sample users and the five sample tickets in section 14, including the original statuses and the labelled demonstration descriptions, creators, and UTC timestamps.
- After seeding, ticket 1 still shows the title “Laptop not charging,” category Hardware, priority High, status Open, description “My laptop shows 0% even when plugged in,” and creator Ravi.
- The displayed created time for ticket 1 is 18 Nov 2026, 09:15 AM in Asia/Kolkata.
- Sample records are not fake rows that exist only in the frontend.
- Sample passwords are not written into source code.

### 15.13 User Interface and Functional Completeness

Related requirements: NFR-U-01 through NFR-U-11, FR-45, FR-49, FR-50.

- Both dashboards display the information required for their role.
- Navigation reaches the screens that role is allowed to use.
- Forms show validation feedback for invalid title, description, category, and priority.
- **Review decision RD-14.** The interface looks attractive, modern, clean, and professional, with large readable fonts, clear visual hierarchy, consistent spacing, alignment, colors, and component styling.
- **Review decision RD-14.** The layout is usable and properly adapted at desktop, tablet, and mobile widths. It uses available screen space effectively, with no unwanted horizontal scrolling, clipped content, or overlapping elements.
- **Review decision RD-14.** Forms, tables, dashboards, navigation, and feedback messages are easy to understand and use. Duplicate information and unnecessary UI elements are avoided.
- **Review decision RD-16.** Every visible button, form, link, filter, and navigation control performs its intended action against the backend and database.
- **Review decision RD-16.** Success, validation, and error messages are clear. No placeholder functionality or decorative control appears operational without doing work.
- A reviewer can install and run the application locally by following the README.

### 15.14 Ticket Comments

Related requirements: FR-46, section 16. **Review decision RD-08.**

- Ticket creation, ticket detail, both dashboards, and the support staff status action show no comment list, comment box, or comment button.
- No API accepts or returns ticket comments.
- The database seed does not insert comments.
- The eight ticket fields remain the only ticket business fields.

### 15.15 User Capacity and Support Staff Creation

Related requirements: FR-02, FR-09, FR-48. **Review decision RD-13.**

- The application does not impose an arbitrary fixed maximum on registered Employee accounts.
- Registering additional Employee accounts does not fail because a fixed account limit was reached.
- There is no public Support Staff registration page or API that lets a visitor or Employee create a Support Staff account.
- Support Staff accounts are created only through the approved secure initialization process or an authorized administrative process.

### 15.16 Database Reliability

Related requirements: FR-41, FR-51, NFR-R-05 through NFR-R-08, NFR-M-05. **Review decision RD-15.**

- Database configuration and connection management are clearly defined and organized rather than duplicated throughout the application.
- A database connection failure is handled safely and does not produce a false success message or a partial change.
- A transaction error leaves stored records consistent and does not create an inconsistent ticket, user, or timestamp.
- Successful changes are persisted and remain available after the application restarts.
- Relationships, constraints, and validation prevent orphaned tickets, missing required ticket fields, invalid roles or statuses, and accidental data loss.
- Database credentials and secrets are not present in source code.

---

## 16. Out of Scope

The initial implementation includes only employee support ticket management as specified above. The following are out of scope for the initial version:

1. Ticket comments. **Review decision RD-08** confirms this exclusion. Comments will be added later as a separate feature enhancement. The initial version must be completed and tested before comments are added. The initial version must not include a comment field, comment record, comment API, comment form, comment display, or comment sample data.
2. AI-based ticket classification.
3. AI chatbots.
4. Email notifications.
5. SMS notifications.
6. Payment functionality.
7. Unnecessary enterprise-level functionality.
8. Additional user roles beyond Employee and Support Staff.
9. Ticket statuses other than Open, In Progress, Resolved, and Closed, unless later approved.
10. Categories other than Hardware, Software, Network, Access, and Other, unless later approved.
11. Reopening a Closed ticket. **Review decision RD-01:** Closed is final in this version unless a future approved feature allows reopening.

This specification does not include ticket comments in any initial-version workflow, data entity, API, dashboard, seed data, or acceptance test. Acceptance section 15.14 checks that exclusion.

---

## 17. Proposed Technology Stack

The product prompt proposes the following technologies. They are proposals, not confirmed decisions. Architecture and implementation choices are to be confirmed in `PLAN.md` before code is generated.

| Area | Proposal |
|---|---|
| Frontend | React, Vite, CSS |
| Backend | Python, FastAPI |
| Database | SQLite |
| Communication | REST APIs |
| Version control | Git and GitHub |
| Configuration | Environment variables |

This specification requires the externally visible behavior in the earlier sections. It does not require a different stack, and it does not treat the proposal as already approved.

---

## 18. Assumptions

These statements are limited to what the product prompt already establishes. They are not extra product features.

| ID | Assumption |
|---|---|
| A-01 | The first implementation is a locally runnable web application for a lab demonstration. |
| A-02 | “Exactly two user roles” means there is no third role, including a separate public administrator role, unless a later approved change adds one. The prompt still allows an authorized administrator-only process for creating support staff accounts. |
| A-03 | “Ignore or reject” a client-supplied registration role means either behavior is acceptable. Honoring the client-supplied role is not acceptable. |
| A-04 | A session and a token are both acceptable authentication mechanisms if the backend verifies them and logout invalidates them. |
| A-05 | Features, fields, roles, statuses, and categories that are absent from the product prompt are not requirements, except for the review decisions in section 1.5. Those review decisions are requirements even though the prompt left them open. |
| A-06 | The eight ticket fields are the complete business content of a ticket. The unique identifier is additional system data required by the integrity rules. |

---

## 19. Unresolved Technical Decisions

These items are intentionally undecided. They must be chosen in `PLAN.md` before implementation. Choosing them must not change the confirmed behavior in this specification.

| ID | Decision still open | Constraint from the prompt |
|---|---|---|
| TD-01 | Confirm or replace the proposed frontend, backend, and database stack. | Behavior in this specification remains the requirement. |
| TD-02 | Use a server session or a token. | The backend verifies it. Logout invalidates it. The frontend does not assign the role. |
| TD-03 | REST resource paths, request bodies, and success status codes. | The capabilities in section 11 remain required. Failure codes are no longer open: section 12.3 defines 400, 401, 403, and 404. |
| TD-04 | User and ticket identifier formats. | Identifiers must be unique, and Created By must reference the user record. |
| TD-05 | How the seed or initialization process receives the sample account passwords. | Use environment variables or secure interactive initialization. Do not hardcode passwords in source code. |

TD-06 is removed. Review decision RD-04 now requires UTC storage and a date-and-time display in Asia/Kolkata. The display form is `18 Nov 2026, 09:15 AM`.

---

## 20. Open Questions

All product open questions are now resolved. No open product questions remain.

| Former question | Resolved by |
|---|---|
| OQ-01 Status transitions | RD-01 |
| OQ-02 Registration validation | RD-02 |
| OQ-03 HTTP responses | RD-03 |
| OQ-04 Description maximum length | RD-09 |
| OQ-05 Timestamp display time zone | RD-04 |
| OQ-06 Timestamp display format | RD-04 |
| OQ-07 Meaning of “recent tickets” | RD-10 |
| OQ-08 Support staff search fields | RD-05 |
| OQ-09 Missing sample ticket details | RD-06 |
| OQ-10 Surrounding whitespace handling | RD-11 |
| OQ-11 Email case sensitivity | RD-12 |

Technical choices that remain undecided are listed in section 19. Those choices must be made in `PLAN.md` before implementation; they must not change the confirmed behavior in this specification.

---

## 21. Approval

This finalized document is the requirements baseline for implementation approval. Original requirements remain in force. Review decisions RD-01 through RD-16 are also in force. No product open questions remain; the unresolved technical decisions in section 19 are resolved in `PLAN.md`.

After explicit approval, the next document is `PLAN.md`. Application code, frontend files, and backend files are not part of this step.
