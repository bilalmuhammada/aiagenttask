# Mastro Scheduler

A Flask-based web application to manage and schedule calls with participants using Google Calendar API. The application allows creating call requests, adding participants, fetching their availability, scheduling events automatically, sending email notifications, and updating call statuses.

---

## Features

- Create and manage call requests with customizable call types, duration, and deadlines.
- Add participants associated with each call request with timezone and email info.
- Integrate with Google Calendar API to check participant availability and schedule calls.
- Automatically send email notifications with call details and Google Meet links.
- View, update, and toggle the status of call requests (`pending` or `confirmed`).
- CRUD operations on call agents.
- Responsive interface with Flask and Jinja2 templates.

---

## Technologies Used

- Python 3.x
- Flask - Lightweight web framework
- Flask-SQLAlchemy - ORM for database management
- Google Calendar API - For scheduling and availability checks
- SQLite (default, can be configured)
- SMTP via Gmail - For sending email notifications
- Jinja2 - Template engine for HTML rendering
- Python-dateutil, pytz - For timezone and datetime parsing/handling

---

## Add Schedule AI Agent Call
<img width="654" height="692" alt="Screenshot 2025-08-07 at 13 51 48" src="https://github.com/user-attachments/assets/42b8d86c-7412-4fbe-bf8b-7d96379be85d" />

# Code of Add Schedule AI Agent Call
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 13 56 30" src="https://github.com/user-attachments/assets/8c07775b-a213-483e-a10e-c238b3230342" />

<img width="1470" height="891" alt="Screenshot 2025-08-07 at 13 58 36" src="https://github.com/user-attachments/assets/0c29a701-8481-4192-abf2-248a0e81d401" />

## Create Event on google Calender
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 14 01 57" src="https://github.com/user-attachments/assets/e6ea6739-f20e-4774-a41b-5a4b6ed3e5d6" />
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 14 02 32" src="https://github.com/user-attachments/assets/f5c8830a-9695-4406-a4b3-54e6b04d6889" />
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 14 13 36" src="https://github.com/user-attachments/assets/b511735e-f0f8-43d2-9649-d16dd7650222" />

# email send to User
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 17 48 31" src="https://github.com/user-attachments/assets/050c0995-e627-4f8e-bede-6b4d7694dedd" />

<img width="1470" height="891" alt="Screenshot 2025-08-07 at 17 49 20" src="https://github.com/user-attachments/assets/e31df4ba-08d1-4a75-878f-5d7f0ccc3c0c" />

# database and table
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 17 52 03" src="https://github.com/user-attachments/assets/c011db02-dc23-40aa-86db-de6c056b8b1d" />

<img width="1470" height="891" alt="Screenshot 2025-08-07 at 17 51 04" src="https://github.com/user-attachments/assets/01e4c985-e485-478f-a55f-124e9e31021d" />
<img width="1470" height="891" alt="Screenshot 2025-08-07 at 17 51 34" src="https://github.com/user-attachments/assets/70644889-56e0-466c-b1e6-4b82216b098c" />










## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/aiagenttask.git
   
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate
   cd aiagenttask
   pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib


   run
   python3 app.py

   
