import face_recognition
import cv2
import os
from telegram_alert import send_telegram_message, send_telegram_photo
import time

known_encodings = []
known_names = []

for file in os.listdir("known_faces"):
    if file.endswith(".jpg") or file.endswith(".png"):
        path = f"known_faces/{file}"
        image = face_recognition.load_image_file(path)
        encoding = face_recognition.face_encodings(image)[0]
        known_encodings.append(encoding)
        known_names.append(os.path.splitext(file)[0])

# Start webcam
cap = cv2.VideoCapture(0)
detected_unknown = False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb)
    face_encodings = face_recognition.face_encodings(rgb, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_names[first_match_index]

        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

        # Alert for unknown
        if name == "Unknown" and not detected_unknown:
            filename = f"screenshots/unknown_{int(time.time())}.jpg"
            cv2.imwrite(filename, frame)
            send_telegram_message("🚨 CrimeCam Alert: Unknown person detected!")
            send_telegram_photo(filename, "📸 Unknown Face Screenshot")
            detected_unknown = True
            print("✅ Alert sent for unknown face")

    cv2.imshow("🧠 Face Recognition - CrimeCam", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
