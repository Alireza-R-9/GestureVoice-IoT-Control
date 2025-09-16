import sys

# ----------------- Mode Runners -----------------
def run_vision_mode():
    """
    Import and run the vision gesture control module.
    """
    from src.vision_main import main as vision_main
    vision_main()


def run_voice_mode():
    """
    Import and run the voice command control module.
    """
    from src.voice_main import main as voice_main
    voice_main()


# ----------------- Main Entry -----------------
def main():
    """
    Main entry point for the project.
    Prompts the user to select between Vision or Voice control mode.
    """
    print("Select mode to run:")
    print("1 - Vision Gesture Control")
    print("2 - Voice Command Control")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == '1':
        print("🚀 Starting Vision Gesture Control...")
        run_vision_mode()
    elif choice == '2':
        print("🎙 Starting Voice Command Control...")
        run_voice_mode()
    else:
        print("❌ Invalid choice. Exiting.")
        sys.exit(1)


# ----------------- Script Execution -----------------
if __name__ == "__main__":
    main()
