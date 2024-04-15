import os
from dotenv import load_dotenv

load_dotenv()


class Setting:
    TOKEN = os.getenv("BOT_TOKEN", "changethis")
