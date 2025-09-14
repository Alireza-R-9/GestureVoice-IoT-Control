import os
import librosa
import soundfile as sf

# مسیر پوشه موسیقی اصلی
music_folder = "music"
processed_folder = os.path.join(music_folder, "processed")

# تنظیمات پردازش
freq_levels = {
    "verylow": 0.5,
    "low": 0.75,
    "normal": 1.0,
    "high": 1.25,
    "veryhigh": 1.5
}

voice_genders = {
    "original": 0,     # تغییر جنسیت ندارد
    "male": -3,        # بم‌تر
    "female": 3        # زیرتر
}


def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def convert_and_save(input_path, output_path, pitch_semitones, time_stretch_factor):
    y, sr = librosa.load(input_path, sr=None)

    # تغییر گام
    if pitch_semitones != 0:
        y = librosa.effects.pitch_shift(y, sr=sr, n_steps=pitch_semitones)

    # تغییر سرعت
    if time_stretch_factor != 1.0:
        y = librosa.effects.time_stretch(y, rate=time_stretch_factor)

    sf.write(output_path, y, sr)


def process_all_tracks():
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