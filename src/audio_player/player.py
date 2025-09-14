import os
import pygame
from src.utils import config

class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.volume = config.DEFAULT_VOLUME
        self.current_index = config.DEFAULT_SONG_INDEX
        self.current_frequency = config.DEFAULT_FREQUENCY
        self.available_folders = self.get_available_folders()
        self.songs = []
        self.load_songs()
        pygame.mixer.music.set_volume(self.volume)

        # ▶ شروع خودکار آهنگ اول فولدر normal
        if self.songs:
            print("🎵 Auto-playing first song in 'normal' folder...")
            self.play()

    # ----------------- Folder / Song Management -----------------
    def get_available_folders(self):
        folders = []
        if not os.path.exists(config.BASE_MUSIC_DIR):
            print(f"❌ Base folder not found: {config.BASE_MUSIC_DIR}")
            return folders
        for item in os.listdir(config.BASE_MUSIC_DIR):
            path = os.path.join(config.BASE_MUSIC_DIR, item)
            if os.path.isdir(path) and any(
                f.endswith((".mp3", ".wav", ".ogg")) for f in os.listdir(path) if not f.startswith(".")
            ):
                folders.append(item)
        if folders:
            print(f"🎵 Detected folders: {folders}")
        else:
            print(f"❌ No valid music folders found in {config.BASE_MUSIC_DIR}")
        return folders

    def load_songs(self):
        folder = os.path.join(config.BASE_MUSIC_DIR, self.current_frequency)
        valid_exts = (".mp3", ".wav", ".ogg")

        if not os.path.exists(folder):
            print(f"❌ Folder not found: {folder}")
            self.songs = []
            return

        self.songs = [
            os.path.join(folder, f)
            for f in os.listdir(folder)
            if f.endswith(valid_exts) and not f.startswith(".")
        ]

        if self.songs:
            print(f"🎵 Found {len(self.songs)} songs in {self.current_frequency}:")
            for idx, song in enumerate(self.songs):
                print(f"   {idx+1}. {os.path.basename(song)}")
        else:
            print(f"❌ No songs found in: {folder}")

    # ----------------- Playback -----------------
    def play(self):
        if not self.songs:
            print("❌ No songs to play!")
            return
        pygame.mixer.music.load(self.songs[self.current_index])
        pygame.mixer.music.play()
        print(f"▶ Playing: {os.path.basename(self.songs[self.current_index])}")

    def stop(self):
        pygame.mixer.music.stop()
        print("⏹ Stopped")

    def pause(self):
        pygame.mixer.music.pause()
        print("⏸ Paused")

    def resume(self):
        pygame.mixer.music.unpause()
        print("▶ Resumed")

    def next_track(self):
        if not self.songs:
            print("❌ No songs loaded")
            return
        self.current_index = (self.current_index + 1) % len(self.songs)
        self.play()

    def prev_track(self):
        if not self.songs:
            print("❌ No songs loaded")
            return
        self.current_index = (self.current_index - 1) % len(self.songs)
        self.play()

    # ----------------- Volume -----------------
    def change_volume(self, delta):
        self.volume = min(1.0, max(0.0, self.volume + delta))
        pygame.mixer.music.set_volume(self.volume)
        print(f"🔊 Volume: {self.volume:.1f}")

    # ----------------- Folder / Frequency -----------------
    def change_frequency(self, freq):
        if freq not in self.available_folders:
            print(f"❌ Unsupported folder/frequency: {freq}")
            print(f"Available folders: {self.available_folders}")
            return
        self.current_frequency = freq
        self.current_index = 0
        self.load_songs()
        self.play()

    def next_folder(self):
        if not self.available_folders:
            return
        idx = self.available_folders.index(self.current_frequency)
        self.current_frequency = self.available_folders[(idx + 1) % len(self.available_folders)]
        self.current_index = 0
        self.load_songs()
        self.play()

    def prev_folder(self):
        if not self.available_folders:
            return
        idx = self.available_folders.index(self.current_frequency)
        self.current_frequency = self.available_folders[(idx - 1) % len(self.available_folders)]
        self.current_index = 0
        self.load_songs()
        self.play()

    def reset_folder(self):
        self.current_frequency = config.DEFAULT_FREQUENCY
        self.current_index = 0
        self.load_songs()
        self.play()


# ----------------- Optional Terminal Control -----------------
def run_player():
    player = MusicPlayer()
    print("🎧 Music control ready! Commands:")
    print(
        "play | pause | resume | stop | next | prev | "
        "volume up | volume down | "
        "freq <folder> | freq next | freq prev | freq reset | quit"
    )

    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "play":
            player.play()
        elif cmd == "stop":
            player.stop()
        elif cmd == "pause":
            player.pause()
        elif cmd == "resume":
            player.resume()
        elif cmd == "next":
            player.next_track()
        elif cmd == "prev":
            player.prev_track()
        elif cmd == "volume up":
            player.change_volume(0.1)
        elif cmd == "volume down":
            player.change_volume(-0.1)
        elif cmd.startswith("freq "):
            _, freq = cmd.split(maxsplit=1)
            player.change_frequency(freq)
        elif cmd == "freq next":
            player.next_folder()
        elif cmd == "freq prev":
            player.prev_folder()
        elif cmd == "freq reset":
            player.reset_folder()
        elif cmd == "quit":
            break
        else:
            print("❓ Unknown command")


if __name__ == "__main__":
    run_player()
