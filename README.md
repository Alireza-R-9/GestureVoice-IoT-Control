# 🎶 GestureVoice IoT Control

**Author:** Alireza Rostami | **Supervisor:** Dr. Mahdi Sifipour  
**University:** Hamedan University of Technology  

---

## 🚀 Project Overview

**GestureVoice IoT Control** is a multi-modal music control system that allows users to manage music playback using:

- **Hand gestures** via camera recognition  
- **Voice commands** via microphone  
- **Manual controls** via a Streamlit dashboard  

It also supports **ESP32 integration**, sending commands over Wi-Fi to control IoT hardware.  
Developed as a **Bachelor's thesis** for embedded systems and IoT applications.

---

## 🎯 Key Features

- Real-time **gesture recognition** for Play, Pause, Next, Previous, Volume control  
- **Voice command execution** for hands-free operation  
- **Streamlit dashboard** for manual control and folder management  
- **ESP32 IoT communication** over Wi-Fi  
- **Multi-modal operation**: gesture, voice, and manual inputs work independently or simultaneously  

---

## ⚡ Quick Start

1. Clone the repository:

```bash
git clone https://github.com/YourUsername/GestureVoice-IoT-Control.git
cd GestureVoice-IoT-Control
````

2. Setup virtual environment and install dependencies:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. Launch the app:

```bash
streamlit run src/streamlit_app.py
```

4. Select control mode (Gesture / Voice) and start interacting!

---

## 💡 Notes

* Ensure **camera and microphone** are enabled
* Test ESP32 connection with `server_test.py`
* Optimized for **embedded processor IoT applications**
* Developed for **educational and academic purposes**

---

## ✨ Author

**Alireza Rostami**
**Supervisor:** Dr. Mahdi Sifipour
**Hamedan University of Technology**
