import sys

def run_vision_mode():
    from src.vision_main import main as vision_main
    vision_main()

def run_voice_mode():
    from src.voice_main import main as voice_main
    voice_main()

def main():
    print("Select mode to run:")
    print("1 - Vision Gesture Control")
    print("2 - Voice Command Control")

    choice = input("Enter choice (1 or 2): ").strip()

    if choice == '1':
        print("Starting Vision Gesture Control...")
        run_vision_mode()
    elif choice == '2':
        print("Starting Voice Command Control...")
        run_voice_mode()
    else:
        print("Invalid choice. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
