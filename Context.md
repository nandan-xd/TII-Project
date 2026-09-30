# Student TaskBoard
## Master Project Context

> **Purpose:** This is the single source of context for continuing development of Student TaskBoard. It explains the problem, project evolution, current product, architecture, tech stack, completed work, pending work, design decisions, and implementation constraints.

---

# 1. Project Overview

| Item | Details |
|---|---|
| **Project** | Student TaskBoard |
| **Type** | College student portal / mini-project |
| **Primary goal** | Centralize academic assignments and campus events |
| **Backend** | Python + Flask |
| **Database** | SQLite locally, PostgreSQL for deployment |
| **ORM** | SQLAlchemy / Flask-SQLAlchemy |
| **Frontend** | HTML + CSS + Bootstrap + Jinja2 |
| **Font** | JetBrains Mono |
| **Deployment direction** | Render + PostgreSQL |
| **Major planned integration** | Microsoft Teams via Microsoft Graph |
| **Current Teams state** | Demo importer; real Graph integration pending permissions |
| **Current student auth** | Student ID + Flask session |
| **Current admin auth** | Username/password + Flask session |
| **Design direction** | Cream + matte orange + matte blue + black, hard shadows, square corners |

---

# 2. Core Idea

Student TaskBoard is a **centralized college portal** that brings together:

1. **Academic assignments/tasks**
2. **College events and activities**

The problem is not that students cannot create a to-do list. The problem is that college information is scattered across different platforms.

```text
Teacher
   ↓
Microsoft Teams
   ↓
Assignment

Club
   ↓
WhatsApp / Instagram / messages
   ↓
Event announcement

Organizer
   ↓
Google Form
   ↓
Event registration
```

The goal is to give students one place to see what they need to do and what is happening on campus.

---

# 3. Project Evolution

## 3.1 Original Concept

The original application was a basic student task manager:

- manually add tasks
- enter deadlines
- set priority
- view tasks
- delete tasks
- mark tasks complete

## 3.2 Feedback That Changed the Project

During the project presentation, the key criticism was:

> If the student manually enters the deadline and priority, the student already knows that information and can manage it themselves.

This made the original project too similar to a generic to-do list.

## 3.3 Current Concept

The project changed into:

> **A centralized student information dashboard that aggregates academic assignments and campus events.**

The important shift is:

```text
OLD
Student knows assignment
        ↓
Student manually enters assignment
        ↓
TaskBoard stores it

NEW
Teacher creates assignment
        ↓
Microsoft Teams
        ↓
TaskBoard imports assignment
        ↓
Student sees it automatically
```

For events:

```text
Club publishes event
        ↓
Student TaskBoard
        ↓
Student discovers event
        ↓
Student registers
```

---

# 4. Problem Definition

## 4.1 Academic Information

Students may receive academic information through:

- Microsoft Teams
- class groups
- messages
- teacher announcements
- other academic channels

## 4.2 Event Information

Students may receive event information through:

- WhatsApp
- club groups
- Instagram
- college announcements
- Google Forms
- messages

## 4.3 Problems Created

### P1. Information is scattered

Students must check multiple platforms.

### P2. Information gets buried

Important announcements can disappear inside older messages.

### P3. Deadlines and registrations can be forgotten

A student may know about something but still fail to act on it.

### P4. Event registration is fragmented

The announcement and registration form may exist in different places.

### P5. No unified student view

Academic tasks and campus events are separated.

### Final problem framing

> **College information is distributed across multiple platforms, increasing the effort required to find, remember and act on it.**

Do not claim that every student constantly misses deadlines.

---

# 5. User Research

## 5.1 Survey Purpose

The survey was used to understand:

- where students receive academic information
- how students track college events
- whether information gets lost/buried
- whether students have missed or nearly missed assignments/events
- how many platforms students use

## 5.2 Important Responses

Examples included:

> “By searching in WhatsApp”

> “Go through the older messages.”

> “I almost forgot I had to submit my DM tutorial.”

> “during MTT i missed an assignment and an event”

> “check older messages, WhatsApp, friends”

## 5.3 Key Observation

**70% of respondents reported often needing to search older messages for college-related information.**

The survey was not unanimous:

- some students reported never missing deadlines
- others reported missing or almost missing assignments/events

Therefore the project should focus on **information fragmentation and retrieval effort**, not claim universal deadline problems.

---

# 6. Design Thinking / Empathy Phase

## 6.1 Recurring Observations

1. Students rely heavily on WhatsApp, Microsoft Teams and messages.
2. Students often search older messages for information.
3. Some students miss or almost miss assignments, deadlines or event registrations.
4. Students use multiple platforms/methods to track information.
5. Students show interest in having academic tasks and college events in one place.

## 6.2 Student Pains

- scattered information
- buried announcements
- forgotten assignments
- forgotten registrations
- repeated searching
- too many platforms to check

## 6.3 Desired Gains

- one place to check
- easier assignment/deadline access
- less searching
- easier event discovery
- convenient registration

## 6.4 Define-Phase Insight

> **A centralized platform that brings academic assignments and college events together.**

---

# 7. Product Scope

## 7.1 Student Features

### Authentication

- Student ID login
- Flask session

### Academic Tasks

- View tasks
- Manually add tasks
- Automatic priority calculation
- Mark tasks completed
- Delete tasks
- Show task source
- Show subject
- Sync/import Teams assignments

### Campus Events

- Browse events
- View club/category
- View date/time/venue
- Register for events
- Open external organizer form
- View registered events

### Notifications

- Task notifications
- Upcoming event notifications
- Dynamic notification count

---

# 8. Admin Features

There are two admin levels.

## 8.1 Club Admin

A Club Admin can:

- log in
- create events for their club
- view their club's events
- delete their club's events
- view registrations for their events

A Club Admin should **not** manage other clubs.

## 8.2 Super Admin

A Super Admin can:

- view all clubs
- view all events
- create events
- delete events
- view registrations
- create new clubs

---

# 9. Initial Clubs

| Club | Purpose |
|---|---|
| **Coding Club** | Technology, coding and hackathon activities |
| **Atrangi Club** | Creative, cultural and artistic activities |
| **College Events** | College-wide events, workshops and competitions |

The Super Admin can create additional clubs later.

---

# 10. Event System

## 10.1 Event Creation Flow

```text
Club Admin
    ↓
Admin Dashboard
    ↓
Create Event
    ↓
Enter:
    • Event title
    • Date
    • Time
    • Venue
    • Description
    • External registration URL
    ↓
Publish
    ↓
Student sees event
    ↓
Student registers
    ↓
Event appears in My Events
```

## 10.2 Event Registration

The system stores:

```text
event_id
user_id
registered_at
```

A unique constraint prevents the same student from registering twice for the same event.

## 10.3 External Google Forms

The portal does not need to replace existing Google Forms.

Admins can paste an external registration URL.

The student can:

1. register through TaskBoard
2. optionally open the organizer's external form

This keeps the project practical and avoids unnecessary complexity.

---

# 11. Microsoft Teams Integration

## 11.1 Intended Final Architecture

```text
Student TaskBoard
        ↓
Microsoft Login
        ↓
Microsoft Graph
        ↓
Microsoft Teams Education API
        ↓
Student Assignments
        ↓
Flask Backend
        ↓
PostgreSQL
        ↓
Student Dashboard
```

Relevant Graph endpoint discussed:

```text
GET /v1.0/education/me/assignments
```

Relevant delegated permission discussed:

```text
EduAssignments.ReadBasic
```

## 11.2 Intended User Experience

```text
Teacher creates assignment
        ↓
Microsoft Teams
        ↓
TaskBoard sync
        ↓
Assignment automatically appears
        ↓
Student sees it in Tasks
```

The student should not have to recreate every Teams assignment manually.

---

# 12. Current Microsoft / NMIMS Constraint

The real Microsoft Teams integration is **not currently connected**.

Microsoft Entra/Azure access issues were encountered with the NMIMS account, including application-registration/tenant restrictions.

Important constraint:

> **The project must not attempt to bypass college tenant restrictions.**

If required permissions are unavailable, legitimate options are:

1. NMIMS IT registers/approves the application.
2. An administrator grants the required permissions.
3. Development uses a separate Microsoft 365 Education test tenant.

---

# 13. Current Teams Demo Importer

Until Graph access is available, the project uses a demo importer.

Current route:

```text
POST /sync-teams
```

It creates sample assignments such as:

```text
OOP Assignment 3
Subject: Object Oriented Programming
```

and:

```text
CN Lab Report
Subject: Computer Networks
```

Imported tasks use:

```text
source = "Teams"
external_id = unique external identifier
```

The dashboard therefore does not care whether a task came from manual entry or Microsoft Graph.

The demo importer can later be replaced with Graph API without redesigning the student dashboard.

---

# 14. Duplicate Teams Assignments

The `external_id` field is intended to prevent duplicates.

```text
First sync
    ↓
Assignment ID 12345 not found
    ↓
Create task

Second sync
    ↓
Assignment ID 12345 already exists
    ↓
Do not create duplicate
```

---

# 15. Authentication

## 15.1 Current Student Login

```text
Student ID
    ↓
Flask session
    ↓
Student dashboard
```

No student password is currently required.

Session key:

```python
session['user_id']
```

## 15.2 Future Student Login

Potential final architecture:

```text
NMIMS Microsoft Account
        ↓
Microsoft OAuth
        ↓
Student authenticated
        ↓
Microsoft Graph
        ↓
Assignments
```

This could provide both identity and Graph authorization.

---

# 16. Admin Authentication

Admin login route:

```text
/admin/login
```

Admin fields:

```text
username
password_hash
role
club_name
```

Roles:

```text
super_admin
club_admin
```

Development accounts currently include:

```text
superadmin
codingadmin
atrangiadmin
collegeadmin
```

These are prototype credentials and should be changed before real deployment.

Passwords use:

```python
generate_password_hash()
check_password_hash()
```

---

# 17. Database Architecture

The application uses **SQLAlchemy / Flask-SQLAlchemy**.

Main models:

```text
Tasks
Admin
Club
Event
Registration
```

## 17.1 Tasks

Purpose: academic tasks and imported assignments.

Fields:

```text
id
title
date
description
priority
user_id
source
external_id
subject
status
```

Values:

```text
source:
    Manual
    Teams

status:
    Pending
    Completed
```

## 17.2 Admin

```text
id
username
password_hash
role
club_name
```

## 17.3 Club

```text
id
name
description
```

## 17.4 Event

```text
id
title
description
event_date
event_time
venue
club_name
registration_url
created_by
```

## 17.5 Registration

```text
id
event_id
user_id
registered_at
```

Unique constraint:

```text
event_id + user_id
```

---

# 18. Automatic Task Priority

Priority is calculated from the due date:

```text
Past due       → Date Missed
Today          → Very High
≤ 3 days       → High
≤ 7 days       → Medium
> 7 days       → Low
```

The student does not manually set priority.

---

# 19. Technology Stack

## Backend

```text
Python
Flask
```

## Database

Local:

```text
SQLite
```

Deployment:

```text
PostgreSQL
```

## ORM

```text
SQLAlchemy
Flask-SQLAlchemy
```

## Frontend

```text
HTML
CSS
Bootstrap
Jinja2
```

## Typography

```text
JetBrains Mono
```

## Security

```text
Flask sessions
Werkzeug password hashing
```

## Deployment

```text
Render
PostgreSQL
Environment variables
```

## External Integration

```text
Microsoft Graph API
Microsoft Entra / OAuth
```

---

# 20. Project Structure

```text
Student-Task-Board/
│
├── app.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── add_task.html
│   ├── your_tasks.html
│   ├── events.html
│   ├── my_events.html
│   │
│   ├── admin_login.html
│   ├── admin_dashboard.html
│   ├── admin_event_form.html
│   ├── admin_registrations.html
│   └── admin_club_form.html
│
├── static/
│   └── ...
│
├── .gitignore
├── .env.example
├── requirements.txt
└── README.md
```

---

# 21. Environment Variables

`.env.example`:

```env
DATABASE_URL=
SECRET_KEY=
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=
```

Real secrets must stay in `.env` or deployment environment variables.

Do not commit the real `.env` to GitHub.

---

# 22. Application Routes

## Student

```text
/
/login
/logout
/add-task
/your-tasks
/complete-task/<task_id>
/delete-task
/sync-teams
/events
/events/<event_id>/register
/my-events
```

## Admin

```text
/admin/login
/admin/logout
/admin
/admin/events/new
/admin/events/<event_id>/delete
/admin/events/<event_id>/registrations
/admin/clubs/new
```

---

# 23. Current UI Pages

## Student

### Login

`/login`

Student ID login.

### Tasks

`/your-tasks`

Shows:

- task title
- subject
- source
- due date
- priority
- status
- Done
- Delete
- Sync Teams

### Add Task

`/add-task`

Fields:

- task
- subject
- due date
- description

### Events

`/events`

Shows:

- club
- title
- description
- date
- time
- venue
- registration
- external organizer form

### My Events

`/my-events`

Shows registered events.

## Admin

### Admin Login

`/admin/login`

### Admin Dashboard

`/admin`

Shows:

- published event count
- scope
- event list
- registration links
- delete controls
- New Event
- New Club for Super Admin

### Create Event

`/admin/events/new`

### Registrations

`/admin/events/<event_id>/registrations`

### Create Club

`/admin/clubs/new`

Super Admin only.

---

# 24. UI / Design System

The project intentionally uses a distinctive non-AI-looking visual style.

## Design goals

- practical
- clean
- human-designed
- college-oriented
- minimal
- bold but not flashy

## Visual system

```text
Cream background
        +
Matte orange
        +
Matte blue
        +
Black
```

## Design characteristics

- JetBrains Mono
- square corners
- thick black borders
- hard offset shadows
- solid cards
- no gradients
- strong typography
- minimal decoration

---

# 25. Notification System

## Current problem

The notification bell in `base.html` was originally hard-coded.

Example fixed items:

```text
OOP Assignment
Coding Club Event
New College Event
```

Therefore:

```text
Delete task
    ↓
Task disappears
    ↓
Hard-coded notification may remain
```

## Intended solution

Generate notifications from the database using a Flask context processor.

```text
Database
   ↓
Pending Tasks
+
Upcoming Events
   ↓
Notification generator
   ↓
base.html
   ↓
Bell + count
```

Expected behaviour:

```text
Pending task
    → notification appears

Completed task
    → task notification disappears

Deleted task
    → task notification disappears

Upcoming event
    → event notification appears
```

This is an active functional task.

---

# 26. Completed Work

## Core application

- [x] Flask application
- [x] Database setup
- [x] SQLAlchemy models
- [x] Student login
- [x] Student sessions
- [x] Manual task creation
- [x] Automatic priority calculation
- [x] Task completion
- [x] Task deletion

## Teams preparation

- [x] Teams sync route
- [x] Teams assignment fields
- [x] `source`
- [x] `external_id`
- [x] subject support
- [x] isolated demo importer
- [ ] real Microsoft Graph integration

## Events

- [x] Event model
- [x] Club model
- [x] Registration model
- [x] Student events page
- [x] My Events page
- [x] Event registration
- [x] External Google Form URL

## Admin

- [x] Admin authentication
- [x] Password hashing
- [x] Super Admin
- [x] Club Admin
- [x] Club-level event restriction
- [x] Event creation
- [x] Event deletion
- [x] Registration viewing
- [x] Club creation

## UI redesign

- [x] Base theme
- [x] Student login
- [x] Tasks page
- [x] Add Task page
- [x] Events page
- [x] My Events page
- [x] Admin login
- [x] Admin event form
- [x] Admin dashboard
- [x] Create club page

---

# 27. Remaining Work

## P0 - Functional

### 1. Dynamic notifications

Replace hard-coded notifications with database-driven notifications.

### 2. Full testing

Test:

```text
Student login
Task creation
Task completion
Task deletion
Teams demo sync
Event creation
Event registration
My Events
Admin registration view
Admin permissions
Super Admin permissions
```

## P1 - UI

### 3. Finish remaining UI review

Primary remaining page:

```text
admin_registrations.html
```

Also check every page against the same design system.

## P2 - Integration

### 4. Real Microsoft Graph integration

Only after required Microsoft/NMIMS permissions are available.

Expected flow:

```text
Microsoft OAuth
       ↓
Access token
       ↓
Graph API
       ↓
/education/me/assignments
       ↓
Parse assignments
       ↓
Check external_id
       ↓
Insert/update Tasks
       ↓
Dashboard
```

## P3 - Finalization

### 5. Deployment testing

Verify:

- PostgreSQL
- environment variables
- sessions
- database persistence
- Render deployment
- production error handling

### 6. Demo/presentation polish

Prepare a clean end-to-end demonstration.

---

# 28. Recommended Development Order

```text
1. Finish remaining HTML redesign
             ↓
2. Fix dynamic notification bell
             ↓
3. Test student workflow
             ↓
4. Test admin workflow
             ↓
5. Test database behaviour
             ↓
6. Clean UI inconsistencies
             ↓
7. Test deployment
             ↓
8. Prepare Microsoft Graph integration
             ↓
9. Presentation/demo polish
```

Do not add unnecessary features. The current scope is already sufficient for a strong college mini-project.

---

# 29. What the Project Is NOT

Student TaskBoard is not primarily:

- a generic to-do list
- an AI assistant
- an AI planner
- a productivity chatbot
- a notes application
- a college ERP replacement
- a replacement for Microsoft Teams
- a replacement for Google Forms

Instead:

> **Student TaskBoard is a centralized student-facing layer that aggregates academic assignments and campus events from existing college communication channels.**

---

# 30. Why Teams Integration Matters

Without Teams:

```text
Student enters task manually
        ↓
Normal task manager
```

With Teams:

```text
Teacher publishes assignment
        ↓
Microsoft Teams
        ↓
TaskBoard sync
        ↓
Assignment appears automatically
```

The student does not have to manually recreate the assignment.

This is the key distinction between the original task manager and the current project.

---

# 31. Why the Events Module Matters

Instead of:

```text
WhatsApp
Instagram
Club groups
Google Forms
College messages
```

students can use:

```text
Student TaskBoard
       ↓
Campus Events
       ↓
Coding Club
Atrangi Club
College Events
```

Students can discover events, register, and see their registered events.

---

# 32. Why the Admin System Matters

The project is not only a student task list.

Clubs get a structured way to publish activities.

```text
Club Admin
     ↓
Publishes event
     ↓
Student TaskBoard
     ↓
Students discover event
     ↓
Students register
     ↓
Club sees registrations
```

Role hierarchy:

```text
                 ADMIN
                   │
          ┌────────┴────────┐
          │                 │
    SUPER ADMIN        CLUB ADMIN
          │                 │
     All clubs         Own club only
     All events        Own events
```

---

# 33. Expected Impact

The project aims to:

- reduce the need to search multiple platforms
- make academic assignments easier to find
- make campus events easier to discover
- provide a centralized view of upcoming activities
- simplify event registration
- give clubs a structured publishing interface
- reduce dependence on buried messages for finding information

Avoid saying:

> “The system will eliminate missed deadlines.”

Prefer:

> **The system is intended to reduce the effort involved in finding and tracking academic and campus information.**

---

# 34. Presentation Context

Current presentation structure:

## 1. Problem Statement

Explain scattered academic/event information.

## 2. Survey Objective

Explain why students were surveyed.

## 3. Survey

Show questions and methodology.

## 4. Survey Analysis

Show results and observations.

## 5. Key Insights

Explain what the responses revealed.

## 6. Idea Proposal

Introduce Student TaskBoard.

## 7. Expected Impact

Explain what the proposed system aims to improve.

Intentionally removed:

- generic introduction
- “What makes it different?”
- overly detailed proposed workflow
- old workload/crunch score concepts

---

# 35. Project Pitch

## One-line pitch

> **Student TaskBoard is a centralized college portal that brings students' academic assignments and campus events into one place by integrating assignment sources such as Microsoft Teams and providing a structured platform for clubs to publish and manage events.**

## 10-second pitch

> **It's a centralized student dashboard for academic assignments and college events, so students don't have to keep searching across multiple platforms.**

---

# 36. Final Architecture

```text
                         STUDENT TASKBOARD
                                │
             ┌──────────────────┴──────────────────┐
             │                                     │
       ACADEMIC SIDE                         CAMPUS SIDE
             │                                     │
      Microsoft Teams                         Club Admins
             │                                     │
       Assignments                              Events
             │                                     │
      Graph API*                                Publish
             │                                     │
             ↓                                     ↓
        ┌───────────┐                       ┌────────────┐
        │   Tasks   │                       │   Events   │
        └─────┬─────┘                       └─────┬──────┘
              │                                   │
              └──────────────┬────────────────────┘
                             ↓
                    STUDENT DASHBOARD
                             │
              ┌──────────────┼──────────────┐
              ↓              ↓              ↓
            Tasks          Events       Notifications
              │              │
           Complete       Register
              │              │
              ↓              ↓
          PostgreSQL      Registration
                             │
                             ↓
                       My Events

* Currently DEMO importer.
  Real Microsoft Graph integration requires
  appropriate Microsoft/NMIMS tenant permissions.
```

---

# 37. Final Project Definition

> **Student TaskBoard is a Flask-based college portal designed to solve the problem of scattered academic and campus information by bringing assignments and college events into one centralized student dashboard. Academic assignments are intended to be imported from Microsoft Teams through Microsoft Graph, while clubs and college administrators can publish events, provide registration links, and manage student registrations. The current prototype includes student task management, a demo Teams importer, event discovery and registration, club-based admin management, notifications, and a PostgreSQL-ready database architecture.**

---

# 38. Current Status Snapshot

| Area | Status |
|---|---|
| Flask backend | 🟢 Mostly complete |
| Database models | 🟢 Complete |
| Student login | 🟢 Functional |
| Task management | 🟢 Functional |
| Automatic priority | 🟢 Functional |
| Events | 🟢 Functional |
| Event registration | 🟢 Functional |
| Admin system | 🟢 Functional |
| Club permissions | 🟢 Functional |
| UI redesign | 🟢 Mostly complete |
| Notifications | 🟡 Needs dynamic implementation/final testing |
| Teams demo importer | 🟢 Functional |
| Real Microsoft Graph | 🔴 Pending permissions |
| PostgreSQL support | 🟢 Prepared |
| Deployment architecture | 🟢 Prepared |
| Presentation structure | 🟢 Complete |
| Final testing | 🟡 Remaining |

---

# 39. Immediate Next Actions

### Right now

1. Finish remaining HTML redesign/review.
2. Fix the notification system.
3. Run through all student workflows.
4. Run through all admin workflows.
5. Check role-based access.
6. Check database persistence.
7. Test deployment.

### After the prototype is stable

8. Work on real Microsoft Graph integration if permissions are available.
9. Prepare the final project demo.
10. Prepare final documentation/presentation.

---

# 40. Important Development Rules

When continuing this project:

- Keep the project focused.
- Do not turn it into an AI product.
- Do not add features just because they are technically possible.
- Prefer practical college workflows.
- Preserve the Flask + SQLAlchemy architecture unless there is a strong reason to change it.
- Keep Microsoft Graph integration isolated from the rest of the application.
- Do not bypass Microsoft/NMIMS permissions.
- Keep student and admin permissions separate.
- Keep Club Admins restricted to their own club.
- Keep the UI consistent with the cream/orange/blue/black design system.
- Use JetBrains Mono.
- Avoid gradients and generic AI-dashboard styling.
- Prefer copy-paste-ready, incremental code changes.
- When changing templates, preserve existing routes and backend logic unless a backend change is actually required.
- Test existing functionality after every meaningful change.

---

# 41. Master Mental Model

The entire project can be remembered as:

```text
                 INFORMATION IS SCATTERED
                           │
          ┌────────────────┴────────────────┐
          │                                 │
     ACADEMIC                            CAMPUS
          │                                 │
   Microsoft Teams                      Clubs
          │                                 │
    Assignments                         Events
          │                                 │
          └────────────────┬────────────────┘
                           ↓
                  STUDENT TASKBOARD
                           │
          ┌────────────────┼────────────────┐
          │                │                │
        TASKS            EVENTS        NOTIFICATIONS
          │                │
       Complete         Register
          │                │
          └────────────────┘
                           │
                       DATABASE
                           │
                  PostgreSQL in production
```

## Core purpose

> **Bring scattered college information into one practical student dashboard.**

---

# END OF MASTER CONTEXT
