import copy
from telegram_bot.schemas import Update
from telegram_bot.services import TelegramUpdateProcessor
from telegram_bot.tests.requests_mocks import telegram_update_mock


class TestTelegramUpdateService:
    def test_prepare_response_for_start_command_ok(
        self,
        session,
        bot,
    ):
        greetings_message = "Some greetings message."
        bot.greeting_message = greetings_message
        session.add(bot)
        session.commit()
        update = copy.deepcopy(telegram_update_mock)
        update["message"]["text"] = "/start"
        update_object = Update(**update)
        assert (
            TelegramUpdateProcessor(update_object, bot).prepare_response()
            == bot.greeting_message
        )

    def test_prepare_response_for_confirm_input_command(self, session, bot):
        confirmed_input_message = "Some confirm input message."
        bot.confirmed_input_message = confirmed_input_message
        session.add(bot)
        session.commit()
        update = copy.deepcopy(telegram_update_mock)
        update["message"]["text"] = "/confirm_input"
        update_object = Update(**update)
        assert (
            TelegramUpdateProcessor(update_object, bot).prepare_response()
            == bot.confirmed_input_message
        )

    def test_prepare_response_for_unconfirm_input_command(self, session, bot):
        unconfirmed_input_message = "Some unconfirm input message."
        bot.unconfirmed_input_message = unconfirmed_input_message
        session.add(bot)
        session.commit()
        update = copy.deepcopy(telegram_update_mock)
        update["message"]["text"] = "/unconfirm_input"
        update_object = Update(**update)
        assert (
            TelegramUpdateProcessor(update_object, bot).prepare_response()
            == bot.unconfirmed_input_message
        )
