import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from links_extraction import form_url, form_recent_event_link, form_upcoming_event_link
from promotion_links import *

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set a higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Hi there! I'm YourMMAnewsBot!"
    follow_up_last = "First, choose the promotion name you want to get information about."
    follow_up_next = "Send /ufc for UFC events, /onefc for ONE FC events, or /pfl for PFL events."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await update.message.reply_text(text=follow_up_last)
    await update.message.reply_text(text=follow_up_next)


def get_promotion_url(promotion):
    url = form_url(promotion)
    return url


async def promotion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    promotion_name = context.args[0].lower() if context.args else None
    if promotion_name:
        url = get_promotion_url(promotion_name)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f'To get the link to the most recent {promotion_name.upper()} event, send /last ')
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Please specify a promotion name.')


async def last_or_next(update: Update, context: ContextTypes.DEFAULT_TYPE, upcoming=True):
    promotion_name = context.args[0].lower() if context.args else None
    if promotion_name:
        url = get_promotion_url(promotion_name)
        link_func = form_upcoming_event_link if upcoming else form_recent_event_link
        link = link_func(url, 0)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=link)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='Please specify a promotion name.')


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await last_or_next(update, context, upcoming=False)


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await last_or_next(update, context, upcoming=True)


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    TOKEN = os.environ.get("MMA_BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    promotion_handler = CommandHandler('promotion', promotion)
    last_handler = CommandHandler('last', last)
    next_handler = CommandHandler('next', next)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(promotion_handler)
    application.add_handler(last_handler)
    application.add_handler(next_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()


    