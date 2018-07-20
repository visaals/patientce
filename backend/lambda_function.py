import pyrebase
from datetime import datetime

def main():

    config = {
      "apiKey": "AIzaSyC7X1Ne05X3p7Y0XWBauRvl4rkwpsUj16U",
      "authDomain": "spalsa-h.firebaseapp.com",
      "databaseURL": "https://spalsa-h.firebaseio.com/",
      "storageBucket": "spalsa-h.appspot.com"
    }
    print("Init firebase...")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database();
    notifyPatientsToComeInEarly()

    my_stream = db.child("Patients").stream(stream_handler)

    return "Hey John, it's cody. Wanna get dinner and grab a few beers tonight and watch lord of the rings?"

"""
Cancel meeting if 15 minutes late
"""
def cancelMeetings():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    for p in orderedDict:
        patientObj = orderedDict[p]
        currTime = int(datetime.now().strftime('%H%M'))
        #print(currTime - patientObj["start24"])
        time_diff = currTime - patientObj["schedStart24"]
        if (time_diff >= 15):
            if (db.child("Patients").child(p).get().val()["isCancelled"] == 0):
                print("Cancel meeting")
                db.child("Patients").child(p).update({"isCancelled": 1})


def getOrderedDictOfPatientsAndDb():
    config = {
      "apiKey": "AIzaSyC7X1Ne05X3p7Y0XWBauRvl4rkwpsUj16U",
      "authDomain": "spalsa-h.firebaseapp.com",
      "databaseURL": "https://spalsa-h.firebaseio.com/",
      "storageBucket": "spalsa-h.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database();
    return db.child("Patients").get().val(), db


"""
if end24 < schedEnd24, then notify the next appointment that they can come in notifyPatientsToComeInEarl
add (earliestCheckIn to fields)

if someone doens't show up late enough to have an appointment cancelled,
like 10 minutes late, then push the next appointments down

"""
# if cancelled only right now
def notifyPatientsToComeInEarly():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    patientList = []
    for i in orderedDict:
        patientList.append(orderedDict[i])
        #print(orderedDict[i]["schedStart24"])
    patientList.sort(key=lambda patient: patient["schedStart24"])
    for i in range(1, len(patientList)):
        prev = patientList[i-1]
        curr = patientList[i]

        # if someone ends early (endTime24), modify the next patients earliestCome24 to earlier
        if prev["end24"] < prev["schedEnd24"] and curr["earliestCome24"] != prev["end24"]:
            print("ended early")
            for patient in orderedDict:
                # get current patient
                if orderedDict[patient]["eventID"] is curr["eventID"]:
                    print(str(orderedDict[patient]["eventID"]) + " curr:" + str(curr["eventID"]) )
                    db.child("Patients").child(patient).update({"earliestCome24": prev["end24"]})

        # else if prev is cancelled, change the curr patient earliest come time to the prev patients scheduled start time
        # and current earliest come time is not previous start
        elif prev["isCancelled"] and curr["earliestCome24"] != prev["schedStart24"]:
            print("isCancelled")
            for patient in orderedDict:
                if orderedDict[patient]["eventID"] is curr["eventID"]:
                    print(str(orderedDict[patient]["eventID"]) + " curr:" + str(curr["eventID"]) )
                    db.child("Patients").child(patient).update({"earliestCome24": prev["schedStart24"]})

def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

    cancelMeetings()
    notifyPatientsToComeInEarly()

print(main())
