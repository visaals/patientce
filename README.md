

## patientce
patientce aims to streamline the hospital waiting room process.  patientce displays live updates to patients concerning his or her appointments status regarding if the hospital is running late or perhaps the patient can get in early.

![enter image description here](https://user-images.githubusercontent.com/23038185/42981027-c000b830-8b9f-11e8-9036-abec20cfc717.png =250x)
Appointment is on time.
![enter image description here](https://user-images.githubusercontent.com/23038185/42981025-bfe0e082-8b9f-11e8-9468-fe334d42253d.png =250x)
Appointment is delayed.
![enter image description here](https://user-images.githubusercontent.com/23038185/42981026-bff0874e-8b9f-11e8-83fe-5f9b5fbaad4f.png =250x)
Appointment is available ahead of time.
![enter image description here](https://user-images.githubusercontent.com/23038185/42981024-bfd0ab36-8b9f-11e8-8e92-6d8cf61221d9.png =250x)
Appointment is cancelled because the patient was too late.

Appointments are pulled of a Google Calendar into a Firebase Database. The Android application retrieves a specific user and then sees that user's appointment details. The check in and check out is done manually by the patient for this build, but in an actual implementation it would be done by the doctor and/or the front desk. As the patient is checked in and checked out a Python application updates all appointments based on if the hospital is running ahead or behind schedule. The Python application also updates the Google Calendar, so the doctor can see the updated schedule.

Contributions:
[Visaal Ambalam](https://github.com/visaals/): Business logic and Firebase Integration
[Cameron Jump](https://github.com/cameronjump/): Android Application and Firebase Integration
[John Bisignano](https://github.com/johnbisognano): Database and Google Calendar Doctor View
[Connor Beganksy](https://github.com/ConnorBegansky): Design and UI decisions 


