import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)

class MicrophoneUtils:
    """
    Professional microphone utilities for voice recognition
    """

    def __init__(self, language="en-US"):
        self.recognizer = sr.Recognizer()
        self.microphone_index = None  # Default microphone (system default)
        self.language = language

    def list_microphones(self):
        """List available microphones"""
        try:
            mics = sr.Microphone.list_microphone_names()
            for i, name in enumerate(mics):
                print(f"{i}: {name}")
            return mics
        except Exception as e:
            logger.error(f"❌ Could not list microphones: {e}")
            return []

    def set_microphone(self, index: int):
        """Select a specific microphone"""
        self.microphone_index = index
        logger.info(f"🎤 Microphone selected: {index}")

    def listen(self, timeout=10, phrase_time_limit=10):
        """
        Record audio with automatic noise adjustment.
        Returns audio data or None if no input detected.
        """
        try:
            with sr.Microphone(device_index=self.microphone_index) as source:
                logger.info("🎙️ Listening... Please speak now.")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
                return audio
        except sr.WaitTimeoutError:
            logger.warning("⏳ Timeout reached, no speech detected.")
            return None
        except OSError as e:
            logger.error(f"❌ Microphone error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Error while recording audio: {e}")
            return None

    def recognize(self, audio):
        """
        Convert recorded audio to text using Google API.
        Returns recognized text or None if failed.
        """
        if audio is None:
            return None
        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            logger.info(f"✅ Recognized text: {text}")
            return text.lower().strip()
        except sr.UnknownValueError:
            logger.error("❌ Speech could not be recognized (unintelligible).")
            return None
        except sr.RequestError as e:
            logger.error(f"❌ Error connecting to Google service: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Unexpected recognition error: {e}")
            return None
