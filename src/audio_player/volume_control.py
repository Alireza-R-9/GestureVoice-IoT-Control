import pygame
from src.utils import config, logger


class VolumeControl:
    """
    Handle volume control for MusicPlayer.
    Volume range: 0.0 (mute) → 1.0 (max)
    """

    def __init__(self, initial_volume=None):
        """Initialize volume control with optional starting volume"""
        if initial_volume is None:
            initial_volume = config.DEFAULT_VOLUME
        self.volume = max(0.0, min(1.0, initial_volume))
        pygame.mixer.music.set_volume(self.volume)
        logger.logger.info(f"🔊 Initial volume set: {self.volume:.2f}")

    def increase(self, step=0.1):
        """Increase volume by a given step"""
        if self.volume < 1.0:
            self.volume = min(1.0, self.volume + step)
            pygame.mixer.music.set_volume(self.volume)
            print(f"🔊 Volume increased → {self.volume:.2f}")
            logger.logger.info(f"🔊 Volume increased: {self.volume:.2f}")
        else:
            print("❌ Maximum volume reached")
            logger.logger.warning("🚫 Attempted to increase volume beyond maximum")

    def decrease(self, step=0.1):
        """Decrease volume by a given step"""
        if self.volume > 0.0:
            self.volume = max(0.0, self.volume - step)
            pygame.mixer.music.set_volume(self.volume)
            print(f"🔉 Volume decreased → {self.volume:.2f}")
            logger.logger.info(f"🔉 Volume decreased: {self.volume:.2f}")
        else:
            print("❌ Minimum volume reached")
            logger.logger.warning("🚫 Attempted to decrease volume below minimum")

    def set_volume(self, value):
        """Set volume directly within allowed range"""
        self.volume = max(0.0, min(1.0, value))
        pygame.mixer.music.set_volume(self.volume)
        print(f"🎚 Volume set → {self.volume:.2f}")
        logger.logger.info(f"🔊 Volume directly set: {self.volume:.2f}")

    def get_volume(self):
        """Return the current volume level"""
        return self.volume


if __name__ == "__main__":
    # Terminal-based volume control demo
    vc = VolumeControl()
    print("Volume test commands: 'up', 'down', 'set <val>', 'get', 'quit'")
    while True:
        cmd = input(">> ").strip().lower()
        if cmd == "up":
            vc.increase()
        elif cmd == "down":
            vc.decrease()
        elif cmd.startswith("set"):
            try:
                val = float(cmd.split()[1])
                vc.set_volume(val)
            except Exception:
                print("❌ Usage: set <value between 0.0 and 1.0>")
        elif cmd == "get":
            print(f"📢 Current volume: {vc.get_volume():.2f}")
        elif cmd == "quit":
            break
        else:
            print("❌ Invalid command! up | down | set <val> | get | quit")
