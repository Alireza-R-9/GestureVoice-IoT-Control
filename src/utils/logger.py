import logging
import os

# ----------------- Log File Configuration -----------------
# Base directory of the project → project.log will be created next to it
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "project.log")

# Optional: create a separate logs folder
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# os.makedirs(LOG_DIR, exist_ok=True)
# LOG_FILE = os.path.join(LOG_DIR, "project.log")

# ----------------- Logger Setup -----------------
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,  # Capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Console handler → also show logs in terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Show INFO and above in console
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console_handler)

# Create named logger
logger = logging.getLogger("MusicVoiceControl")

# ----------------- Test Logger -----------------
if __name__ == "__main__":
    logger.info("✅ Test info from logger.py")
    logger.error("❌ Test error from logger.py")
    print(f"Logger test completed! Check file: {LOG_FILE}")
