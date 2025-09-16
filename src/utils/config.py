import os

# ----------------- Project Directories -----------------
# Base directory (project root)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# Main music directory (processed original tracks)
BASE_MUSIC_DIR = os.path.join(BASE_DIR, "music", "processed", "original")

# ----------------- Default Settings -----------------
DEFAULT_FREQUENCY = "normal"      # Default folder to start playback
DEFAULT_SONG_INDEX = 0            # Default song index
DEFAULT_VOLUME = 0.7              # Playback volume (0.0 → 1.0)
DEFAULT_SPEED = 1.0               # Placeholder (pygame does not support direct speed change yet)

# Supported frequency levels
SUPPORTED_FREQUENCIES = ["verylow", "low", "normal", "high", "veryhigh"]

# ----------------- Helper Functions -----------------
def ensure_music_dir():
    """
    Ensure the main music directory exists; create it if missing.
    """
    if not os.path.exists(BASE_MUSIC_DIR):
        os.makedirs(BASE_MUSIC_DIR, exist_ok=True)
        print(f"📂 Created music directory at {BASE_MUSIC_DIR}")


# ----------------- Test Config -----------------
if __name__ == "__main__":
    print("📀 config.py test")
    print("BASE_DIR:", BASE_DIR)
    print("BASE_MUSIC_DIR:", BASE_MUSIC_DIR)
    print("DEFAULT_FREQUENCY:", DEFAULT_FREQUENCY)
    print("DEFAULT_VOLUME:", DEFAULT_VOLUME)
    print("SUPPORTED_FREQUENCIES:", SUPPORTED_FREQUENCIES)
    ensure_music_dir()
