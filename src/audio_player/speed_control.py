import pygame
from src.utils import config, logger


class SpeedControl:
    """
    Handle playback speed control for MusicPlayer.
    Stores speed value and logs changes.
    Note: Direct speed adjustment is not supported by pygame mixer.
    """

    def __init__(self):
        # Initialize speed control with default, min, and max speed
        self.speed = 1.0  # Normal speed
        self.min_speed = 0.5
        self.max_speed = 2.0
        logger.logger.info("⚡ SpeedControl ready (normal speed)")

    def increase(self):
        """Increase playback speed by 0.1x"""
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
        """Decrease playback speed by 0.1x"""
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
        """Reset playback speed to normal (1.0x)"""
        self.speed = 1.0
        self._apply_speed()
        msg = "🔄 Speed reset to normal (1.0x)"
        print(msg)
        logger.logger.info(msg)

    def _apply_speed(self):
        """
        Placeholder for applying speed to playback.
        Note: pygame.mixer does not support changing speed directly.
        The current implementation keeps the speed value for future use
        with an external library (e.g., pydub) if needed.
        """
        # Keep volume unchanged as a placeholder action
        pygame.mixer.music.set_volume(pygame.mixer.music.get_volume())


if __name__ == "__main__":
    # Example usage of SpeedControl
    sc = SpeedControl()
    sc.increase()
    sc.increase()
    sc.decrease()
    sc.reset()
