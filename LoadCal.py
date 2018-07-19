from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from firebase import firebase

#Firebase connection
firebase = firebase.FirebaseApplication('https://spalsa-h.firebaseio.com/', None)

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z'
events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                      orderBy='startTime').execute()
events = events_result.get('items', [])
for event in events:
	start = int(event['start'].values()[0].split("T")[1].split("00-")[0].replace(":",""))
	end = int(event['end'].values()[0].split("T")[1].split("00-")[0].replace(":",""))
	firebase.put('/Patients', event['summary'], {'CheckedIn': 0, 'Start24': start, 'End24': end, 
                                      'SchedStart24': start, 'SchedEnd24': end})
