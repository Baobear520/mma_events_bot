import os
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes
from news_api import get_last_and_next

#Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = "Hi there! I'm YourMMAnewsBot!"
    follow_up_last = "To get the link with the most recent UFC event results, send /last."
    follow_up_next = "To get the link to the upcoming event, send /next."
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    await update.message.reply_text(text=follow_up_last)
    await update.message.reply_text(text=follow_up_next)

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = last
    await context.bot.send_message(chat_id=update.effective_chat.id, text=url)

async def next(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = next
    await context.bot.send_message(chat_id=update.effective_chat.id, text=url)

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")



if __name__ == '__main__':

    TOKEN = os.environ.get("MMA_BOT_TOKEN")
    next, last = get_last_and_next()

    application = ApplicationBuilder().token(TOKEN).build()
    
    start_handler = CommandHandler('start', start)
    
    last_handler = CommandHandler('last', last)
    next_handler = CommandHandler('next', next)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)
    

    application.add_handler(start_handler)
  
    application.add_handler(last_handler)
    application.add_handler(next_handler)
    application.add_handler(unknown_handler)
    
    application.run_polling()