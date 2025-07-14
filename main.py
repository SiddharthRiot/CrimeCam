import cv2
from ultralytics import YOLO
import time
import os
from telegram_alert import send_telegram_message, send_telegram_photo

model = YOLO("yolov8m.pt")
cap = cv2.VideoCapture(0)

BAG_CLASSES = [24, 26, 28]
UNATTENDED_THRESHOLD = 15
LOITER_THRESHOLD = 15
DIST_THRESHOLD = 200

unattended_bags = {}
loitering_people = {}

os.makedirs("screenshots", exist_ok=True)

def center(box):
    x1, y1, x2, y2 = box
    return ((x1 + x2) / 2, (y1 + y2) / 2)

def is_bag_near_any_person(bag_c, person_centers):
    for pc in person_centers:
        dist = ((bag_c[0] - pc[0])**2 + (bag_c[1] - pc[1])**2)**0.5
        if dist < DIST_THRESHOLD:
            return True
    return False

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    annotated_frame = results[0].plot()

    boxes = results[0].boxes.xyxy.cpu().numpy()
    classes = results[0].boxes.cls.cpu().numpy()

    person_centers = []
    bag_centers = []

    current_time = time.time()

    for box, cls in zip(boxes, classes):
        cls = int(cls)
        name = model.names[cls]
        c = center(box)
        print(f"🧠 Detected: {name}")

        if cls == 0:
            person_centers.append(c)
        elif cls in BAG_CLASSES:
            rounded_c = (round(c[0], -1), round(c[1], -1))
            bag_centers.append(rounded_c)

    # unattended bag detection
    for bag_c in bag_centers:
        near_person = is_bag_near_any_person(bag_c, person_centers)
        print(f"👜 Bag center: {bag_c}, Near person: {near_person}")

        if not near_person:
            if bag_c not in unattended_bags:
                unattended_bags[bag_c] = current_time
                print(f"⏳ Started bag timer: {bag_c}")
            else:
                elapsed = current_time - unattended_bags[bag_c]
                print(f"⏱ Unattended bag time: {elapsed:.2f} sec")

                if elapsed > UNATTENDED_THRESHOLD:
                    cv2.putText(annotated_frame, "Unattended Bag!", (int(bag_c[0]), int(bag_c[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    filename = f"screenshots/bag_alert_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)

                    send_telegram_message("🚨 CrimeCam Alert: Unattended bag detected!")
                    send_telegram_photo(filename, "📸 Bag Screenshot")
                    print(f"✅ Telegram: Bag alert + photo sent! Saved as {filename}")
                    unattended_bags[bag_c] = current_time + 999
        else:
            if bag_c in unattended_bags:
                del unattended_bags[bag_c]

    # loitering detection
    for person_c in person_centers:
        found = False
        for saved_c in list(loitering_people):
            dist = ((person_c[0] - saved_c[0])**2 + (person_c[1] - saved_c[1])**2)**0.5
            if dist < 50:
                elapsed = current_time - loitering_people[saved_c]
                print(f"🧍‍♂️ Loitering at {saved_c} for {elapsed:.2f} sec")

                if elapsed > LOITER_THRESHOLD:
                    cv2.putText(annotated_frame, "Loitering!", (int(saved_c[0]), int(saved_c[1])),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
                    filename = f"screenshots/loitering_{int(time.time())}.jpg"
                    cv2.imwrite(filename, frame)

                    send_telegram_message("🚨 CrimeCam Alert: Loitering detected!")
                    send_telegram_photo(filename, "📸 Loitering Screenshot")
                    print(f"✅ Telegram: Loitering alert + photo sent! Saved as {filename}")
                    loitering_people[saved_c] = current_time + 999
                found = True
                break
        if not found:
            loitering_people[person_c] = current_time
            print(f"⏳ Started loitering timer: {person_c}")

    cv2.imshow("🎥 CrimeCam v3 - Smart Surveillance", annotated_frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
