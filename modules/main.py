from functools import wraps
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler, CallbackContext
from static.const import get_allowed_users
def restricted(func):
    @wraps(func)
    async def wrapped(update, context, *args, **kwargs):
        username = update.effective_user.username
        if not username:
            print("Unauthorized access denied for an unknown user.")
            return None
        if username not in get_allowed_users():
            print(f"Unauthorized access denied for {username}.")
            return None
        return await func(update, context, *args, **kwargs)
    return wrapped

@restricted
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
    Bienvenido a Araitek Telegram Bot

    Opciones:    """
    keyboard = [
        [InlineKeyboardButton("Ver estado de cuenta", callback_data="1")],
        [InlineKeyboardButton("Ver Lista", callback_data="2")],
        [InlineKeyboardButton("Agregar a la lista", callback_data="3")],
        [InlineKeyboardButton("Eliminar de la lista", callback_data="4")],
        [InlineKeyboardButton("Ver Recordatorios", callback_data="5")],
        [InlineKeyboardButton("Agregar al recordatorio", callback_data="6")],
        [InlineKeyboardButton("Eliminar recordatorio", callback_data="7")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(
        photo=open("static/img/mobile.png", 'rb'),  # Use the URL or file path of the image
        caption=text,  # Add the text as the caption
        reply_markup=reply_markup  # Inline keyboard with the options
    )


async def home(update: Update, context: CallbackContext):
    text = """
    Bienvenido a Araitek Telegram Bot

    Opciones:    """
    keyboard = [
        [InlineKeyboardButton("Ver estado de cuenta", callback_data="1")],
        [InlineKeyboardButton("Ver Lista", callback_data="2")],
        [InlineKeyboardButton("Agregar a la lista", callback_data="3")],
        [InlineKeyboardButton("Eliminar de la lista", callback_data="4")],
        [InlineKeyboardButton("Ver Recordatorios", callback_data="5")],
        [InlineKeyboardButton("Agregar al recordatorio", callback_data="6")],
        [InlineKeyboardButton("Eliminar recordatorio", callback_data="7")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.callback_query.message.reply_photo(
        photo=open("static/img/mobile.png", 'rb'),  # Use the URL or file path of the image
        caption=text,  # Add the text as the caption
        reply_markup=reply_markup  # Inline keyboard with the options
    )

async def cancel_conversation(update, context):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press
    await query.message.edit_text("Conversación cancelada.")
    return ConversationHandler.END