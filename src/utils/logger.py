import logging
import os

# Log file path → project.log کنار پوشه اصلی پروژه
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_FILE = os.path.join(BASE_DIR, "project.log")

# Ensure logs directory exists (اختیاری، اگه بخوای پوشه جدا باشه)
# LOG_DIR = os.path.join(BASE_DIR, "logs")
# os.makedirs(LOG_DIR, exist_ok=True)
# LOG_FILE = os.path.join(LOG_DIR, "project.log")

# Logger configuration
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

# Console handler (نمایش لاگ همزمان در ترمینال)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))
logging.getLogger().addHandler(console_handler)

logger = logging.getLogger("MusicVoiceControl")

if __name__ == "__main__":
    logger.info("Test info from logger.py")
    logger.error("Test error from logger.py")
    print(f"✅ Logger test completed! Output in file: {LOG_FILE}")
