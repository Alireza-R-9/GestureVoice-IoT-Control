import os

# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Main directory for music
BASE_MUSIC_DIR = os.path.join(BASE_DIR, "music", "processed", "original")

# Default folder to start
DEFAULT_FREQUENCY = "normal"

# Default song index
DEFAULT_SONG_INDEX = 0

# Playback settings
DEFAULT_VOLUME = 0.7   # Range: 0.0 → 1.0
DEFAULT_SPEED = 1.0    # Placeholder (pygame doesn’t support direct speed change yet)

# Supported frequencies
SUPPORTED_FREQUENCIES = ["verylow", "low", "normal", "high", "veryhigh"]

# Helper: Ensure music directory exists
def ensure_music_dir():
    if not os.path.exists(BASE_MUSIC_DIR):
        os.makedirs(BASE_MUSIC_DIR, exist_ok=True)
        print(f"📂 Created music directory at {BASE_MUSIC_DIR}")

if __name__ == "__main__":
    print("📀 config.py test")
    print("BASE_DIR:", BASE_DIR)
    print("BASE_MUSIC_DIR:", BASE_MUSIC_DIR)
    print("DEFAULT_FREQUENCY:", DEFAULT_FREQUENCY)
    print("DEFAULT_VOLUME:", DEFAULT_VOLUME)
    print("SUPPORTED_FREQUENCIES:", SUPPORTED_FREQUENCIES)
    ensure_music_dir()
