import os
from src.utils import config, logger


class FrequencyControl:
    def __init__(self):
        # Initialize the supported frequencies, current frequency, and base music directory
        self.supported = config.SUPPORTED_FREQUENCIES
        self.current = config.DEFAULT_FREQUENCY
        self.base_dir = config.BASE_MUSIC_DIR
        logger.logger.info(f"🎼 FrequencyControl activated → {self.current}")

    def set_frequency(self, freq: str):
        """Change frequency to a specified value"""
        if freq not in self.supported:
            print(f"❌ Invalid frequency! Allowed values: {self.supported}")
            logger.logger.warning(f"🚫 Attempted to select invalid frequency: {freq}")
            return None

        new_dir = os.path.join(os.path.dirname(self.base_dir), freq)
        if not os.path.exists(new_dir):
            print(f"❌ Path {new_dir} not found")
            logger.logger.error(f"❌ Frequency path {new_dir} does not exist")
            return None

        self.current = freq
        self.base_dir = new_dir
        print(f"🎼 Frequency changed to: {self.current}")
        logger.logger.info(f"🎼 Frequency changed to: {self.current}")
        return self.base_dir

    def next_frequency(self):
        """Move to the next frequency in the list"""
        idx = self.supported.index(self.current)
        new_idx = (idx + 1) % len(self.supported)
        return self.set_frequency(self.supported[new_idx])

    def prev_frequency(self):
        """Move to the previous frequency in the list"""
        idx = self.supported.index(self.current)
        new_idx = (idx - 1) % len(self.supported)
        return self.set_frequency(self.supported[new_idx])

    def reset(self):
        """Reset to the default/normal frequency"""
        return self.set_frequency(config.DEFAULT_FREQUENCY)


if __name__ == "__main__":
    # Example usage of FrequencyControl
    fc = FrequencyControl()
    fc.set_frequency("high")
    fc.next_frequency()
    fc.prev_frequency()
    fc.reset()
