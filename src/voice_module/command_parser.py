class CommandParser:
    """
    Convert raw recognized text to standardized music commands
    """

    def __init__(self):
        self.command_map = {
            # Playback
            "play": "play",
            "pause": "pause",
            "resume": "resume",
            "stop": "stop",

            # Navigation
            "next": "next",
            "previous": "prev",
            "prev": "prev",

            # Volume
            "volume up": "volume up",
            "increase volume": "volume up",
            "louder": "volume up",
            "volume down": "volume down",
            "decrease volume": "volume down",
            "quieter": "volume down",

            # Speed
            "speed up": "speed up",
            "increase speed": "speed up",
            "speed down": "speed down",
            "decrease speed": "speed down",
            "speed reset": "speed reset",
            "normal speed": "speed reset",

            # Frequency / folder
            "freq next": "freq next",
            "freq prev": "freq prev",
            "freq reset": "freq reset",

            # Program control
            "quit": "quit",
            "exit": "quit",
            "close": "quit",
        }

    def parse(self, text: str):
        if not text:
            return None
        text = text.strip().lower()

        # Exact matches
        if text in self.command_map:
            return self.command_map[text]

        # Partial or flexible commands
        for cmd in ["speed", "freq", "volume"]:
            if text.startswith(cmd):
                return text

        return None
