# import cv2
# import face_recognition
# import pickle
# import firebase_admin
# from firebase_admin import credentials, db, storage
# from datetime import datetime

# # Initialize Firebase
# cred = credentials.Certificate("D:/vscode/Face_Recognition_System/serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "https://facial-attendance-system-94fe0-default-rtdb.firebaseio.com/",
#     'storageBucket': "facial-attendance-system-94fe0.appspot.com"
# })

# # Load encoded data
# with open('EncodeFile.p', 'rb') as file:
#     encodeListKnownWithIds = pickle.load(file)

# encodeListKnown, studentIds = encodeListKnownWithIds

# # Initialize Firebase storage bucket
# bucket = storage.bucket()

# # Initialize webcam
# cap = cv2.VideoCapture(0)
# cap.set(3, 640)
# cap.set(4, 480)

# while True:
#     success, img = cap.read()

#     # Resize and convert to RGB for face recognition
#     imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
#     imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

#     # Face recognition on current framea
#     faceCurFrame = face_recognition.face_locations(imgS)
#     encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

#     for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
#         matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
#         faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

#         matchIndex = min(range(len(faceDis)), key=faceDis.__getitem__)

#         if matches[matchIndex]:
#             id = studentIds[matchIndex]

#             # Retrieve student information from Firebase
#             student_ref = db.reference(f'Students/{id}')
#             student_info = student_ref.get()

#             # Check if student_info is not None before accessing attributes
#             if student_info is not None:
#                 # Update attendance if needed
#                 last_attendance_time = datetime.strptime(student_info.get('last_attendance_time', "1970-01-01 00:00:00"),
#                                                         "%Y-%m-%d %H:%M:%S")
#                 seconds_elapsed = (datetime.now() - last_attendance_time).total_seconds()

#                 if seconds_elapsed > 30:
#                     new_total_attendance = student_info.get('total_attendance', 0) + 1
#                     student_ref.update({
#                         'total_attendance': new_total_attendance,
#                         'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#                     })

#                     # Print the updated attendance for verification
#                     print(f"Updated Total Attendance for {id}: {new_total_attendance}")

#                 # Display all information in the terminal
#                 print("Student Information:")
#                 print(f"Student ID: {id}")
#                 print(f"Name: {student_info.get('name', 'N/A')}")
#                 print(f"Major: {student_info.get('major', 'N/A')}")
#                 print(f"Year: {student_info.get('year', 'N/A')}")
#                 print(f"Standing: {student_info.get('standing', 'N/A')}")
#                 print(f"Total Attendance: {student_info.get('total_attendance', 'N/A')}")
#                 print(f"Last Attendance Time: {student_info.get('last_attendance_time', 'N/A')}")
#                 print("-----------------------------")

#     # Display the image
#     cv2.imshow("Face Recognition System", img)
#     cv2.waitKey(2)
# cv2.destroyAllWindows()


import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

# Initialize Firebase
cred = credentials.Certificate("D:/vscode/Face_Recognition_System/serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://facial-attendance-system-94fe0-default-rtdb.firebaseio.com/",
    'storageBucket': "facial-attendance-system-94fe0.appspot.com"
})

# Load encoded data
with open('EncodeFile.p', 'rb') as file:
    encodeListKnownWithIds = pickle.load(file)

encodeListKnown, studentIds = encodeListKnownWithIds

# Initialize Firebase storage bucket
bucket = storage.bucket()

# Initialize webcam
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Capture a single frame
success, img = cap.read()

# Resize and convert to RGB for face recognition
imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

# Face recognition on the captured frame
faceCurFrame = face_recognition.face_locations(imgS)
encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
    matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
    faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

    matchIndex = min(range(len(faceDis)), key=faceDis.__getitem__)

    if matches[matchIndex]:
        id = studentIds[matchIndex]

        # Retrieve student information from Firebase
        student_ref = db.reference(f'Students/{id}')
        student_info = student_ref.get()

        # Check if student_info is not None before accessing attributes
        if student_info is not None:
            # Update attendance if needed
            last_attendance_time = datetime.strptime(student_info.get('last_attendance_time', "1970-01-01 00:00:00"),
                                                    "%Y-%m-%d %H:%M:%S")
            seconds_elapsed = (datetime.now() - last_attendance_time).total_seconds()

            if seconds_elapsed > 30:
                new_total_attendance = student_info.get('total_attendance', 0) + 1
                student_ref.update({
                    'total_attendance': new_total_attendance,
                    'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                # Print the updated attendance for verification
                
            # Display all information in the terminal
            print("Student Information:")
            print(f"Student ID: {id}")
            print(f"Name: {student_info.get('name', 'N/A')}")
            print(f"Major: {student_info.get('major', 'N/A')}")
            print(f"Year: {student_info.get('year', 'N/A')}")
            print(f"Standing: {student_info.get('standing', 'N/A')}")
            print(f"Updated Total Attendance: {new_total_attendance}")
            print(f"Last Attendance Time: {student_info.get('last_attendance_time', 'N/A')}")
            print("-----------------------------")

# Display the image
cv2.imshow("Face Recognition System", img)
cv2.waitKey(0)
cap.release()
