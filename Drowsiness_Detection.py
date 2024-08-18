from flask import Flask, render_template, Response
import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance
import pygame
import time

app = Flask(__name__)

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False, max_num_faces=1, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

thresh = 0.25
start_time = None

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear

def play_alert_sound():
    pygame.mixer.init()
    pygame.mixer.music.load('buzzer.mp3')
    pygame.mixer.music.play()

def detect_drowsiness(frame):
    global start_time

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb_frame)

    if result.multi_face_landmarks:
        for face_landmarks in result.multi_face_landmarks:
            left_eye = [
                (int(face_landmarks.landmark[33].x * frame.shape[1]), int(face_landmarks.landmark[33].y * frame.shape[0])),
                (int(face_landmarks.landmark[160].x * frame.shape[1]), int(face_landmarks.landmark[160].y * frame.shape[0])),
                (int(face_landmarks.landmark[158].x * frame.shape[1]), int(face_landmarks.landmark[158].y * frame.shape[0])),
                (int(face_landmarks.landmark[133].x * frame.shape[1]), int(face_landmarks.landmark[133].y * frame.shape[0])),
                (int(face_landmarks.landmark[153].x * frame.shape[1]), int(face_landmarks.landmark[153].y * frame.shape[0])),
                (int(face_landmarks.landmark[144].x * frame.shape[1]), int(face_landmarks.landmark[144].y * frame.shape[0]))
            ]
            right_eye = [
                (int(face_landmarks.landmark[362].x * frame.shape[1]), int(face_landmarks.landmark[362].y * frame.shape[0])),
                (int(face_landmarks.landmark[385].x * frame.shape[1]), int(face_landmarks.landmark[385].y * frame.shape[0])),
                (int(face_landmarks.landmark[387].x * frame.shape[1]), int(face_landmarks.landmark[387].y * frame.shape[0])),
                (int(face_landmarks.landmark[263].x * frame.shape[1]), int(face_landmarks.landmark[263].y * frame.shape[0])),
                (int(face_landmarks.landmark[373].x * frame.shape[1]), int(face_landmarks.landmark[373].y * frame.shape[0])),
                (int(face_landmarks.landmark[380].x * frame.shape[1]), int(face_landmarks.landmark[380].y * frame.shape[0]))
            ]

            # Draw the left eye
            cv2.polylines(frame, [np.array(left_eye, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)

            # Draw the right eye
            cv2.polylines(frame, [np.array(right_eye, dtype=np.int32)], isClosed=True, color=(0, 0, 255), thickness=2)

            leftEAR = eye_aspect_ratio(left_eye)
            rightEAR = eye_aspect_ratio(right_eye)
            ear = (leftEAR + rightEAR) / 2.0

            if ear < thresh:
                if start_time is None:
                    start_time = time.time()
                elif (time.time() - start_time) >= 3:  # Check if eyes have been closed for 3 seconds
                    play_alert_sound()
                    cv2.putText(frame, "ALERT you're sleeping!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            else:
                start_time = None  # Reset the start time if eyes open

    return frame

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, (640, 480))
        frame = detect_drowsiness(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)
