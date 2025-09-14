import logging
from src.audio_player.player import MusicPlayer
from src.voice_module.voice_command_handler import VoiceCommandHandler

logging.basicConfig(level=logging.INFO)

def main():
    player = MusicPlayer()
    handler = VoiceCommandHandler(player)

    command_list = """
🎙️ Available commands (type or voice):
Playback control:
  play, pause, resume, stop

Track navigation:
  next, prev

Volume control:
  volume up, volume down

Playback speed:
  speed up, speed down, speed reset

Frequency/folder:
  freq <folder> (high, low, veryhigh, verylow, normal)
  freq next, freq prev, freq reset

Program control:
  quit
  help → show this list
"""

    print("🎶 Voice-Control Music Player is ready!")
    print(command_list)
    print("💻 Type a command or just press Enter for voice input...")

    while True:
        user_input = input("\nType command or press Enter for voice: ").strip().lower()

        if user_input == "help":
            print(command_list)
            continue

        if user_input:
            # User typed a command
            player.stop()
            handler.handle_command(user_input)
        else:
            # Voice command
            player.stop()
            handler.listen_and_execute()


if __name__ == "__main__":
    main()
