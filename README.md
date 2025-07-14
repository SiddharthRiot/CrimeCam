# 📸 CrimeCam - Smart Surveillance System

CrimeCam is an AI-powered smart surveillance system that automatically detects:

- 👜 **Unattended Bags** (backpacks, handbags, suitcases)
- 🚶‍♂️ **Loitering** (people standing still for too long)
- 📩 Sends real-time **alerts to Telegram** with screenshots

---

## 📦 Features

- ✅ YOLOv8 object detection  
- ✅ Loitering detection using movement tracking  
- ✅ Unattended bag detection based on person distance  
- ✅ Screenshot capture on alert  
- ✅ Telegram message + photo alert system  
- ✅ Clean modular code structure

---

## 📁 Project Structure

Crime Cam/
│
├── main.py
├── face_recog.py
├── telegram_alert.py
├── requirements.txt
├── README.md
|
├── known_faces/
| └── yourimg.jpeg, jpg
│
└── screenshots/


---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/SiddharthRiot/crimecam.git
cd crimecam

