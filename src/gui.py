import streamlit as st
import cv2
from gesture_module.hand_detector import HandDetector
from gesture_module.gesture_controller import GestureController
from music_module.music_controller import MusicController
import threading
import time

def run_camera(gesture_ctrl, detector, music_ctrl, stop_event):
    cap = cv2.VideoCapture(0)
    stframe = st.empty()

    freq_perc = 50
    speed_perc = 50
    vol_perc = 70
    current_voice = "original"

    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            st.warning("No camera feed!")
            break

        img = detector.find_hands(frame)
        allHands = detector.get_landmarks(img)

        # (در اینجا کد پردازش ژست‌ها و کنترل موزیک رو قرار بدید)

        stframe.image(img, channels="BGR")
        time.sleep(0.03)  # فریم ریت تقریباً 30fps

    cap.release()


def main():
    st.title("GestureVoice IoT Control - GUI")

    music_ctrl = MusicController("music/")
    detector = HandDetector()
    gesture_ctrl = GestureController()

    mode = st.radio("Select Control Mode:", ("Gesture", "Voice (future)", "Off"))

    if mode == "Gesture":
        st.info("Running Gesture Control Mode")

        stop_event = threading.Event()
        cam_thread = threading.Thread(target=run_camera, args=(gesture_ctrl, detector, music_ctrl, stop_event))
        cam_thread.start()

        if st.button("Stop Gesture Control"):
            stop_event.set()
            cam_thread.join()
            st.success("Gesture Control Stopped")

    elif mode == "Voice (future)":
        st.warning("Voice Control mode not implemented yet.")

    else:
        st.write("Control is off.")

if __name__ == "__main__":
    main()
