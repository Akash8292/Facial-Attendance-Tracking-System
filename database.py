import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("D:/vscode/python/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facial-attendance-system-94fe0-default-rtdb.firebaseio.com/"
})



ref = db.reference('Students')

data = {
         "1":
        {
            "name": "Jayesh jroli",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "2":
        {
            "name": "Ashutosh Dhumal",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "3":
        {
            "name": "Akash kumar Saw",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "4":
        {
            "name": "Ashif",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
           "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "5":
        {
            "name": "Govind Garg",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
           "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "6":
        {
            "name": "Rohit shirsat",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
          "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "7":
        {
            "name": "Omakar mohanty",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "B",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        },
         "8":
        {
            "name": "Uttam kumar",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        }, 
        "9":
        {
            "name": "Rohith M",
            "major": "CSE",
            "starting_year": 2021,
            "total_attendance": 1,
            "standing": "G",
            "year": 3,
            "last_attendance_time": "2023-12-11 00:54:34"
        }
    
}

for key, value in data.items():
    ref.child(key).set(value)


