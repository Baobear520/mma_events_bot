import logging
import os

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from links_extraction import form_url, form_recent_event_links, form_upcoming_event_links


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

PROMOTION, ACTION, LAST_EVENT, NEXT_EVENT, LINK = range(5)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["UFC", "PFL", "ONE_FC"]]

    await update.message.reply_text(
        "Hi! My name is MMA bot. I can help you to get the MMA news. "
        "Send /cancel to stop talking to me.\n\n"
        "Which promotion do you want to get info about?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return PROMOTION


async def promotion(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected promotion and asks to choose the action."""
    
    user_response = update.message.text
    logger.info("Promotion %s" , user_response)

    global url
    url = form_url(user_response)
    logger.info(f"Got the url: {url}")

    message_1 = f"To get the link to the recent {user_response} events, send /last"
    message_2 = f"To get the link to the upcoming {user_response} events, send /next"
    await update.message.reply_text(text=message_1)
    await update.message.reply_text(text=message_2)

    return ACTION

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """If user sends /last command, it promts them to choose one of 3 events"""
    user = update.message.from_user
    logger.info("User %s chose /last", user.first_name)
   
    reply_keyboard = [["1","2","3"]]

    await update.message.reply_text(
        "Choose one of these 3 events",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return LAST_EVENT


async def next(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """If user sends /next command, it promts them to choose one of 3 events"""
    user = update.message.from_user
    logger.info("User %s chose /next", user.first_name)
    
    reply_keyboard = [["1","2","3"]]

    await update.message.reply_text(
        "Choose one of these 3 events",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, resize_keyboard=True
        ),
    )

    return NEXT_EVENT


async def last_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Replies with the link to desired event """

    links = form_recent_event_links(url)

    if type(links) == list:
        if update.message.text == "1":
            link = links[0]
        elif update.message.text == "2":
            link = links[1]
        else: 
            link = links[2]

        logger.info(f"Got the links to events")

        await update.message.reply_text(text=f"Great! Here's the link:\n {link}")
    else:
        await update.message.reply_text("Sorry, there are no events on the schedule.")



async def next_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Prompts user to choose one of the events."""

    links = form_upcoming_event_links(url)
    if type(links) == list:
        if update.message.text == "1":
            link = links[0]
        elif update.message.text == "2":
            link = links[1]
        else: 
            link = links[2]

        logger.info(f"Got the links to events")

        await update.message.reply_text(text=f"Great! Here's the link:\n {link}")
    else:
        await update.message.reply_text("Sorry, there are no events on the schedule.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    TOKEN = os.environ.get("MMA_BOT_TOKEN")
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PROMOTION: [MessageHandler(filters.Regex("^(UFC|ONE_FC|PFL)$"), promotion)],
            ACTION: [CommandHandler("last",last),CommandHandler("next",next)],
            LAST_EVENT: [MessageHandler(filters.TEXT, last_event)],
            NEXT_EVENT: [MessageHandler(filters.TEXT, next_event)]
        },
        fallbacks=[CommandHandler("cancel", cancel),MessageHandler(filters.COMMAND, unknown)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()



   
