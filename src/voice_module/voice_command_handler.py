import logging
from src.audio_player.player import MusicPlayer
from src.audio_player.speed_control import SpeedControl
from src.voice_module.microphone_utils import MicrophoneUtils
from src.voice_module.command_parser import CommandParser

logger = logging.getLogger(__name__)


class VoiceCommandHandler:
    """
    Handle voice & manual commands (English) and control the MusicPlayer
    """

    def __init__(self, player: MusicPlayer):
        self.player = player
        self.speed_control = SpeedControl()
        self.mic = MicrophoneUtils(language="en-US")
        self.parser = CommandParser()

    def listen_and_execute(self):
        """Listen from mic, parse command, and execute"""
        audio = self.mic.listen(timeout=10, phrase_time_limit=10)
        if not audio:
            return
        text = self.mic.recognize(audio)
        if not text:
            print("❌ No text detected.")
            return

        command = self.parser.parse(text)
        if not command:
            print("❌ Unknown command.")
            logger.warning(f"Unknown command: {text}")
            return

        print(f"👉 Executing command: {command}")
        logger.info(f"Executing command: {command}")
        self._execute(command)

    def manual_input(self):
        """
        Allow user to type commands manually.
        Music stops temporarily while manual command is entered.
        """
        self.player.stop()
        print("\n⌨ Manual Command Mode Activated")
        print("📜 Available commands:")
        print("play, pause, resume, stop, next, prev, volume up, volume down")
        print("speed up, speed down, speed reset")
        print("freq <folder>, freq next, freq prev, freq reset")
        print("quit\n")

        while True:
            command = input("👉 Type a command (or 'back' to return): ").strip().lower()
            if command == "back":
                print("↩ Returning to main loop...")
                break
            if command:
                self._execute(command)

    def _execute(self, command: str):
        """Execute the command on MusicPlayer"""
        if command == "play":
            self.player.play()
        elif command == "pause":
            self.player.pause()
        elif command == "resume":
            self.player.resume()
        elif command == "stop":
            self.player.stop()
        elif command == "next":
            self.player.next_track()
        elif command == "prev":
            self.player.prev_track()
        elif command == "volume up":
            self.player.change_volume(0.1)
        elif command == "volume down":
            self.player.change_volume(-0.1)
        elif command == "speed up":
            self.speed_control.increase()
        elif command == "speed down":
            self.speed_control.decrease()
        elif command == "speed reset":
            self.speed_control.reset()
        elif command.startswith("freq"):
            parts = command.split()
            if len(parts) == 2:
                if parts[1] == "next":
                    self.player.next_folder()
                elif parts[1] == "prev":
                    self.player.prev_folder()
                elif parts[1] == "reset":
                    self.player.reset_folder()
                else:
                    # folder name like high, low, normal...
                    self.player.change_frequency(parts[1])
            else:
                print("❌ Invalid freq command. Example: freq high, freq next")
        elif command == "quit":
            print("👋 Exiting program")
            exit(0)
        else:
            print("❌ Command not recognized.")
            logger.warning(f"Invalid command executed: {command}")
