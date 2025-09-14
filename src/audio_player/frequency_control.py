import os
from src.utils import config, logger


class FrequencyControl:
    def __init__(self):
        self.supported = config.SUPPORTED_FREQUENCIES
        self.current = config.DEFAULT_FREQUENCY
        self.base_dir = config.BASE_MUSIC_DIR
        logger.logger.info(f"🎼 FrequencyControl فعال شد → {self.current}")

    def set_frequency(self, freq: str):
        """تغییر فرکانس به یک مقدار مشخص"""
        if freq not in self.supported:
            print(f"❌ فرکانس نامعتبر! مقادیر مجاز: {self.supported}")
            logger.logger.warning(f"🚫 تلاش برای انتخاب فرکانس نامعتبر: {freq}")
            return None

        new_dir = os.path.join(os.path.dirname(self.base_dir), freq)
        if not os.path.exists(new_dir):
            print(f"❌ مسیر {new_dir} یافت نشد")
            logger.logger.error(f"❌ مسیر فرکانس {new_dir} موجود نیست")
            return None

        self.current = freq
        self.base_dir = new_dir
        print(f"🎼 فرکانس تغییر یافت به: {self.current}")
        logger.logger.info(f"🎼 فرکانس تغییر یافت به: {self.current}")
        return self.base_dir

    def next_frequency(self):
        """رفتن به فرکانس بعدی در لیست"""
        idx = self.supported.index(self.current)
        new_idx = (idx + 1) % len(self.supported)
        return self.set_frequency(self.supported[new_idx])

    def prev_frequency(self):
        """رفتن به فرکانس قبلی در لیست"""
        idx = self.supported.index(self.current)
        new_idx = (idx - 1) % len(self.supported)
        return self.set_frequency(self.supported[new_idx])

    def reset(self):
        """بازگشت به فرکانس نرمال"""
        return self.set_frequency(config.DEFAULT_FREQUENCY)


if __name__ == "__main__":
    fc = FrequencyControl()
    fc.set_frequency("high")
    fc.next_frequency()
    fc.prev_frequency()
    fc.reset()
