from models import CallRequest, Participant
from emailer import send_availability_email
from datetime import datetime

def schedule_call(data, db):
    call = CallRequest(
        call_type=data['call_type'],
        duration=data['duration'],
        deadline=datetime.fromisoformat(data['deadline'])
    )
    db.session.add(call)
    db.session.commit()

    slots = ["2025-08-03 15:00", "2025-08-03 16:00", "2025-08-03 17:00"]
    for p in data['participants']:
        participant = Participant(
            call_id=call.id,
            name=p['name'],
            email=p['email']
        )
        db.session.add(participant)
        send_availability_email(participant.email, slots, participant.id)
    
    db.session.commit()
    return call
