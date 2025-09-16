import os
import vlc

class MusicController:
    """
    Handle music playback with VLC, supporting:
    - Processed tracks based on voice gender and frequency label
    - Basic controls: play, pause, stop, next, previous
    - Volume and playback speed adjustment
    """

    def __init__(self, music_folder):
        # Convert path to absolute
        self.music_folder = os.path.abspath(music_folder)
        self.processed_folder = os.path.join(self.music_folder, "processed")
        self.voice_gender = "original"  # Options: original, male, female
        self.freq_label = "normal"      # Options: verylow, low, normal, high, veryhigh

        self.player = vlc.MediaPlayer()
        self.track_list = self.load_tracks()
        self.track_index = 0

        if self.track_list:
            self.load_track(self.track_index)
            self.play()

    def load_tracks(self):
        """Load all mp3 tracks from the music folder"""
        return [file for file in os.listdir(self.music_folder) if file.endswith('.mp3')]

    def get_processed_track_path(self, filename):
        """
        Return the path to the processed track based on voice gender and frequency.
        If processed version does not exist, return the original track path.
        """
        name, _ = os.path.splitext(filename)

        # Original track if no processing is required
        if self.voice_gender == "original" and self.freq_label == "normal":
            return os.path.join(self.music_folder, filename)

        processed_path = os.path.join(
            self.processed_folder,
            self.voice_gender,
            self.freq_label,
            f"{name}_{self.voice_gender}_{self.freq_label}.mp3"
        )

        # Use processed file if it exists
        if os.path.exists(processed_path):
            return processed_path
        else:
            return os.path.join(self.music_folder, filename)

    def load_track(self, index):
        """Load the track at the given index into VLC player"""
        if 0 <= index < len(self.track_list):
            original_file = self.track_list[index]
            track_path = self.get_processed_track_path(original_file)
            self.player.set_media(vlc.Media(track_path))

    # ----------------- Playback Controls -----------------
    def play(self):
        """Start or resume playback"""
        if not self.player.is_playing():
            self.player.play()

    def pause(self):
        """Pause playback"""
        if self.player.is_playing():
            self.player.pause()

    def stop(self):
        """Stop playback"""
        self.player.stop()

    def next_track(self):
        """Play the next track in the playlist"""
        self.track_index = (self.track_index + 1) % len(self.track_list)
        self.load_track(self.track_index)
        self.play()

    def previous_track(self):
        """Play the previous track in the playlist"""
        self.track_index = (self.track_index - 1) % len(self.track_list)
        self.load_track(self.track_index)
        self.play()

    # ----------------- Audio Settings -----------------
    def set_volume(self, volume):
        """
        Set volume (0.0 → 1.0)
        VLC volume scale: 0 → 100
        """
        volume = int(max(0, min(volume, 1)) * 100)
        self.player.audio_set_volume(volume)

    def set_playback_speed(self, speed):
        """
        Set playback speed (0.5 → 2.0)
        """
        if 0.5 <= speed <= 2.0:
            self.player.set_rate(speed)

    # ----------------- Voice / Frequency -----------------
    def toggle_voice_gender(self):
        """
        Cycle through voice genders: original → male → female → original
        Frequency label remains unchanged
        """
        if self.voice_gender == "original":
            self.voice_gender = "male"
        elif self.voice_gender == "male":
            self.voice_gender = "female"
        else:
            self.voice_gender = "original"

        print(f"[Voice Gender] Switched to {self.voice_gender}")
        self.load_track(self.track_index)
        self.play()

    def set_voice_and_freq(self, gender, freq_label):
        """
        Set both voice gender and frequency label simultaneously
        """
        self.voice_gender = gender
        self.freq_label = freq_label
        print(f"[Voice/Freq] Switched to {gender}/{freq_label}")
        self.load_track(self.track_index)
        self.play()
