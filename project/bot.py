import os
import logging
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackContext
from links_extraction import  form_url,form_recent_event_link, form_upcoming_event_link


# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Set a higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

PROMOTION, COMMAND = range(2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the conversation and asks the user about the promotion they want to get info about"""
    reply_variants = [['UFC', 'PFL', 'ONE_FC']]

    message = "Hi there! I'm YourMMAnewsBot!"
    follow_up_message = "First, choose the promotion name you want to get information about."
    
    # Corrected line: using ReplyKeyboardMarkup to create a custom keyboard
    reply_markup = ReplyKeyboardMarkup(reply_variants, one_time_keyboard=True)
  
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message)
    # Corrected line: passing reply_markup to include the custom keyboard
    await update.message.reply_text(text=follow_up_message, reply_markup=reply_markup)
    

# Define a callback function to handle the user's response
async def handle_promotion_choice(update: Update, context: CallbackContext):
    user_response = update.message.text  # Get the text of the selected option
    chat_id = update.effective_chat.id

    # Now you can use user_response and chat_id as needed
    # For example, you might want to continue the conversation based on the user's choice

    await context.bot.send_message(chat_id=chat_id, text=f"To get the link to the recent {user_response} events, send /last ")
    await context.bot.send_message(chat_id=chat_id, text=f"To get the link to the upcoming {user_response} events, send /next ")


async def last(update: Update, context: CallbackContext):
    user_response = update.message.text  # Get the text of the selected option
    chat_id = update.effective_chat.id
    message = "Select the event"
    
    url = form_url(user_response)
    reply_variants = [form_recent_event_link(url)]
    
    reply_markup = ReplyKeyboardMarkup(reply_variants, one_time_keyboard=True)
    await update.message.reply_text(text=message, reply_markup=reply_markup)

    


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


def main():
    TOKEN = os.environ.get("MMA_BOT_TOKEN")
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    promotion_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_promotion_choice)
    #need to handle a callback
    last_handler = CommandHandler('last', last)
    #next_handler = CommandHandler('next', next)
    unknown_handler = MessageHandler(filters.COMMAND, unknown)

    application.add_handler(start_handler)
    application.add_handler(promotion_handler)
    application.add_handler(last_handler)
    #application.add_handler(next_handler)
    application.add_handler(unknown_handler)

    application.run_polling()


if __name__ == '__main__':
    main()


    