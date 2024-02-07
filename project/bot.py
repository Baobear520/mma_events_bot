import logging
import os, re
from dotenv import dotenv_values

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from links_extraction import form_url, form_event_links


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

PROMOTION, ACTION, LINK = range(3)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    
    reply_keyboard = [["UFC", "PFL", "ONE_FC"]]

    await update.message.reply_text(
        "Hi! My name is MMA events bot. I can show you the results of the recent MMA events and tell you about what's coming soon.\n\n "
        "Send /cancel to stop talking to me.\n\n"
        "Which promotion do you want to get news about?",
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

async def action(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ The bot will prompt users to choose one of the events.
    If there's only one event, the link to the event will be returned """
    

    user = update.message.from_user
    user_response = update.message.text
    logger.info(f"User {user.first_name} chose {user_response}.")

    global links
    links = form_event_links(url, user_response)

    if not links:
        await update.message.reply_text("Sorry, there are no events on the schedule.\nTry another promotion.")
    else:
        # If there is only one event available
        if len(links) == 1:
            link = links[0]
            logger.info(f"Directly sending the link: {link}")
            await update.message.reply_text(f"Great! Here's the link: {link}")
            return LINK

        # If there are more than 1 event and less or equal 3 available
        elif 1 < len(links) <= 3:
            reply_keyboard = [[str(i + 1) for i in range(len(links))]]

            await update.message.reply_text(
                f"Choose one of these {len(links)} events:\n"
                "\n"
                f"Hints:\nIf 'next' is chosen:\n1 - the event happening soonest,\n"
                f"2 - the event happening next,\n"
                f"3 - the event happening after the event 3 (if exists).\n"
                "\n"
                f"If 'last'is chosen:\n1 - the most recent event,\n"
                f"2 - the event before the event 1,\n"
                f"3 - the event before the event 2 (if exists).",
                reply_markup=ReplyKeyboardMarkup(
                    reply_keyboard, one_time_keyboard=True, resize_keyboard=True
                ),
            )
            return LINK
        
        #Shortening the list of links to maximum 3
        links = links[:3]
        reply_keyboard = [["1","2","3"]]

        await update.message.reply_text(
            f"Choose one of these 3 events:\n"
            "\n"
            f"Hints:\nIf 'next' is chosen:\n1 - the event happening soonest,\n"
            f"2 - the event happening next,\n"
            f"3 - the event happening after the event 3.\n"
            "\n"
            f"If 'last'is chosen:\n1 - the most recent event,\n"
            f"2 - the event before the event 1,\n"
            f"3 - the event before the event 2.",
            reply_markup=ReplyKeyboardMarkup(
                reply_keyboard, one_time_keyboard=True, resize_keyboard=True
            ),
        )
        return LINK
        
    return ConversationHandler.END  # This line ensures that the conversation ends if there's an issue

async def link(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Replies with the link to the desired event """

    if update.message.text:
        index = int(update.message.text) - 1
        link = links[index]
        logger.info(f"This '{link}' will be sent to the user")
        await update.message.reply_text(text=f"Great! Here's the link: {link}")
    else:
        # This case should not occur, but handle it just in case
        await update.message.reply_text("Sorry, there was an issue. Please try again.")


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancels and ends the conversation."""

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)

    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    
    #Load the env variables from .env file
    dir_name = os.getcwd()
    path_to_env = os.path.join(dir_name,".env")
    logger.info(f"The path to .env file is {path_to_env}")
    env = dotenv_values(path_to_env)
    logger.info(env)
    #Get the MMA_BOT_TOKEN variable
    TOKEN = env["MMA_BOT_TOKEN"]


    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Add conversation handler with the states 
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            PROMOTION: [MessageHandler(filters.Regex(re.compile("^(UFC|ONE_FC|PFL)$",re.IGNORECASE)), promotion)],
            ACTION: [CommandHandler("last",action),CommandHandler("next",action)],
            LINK: [MessageHandler(filters.Regex("^(1|2|3)$"),link)]
        },
        fallbacks=[CommandHandler("cancel", cancel),MessageHandler(filters.ALL, unknown)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()



   
