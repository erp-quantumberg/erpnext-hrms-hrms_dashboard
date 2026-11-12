# HRMS Dashboard

## Table of contents

- [Overview](#overview)
- [Features](#features)
- [Technology](#technology)
- [Requirements](#requirements)
- [Installation](#installation)
- [Frontend development](#frontend-development)
- [Build and deployment](#build-and-deployment)
- [How the dashboard works](#how-the-dashboard-works)
- [Data sources and date behavior](#data-sources-and-date-behavior)
- [Roles, permissions, and privacy](#roles-permissions-and-privacy)
- [Configuration](#configuration)
- [Project structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Testing and code quality](#testing-and-code-quality)
- [Contributing](#contributing)
- [License](#license)

## Overview

HRMS Dashboard is a Frappe app with a Vue 3 dashboard embedded in the Frappe
Desk. It provides a personal workspace for employees and a workforce overview
for HR users and administrators. Dashboard records are read from the installed
Frappe/HRMS site using the signed-in user's session.

The dashboard is available at `/app/hrms_dashboard`. Its frontend is built
with Vite and output to the app's `hrms_dashboard/public/frontend` directory.
The Frappe app hook includes the generated JavaScript bundle in the Desk; the
bundle mounts the Vue interface only when the current Desk route is
`hrms_dashboard`.

This repository contains the dashboard app and its frontend. The dashboard
uses standard Frappe and HRMS DocTypes; it does not provide a separate HR
database, login system, WhatsApp integration, or custom public API.

## Features

### Employee workspace

- **Attendance summary:** counts submitted Present, Absent, and Half Day
  Attendance records for the selected date range.
- **GPS check-in/check-out:** records an Employee Checkin with the employee,
  `IN` or `OUT` log type, current browser time, latitude, and longitude. The
  browser must support and grant location access, and the selected date range
  must include today.
- **Check-in history:** shows up to five recent Employee Checkin records in
  the selected range.
- **Shift:** shows the first submitted Shift Assignment overlapping the
  selected range and its Shift Type times, if available.
- **Leave overview:** lists up to four Leave Applications overlapping the
  selected range and up to four submitted Leave Allocations overlapping it.
  Allocations display the allocated amount; this card does not calculate
  remaining leave balance.
- **Salary slips:** lists up to five submitted Salary Slips overlapping the
  selected range. Net pay can be hidden or shown in the interface, and a
  Standard-format PDF can be downloaded.
- **Assigned tasks:** lists up to four open ToDo records allocated to the user
  with a due date in the selected range.
- **Holidays:** shows up to five upcoming holidays from available Holiday Lists.
- **Shortcuts:** opens related Frappe pages, including Attendance, Employee
  Checkin, ToDo, Leave Application, Shift Assignment, Salary Slip, Holiday
  List, Employee, and User.

### HR workspace

- Displays employee and department totals, Present and Absent attendance
  counts, leave applications, submitted salary slips, and the payroll summary
  for the selected range.
- Displays an Employee Checkin table grouped by employee and date. The table
  uses the earliest `IN` and latest `OUT` record found for each day.
- Shows upcoming holidays and shortcuts to HRMS pages.

### Administrator overview

- Displays the same workforce metrics, attendance overview, leave application
  list, salary slip summary, holidays, and HRMS shortcuts.
- Does not display the HR-only employee check-in table.

### Shared behavior

- The initial date range is today. Users can apply a date range or reset it to
  today; a start date later than the end date is rejected.
- Notifications show up to 30 recent Notification Log records for the signed-in
  user. Users can mark a notification as read and open its linked Desk record
  when it has one.
- While the notification panel is closed, the notification list refreshes once
  per minute.
- The interface is responsive and its dashboard CSS is loaded inside a Shadow
  DOM to isolate it from Desk styles.
- Dates and amounts are currently formatted for the `en-IN` locale and Indian
  rupees (₹).

## Technology

| Area                                 | Technology                                        |
| ------------------------------------ | ------------------------------------------------- |
| Frontend framework                   | Vue 3                                             |
| Build tool and development server    | Vite                                              |
| UI components and Frappe integration | Frappe UI                                         |
| Styling                              | Tailwind CSS and project CSS                      |
| Charts package                       | ApexCharts and `vue3-apexcharts` are dependencies |
| Backend platform                     | Frappe Framework and the HRMS app                 |
| Frontend package manager             | npm (a `package-lock.json` is provided)           |

Key frontend package versions are declared in `frontend/package.json` and
locked in `frontend/package-lock.json`:

| Package              | Declared version |
| -------------------- | ---------------- |
| `vue`                | `^3.2.25`        |
| `vue-router`         | `^4.0.12`        |
| `frappe-ui`          | `^0.0.105`       |
| `vite`               | `^2.7.2`         |
| `tailwindcss`        | `^3.0.15`        |
| `@vitejs/plugin-vue` | `^2.0.0`         |
| `apexcharts`         | `^6.6.1`         |
| `vue3-apexcharts`    | `^1.11.1`        |

## Requirements

- A working Frappe bench and site.
- Python 3.10 or later, as specified in `pyproject.toml`.
- Node.js and npm for frontend development and asset generation. The repository
  CI workflow uses Node.js 18.
- The Frappe HRMS app installed on the site before using HRMS records.
- A signed-in Frappe user. To receive the employee workspace, the account must
  be linked to an Employee record through `Employee.user_id`.
- Appropriate Frappe roles and DocType permissions for the records that the
  user is expected to see or create.

This repository does not pin a specific Frappe or HRMS version in its package
metadata. Confirm compatibility with the versions installed on your bench.

## Installation

### 1. Install HRMS

Install the Frappe HRMS app on your bench and site if it is not already
installed. Follow the installation instructions for the HRMS version used by
your bench.

### 2. Fetch this app

From the bench directory:

```bash
bench get-app hrms_dashboard <REPOSITORY_URL>
```

Replace `<REPOSITORY_URL>` with the Git URL for this repository.

### 3. Install the app on your site

```bash
bench --site <SITE_NAME> install-app hrms_dashboard
```

Replace `<SITE_NAME>` with the Frappe site name.

### 4. Build frontend assets

From the app's frontend directory:

```bash
cd apps/hrms_dashboard/frontend
npm ci
npm run build
```

Then, from the bench directory, build the app assets:

```bash
bench build --app hrms_dashboard
```

### 5. Open the dashboard

Sign in to the site and open **HRMS Dashboard** from the Desk or navigate to:

```text
/app/hrms_dashboard
```

## Frontend development

### Install frontend dependencies

From `apps/hrms_dashboard/frontend`:

```bash
npm ci
```

`npm ci` installs the versions recorded in `package-lock.json`.

### Start Vite

Start the Frappe bench in one terminal:

```bash
cd <BENCH_DIRECTORY>
bench start
```

In another terminal, from `apps/hrms_dashboard/frontend`:

```bash
npm run dev
```

Vite listens on port `8080`. Its development proxy targets the Frappe web
server port configured in `sites/common_site_config.json`.

The dashboard is integrated with the Frappe Desk rather than being a standalone
Vue site: `src/main.js` waits for the Frappe Desk runtime and mounts only on the
`hrms_dashboard` Desk route. For an end-to-end check of the Desk integration,
build the assets and open the dashboard in the signed-in Frappe site.

### Preview a production build

After running `npm run build`, the package provides:

```bash
npm run preview
```

The preview server is for inspecting the generated Vite output. The complete
Desk experience still requires the Frappe runtime and an authenticated site.

## Build and deployment

The production frontend build is configured in `frontend/vite.config.js`:

- Output directory: `hrms_dashboard/public/frontend`
- JavaScript entry file: `index.js`
- CSS entry file: `index.css`
- Production asset base: `/assets/hrms_dashboard/frontend/`
- JavaScript output format: IIFE bundle named `HRMSDashboard`

The Frappe app hook in `hrms_dashboard/hooks.py` includes
`/assets/hrms_dashboard/frontend/index.js` in Desk pages. The JavaScript checks
the current Frappe route, mounts the Vue app on `hrms_dashboard`, and unmounts
it after navigating away.

For deployment, rebuild the frontend after changing frontend source, then run
`bench build --app hrms_dashboard` from the bench directory. Refresh the browser
after deployment; if old assets remain visible, clear the site cache and
perform a hard refresh.

## How the dashboard works

1. The Frappe hook loads the built JavaScript bundle in Desk.
2. `frontend/src/main.js` waits until Frappe's router is available.
3. On the `hrms_dashboard` route, the script creates a host element and a
   Shadow DOM, loads the built CSS inside it, and mounts the Vue application.
4. `frontend/src/pages/Home.vue` identifies the signed-in user and their
   workspace.
5. The frontend requests data through Frappe's standard REST resource endpoints
   and `frappe.client.get_count`, using the current session and Frappe
   permissions.
6. User actions such as marking notifications read or recording a check-in
   write through those same authenticated Frappe endpoints.

There are no app-specific Python API methods used by this dashboard in the
current implementation. The page controller at
`hrms_dashboard/www/hrms_dashboard.py` supplies no-cache page context for the
website page; the Desk dashboard itself is mounted by the app's Desk JavaScript
hook.

## Data sources and date behavior

| Dashboard information        | DocType or endpoint                             | Date/filter behavior                                                                                                                               |
| ---------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| Signed-in user and profile   | `frappe.auth.get_logged_user`, User             | The linked Employee is looked up by `Employee.user_id`.                                                                                            |
| Employee totals              | Employee                                        | Total count; not limited by the selected range.                                                                                                    |
| Department totals            | Department                                      | Total count; not limited by the selected range.                                                                                                    |
| Employee attendance          | Attendance                                      | Submitted records for the employee and selected dates.                                                                                             |
| Workforce attendance metrics | Attendance                                      | Submitted records within the selected dates; Present and Absent are counted separately.                                                            |
| Check-in history             | Employee Checkin                                | Employee records between the selected dates.                                                                                                       |
| HR check-in table            | Employee Checkin                                | Records in the selected range, grouped by employee and calendar date. HR workspace only.                                                           |
| Leave applications           | Leave Application                               | Applications whose `from_date`/`to_date` overlap the selected range. The workforce pending count includes statuses `Open`, `Pending`, and `Draft`. |
| Employee leave allocations   | Leave Allocation                                | Submitted allocations overlapping the selected range. The displayed value is allocated leave, not a computed balance.                              |
| Employee salary slips        | Salary Slip                                     | Submitted slips whose salary period overlaps the selected range; net pay is displayed and can be hidden in the UI.                                 |
| Workforce payroll            | Salary Slip                                     | Submitted slips whose salary period overlaps the selected range; the summary total uses `gross_pay`.                                               |
| Tasks                        | ToDo                                            | Open tasks allocated to the signed-in user and due within the selected dates.                                                                      |
| Shift details                | Shift Assignment and Shift Type                 | Submitted assignments overlapping the selected dates; the first result is shown.                                                                   |
| Upcoming holidays            | Holiday List Assignment, Employee, Holiday List | Uses assigned lists where available, then falls back to available Holiday Lists; shows the next five upcoming holidays.                            |
| Notifications                | Notification Log                                | Up to 30 records for the signed-in user, newest first.                                                                                             |

The date range is used for date-based dashboard sections. Employee totals,
department totals, and upcoming holidays are not constrained to that range.
Some dashboard cards intentionally show only a short list of records; use the
linked Frappe page to see the full list.

## Roles, permissions, and privacy

The frontend chooses which workspace to render using the signed-in user's
identity, roles, and linked Employee record:

| Detection                                                                                | Workspace                                                                |
| ---------------------------------------------------------------------------------------- | ------------------------------------------------------------------------ |
| User is `Administrator` or has the `System Manager` role                                 | Administrator overview                                                   |
| User has `HR Manager`, `HR User`, or `Employee Manager` role and is not an administrator | HR workspace                                                             |
| User has a linked Employee record and is neither HR nor administrator                    | Employee workspace                                                       |
| No linked Employee record and no recognized HR role                                      | Non-employee dashboard layout (labeled Administrator Overview by the UI) |

This frontend workspace selection is **not** an authorization boundary.
Configure access through Frappe roles and DocType permissions. Frappe decides
whether the authenticated user can read or write each record; restricted
requests may fail or return no records.

The check-in feature requests browser geolocation and sends the returned
latitude and longitude with the Employee Checkin record. Inform users of this
behavior and configure Employee Checkin permissions appropriately.

The employee salary “Show/Hide” control only hides the amount in the current
interface. It does not replace Frappe permissions or protect salary data from
users who can inspect the browser or access the record through permitted
endpoints.

## Configuration

| Setting                        | Current value                                       | Where it is defined                         |
| ------------------------------ | --------------------------------------------------- | ------------------------------------------- |
| Frappe page route              | `/app/hrms_dashboard`                               | Standard Frappe Page named `hrms_dashboard` |
| Desk bundle                    | `/assets/hrms_dashboard/frontend/index.js`          | `hrms_dashboard/hooks.py`                   |
| Vite development port          | `8080`                                              | `frontend/vite.config.js`                   |
| Development proxy port         | `webserver_port` in `sites/common_site_config.json` | `frontend/vite.config.js`                   |
| Production asset base          | `/assets/hrms_dashboard/frontend/`                  | `frontend/vite.config.js`                   |
| Build output                   | `hrms_dashboard/public/frontend`                    | `frontend/vite.config.js`                   |
| Frontend scripts               | `dev`, `build`, `preview`                           | `frontend/package.json`                     |
| Currency and number formatting | `en-IN`, rupee symbol (₹)                           | `frontend/src/pages/Home.vue`               |
| Default date range             | Today                                               | `frontend/src/pages/Home.vue`               |

The role names, date behavior, display limits, and formatting are currently
defined in the source rather than exposed as site settings.

## Project structure

```text
hrms_dashboard/
├── frontend/
│   ├── src/
│   │   ├── pages/Home.vue       # Dashboard UI, data requests, and interactions
│   │   ├── App.vue              # Vue root component
│   │   ├── main.js              # Desk route detection and Vue mounting
│   │   ├── router.js            # Vue Router configuration
│   │   └── index.css            # Dashboard styles
│   ├── package.json             # Frontend dependencies and scripts
│   ├── package-lock.json        # npm dependency lockfile
│   └── vite.config.js           # Dev proxy and production build settings
├── hrms_dashboard/
│   ├── hooks.py                 # Frappe app hooks, including Desk JS bundle
│   ├── page/hrms_dashboard/     # Standard Frappe Desk Page definition
│   ├── public/frontend/         # Generated frontend assets
│   └── www/                     # Website page controller and template
├── pyproject.toml               # Python package metadata and Ruff settings
└── README.md                    # App-level README
```

## Troubleshooting

| Problem                                            | Checks and actions                                                                                                                                                                                          |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Dashboard does not appear in the Desk              | Confirm the app is installed on the site, run the frontend build and `bench build --app hrms_dashboard`, then hard-refresh the browser. Check the browser console for JavaScript errors.                    |
| Page is blank or keeps showing “Loading dashboard” | Confirm the user is signed in, the Desk runtime loaded, and the browser console/network panel has no failed API or asset requests. Check Frappe Error Log for server errors.                                |
| Employee sees a non-employee workspace             | Confirm the Employee record's `user_id` matches the signed-in user and that the user does not have one of the recognized HR or administrator roles.                                                         |
| Employee dashboard sections are empty              | Confirm HRMS is installed, an Employee is linked, records overlap the selected date range, and the user has permission to read the relevant DocTypes.                                                       |
| HR data is missing                                 | Confirm the user has one of the recognized HR roles and permissions to read Employee Checkin, Attendance, Leave Application, Salary Slip, and any other required DocTypes.                                  |
| Attendance check-in is disabled                    | The selected date range must include today, and an Employee record must be linked to the signed-in user.                                                                                                    |
| Check-in fails with a location message             | Allow location access in the browser, use a browser/device that supports geolocation, and ensure the site is served from a secure context (HTTPS or localhost) and the location can be determined.          |
| Check-in request is rejected                       | Confirm the user can create Employee Checkin records and that Frappe CSRF/session configuration is valid. Review the browser network response and Frappe Error Log.                                         |
| Vite cannot reach the Frappe backend               | Start the bench and verify the `webserver_port` value in `sites/common_site_config.json`.                                                                                                                   |
| Frontend changes are not visible                   | Run `npm run build` in `apps/hrms_dashboard/frontend`, run `bench build --app hrms_dashboard` from the bench directory, then hard-refresh.                                                                  |
| Holiday list is empty                              | Confirm Holiday Lists and assignments exist and that the current date precedes at least one holiday date. The dashboard falls back to available Holiday Lists if assigned lists yield no upcoming holidays. |

## Testing and code quality

The frontend package currently defines `dev`, `build`, and `preview` scripts; it
does not define a frontend test or lint script. A production build can be
checked with:

```bash
cd apps/hrms_dashboard/frontend
npm ci
npm run build
```

The repository's GitHub Actions CI workflow installs the app on a test Frappe
site and invokes `bench --site test_site run-tests --app hrms_dashboard`. The
lint workflow runs the configured pre-commit hooks, Frappe Semgrep rules, and
`pip-audit`.

## Contributing

Install the repository's pre-commit hooks from the app directory:

```bash
cd apps/hrms_dashboard
pre-commit install
```

The configured hooks include Python checks and formatting/linting for the
supported source files. Keep changes focused, run the applicable checks, and
update this README when setup or user-visible behavior changes.

## License

MIT. See [`license.txt`](license.txt).
