from __future__ import print_function
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import datetime
from firebase import firebase
import time




#Firebase connection
firebase = firebase.FirebaseApplication('https://spalsa-h.firebaseio.com/', None)

# Setup the Calendar API
SCOPES = 'https://www.googleapis.com/auth/calendar'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
    creds = tools.run_flow(flow, store)
service = build('calendar', 'v3', http=creds.authorize(Http()))


patients = firebase.get('/Patients', None)

for key in patients:
	stime = str(patients[key]['start24'])
	etime = str(patients[key]['end24'])
	while len(stime) < 4:
		stime = '0' + stime
	while len(etime) < 4:
		etime = '0' + etime
	start = '2018-07-20T' + stime[:2] + ':' + stime[2:] + ':00-05:00'
	end = '2018-07-20T' + etime[:2] + ':' + etime[2:] + ':00-05:00'
	print('----------')
	print(key)
	print(start)
	print(end)

	if patients[key]['isCancelled'] == 1:
		event = {
		  'summary': key,
		  'colorId': '11',
		  'start': {
		    'dateTime': start
		  },
		  'end': {
		    'dateTime': end
		  }
	  	}
	  	service.events().update(calendarId='primary', eventId=patients[key]['eventID'], body=event).execute()
  	else:
		event = {
		  'summary': key,
		  'start': {
		    'dateTime': start
		  },
		  'end': {
		    'dateTime': end
		  }
	  	}
  		service.events().update(calendarId='primary', eventId=patients[key]['eventID'],  body=event).execute()