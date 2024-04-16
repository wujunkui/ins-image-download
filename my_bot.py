import asyncio
import os
import logging
from typing import Optional

import validators
from telegram import ForceReply, Update, InputMediaPhoto
from telegram.request import BaseRequest, HTTPXRequest, RequestData

from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram._utils.types import HTTPVersion, ODVInput, SocketOpt
from telegram.error import NetworkError, TimedOut

from config import Setting
from download_by_tiqu import TiQuRequest

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.INFO)

logger = logging.getLogger(__name__)

if Setting.use_proxy:
    # add vpn support
    logger.info("Use Proxy")
    os.environ['http_proxy'] = "http://127.0.0.1:7890"
    os.environ['https_proxy'] = "http://127.0.0.1:7890"
    os.environ['all_proxy'] = "http://127.0.0.1:7890"


class MyRetryRequest(HTTPXRequest):

    async def do_request(self,
                         url: str,
                         method: str,
                         request_data: Optional[RequestData] = None,
                         read_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
                         write_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
                         connect_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE,
                         pool_timeout: ODVInput[float] = BaseRequest.DEFAULT_NONE, ):
        retry_times = 5
        delay = 1
        for i in range(retry_times):
            logger.info(f'retry times: {i}')
            try:
                return await super().do_request(url, method, request_data, read_timeout, write_timeout, connect_timeout,
                                                pool_timeout)
            except NetworkError:
                await asyncio.sleep(delay)


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

    application = Application.builder().token(Setting.TOKEN).get_updates_connection_pool_size(
        10).get_updates_pool_timeout(30).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e. message - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
