import abc

from models import TelegramBot
from telegram_bot.schemas import Update


class SurveyMessagesProcessor:
    pass


class TelegramUpdateProcessorBase(abc.ABC):
    def __init__(self, update: Update):
        self.update = update

    @abc.abstractmethod
    def process(self): ...

    @abc.abstractmethod
    def prepare_response(self): ...


class TelegramMessageProcessor(TelegramUpdateProcessorBase):
    pass


class TelegramCommandProcessor(TelegramUpdateProcessorBase):
    pass


class TelegramUpdateService:
    def __init__(self, update: Update, bot: TelegramBot):
        self.update = update

    def process(self):
        processor = self._get_processor()
        processor.process()
        response = processor.prepare_response()
        self._send_response(response)

    def _get_processor(self) -> TelegramMessageProcessor | TelegramCommandProcessor:
        raise NotImplementedError()

    def _send_response(self, response):
        raise NotImplementedError()
