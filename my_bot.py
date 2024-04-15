import os
import logging


import validators
from telegram import ForceReply, Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from config import Setting
from download_by_tiqu import TiQuRequest

# add vpn support

os.environ['http_proxy'] = "http://127.0.0.1:7890"
os.environ['https_proxy'] = "http://127.0.0.1:7890"
os.environ['all_proxy'] = "http://127.0.0.1:7890"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Send me a instagram share link!")


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # 1. check the link valid
    link = update.message.text.strip()
    is_valid_link = validators.url(link)
    if not is_valid_link:
        await update.message.reply_text("Invalid link!(你输入的instagram链接有误，请重新输入)")
        return
    # 2. get the url
    media_getter = TiQuRequest()
    # asyncio.create_task(update.message.reply_text("Please wait..."))
    try:
        media_lst = media_getter.get_medias(link)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("Sorry, Please try again later.")
        return
    # 3. reply
    await update.message.reply_media_group(media=media_lst)
    # await update.message.reply_photo(photo=url)
    # await update.message.reply_document(document=url)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(Setting.TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
