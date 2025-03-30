import logging
import os
from pathlib import Path
import requests

class OC_logger:
    _loggers = {}

    class TelegramHandler(logging.Handler):
        def __init__(self, token: str, chat_id: str):
            super().__init__(level=logging.ERROR)
            self.token = token
            self.chat_id = chat_id
            self.url = f"https://api.telegram.org/bot{token}/sendMessage"

        def emit(self, record):
            log_entry = self.format(record)
            try:
                requests.post(self.url, data={
                    "chat_id": self.chat_id,
                    "text": f"🛑 {log_entry}"
                })
            except Exception:
                pass  # не ламаємо логер, якщо телега недоступна

    class ColorFormatter(logging.Formatter):
        COLORS = {
            "DEBUG": "\033[90m",
            "INFO": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[97;41m"
        }
        RESET = "\033[0m"

        def format(self, record):
            color = self.COLORS.get(record.levelname, "")
            message = super().format(record)
            return f"{color}{message}{self.RESET}"

    @staticmethod
    def oc_log(name_log: str) -> logging.Logger:
        file_path = f"log/{name_log}.log"
        error_path = "log/error.log"

        if file_path in OC_logger._loggers:
            return OC_logger._loggers[file_path]

        Path("log").mkdir(exist_ok=True)

        logger = logging.getLogger(name_log)
        logger.setLevel(OC_logger._get_level())

        if not logger.handlers:
            formatter = logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
            )

            file_handler = logging.FileHandler(file_path)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

            if OC_logger._is_dev():
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(OC_logger.ColorFormatter(
                    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
                ))
                logger.addHandler(console_handler)

            error_handler = logging.FileHandler(error_path)
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(formatter)
            logger.addHandler(error_handler)

            # 🔥 Telegram error handler
            bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            if bot_token and chat_id:
                tg_handler = OC_logger.TelegramHandler(bot_token, chat_id)
                tg_handler.setFormatter(formatter)
                logger.addHandler(tg_handler)

        OC_logger._loggers[file_path] = logger
        return logger

    @staticmethod
    def _get_level() -> int:
        return logging.DEBUG if OC_logger._is_dev() else logging.INFO

    @staticmethod
    def _is_dev() -> bool:
        return os.getenv("ENV", "prod").lower() == "dev"
