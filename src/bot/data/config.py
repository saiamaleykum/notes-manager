import os

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN: str = os.environ.get("BOT_TOKEN")

USE_WEBHOOK: bool = os.environ.get("USE_WEBHOOK", False)

if USE_WEBHOOK:
    pass
