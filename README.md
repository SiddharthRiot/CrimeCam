# 📸 CrimeCam - Smart Surveillance System

CrimeCam is an AI-powered smart surveillance system that automatically detects:

- 👜 **Unattended Bags** (backpacks, handbags, suitcases)
- 🚶‍♂️ **Loitering** (people standing still for too long)
- 📩 Sends real-time **alerts to Telegram** with screenshots

----

## 📦 Features

- ✅ YOLOv8 object detection  
- ✅ Loitering detection using movement tracking  
- ✅ Unattended bag detection based on person distance  
- ✅ Screenshot capture on alert  
- ✅ Telegram message + photo alert system  
- ✅ Clean modular code structure

----

## 📁 Project Structure

CrimeCam/ > main.py > face_recog.py > telegram_alert.py > known_faces/ > yourimages.jpeg, jpg > screenshots/

----

## 📋Install requirements
```bash 
pip install -r requirements.txt
```

----

## 🛠️ Telegram Bot Setup
### Create a bot using @BotFather
```bash
Get your BOT_TOKEN
```
### You can use @userinfobot to get your ID
  ```bash
Get your USER_ID
```
Start a chat with your bot and get your CHAT_ID
(You can use @userinfobot to get your ID)

----

### Add credentials
Edit the file ```alert/telegram_alert.py```:
```bash
BOT_TOKEN = "your-bot-token-here"
CHAT_ID = "your-chat-id-here"
```

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/SiddharthRiot/crimecam.git
cd crimecam
```


