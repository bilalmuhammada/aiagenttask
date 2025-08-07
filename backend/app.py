from flask import Flask, render_template, jsonify, request, redirect, url_for, flash ,abort
from flask_sqlalchemy import SQLAlchemy
from config import Config
from datetime import datetime, timedelta
from dateutil.parser import parse
from google_calendar_service import get_calendar_service
import pytz
import uuid

from sqlalchemy import text
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "flash message"
app.config.from_object(Config)
db = SQLAlchemy(app)


class CallAgent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    username = db.Column(db.String(20))


class CallRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_type = db.Column(db.String(50))
    duration = db.Column(db.Integer)  # in minutes
    deadline = db.Column(db.DateTime)
    status = db.Column(db.String(50), default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    call_id = db.Column(db.Integer, db.ForeignKey('call_request.id'))
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    timezone = db.Column(db.String(50))


with app.app_context():
    db.create_all()


def schedule_event_with_availability(summary="summary", email="bilalahmada774@gmial.com", deadline=None, duration_minutes=30, timezone="Europe/Rome"):
    service = get_calendar_service()
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)

    if isinstance(deadline, datetime):
        pass
    elif isinstance(deadline, str):
        deadline = parse(deadline)
    elif isinstance(deadline, int):
        deadline = datetime.fromtimestamp(deadline)
    else:
        raise TypeError(f"Unsupported deadline type: {type(deadline)}")

    if deadline.tzinfo is None:
        deadline = tz.localize(deadline)
    else:
        deadline = deadline.astimezone(tz)

    body = {
        "timeMin": now.isoformat(),
        "timeMax": deadline.isoformat(),
        "timeZone": timezone,
        "items": [{"id": email}]
    }

    events_result = service.freebusy().query(body=body).execute()
    busy = events_result['calendars'][email]['busy']

    slot_start = now
    slot_end = deadline
    duration = timedelta(minutes=duration_minutes)

    while slot_start + duration <= slot_end:
        potential_end = slot_start + duration

        conflict = any(
            (slot_start < datetime.fromisoformat(b['end']) and potential_end > datetime.fromisoformat(b['start']))
            for b in busy
        )

        if not conflict:
            event = {
                'summary': summary,
                'start': {
                    'dateTime': slot_start.isoformat(),
                    'timeZone': timezone,
                },
                'end': {
                    'dateTime': potential_end.isoformat(),
                    'timeZone': timezone,
                },
                #'attendees': [{'email': email}],
                
            }

            created_event = service.events().insert(
                calendarId='primary',
                body=event,
                conferenceDataVersion=1,
               # sendUpdates='all'
            ).execute()

            return {
                "status": "success",
                "start": slot_start.isoformat(),
                "end": potential_end.isoformat(),
                "meet_link": created_event.get('hangoutLink'),
                "calendar_link": created_event.get('htmlLink')
            }

        slot_start += timedelta(minutes=15)

    return {"status": "no_available_slots"}


@app.route('/list_events')
def list_events():
    service = get_calendar_service()
    events_result = service.events().list(calendarId='primary', maxResults=10).execute()
    events = events_result.get('items', [])
    return jsonify(events)
def trigger_availability_fetch(call_id):
    call = CallRequest.query.get(call_id)
    participants = Participant.query.filter_by(call_id=call_id).all()

    for p in participants:
        if p.email:
            slots = schedule_event_with_availability(
                summary=f"{call.call_type} Call",
                email=p.email,
                deadline=call.deadline,
                duration_minutes=call.duration,
                timezone=p.timezone
            )
            print(f"{p.email} has slots: {slots}")

            if slots.get("status") == "success":

                start_time = slots.get("start")
                end_time = slots.get("end")
                meet_link = slots.get("meet_link") or "Meet link not generated"
                calendar_link = slots.get("calendar_link")

                # Build email content
                subject = f"{call.call_type} Scheduled"
                body = f"""
                <p>Dear {p.name},</p>
                <p>Your {call.call_type.lower()} call has been scheduled.</p>
                <p><strong>Start:</strong> {start_time}<br>
                <strong>End:</strong> {end_time}<br>
                <strong>Google Meet:</strong> <a href="{meet_link}">{meet_link}</a><br>
                <strong>View in Calendar:</strong> <a href="{calendar_link}">Open Calendar</a></p>
                <p>Best regards,<br>Mastro Scheduler</p>
                """

                # Send the email
                send_email(p.email, subject, body)

                return "Done"
        else:
            return "Email sent."


@app.route("/")
def Index():
    # Raw SQL query as a string
    sql = text("""
        SELECT
            cr.id AS id,
            p.name,
            cr.call_type,
            cr.deadline,
            cr.duration,
            p.id AS participant_id,
            p.email,
            cr.status,
            p.timezone
        FROM
            call_request cr
        JOIN
            participant p ON cr.id = p.id
    """)

    # Execute the query
    result = db.session.execute(sql)

   

    return render_template("index.html", entries=result)


@app.route("/status/<int:id>", methods=['POST'])
def status(id):

   
    # Get status from form data
    new_status = request.form.get('status')

    # Validate status value
    if new_status not in ['confirmed', 'pending']:
        return abort(400, description="Invalid status. Must be 'confirm' or 'pending'.")

    # Update call_request status in DB
    update_sql = text("UPDATE call_request SET status = :status WHERE id = :id")
    db.session.execute(update_sql, {'status': new_status, 'id': id})
    db.session.commit()
    # Raw SQL query as a string
    sql = text("""
        SELECT
            cr.id AS id,
            p.name,
            cr.call_type,
            cr.deadline,
            cr.duration,
            cr.status,
            p.id AS participant_id,
            p.email,
            p.timezone
        FROM
            call_request cr
        JOIN
            participant p ON cr.id = p.id
    """)

    # Execute the query
    result = db.session.execute(sql)

   

    return render_template("index.html", entries=result)


@app.route("/insert", methods=["POST"])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully")
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]
        username = request.form["username"]

        new_entry = CallAgent(name=name, email=email, phone=phone, username=username)
        db.session.add(new_entry)
        db.session.commit()

        return redirect(url_for("Index"))



@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    entry = CallAgent.query.get_or_404(id)
    if request.method == 'POST':
        entry.name = request.form['name']
        entry.email = request.form['email']
        entry.phone = request.form['phone']
        db.session.commit()
        flash("Update Inserted Successfully")
        return redirect(url_for('Index'))
    return render_template('index.html', entry=entry)







@app.route('/delete/<int:id>')
def delete(id):
    entry = CallAgent.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    flash("Deleted successfully!", "success")
    return redirect(url_for('Index'))


@app.route('/schedule', methods=['POST'])
def schedule_call():
    data = request.form
    call = CallRequest(
        call_type=data['call_type'],
        duration=int(data['preferred_duration']),
        deadline=parse(data['deadline'])
    )
    db.session.add(call)
    db.session.commit()

    name = data['name']
    email = data['email']
    tz = data['timezone']
    participant = Participant(call_id=call.id, name=name, email=email, timezone=tz)
    db.session.add(participant)
    db.session.commit()

    trigger_availability_fetch(call.id)

    flash("Call request submitted. Gathering availability...", "info")
    return redirect(url_for('Index'))





def send_email(to_email, subject, body):
    sender_email = "bilalahmada774@gmail.com"
    sender_password = "clrx eyro zpth yjsi"  # use app password if 2FA is on

    msg = MIMEText(body, "html")
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
            print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")

if __name__ == "__main__":
    app.run(debug=True)
