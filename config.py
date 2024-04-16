import os
from dotenv import load_dotenv

load_dotenv()


class Setting:
    TOKEN = os.getenv("BOT_TOKEN", "changethis")
    use_proxy = os.getenv("USE_PROXY", "") == "True"
