from google.oauth2 import service_account


from googleapiclient.discovery import build
import os
# Define constants
SERVICE_ACCOUNT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'service_account.json'))

SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service
