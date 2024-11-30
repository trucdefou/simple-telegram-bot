import datetime
import logging
from telegram import Update
from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
DEADLINE_DATE = datetime.date(2024, 12, 30)
def days_remaining():
    today = datetime.date.today()
    remaining = (DEADLINE_DATE - today).days
    return max(remaining, 0)

async def get_account(update: Update, context: CallbackContext):
    message = "Estado de cuenta:\n"
    message = f"<b>Resumen de estado de cuenta</b>\n"
    logging.info("Counter sent.")
    keyboard = [[InlineKeyboardButton("Volver al Inicio", callback_data="home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)
    