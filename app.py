from flask import Flask, render_template, Response, jsonify
import cv2
import face_recognition
import pickle
import firebase_admin
from firebase_admin import credentials, db, storage
from datetime import datetime

app = Flask(__name__)

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

def generate_frames():
    while True:
        success, img = cap.read()

        # Resize and convert to RGB for face recognition
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        # Face recognition on current frame
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

                if student_info is not None:
                    last_attendance_time = datetime.strptime(
                        student_info.get('last_attendance_time', "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")
                    seconds_elapsed = (datetime.now() - last_attendance_time).total_seconds()

                    if seconds_elapsed > 30:
                        new_total_attendance = student_info.get('total_attendance', 0) + 1
                        student_ref.update({
                            'total_attendance': new_total_attendance,
                            'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        })

                        # Print the updated attendance for verification
                        print(f"Updated Total Attendance for {id}: {new_total_attendance}")

                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + cv2.imencode('.jpg', img)[1].tobytes() + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/get_student_info')
def get_student_info():
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    matches = []
    matchIndex = 0
    new_total_attendance = 0  # Default value
    id = 'N/A'  # Default value
    new_total_attendance = 0  # Default value

    for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = min(range(len(faceDis)), key=faceDis.__getitem__)

    if matches and matches[matchIndex]:
        id = studentIds[matchIndex]

        student_ref = db.reference(f'Students/{id}')
        student_info = student_ref.get()

        if student_info is not None:
            last_attendance_time = datetime.strptime(
                student_info.get('last_attendance_time', "1970-01-01 00:00:00"), "%Y-%m-%d %H:%M:%S")
            seconds_elapsed = (datetime.now() - last_attendance_time).total_seconds()

            if seconds_elapsed > 30:
                new_total_attendance = student_info.get('total_attendance', 0) + 1
                student_ref.update({
                    'total_attendance': new_total_attendance,
                    'last_attendance_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                })

                print(f"Updated Total Attendance for {id}: {new_total_attendance}")
                a={new_total_attendance}

    student_info_html = f"""
        <p>Student ID: {id}</p>
        <p>Name: {student_info.get('name', 'N/A') if student_info else 'N/A'}</p>
        <p>Major: {student_info.get('major', 'N/A') if student_info else 'N/A'}</p>
        <p>Year: {student_info.get('year', 'N/A') if student_info else 'N/A'}</p>
        <p>Standing: {student_info.get('standing', 'N/A') if student_info else 'N/A'}</p>
        <p>Updated Total Attendance:  {student_info.get('total_attendance', 'N/A') if student_info else 'N/A'}</p>
        <p>Last Attendance Time: {student_info.get('last_attendance_time', 'N/A') if student_info else 'N/A'}</p>
        <hr>
    """

    return jsonify({'studentInfo': student_info_html})

    return jsonify({'studentInfo': ''})

if __name__ == '__main__':
    app.run(debug=True)
