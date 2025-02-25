import argparse
import os
import requests
from loguru import logger
from starlette import status


def set_webhook(webhook_base: str):
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    webhook = webhook_base + "/telegram_bot/webhook/"
    response = requests.post(
        url=f"https://api.telegram.org/bot{token}/setWebhook", data={"url": webhook}
    )
    if response.status_code == status.HTTP_200_OK:
        if response.json()["ok"] is True:
            logger.info("Webhook set successfully.")
        else:
            logger.exception(f"Failed to set webhook: {response.json()}")
    else:
        logger.exception(f"Failed to set webhook: {response.json()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("webhook_base", help="webhook url")
    args = parser.parse_args()
    logger.info("Starting webhook setting.")
    set_webhook(args.webhook_base)
    logger.info("Finishing webhook setting.")
