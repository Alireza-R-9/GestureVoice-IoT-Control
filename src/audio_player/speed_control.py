import pygame
from src.utils import config, logger


class SpeedControl:
    """
    Handle playback speed control for MusicPlayer
    """

    def __init__(self):
        self.speed = 1.0  # Normal speed
        self.min_speed = 0.5
        self.max_speed = 2.0
        logger.logger.info("⚡ SpeedControl ready (normal speed)")

    def increase(self):
        """Increase playback speed"""
        if self.speed < self.max_speed:
            self.speed += 0.1
            self.speed = round(self.speed, 2)
            self._apply_speed()
            msg = f"⚡ Speed increased → {self.speed}x"
            print(msg)
            logger.logger.info(msg)
        else:
            msg = "❌ Maximum speed reached"
            print(msg)
            logger.logger.warning(msg)

    def decrease(self):
        """Decrease playback speed"""
        if self.speed > self.min_speed:
            self.speed -= 0.1
            self.speed = round(self.speed, 2)
            self._apply_speed()
            msg = f"🐢 Speed decreased → {self.speed}x"
            print(msg)
            logger.logger.info(msg)
        else:
            msg = "❌ Minimum speed reached"
            print(msg)
            logger.logger.warning(msg)

    def reset(self):
        """Reset speed to normal"""
        self.speed = 1.0
        self._apply_speed()
        msg = "🔄 Speed reset to normal (1.0x)"
        print(msg)
        logger.logger.info(msg)

    def _apply_speed(self):
        """
        Direct speed change not supported in pygame.
        This stores the speed value for future playback speed implementation.
        """
        # pygame currently does not support playback speed change directly.
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())
        # Placeholder: external library (like pydub) could be integrated here.


if __name__ == "__main__":
    sc = SpeedControl()
    sc.increase()
    sc.increase()
    sc.decrease()
    sc.reset()
