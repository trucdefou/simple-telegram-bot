from dotenv import load_dotenv
import os
from functools import wraps
import logging
import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters, ConversationHandler

from modules.reminder import add_task, delete_task, list_tasks
from modules.araitek_list import araitek_list, handle_add_to_list, delete_from_list, handle_delete
from modules.araitek_reminder import araitek_reminder, delete_from_reminder, handle_delete_reminder, handle_add_to_reminder_start, handle_get_date, handle_get_text, daily_reminder
from modules.main import start, home, cancel_conversation

from inc import buttons
from static.const import get_add_to_list, get_allowed_users, get_add_to_reminder, get_date_for_reminder,get_text_for_reminder

load_dotenv() 
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
#Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling an update: {context.error}", exc_info=context.error)
#Check if the user is authorized
def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        username = update.effective_user.username
        if not username:
            print("Unauthorized access denied for an unknown user.")
            return None
        if username not in get_allowed_users:
            print(f"Unauthorized access denied for {username}.")
            return None
        return await func(update, context, *args, **kwargs)
    return wrapped

if __name__ == '__main__':
    token = os.getenv('TOKEN')
    application = ApplicationBuilder().token(token).build()
    # Handlers
    start_handler = CommandHandler('start', start)
    araitek_list_handler = CommandHandler('araitek_list', araitek_list)
    araitek_reminder_handler = CommandHandler('araitek_reminder', araitek_reminder)
    main_handler = CallbackQueryHandler(home, pattern="^home")
    add_to_list_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(buttons.button, pattern="^3$")],
        states={
            get_add_to_list: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add_to_list),
                              CallbackQueryHandler(cancel_conversation, pattern="^cancel_conversation$")],
            
        },
        fallbacks=[],
    )
    add_to_reminder_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(handle_add_to_reminder_start, pattern="^6$")],  # Trigger the conversation
        states={
            get_date_for_reminder: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_date)],
            get_text_for_reminder: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_get_text)],
        },
        fallbacks=[CommandHandler('cancel', cancel_conversation)],
    )
    delete_from_list_handler = CallbackQueryHandler(delete_from_list, pattern="^4$")
    delete_from_reminder_handler = CallbackQueryHandler(delete_from_reminder, pattern="^7$")
    handle_delete_handler = CallbackQueryHandler(handle_delete, pattern="^delete_")
    handle_delete_reminder_handler = CallbackQueryHandler(handle_delete_reminder, pattern="^delete_")
    

    application.add_handler(add_to_list_handler)
    application.add_handler(add_to_reminder_handler)
    # Add handlers to the application
    application.add_handler(CallbackQueryHandler(buttons.button))
    application.add_handler(start_handler)
    application.add_handler(main_handler)
    application.add_handler(araitek_list_handler)
    application.add_handler(delete_from_list_handler)
    application.add_handler(handle_delete_handler)
    application.add_handler(araitek_reminder_handler)
    application.add_handler(delete_from_reminder_handler)
    application.add_handler(handle_delete_reminder_handler)
    application.add_error_handler(error_handler)
    job_queue = application.job_queue
    chat_id = os.getenv('CHAT_ID')  # Ensure this is set in your environment variables
    job_queue.run_daily(
        daily_reminder, 
        time= datetime.time(hour=10, minute=0),  # Set the desired time (9:00 AM)
        chat_id=chat_id
    )
    #job_queue.run_daily(daily_reminder, time=datetime.time(hour=21, minute=7), chat_id=chat_id) 
    #Testing purpose, send the messge after 1 minute
    job_queue.run_once(daily_reminder, when=6, chat_id=chat_id) 
    
    application.run_polling()