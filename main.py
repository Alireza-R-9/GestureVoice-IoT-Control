import cv2
import numpy as np
import time
from hand_detector import HandDetector
from gesture_controller import GestureController
from music_controller import MusicController


def draw_progress_bar_vertical(img, perc, x=50, y=150, w=40, h=300, color=(0, 255, 0)):
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
    fill = int((perc / 100) * h)
    cv2.rectangle(img, (x, y + h - fill), (x + w, y + h), color, cv2.FILLED)
    cv2.putText(img, f'{int(perc)}%', (x - 10, y + h + 45),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 3)


def draw_progress_bar_horizontal(img, perc, y=50, h=30, color=(255, 100, 255)):
    w = 300
    x = (img.shape[1] - w) // 2
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
    fill = int((perc / 100) * w)
    cv2.rectangle(img, (x, y), (x + fill, y + h), color, cv2.FILLED)
    cv2.putText(img, f'{int(perc)}%', (x + w + 10, y + h - 5),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
    cv2.putText(img, 'Volume', (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)


def freq_label(perc):
    freq_hz = np.interp(perc, [0, 100], [100, 5000])
    if freq_hz < 300:
        return "verylow"
    elif freq_hz < 800:
        return "low"
    elif freq_hz < 2000:
        return "normal"
    elif freq_hz < 3500:
        return "high"
    else:
        return "veryhigh"


def speed_label(perc):
    speed = np.interp(perc, [0, 100], [0.5, 2.0])
    if speed < 0.7:
        return f"Very Slow ({speed:.2f}x)"
    elif speed < 0.9:
        return f"Slow ({speed:.2f}x)"
    elif speed < 1.2:
        return f"Medium ({speed:.2f}x)"
    elif speed < 1.5:
        return f"Fast ({speed:.2f}x)"
    else:
        return f"Very Fast ({speed:.2f}x)"


def main():
    cap = cv2.VideoCapture(0)
    detector = HandDetector(maxHands=2)
    gesture_ctrl = GestureController()
    music_ctrl = MusicController("music/")

    freq_perc = 50
    speed_perc = 50
    vol_perc = 70
    last_freq_perc = freq_perc
    last_speed_perc = speed_perc
    last_freq_label = "normal"
    current_freq_label = "normal"

    gesture_text = ""
    last_action_time = 0
    action_interval = 3
    last_track_action = None
    gesture_text_show_time = 0
    gesture_text_duration = 2

    current_voice = "original"
    one_held = False
    one_hold_start = None
    last_one_time = 0

    voice_change_text = ""
    voice_change_time = 0

    while True:
        success, img = cap.read()
        if not success:
            break

        img = detector.find_hands(img)
        allHands = detector.get_landmarks(img)
        gesture_text = ""
        current_time = time.time()

        if len(allHands) == 2:
            freq_perc = gesture_ctrl.get_distance_percentage(allHands[0])
            speed_perc = gesture_ctrl.get_distance_percentage(allHands[1])
            last_freq_perc = freq_perc
            last_speed_perc = speed_perc

            hand1_x = np.mean([pt[1] for pt in allHands[0]])
            hand2_x = np.mean([pt[1] for pt in allHands[1]])

            if hand1_x < hand2_x:
                left_thumb = allHands[0][4][1:]
                right_thumb = allHands[1][4][1:]
            else:
                left_thumb = allHands[1][4][1:]
                right_thumb = allHands[0][4][1:]

            dist = gesture_ctrl.distance(left_thumb, right_thumb)
            vol_perc = np.interp(dist, [50, 300], [0, 100])
            vol_perc = max(0, min(vol_perc, 100))
            music_ctrl.set_volume(vol_perc / 100)

            speed = np.interp(speed_perc, [0, 100], [0.5, 2.0])
            music_ctrl.set_playback_speed(speed)

            current_freq_label = freq_label(freq_perc)
            if current_freq_label != last_freq_label:
                last_freq_label = current_freq_label
                music_ctrl.set_voice_and_freq(current_voice, current_freq_label)

            last_track_action = None

        elif len(allHands) == 1:
            freq_perc = last_freq_perc
            speed_perc = last_speed_perc

            fingers_count = gesture_ctrl.count_fingers(allHands[0])
            open_fingers = gesture_ctrl.get_open_fingers(allHands[0])

            if open_fingers == [1, 1, 0, 0, 0]:  # 👌 OK
                freq_perc = 50
                speed_perc = 50
                vol_perc = 70
                current_voice = "original"
                current_freq_label = "normal"
                last_freq_label = "normal"
                music_ctrl.set_volume(0.7)
                music_ctrl.set_playback_speed(1.0)
                music_ctrl.set_voice_and_freq(current_voice, current_freq_label)
                music_ctrl.play()
                gesture_text = "Reset to Default"

            elif fingers_count == 5:
                music_ctrl.pause()
                gesture_text = "Pause"
            elif fingers_count == 0:
                music_ctrl.play()
                gesture_text = "Play"
            elif fingers_count == 2:
                if last_track_action != "next" or (current_time - last_action_time) > action_interval:
                    music_ctrl.next_track()
                    last_action_time = current_time
                    last_track_action = "next"
                    gesture_text = "Next Track"
                    gesture_text_show_time = current_time
            elif fingers_count == 3:
                if open_fingers[0] and open_fingers[1] and open_fingers[2] and not open_fingers[3] and not open_fingers[4]:
                    if last_track_action != "prev" or (current_time - last_action_time) > action_interval:
                        music_ctrl.previous_track()
                        last_action_time = current_time
                        last_track_action = "prev"
                        gesture_text = "Previous Track"
                        gesture_text_show_time = current_time
            elif fingers_count == 1:
                if not one_held:
                    one_hold_start = current_time
                    one_held = True
                elif current_time - one_hold_start >= 2 and (current_time - last_one_time > 2):
                    current_voice = (
                        "female" if current_voice == "male"
                        else "male" if current_voice == "original"
                        else "original"
                    )
                    music_ctrl.set_voice_and_freq(current_voice, current_freq_label)
                    voice_change_text = f"Voice: {current_voice.upper()}"
                    voice_change_time = current_time
                    last_one_time = current_time
            else:
                one_held = False
                one_hold_start = None
                last_track_action = None

        else:
            freq_perc = last_freq_perc
            speed_perc = last_speed_perc
            last_track_action = None

        if current_time - gesture_text_show_time > gesture_text_duration:
            if gesture_text in ["Next Track", "Previous Track", "Reset to Default"]:
                gesture_text = ""

        draw_progress_bar_vertical(img, freq_perc, x=50, y=120, color=(0, 150, 255))
        cv2.putText(img, 'Frequency', (45, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 150, 255), 3)
        cv2.putText(img, freq_label(freq_perc).capitalize(), (10, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 150, 255), 2)

        draw_progress_bar_vertical(img, speed_perc, x=img.shape[1] - 90, y=120, color=(0, 255, 150))
        cv2.putText(img, 'Speed', (img.shape[1] - 140, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 150), 3)
        cv2.putText(img, speed_label(speed_perc), (img.shape[1] - 280, 490), cv2.FONT_HERSHEY_SIMPLEX, 0.9,
                    (0, 255, 150), 2)

        draw_progress_bar_horizontal(img, vol_perc, y=50, color=(255, 100, 255))

        if gesture_text:
            cv2.putText(img, gesture_text, (img.shape[1] // 2 - 150, img.shape[0] - 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3, cv2.LINE_AA)

        if current_time - voice_change_time < 2:
            cv2.putText(img, voice_change_text, (img.shape[1] // 2 - 200, img.shape[0] - 90),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 0), 3, cv2.LINE_AA)

        cv2.imshow("Hand Gesture Frequency & Speed Control", img)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
