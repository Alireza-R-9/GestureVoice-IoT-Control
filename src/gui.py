import streamlit as st
import subprocess
import sys
import os

st.title("GestureVoice IoT Control")

mode = st.radio(
    "Select control mode:",
    ("Gesture Control", "Voice Control")
)

if st.button("Start"):
    st.write(f"Starting {mode}...")

    # فرض کنیم فایل ها:
    # Gesture Control: src/vision_main.py
    # Voice Control: src/voice_main.py

    if mode == "Gesture Control":
        # اجرای فایل vision_main.py به صورت subprocess
        st.write("Launching Gesture Control (vision_main.py)...")
        subprocess.Popen([sys.executable, os.path.join("src", "vision_main.py")])
    else:
        # اجرای فایل voice_main.py
        st.write("Launching Voice Control (voice_main.py)...")
        subprocess.Popen([sys.executable, os.path.join("src", "voice_main.py")])

    st.write("If the new window does not open automatically, please run the selected module manually.")
