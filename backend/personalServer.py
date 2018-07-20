import pyrebase
from datetime import datetime
from subprocess import call
call(["python", "loadcal.py"])
def main():
    config = {
      "apiKey": "AIzaSyC7X1Ne05X3p7Y0XWBauRvl4rkwpsUj16U",
      "authDomain": "spalsa-h.firebaseapp.com",
      "databaseURL": "https://spalsa-h.firebaseio.com/",
      "storageBucket": "spalsa-h.appspot.com"
    }
    print("Initializing firebase...")
    firebase = pyrebase.initialize_app(config)
    db = firebase.database();
    my_stream = db.child("Patients").stream(stream_handler)
"""
Cancel meeting if >= 15 minutes late (start24 > schedStart24)
if x < 15 minutes late, change end24 to x + prevEndTime which is schedEnd24
"""
def cancelMeetings():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    for key in orderedDict:
        patientObj = orderedDict[key]
        currTime = int(datetime.now().strftime('%H%M'))
        #print(currTime - patientObj["start24"])
        time_diff = currTime - patientObj["schedStart24"]
        push_diff = patientObj["start24"] - patientObj["schedStart24"]
        print(push_diff)
        if (time_diff >= 15):
            if (db.child("Patients").child(key).get().val()["isCancelled"] == 0):
                print("Cancel meeting")
                db.child("Patients").child(key).update({"isCancelled": 1})
        if push_diff < 15 and push_diff > 0 and patientObj["isDone"] == 0:
            if (db.child("Patients").child(key).get().val()["isCancelled"] == 0):
                print("Pushing meeting")
                prevEndTime = patientObj["schedEnd24"]
                print("Prev end time: " + str(prevEndTime) + " ==> Curr end time: " + str(addDiff(prevEndTime, push_diff)))
                db.child("Patients").child(key).update({"end24": addDiff(prevEndTime, push_diff)})
"""
if end time of previous is greater than start time of next, (end24 > schedStart24)
push next down and repeat
"""
def cascade():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    sortedPatients = []
    for key in orderedDict:
        sortedPatients.append(orderedDict[key])
    sortedPatients.sort(key=lambda patient: patient["schedStart24"])
    for idx in range(1, len(sortedPatients)):
        currentPatient = sortedPatients[idx]
        previousPatient = sortedPatients[idx-1]
        # if previous patient ends after current patient is scheduled to start
        if previousPatient["end24"] > currentPatient["schedStart24"] and currentPatient["isDone"] == 0:
            # then move their scheduled start and end times
            newSchedStart = previousPatient["end24"]
            newSchedEnd = addThirty(previousPatient["end24"])
            for key in orderedDict:
                # if we find the correct current patient
                if orderedDict[key]["eventID"] is currentPatient["eventID"]:
                    print("Prev end24: " + str(currentPatient["end24"]) + " ==> Curr end time: " + str(newSchedEnd))
                    # update it's start and end
                    db.child("Patients").child(key).update({"start24": newSchedStart})
                    db.child("Patients").child(key).update({"end24": newSchedEnd})
                    db.child("Patients").child(key).update({"earliestCome24":newSchedStart})
"""
if (end24 < schedEnd24) checkout before scheduled checkout,
then notify the next appointment that they can come in notifyPatientsToComeInEarl
    add (earliestCheckIn to fields)
if someone doens't show up late enough to have an appointment cancelled,
like 10 minutes late, then push end24 down by 10 minutes
"""
# if cancelled only right now
def notifyPatientsToComeInEarly():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    patientList = []
    for key in orderedDict:
        patientList.append(orderedDict[key])
    patientList.sort(key=lambda patient: patient["schedStart24"])
    for idx in range(1, len(patientList)):
        prev = patientList[idx-1]
        curr = patientList[idx]
        # if someone ends early (endTime24), modify the next patients earliestCome24 to when prevEnds
        if prev["end24"] < prev["schedEnd24"] and curr["earliestCome24"] != prev["end24"]:
            print("ended early")
            # get current patient
            for key in orderedDict:
                if orderedDict[key]["eventID"] is curr["eventID"]:
                    #print("prev: " + str(prev["eventID"]) + " curr:" + str(curr["eventID"]) )
                    db.child("Patients").child(key).update({"earliestCome24": prev["end24"]})
        # else if prev is cancelled, change the curr patient earliest come time to the prev patients scheduled start time
        # and current earliest come time is not previous start
        elif prev["isCancelled"] and curr["earliestCome24"] != prev["schedStart24"]:
            print("Notify come in early because cancelled")
            for key in orderedDict:
                if orderedDict[key]["eventID"] is curr["eventID"]:
                    print(str(prev["eventID"]) + " curr:" + str(curr["eventID"]) )
                    db.child("Patients").child(key).update({"earliestCome24": prev["schedStart24"]})
"""
HELPER FUNCTIONS
"""
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
def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}
    notifyPatientsToComeInEarly()
    cascade()
    cancelMeetings()
    call(["python", "loaddatatocal.py"])
def addDiff(number, diff):
        s = str(number)
        while (len(s)<4):
                s = '0' + s
        b = s[:2]
        e = s[2:4]
        bi = int(b)
        ei = int(e)
        ei = ei + diff
        if ei >= 60:
                ei = ei-60
                bi = bi + 1
                if bi is 24:
                        bi = 0
        bb = str(bi)
        ee = str(ei)
        while(len(bb) < 2):
                bb = '0' + bb
        while(len(ee) < 2):
                ee = '0' + ee
        s = bb + ee
        return int(s)

def addThirty(number):
        s = str(number)
        while (len(s)<4):
                s = '0' + s
        b = s[:2]
        e = s[2:4]
        bi = int(b)
        ei = int(e)
        ei = ei + 30
        if ei >= 60:
                ei = ei-60
                bi = bi + 1
                if bi is 24:
                        bi = 0
        bb = str(bi)
        ee = str(ei)
        while(len(bb) < 2):
                bb = '0' + bb
        while(len(ee) < 2):
                ee = '0' + ee
        s = bb + ee
        return int(s)
main()