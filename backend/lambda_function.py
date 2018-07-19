import pyrebase

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
    my_stream = db.child("Patients").stream(stream_handler)

    return "Hey John, it's cody. Wanna get dinner and grab a few beers tonight and watch lord of the rings?"


def cancelMeetings():
    orderedDict, db = getOrderedDictOfPatientsAndDb();
    for p in orderedDict:
        patientObj = orderedDict[p]
        print(abs(patientObj["schedStart24"] - patientObj["start24"]))
        if (patientObj["start24"] - patientObj["schedStart24"] >= 15):
            print("cancel meeting")
            if (db.child("Patients").child(p).get().val()["isCancelled"] == 0):
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

def notifyPatientsToComeInEarly():
    return 0



def stream_handler(message):
    print(message["event"]) # put
    print(message["path"]) # /-K7yGTTEp7O549EzTYtI
    print(message["data"]) # {'title': 'Pyrebase', "body": "etc..."}

    cancelMeetings()





print(main())
