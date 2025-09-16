import sys
import os
import subprocess
import streamlit as st
import socket
import json

# ----------------- Project Path -----------------
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audio_player.player import MusicPlayer
from voice_module.voice_command_handler import VoiceCommandHandler

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="🎶 GestureVoice IoT Control", layout="wide", page_icon="🎵")
st.markdown(
    """
    <style>
        .stButton > button {
            width: 100%;
            border-radius: 10px;
            padding: 10px;
            background-color: #4B0082;
            color: white;
            font-weight: bold;
        }
        .stButton > button:hover {
            background-color: #6A0DAD;
            color: #f0f0f0;
        }
        .song-card {
            padding: 10px;
            border-radius: 12px;
            background-color: #f8f8ff;
            margin-bottom: 8px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='text-align:center; color: #4B0082;'>🎶 GestureVoice IoT Control</h1>", unsafe_allow_html=True)


# ----------------- Socket Client -----------------
class ESP32Client:
    def __init__(self, host="127.0.0.1", port=5055):
        self.host = host
        self.port = port

    def send_command(self, command, data=None):
        try:
            msg = json.dumps({"command": command, "data": data})
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                s.connect((self.host, self.port))
                s.sendall(msg.encode("utf-8"))
        except Exception as e:
            st.warning(f"⚠️ Socket Error: {e}")


# ----------------- Session State -----------------
defaults = {
    "mode_confirmed": False,
    "exited": False,
    "selected_mode": "",
    "player": None,
    "handler": None,
    "esp_client": None
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

if st.session_state.esp_client is None:
    st.session_state.esp_client = ESP32Client()

esp_client = st.session_state.esp_client

# ----------------- Exit Check -----------------
if st.session_state.exited:
    st.markdown("<h2 style='color:red; text-align:center;'>❌ Project Exited</h2>", unsafe_allow_html=True)
    st.stop()

# ----------------- Select Mode -----------------
selected_mode = st.radio("Select control mode:", ("", "Gesture Control", "Voice Control"), index=0, horizontal=True)
if st.button("✅ Confirm Mode") and selected_mode:
    st.session_state.selected_mode = selected_mode
    st.session_state.mode_confirmed = True

# ----------------- Initialize Player & Handler -----------------
if st.session_state.mode_confirmed:
    if st.session_state.player is None:
        st.session_state.player = MusicPlayer()
        st.session_state.handler = VoiceCommandHandler(st.session_state.player)

    player = st.session_state.player
    handler = st.session_state.handler

    # ----------------- Top Buttons -----------------
    top_col1, top_col2 = st.columns([1, 1])
    with top_col1:
        if st.button("🔄 Switch Mode"):
            player.stop()
            esp_client.send_command("STOP")
            st.session_state.mode_confirmed = False
            st.session_state.selected_mode = ""
    with top_col2:
        if st.button("❌ Exit Project"):
            player.stop()
            esp_client.send_command("STOP")
            st.session_state.exited = True

    st.markdown("---")

    # ----------------- Voice Control -----------------
    if st.session_state.selected_mode == "Voice Control":
        st.subheader("🎤 Voice & Manual Command Control")
        st.info("Use controls below to manage music and voice commands.")

        # Current Folder & Song
        st.markdown(f"**Current Folder:** `{player.current_frequency}`")
        now_playing = os.path.basename(player.songs[player.current_index]) if player.songs else "No songs loaded"
        st.markdown(f"**Now Playing:** `{now_playing}`")

        # Folder Selection
        folder_selected = st.selectbox("Change Folder", player.available_folders,
                                       index=player.available_folders.index(player.current_frequency))
        if st.button("Set Folder"):
            player.change_frequency(folder_selected)
            esp_client.send_command("FOLDER", {"folder": folder_selected})

        # Song List as Cards
        if player.songs:
            st.markdown("### 🎵 Song List")
            for idx, song in enumerate(player.songs):
                with st.container():
                    st.markdown(f"<div class='song-card'><b>{idx+1}. {os.path.basename(song)}</b></div>", unsafe_allow_html=True)
                    btn_col1, btn_col2 = st.columns([1, 1])
                    with btn_col1:
                        if st.button("▶ Play", key=f"play_{idx}"):
                            player.current_index = idx
                            player.play()
                            esp_client.send_command("PLAY", {"track_index": idx})
                    with btn_col2:
                        if st.button("⏹ Stop", key=f"stop_{idx}"):
                            player.stop()
                            esp_client.send_command("STOP")

        # Playback Controls
        play_col1, play_col2, play_col3, play_col4, play_col5 = st.columns(5)
        if play_col1.button("▶ Play"):
            player.play()
            esp_client.send_command("PLAY", {"track_index": player.current_index})
        if play_col2.button("⏸ Pause"):
            player.pause()
            esp_client.send_command("PAUSE")
        if play_col3.button("▶ Resume"):
            player.resume()
            esp_client.send_command("RESUME")
        if play_col4.button("⏹ Stop"):
            player.stop()
            esp_client.send_command("STOP")
        if play_col5.button("⏭ Next"):
            player.next_track()
            esp_client.send_command("NEXT")

        pr_col1, pr_col2 = st.columns(2)
        if pr_col1.button("⏮ Prev"):
            player.prev_track()
            esp_client.send_command("PREV")
        if pr_col2.button("🔄 Reset Folder"):
            player.reset_folder()
            esp_client.send_command("RESET_FOLDER")

        # Volume Controls
        vol_col1, vol_col2, vol_col3 = st.columns(3)
        if vol_col1.button("🔊 Volume Up"):
            player.change_volume(0.1)
            esp_client.send_command("VOLUME", {"delta": 0.1})
        if vol_col2.button("🔉 Volume Down"):
            player.change_volume(-0.1)
            esp_client.send_command("VOLUME", {"delta": -0.1})
        if vol_col3.button("🔇 Mute"):
            player.change_volume(-player.volume)
            esp_client.send_command("VOLUME", {"delta": -player.volume})

        # Speed Controls
        sp_col1, sp_col2, sp_col3 = st.columns(3)
        if sp_col1.button("⚡ Speed Up"):
            handler.speed_control.increase()
            esp_client.send_command("SPEED", {"delta": 0.1})
        if sp_col2.button("🐢 Speed Down"):
            handler.speed_control.decrease()
            esp_client.send_command("SPEED", {"delta": -0.1})
        if sp_col3.button("🔄 Reset Speed"):
            handler.speed_control.reset()
            esp_client.send_command("SPEED", {"reset": True})

        # Manual Command
        manual_cmd = st.text_input("Type a manual command:")
        if st.button("Execute Command") and manual_cmd:
            handler._execute(manual_cmd.lower())
            esp_client.send_command("MANUAL", {"command": manual_cmd.lower()})
            st.success(f"Executed: `{manual_cmd.lower()}`")

        # Voice Command
        if st.button("🎙️ Listen for Voice Command"):
            try:
                handler.listen_and_execute()
                esp_client.send_command("VOICE", {"command": "executed"})
                st.success("✅ Voice command executed")
            except Exception as e:
                st.error(f"❌ Error: {e}")

    # ----------------- Gesture Control -----------------
    elif st.session_state.selected_mode == "Gesture Control":
        st.subheader("🎥 Gesture Control")
        st.info("This mode launches vision_main.py in a separate process.")
        vision_file = os.path.join("src", "vision_main.py")
        if st.button("Start Gesture Control"):
            if os.path.exists(vision_file):
                player.stop()
                esp_client.send_command("STOP")
                subprocess.Popen([sys.executable, vision_file])
                st.success("🎬 Gesture Control started in a new window.")
            else:
                st.error("❌ vision_main.py not found.")

else:
    st.warning("⚠️ Please select a control mode and press ✅ Confirm Mode to start.")
