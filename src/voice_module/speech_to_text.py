import speech_recognition as sr
import logging

logger = logging.getLogger(__name__)


class SpeechToText:
    def __init__(self, language="en-US"):
        """
        :param language: Default language ('en-US' for English, 'fa-IR' for Persian)
        """
        self.recognizer = sr.Recognizer()
        self.language = language

    def listen_and_convert(self, timeout=10, phrase_time_limit=10):
        """
        Listen from microphone and convert speech to text
        """
        with sr.Microphone() as source:
            logger.info("🎙️ Please speak now...")
            print("🎙️ Please speak now...")

            try:
                # Adjust for background noise
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)

                # Convert audio to text
                text = self.recognizer.recognize_google(audio, language=self.language)
                logger.info(f"✅ Recognized text: {text}")
                return text.strip().lower()

            except sr.WaitTimeoutError:
                logger.warning("⏳ Timeout reached, no speech detected.")
                return None
            except sr.UnknownValueError:
                logger.error("❌ Speech could not be understood.")
                return None
            except sr.RequestError as e:
                logger.error(f"❌ Error connecting to Google service: {e}")
                return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    stt = SpeechToText(language="en-US")  # English recognition

    while True:
        text = stt.listen_and_convert()
        if text:
            print("👉 Text:", text)
        else:
            print("❌ No text detected.")
