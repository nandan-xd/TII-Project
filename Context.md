Student TaskBoard - Complete Project Context

1. Project Identity

Project Name: Student TaskBoard

Student TaskBoard is a college-focused centralized student portal that brings together:

Academic tasks and assignments

College events and activities

The core problem is not that students cannot create a to-do list. The problem is that college information is scattered across multiple platforms.

Typical flow:

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

The goal is to provide one student-facing place where students can see what they need to do and what is happening on campus.

2. Why the Project Exists

The original project was essentially a normal task-management application:

manually add tasks

enter deadlines

assign priority

view tasks

delete tasks

mark tasks complete

During the project presentation, the professor/ma'am pointed out an important weakness:

If a student has to manually enter the deadline and priority, the student already knows the information and can manage it themselves.

That led to the main conceptual change.

Original concept

A better to-do list for students.

Current concept

A centralized student information dashboard that aggregates academic assignments and campus events.

This shift is very important to the project's identity.

3. Problem Statement

Students receive college-related information through multiple platforms.

Academic information

Usually comes through:

Microsoft Teams

class groups

messages

teacher announcements

other academic channels

Event information

Usually comes through:

WhatsApp

club groups

Instagram

college announcements

Google Forms

messages

This creates several problems:

Problem 1: Information is scattered

Students have to check multiple platforms.

Problem 2: Information gets buried

Important assignments or event announcements can disappear into old messages.

Problem 3: Deadlines/events can be forgotten

A student may know about something but still forget to act on it.

Problem 4: Event registration is fragmented

A club may announce an event in one place and use a separate Google Form for registration.

Problem 5: There is no unified student view

Academic tasks and campus activities exist separately.

The defensible problem statement is:

College information is distributed across multiple platforms, increasing the effort required to find, remember and act on it.

Do not claim that every student constantly misses deadlines.

4. Survey Findings

A survey was conducted to validate the problem.

Some responses included:

"By searching in WhatsApp"

"Go through the older messages."

"I almost forgot I had to submit my DM tutorial."

"during MTT i missed an assignment and an event"

"check older messages, WhatsApp, friends"

The survey indicated that students commonly rely on:

WhatsApp

Microsoft Teams

messages

calendars

friends

other channels

for college-related information.

A useful observation from the survey was that 70% of respondents reported often needing to search older messages for college-related information.

The responses were not uniform. Some students reported never missing deadlines, while others reported missing or almost missing assignments/events.

Therefore, the project should frame the issue as information fragmentation and retrieval effort, rather than claiming universal deadline failure.

5. Empathy / Design Thinking Work

The project went through the Empathy phase.

Recurring observations

Students rely heavily on WhatsApp, Microsoft Teams and messages.

Students often search older messages for information.

Some students miss or almost miss assignments, deadlines or event registrations.

Students use multiple platforms/methods to track information.

Students show interest in having academic tasks and college events in one place.

Student pains

scattered information

buried announcements

forgotten assignments

forgotten registrations

repeated searching

too many places to check

Desired gains

one place to check

easier assignment/deadline access

less searching

easier event discovery

convenient event registration

Define-phase insight

A centralized platform that brings academic assignments and college events together.

6. What the Application Does

The application has two major sides.

A. Student side

Students can:

log in

view academic tasks

manually add tasks

sync/import Teams assignments

mark tasks complete

delete tasks

see automatically calculated task priority

browse college events

discover events

register for events

view their registered events

receive dashboard notifications

B. Admin side

Admins manage events.

There are two levels.

Club Admin

Each club gets its own admin.

Example:

Coding Club Admin
        ↓
Can manage Coding Club events

Atrangi Club Admin
        ↓
Can manage Atrangi Club events

College Events Admin
        ↓
Can manage College Events

A club admin should not be able to manage another club's events.

Super Admin

Super Admin can:

view all clubs

view all events

create events

delete events

view registrations

create new clubs

7. Clubs Currently Supported

The initial seeded clubs are:

Coding Club

Technology, coding and hackathon activities.

Atrangi Club

Creative, cultural and artistic activities.

College Events

College-wide events, workshops and competitions.

The Super Admin can later create additional clubs.

8. Event Workflow

Club Admin
     ↓
Admin Dashboard
     ↓
Create Event
     ↓
Enter:
    • Event name
    • Date
    • Time
    • Venue
    • Description
    • Registration form
     ↓
Publish
     ↓
Student sees event
     ↓
Student registers
     ↓
Event appears in "My Events"

9. Google Forms Integration

A club may already have a Google Form for registration.

The project does not need to rebuild the entire registration system.

Instead, the admin can provide an external registration URL.

Example:

Event:
Hackathon 2026

Student TaskBoard:
[Register]

External organizer form:
[Open organizer form ↗]

The portal handles event discovery and stores its own registration record, while the club can continue using its existing Google Form.

10. Microsoft Teams Integration

This is the major planned integration.

Desired final architecture:

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

The relevant Microsoft Graph Education endpoint discussed is:

GET /v1.0/education/me/assignments

The relevant delegated permission discussed is:

EduAssignments.ReadBasic

The intended workflow is:

Teacher creates assignment
        ↓
Teams
        ↓
Student TaskBoard sync
        ↓
Assignment appears automatically

This is what makes the academic side more meaningful than a normal manual to-do list.

11. Current Teams Situation

The real Microsoft Teams integration is not fully connected yet.

Microsoft Entra/Azure access issues were encountered with the NMIMS account, including tenant/application registration restrictions.

The project cannot legitimately bypass those tenant restrictions.

If the college tenant does not allow students to register applications or obtain the required Graph permissions, the real integration requires one of:

College IT registers/approves the application.

An administrator grants the required permissions.

Development happens using a separate Microsoft 365 Education test tenant.

12. Current Teams Solution: Demo Importer

For now, the project contains a demo Teams importer.

It is intentionally isolated so Microsoft Graph can replace it later.

Current route:

POST /sync-teams

It creates demo assignments such as:

OOP Assignment 3
Subject:
Object Oriented Programming

and:

CN Lab Report
Subject:
Computer Networks

These are stored as normal Tasks with:

source = "Teams"

and an:

external_id

The database is therefore already prepared for externally imported assignments.

13. Why the Demo Importer Is Useful

The prototype can demonstrate:

Student
 ↓
Sync Teams
 ↓
Assignments imported
 ↓
Tasks appear automatically
 ↓
Dashboard displays them

Later, the implementation can change from:

demo_assignments = [...]

to:

Microsoft Graph API

without redesigning the dashboard.

The importer was deliberately isolated for this reason.

14. Student Login

Current student authentication is intentionally simple.

Students enter their student ID:

Student ID
[ 23XXXXX ]

[ Continue → ]

No password system is currently required for students.

The session stores:

session['user_id']

This is suitable for the current prototype.

15. Future Student Authentication

The planned future flow is:

NMIMS Microsoft Account
        ↓
Microsoft OAuth
        ↓
Student authenticated
        ↓
Microsoft Graph
        ↓
Assignments retrieved

This would allow Microsoft authentication to serve both authentication and authorization for Teams data.

16. Admin Authentication

Admins have a separate login:

/admin/login

Admin accounts are stored in the database.

Admin fields include:

username
password_hash
role
club_name

Roles:

super_admin
club_admin

Club admins have a club_name.

17. Development Admin Accounts

The development database currently seeds:

superadmin
codingadmin
atrangiadmin
collegeadmin

with development passwords.

These are prototype credentials and should be changed before real deployment.

Passwords are hashed using:

generate_password_hash()

and checked using:

check_password_hash()

18. Database Models

The application uses SQLAlchemy.

There are five main models:

Tasks

Admin

Club

Event

Registration

19. Tasks Model

Stores academic tasks.

Fields:

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

Important fields

source

Distinguishes:

Manual
Teams

external_id

Identifies an externally imported assignment.

subject

Stores the academic subject.

status

Currently:

Pending
Completed

20. Automatic Task Priority

Priority is calculated automatically from the due date.

Current rules:

Past due       → Date Missed
Today          → Very High
≤ 3 days       → High
≤ 7 days       → Medium
> 7 days       → Low

The student does not manually enter priority.

This is important because the original project criticism was partly about students manually setting information the system could determine itself.

21. Admin Model

Stores admin accounts.

Fields:

id
username
password_hash
role
club_name

22. Club Model

Stores clubs.

Fields:

id
name
description

Initial examples:

Coding Club
Atrangi Club
College Events

23. Event Model

Stores campus events.

Fields:

id
title
description
event_date
event_time
venue
club_name
registration_url
created_by

24. Registration Model

Stores which student registered for which event.

Fields:

id
event_id
user_id
registered_at

There is a unique constraint on:

event_id + user_id

Therefore a student cannot register for the same event twice.

25. Technology Stack

Backend

Python + Flask

Database

Development:

SQLite

Production:

PostgreSQL

ORM:

SQLAlchemy / Flask-SQLAlchemy

Frontend

HTML
CSS
Bootstrap
Jinja2

Custom CSS is layered over Bootstrap.

Font

JetBrains Mono

Security

Admin password hashing:

Werkzeug

Session authentication:

Flask sessions

Deployment

The project has been designed around:

Render
+
PostgreSQL

with environment variables.

External Integration

Planned:

Microsoft Graph API

for Teams Education assignments.

Potential future authentication:

Microsoft Entra ID / Microsoft OAuth

26. Current Visual Design

The UI has been redesigned into a strong, consistent visual identity.

Colors

Cream / off-white
        +
Matte orange
        +
Matte blue
        +
Black

Style

square corners

thick black borders

hard offset shadows

solid cards

no gradients

minimal decoration

JetBrains Mono

strong typography

practical dashboard appearance

The design goal is:

Human-designed college portal, not an AI dashboard.

The project should look practical and intentional rather than like a generic AI SaaS template.

27. Student Pages

Login

/login

Student ID login.

Tasks

/your-tasks

Shows:

task title

subject

source

due date

priority

status

Done

Delete

Also contains:

↻ Sync Teams

Add Task

/add-task

Allows:

task

subject

due date

description

Priority is calculated automatically.

Events

/events

Displays campus events.

Each event can show:

club

title

description

date

time

venue

registration

organizer form

My Events

/my-events

Shows events the student has registered for.

28. Admin Pages

Admin Login

/admin/login

Admin Dashboard

/admin

Shows:

published event count

admin scope

events

registration links

delete controls

create event

Super Admin's create club button

Create Event

/admin/events/new

Registrations

/admin/events/<event_id>/registrations

Shows students registered for an event.

Create Club

/admin/clubs/new

Super Admin only.

29. Navbar

The navbar provides access to the main student areas.

Conceptually:

STUDENT TASKBOARD

Tasks
Events
My Events
🔔
Logout

The notification bell is part of the shared base.html.

30. Notification System

This is one of the parts currently being improved.

Originally, the notification bell in base.html was hard-coded.

It contained fixed items such as:

OOP Assignment
Coding Club Event
New College Event

This caused a bug.

For example:

Task exists
   ↓
Notification appears

Task deleted
   ↓
Notification should disappear

But because the notification was hard-coded, it could remain visible after the task was deleted or completed.

31. Correct Notification Architecture

The intended fix is to make notifications database-driven using a Flask context processor.

Conceptually:

Database
   ↓
Pending tasks
   +
Upcoming events
   ↓
Notification generator
   ↓
base.html
   ↓
Bell

Therefore:

Pending task

Can appear in notifications.

Completed task

Should disappear from task notifications.

Deleted task

Should disappear.

Upcoming event

Can appear.

This is much cleaner than hard-coded notification content.

32. Current Notification Idea

Notifications can include:

Tasks

Based on:

Pending

and ordered by due date.

Events

Upcoming campus events can appear.

The bell count should be generated from the actual notification list.

33. Important Backend Routes

Current routes include:

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

/admin/login

/admin/logout

/admin

/admin/events/new

/admin/events/<event_id>/delete

/admin/events/<event_id>/registrations

/admin/clubs/new

34. Backend Architecture

The backend is currently a single Flask application:

app.py

Conceptually:

Flask app
    │
    ├── Database configuration
    │
    ├── Models
    │     ├── Tasks
    │     ├── Admin
    │     ├── Club
    │     ├── Event
    │     └── Registration
    │
    ├── Authentication
    │
    ├── Student routes
    │
    ├── Task management
    │
    ├── Teams importer
    │
    ├── Event management
    │
    └── Admin management

For a college mini-project, keeping this relatively simple is intentional.

35. Project Structure

Approximate structure:

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

The exact static files may vary depending on the current repository state.

36. Environment Variables

The project uses environment variables for secrets/configuration.

.env.example:

DATABASE_URL=
SECRET_KEY=
MICROSOFT_CLIENT_ID=
MICROSOFT_CLIENT_SECRET=

The real .env must not be committed to GitHub.

37. Gitignore

The project already ignores common development files such as:

__pycache__
venv
.env
instance
*.db
*.sqlite
.vscode
.idea
.pytest_cache
build
dist

This prevents local databases, secrets and development junk from being pushed.

38. What Is Already Done

Core application

Flask application

Database setup

SQLAlchemy models

Student login

Student sessions

Manual task creation

Automatic priority calculation

Task completion

Task deletion

Teams preparation

Teams sync route

Teams assignment fields in database

source field

external_id

subject support

isolated demo importer

Real Microsoft Graph integration

Events

Event model

Club model

Registration model

Student events page

My Events page

Event registration

External Google Form URL

Admin

Admin authentication

Password hashing

Super Admin

Club Admin

Club-level event restriction

Event creation

Event deletion

Registration viewing

Club creation

UI

Base theme

Student login redesign

Task page redesign

Add task redesign

Events redesign

My Events redesign

Admin login redesign

Admin event form redesign

Admin dashboard redesign

Create club redesign

Design system

JetBrains Mono

matte orange

matte blue

cream background

black borders

solid cards

hard shadows

square corners

39. What Still Needs To Be Done

The project is not completely finished, but the core application is in place.

Priority 1: Finish UI

Potential remaining page to redesign/review:

admin_registrations.html

Also check any remaining pages for consistency with the new visual system.

Priority 2: Fix dynamic notifications

Replace the hard-coded notification bell with database-driven notifications.

This is currently an important functional improvement.

Priority 3: Test workflows

Student workflow

Login
 ↓
Add task
 ↓
Task appears
 ↓
Mark complete
 ↓
Notification disappears
 ↓
Delete task
 ↓
Task disappears

Event workflow

Admin creates event
 ↓
Student sees event
 ↓
Student registers
 ↓
My Events updates
 ↓
Admin sees registration

Permission workflow

Coding Admin
    ↓
Coding events only

and:

Super Admin
    ↓
All events
    +
All clubs

Priority 4: Teams integration

Eventually replace:

demo_assignments = [...]

with Microsoft Graph.

40. Final Teams Implementation

Expected eventual flow:

Microsoft OAuth
       ↓
Access token
       ↓
Graph API
       ↓
/education/me/assignments
       ↓
Parse assignment
       ↓
Check external_id
       ↓
Insert/update Tasks
       ↓
Dashboard

The existing database fields provide the foundation for this.

41. Duplicate Assignment Handling

The external_id exists specifically to prevent duplicates.

Example:

First sync:

assignment ID = 12345
       ↓
12345 does not exist
       ↓
Create task

Second sync:

assignment ID = 12345
       ↓
12345 already exists
       ↓
Do not create duplicate

This is an important part of the eventual real Teams sync.

42. Expected Final Student Experience

                 STUDENT TASKBOARD
                        │
          ┌─────────────┴─────────────┐
          │                           │
       ACADEMIC                    CAMPUS
          │                           │
     Microsoft Teams                Clubs
          │                           │
     Assignments                    Events
          │                           │
          └─────────────┬─────────────┘
                        │
                 STUDENT DASHBOARD
                        │
             ┌──────────┼──────────┐
             │          │          │
           Tasks      Events     Alerts
             │          │          │
          Complete   Register    Bell

43. What the Project Is NOT

The project is not primarily:

a generic to-do list

an AI assistant

an AI planner

a productivity chatbot

a notes application

a college ERP replacement

a replacement for Microsoft Teams

a replacement for Google Forms

Instead:

It is a centralized student-facing layer that aggregates academic assignments and campus events from existing college communication channels.

44. Why Microsoft Teams Matters

Without Teams integration:

Student enters task manually

This becomes a normal task manager.

With Teams integration:

Teacher publishes assignment
          ↓
Teams
          ↓
TaskBoard automatically receives it

The student does not have to manually recreate the assignment.

That is the key distinction between the original project and the current concept.

45. Why the Events Section Matters

Instead of:

WhatsApp
Instagram
Club groups
Google Forms
College messages

students can browse:

Student TaskBoard
       ↓
Campus Events
       ↓
Coding Club
Atrangi Club
College Events

and register through the portal and/or the organizer's external form.

46. Why Admins Matter

The portal is not only a student task list.

Clubs get a structured way to publish activities.

The ecosystem becomes:

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

User types:

STUDENT
ADMIN

Admin roles:

SUPER ADMIN
CLUB ADMIN

47. Expected Impact

The project aims to:

reduce the need to search multiple platforms

make academic assignments easier to find

make campus events easier to discover

provide a centralized view of upcoming activities

simplify event registration

give clubs a structured publishing interface

reduce dependence on buried messages for finding information

Avoid claiming:

"The system will eliminate missed deadlines."

Better wording:

The system is intended to reduce the effort involved in finding and tracking academic and campus information.

48. Current Presentation Structure

The current presentation structure is:

1. Problem Statement

Explain scattered academic/event information.

2. Survey Objective

Explain why students were surveyed.

3. Survey

Show questions and methodology.

4. Survey Analysis

Show results and observations.

5. Key Insights

Explain what the responses revealed.

6. Idea Proposal

Introduce Student TaskBoard.

7. Expected Impact

Explain what the proposed system aims to improve.

Unnecessary slides were intentionally removed, including:

generic introduction

"What makes it different?"

overly detailed proposed workflow

old workload/crunch score concepts

49. One-Line Project Pitch

If the professor asks:

"What is Student TaskBoard?"

Use:

Student TaskBoard is a centralized college portal that brings students' academic assignments and campus events into one place by integrating assignment sources such as Microsoft Teams and providing a structured platform for clubs to publish and manage events.

50. Short Pitch

If you have about 10 seconds:

It's a centralized student dashboard for academic assignments and college events, so students don't have to keep searching across multiple platforms.

51. Recommended Development Order From Here

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
8. Prepare Teams Graph integration layer
             ↓
9. Presentation/demo polish

Do not start adding random features.

The project already has enough scope. The priority now is to make the existing system reliable, coherent and presentation-ready.

52. Final Project Architecture

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

53. Final Definition

Student TaskBoard is a Flask-based college portal designed to solve the problem of scattered academic and campus information by bringing assignments and college events into one centralized student dashboard. Academic assignments are intended to be imported from Microsoft Teams through Microsoft Graph, while clubs and college administrators can publish events, provide registration links, and manage student registrations. The current prototype includes student task management, a demo Teams importer, event discovery and registration, club-based admin management, notifications, and a PostgreSQL-ready database architecture.

Current Status

Area

Status

Core Flask app

Mostly complete

Database

Complete

Student task management

Functional

Automatic priority

Functional

Events

Functional

Event registration

Functional

Admin system

Functional

Club roles

Functional

UI redesign

Mostly complete

Notifications

Being corrected

Teams demo importer

Functional

Real Microsoft Graph

Pending permissions

PostgreSQL support

Prepared

Deployment architecture

Prepared

Presentation

Core structure complete

Immediate next tasks

Finish remaining HTML redesign/review.

Fix the notification bell so it uses actual database data.

Test all student and admin workflows.

Test deployment/database behaviour.

Then work on the real Microsoft Graph integration if the required Microsoft/NMIMS permissions become available.