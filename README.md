# Student TaskBoard

Minimal Flask web app for academic tasks and campus events.

## Features
- Student login (simple ID for now)
- Manual academic tasks
- Demo Microsoft Teams sync layer
- Deadline-based priority and alerts
- Club/college event discovery
- Event registration and optional external Google Form link
- Separate admin dashboard for each club
- Super Admin with ability to create additional clubs
- PostgreSQL support through `DATABASE_URL`
- JetBrains Mono based minimal UI

## Demo admin accounts
- `superadmin` / `super123`
- `codingadmin` / `coding123`
- `atrangiadmin` / `atrangi123`
- `collegeadmin` / `college123`

Change these before any real deployment.

## Teams integration
`/sync-teams` currently imports mock Teams assignments. The function is isolated so the mock data can later be replaced by Microsoft Graph after Entra/Graph permissions are approved by the college.
