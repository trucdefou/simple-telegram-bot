from telegram.ext import ContextTypes, CallbackContext, ConversationHandler
from modules.account import get_account
from modules.araitek_list import araitek_list, delete_from_list, handle_delete
from modules.araitek_reminder import araitek_reminder, delete_from_reminder, handle_delete_reminder, load_araitek_reminder
from static.const import get_add_to_list, get_add_to_reminder
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from modules.araitek_list import load_araitek_list
from modules.main import start, home, cancel_conversation
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    araiteklist = load_araitek_list()
    araitekreminder = load_araitek_reminder()
    query = update.callback_query
    await query.answer()
    if query.data == "1":
        await get_account(update, context)
    elif query.data == "2":
        await araitek_list(update, context)
    elif query.data == "3":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # Correctly fetches the chat ID
        text="Por favor, escribe el elemento de la lista.\n"
             "Ejemplo: <b>Ver adhesion para evento</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_conversation")]
    ])
        )
        return get_add_to_list
    elif query.data == "4":
        await delete_from_list(update, context)
    elif query.data == "5":
        await araitek_reminder(update, context)
    elif query.data == "6":
        await context.bot.send_message(
            chat_id=update.effective_chat.id,  # Correctly fetches the chat ID
        text="Por favor, escribe el elemento en recordatorios.\n"
             "Ejemplo: <b>Cena de fin de año</b>",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("❌ Cancelar", callback_data="cancel_conversation")]
    ])
        )
        return get_add_to_reminder
    elif query.data == "7":
        await delete_from_reminder(update, context)
    elif query.data == "home":
        await home(update, context)
    elif query.data == "cancel_conversation":
        await cancel_conversation(update, context)
    for idx, value in enumerate(araiteklist):
        if query.data == f"delete_{idx}":
            await handle_delete(update, context)
    for idx, value in enumerate(araitekreminder):
        if query.data == f"delete_{idx}":
            await handle_delete_reminder(update, context)
    
            
            
