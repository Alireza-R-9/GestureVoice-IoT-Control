from src.audio_player.player import MusicPlayer
import time

if __name__ == "__main__":
    player = MusicPlayer()
    player.play()

    time.sleep(5)
    player.next_song()
    time.sleep(5)
    player.prev_song()
    time.sleep(5)
    player.stop()
