import os
import librosa
import soundfile as sf

# Base music folder
music_folder = "music"
processed_folder = os.path.join(music_folder, "processed")

# ----------------- Processing Settings -----------------
freq_levels = {
    "verylow": 0.5,
    "low": 0.75,
    "normal": 1.0,
    "high": 1.25,
    "veryhigh": 1.5
}

voice_genders = {
    "original": 0,     # No pitch shift
    "male": -3,        # Lower pitch
    "female": 3        # Higher pitch
}


def ensure_directory(path):
    """
    Ensure that a directory exists; create it if it does not.
    """
    if not os.path.exists(path):
        os.makedirs(path)


def convert_and_save(input_path, output_path, pitch_semitones, time_stretch_factor):
    """
    Convert a single track with pitch shift and time-stretching, then save it.

    Args:
        input_path (str): Path to the input audio file.
        output_path (str): Path to save the processed audio file.
        pitch_semitones (int/float): Number of semitones to shift (positive or negative).
        time_stretch_factor (float): Factor to stretch/compress time (speed).
    """
    y, sr = librosa.load(input_path, sr=None)

    # Apply pitch shift
    if pitch_semitones != 0:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_semitones)

    # Apply time stretch
    if time_stretch_factor != 1.0:
        y = librosa.effects.time_stretch(y, rate=time_stretch_factor)

    sf.write(output_path, y, sr)


def process_all_tracks():
    """
    Process all .mp3 tracks in the base music folder.
    For each track, create processed versions for all combinations of:
    - Voice genders (original, male, female)
    - Frequency/speed levels (verylow → veryhigh)
    """
    print("🎵 Starting pitch conversion...")

    for file in os.listdir(music_folder):
        if file.endswith(".mp3"):
            source_path = os.path.join(music_folder, file)

            for gender, semitone_shift in voice_genders.items():
                for freq_level, speed_factor in freq_levels.items():
                    output_dir = os.path.join(processed_folder, gender, freq_level)
                    ensure_directory(output_dir)

                    output_path = os.path.join(output_dir, file)

                    print(f"🔧 Processing {file} | Gender: {gender} | Freq: {freq_level}")
                    convert_and_save(
                        input_path=source_path,
                        output_path=output_path,
                        pitch_semitones=semitone_shift,
                        time_stretch_factor=speed_factor
                    )

    print("✅ All tracks processed and saved.")


if __name__ == "__main__":
    process_all_tracks()
