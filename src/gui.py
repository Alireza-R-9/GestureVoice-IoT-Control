import sys
import os
import subprocess
import streamlit as st

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from audio_player.player import MusicPlayer
from voice_module.voice_command_handler import VoiceCommandHandler

# ----------------- Streamlit Config -----------------
st.set_page_config(page_title="🎶 GestureVoice IoT Control", layout="wide", page_icon="🎵")
st.markdown("<h1 style='text-align:center; color: #4B0082;'>🎶 GestureVoice IoT Control</h1>", unsafe_allow_html=True)

# ----------------- Session State -----------------
for key in ["mode_confirmed", "exited", "selected_mode", "player", "handler"]:
    if key not in st.session_state:
        st.session_state[key] = False if "confirmed" in key or "exited" in key else None if key in ["player","handler"] else ""

# ----------------- Exit Check -----------------
if st.session_state.exited:
    st.markdown("<h2 style='color:red; text-align:center;'>❌ Project Exited</h2>", unsafe_allow_html=True)
    st.stop()

# ----------------- Select Mode -----------------
selected_mode = st.radio("Select control mode:", ("", "Gesture Control", "Voice Control"), index=0, horizontal=True)
if st.button("✅ Confirm Mode") and selected_mode:
    st.session_state.selected_mode = selected_mode
    st.session_state.mode_confirmed = True
    # پاک کردن Player و Handler اگر حالت تغییر کرد
    if selected_mode != "Voice Control":
        if st.session_state.player:
            st.session_state.player.stop()
        st.session_state.player = None
        st.session_state.handler = None

# ----------------- Initialize Player & Handler (Voice Only) -----------------
if st.session_state.mode_confirmed and st.session_state.selected_mode == "Voice Control":
    if st.session_state.player is None:
        st.session_state.player = MusicPlayer()
        st.session_state.handler = VoiceCommandHandler(st.session_state.player)

    player = st.session_state.player
    handler = st.session_state.handler

    # ----------------- Top Buttons -----------------
    top_col1, top_col2 = st.columns([1,1])
    with top_col1:
        if st.button("🔄 Switch Mode"):
            player.stop()
            st.session_state.player = None
            st.session_state.handler = None
            st.session_state.mode_confirmed = False
            st.session_state.selected_mode = ""
    with top_col2:
        if st.button("❌ Exit Project"):
            player.stop()
            st.session_state.player = None
            st.session_state.handler = None
            st.session_state.exited = True

    st.markdown("---")

    # ----------------- Voice Control -----------------
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

    # Song List
    if player.songs:
        st.markdown("### 🎵 Song List")
        for idx, song in enumerate(player.songs):
            with st.container():
                st.markdown(f"<div style='padding:10px; border-radius:10px; background-color:#f0f8ff;'>"
                            f"<b>{idx+1}. {os.path.basename(song)}</b></div>", unsafe_allow_html=True)
                btn_col1, btn_col2 = st.columns([1,1])
                with btn_col1:
                    if st.button("▶ Play", key=f"play_{idx}"):
                        player.current_index = idx
                        player.play()
                with btn_col2:
                    if st.button("⏹ Stop", key=f"stop_{idx}"):
                        player.stop()

    # Playback Controls
    play_col1, play_col2, play_col3, play_col4, play_col5 = st.columns(5)
    if play_col1.button("▶ Play"): player.play()
    if play_col2.button("⏸ Pause"): player.pause()
    if play_col3.button("▶ Resume"): player.resume()
    if play_col4.button("⏹ Stop"): player.stop()
    if play_col5.button("⏭ Next"): player.next_track()

    # Volume Controls
    vol_col1, vol_col2, vol_col3 = st.columns(3)
    if vol_col1.button("🔊 Volume Up"): player.change_volume(0.1)
    if vol_col2.button("🔉 Volume Down"): player.change_volume(-0.1)
    if vol_col3.button("🔇 Mute"): player.change_volume(-player.volume)

    # Speed Controls
    sp_col1, sp_col2, sp_col3 = st.columns(3)
    if sp_col1.button("⚡ Speed Up"): handler.speed_control.increase()
    if sp_col2.button("🐢 Speed Down"): handler.speed_control.decrease()
    if sp_col3.button("🔄 Reset Speed"): handler.speed_control.reset()

    # Manual Command
    manual_cmd = st.text_input("Type a manual command:")
    if st.button("Execute Command") and manual_cmd:
        handler._execute(manual_cmd.lower())
        st.success(f"Executed: `{manual_cmd.lower()}`")

    # Voice Command
    if st.button("🎙️ Listen for Voice Command"):
        try:
            handler.listen_and_execute()
            st.success("✅ Voice command executed")
        except Exception as e:
            st.error(f"❌ Error: {e}")

# ----------------- Gesture Control -----------------
elif st.session_state.mode_confirmed and st.session_state.selected_mode == "Gesture Control":
    st.subheader("🎥 Gesture Control")
    st.info("This mode launches vision_main.py in a separate process.")
    vision_file = os.path.join("src", "vision_main.py")
    if st.button("Start Gesture Control"):
        if os.path.exists(vision_file):
            subprocess.Popen([sys.executable, vision_file])
            st.success("🎬 Gesture Control started in a new window.")
        else:
            st.error("❌ vision_main.py not found.")

else:
    st.warning("Please select a control mode and press ✅ Confirm Mode to start.")
