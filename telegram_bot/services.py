from models import TelegramBot
from telegram_bot.schemas import Update


class SurveyMessagesProcessor:
    pass


class TelegramUpdateProcessor:
    def __init__(self, update: Update, bot: TelegramBot):
        self.update = update
        self.bot = bot

    def process(self): ...

    def prepare_response(self):
        match self.update.message.text:
            case "/start":
                return self.bot.greeting_message
            case "/confirm_input":
                return self.bot.confirmed_input_message
            case "/unconfirm_input":
                return self.bot.unconfirmed_input_message
        raise NotImplementedError


class TelegramUpdateService:
    def __init__(self, update: Update, bot: TelegramBot):
        self.update = update
        self.bot = bot

    def process(self):
        response = ""
        processor = self._get_processor()
        if self.update.edited_message:
            response = f"{self.bot.edited_message_response}\n\n"
        else:
            processor.process()
        response += processor.prepare_response()
        self._send_response(response)

    def _get_processor(self) -> TelegramUpdateProcessor:
        return TelegramUpdateProcessor(self.update, self.bot)

    def _send_response(self, response):
        raise NotImplementedError()
