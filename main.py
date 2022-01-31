import os
import time

import requests
from dotenv import load_dotenv
from loguru import logger
from telegram import Bot


def get_last_homework_status():
    """Functions that gets homework status by url."""

    try:
        with requests.get(URL, headers=HEADERS) as response:
            js_response = response.json()
    except requests.exceptions.ConnectionError:
        pass
    else:
        homework_status = js_response["status"]
        return homework_status


def prepare_message():
    """Prepares message to telegram."""

    homework_status = get_last_homework_status()
    if homework_status == "found":
        logger.debug("Статус изменился")
        return "Домашку проверили"
    else:
        logger.debug("Статус не изменился")
        return None


def send_message():
    """Sending message if status is changed."""

    message = prepare_message()
    if message is not None:
        return bot.send_message(TELEGRAM_CHAT_ID, message)


def main():
    """Function that starts our service."""

    time.sleep(3)  # Necessary delay for sending message to telegram
    send_message()


if __name__ == "__main__":

    dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
    if os.path.exists(dotenv_path):
        load_dotenv(dotenv_path)

    DEVMAN_AUTHORISATION_TOKEN = os.environ.get("authorization_token")
    timestamp = (
        time.time()
    )  # Time point which checking begins from. Creates with program start.
    URL = "https://dvmn.org/api/long_polling/" + "?" + str(timestamp)
    HEADERS = {"Authorization": DEVMAN_AUTHORISATION_TOKEN}
    TELEGRAM_BOT_TOKEN = os.environ.get("telegram_bot_token")
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    TELEGRAM_CHAT_ID = os.environ.get("telegram_chat_id")

    while True:
        main()
