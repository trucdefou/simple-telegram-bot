

import json
from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import sys
from static.const import get_add_to_list, get_delete_from_list
from modules.main import start
sys.path.append('..')
def load_araitek_list():
    try:
        with open("araitek_list.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

        
def save_araitek_list(list):
    with open("araitek_list.json", "w") as file:
        json.dump(list, file, indent=4)

async def handle_add_to_list(update: Update, context: CallbackContext):
    
    try:
        user_input = update.message.text
        araitek_list = load_araitek_list()
        araitek_list.append(user_input)
        save_araitek_list(araitek_list)
        await update.message.reply_text(
            f"Elemento añadido exitosamente:\n"
            f"- {user_input}",
            parse_mode="HTML",
        )
        await start(update, context)
        return ConversationHandler.END  # End the conversation
    except Exception as e:
        await update.reply_text(
            f"Ha ocurrido un error: {str(e)}. Por favor, inténtalo de nuevo."
        )
        return get_add_to_list


async def araitek_list(update: Update, context: CallbackContext):
    araiteklist = load_araitek_list()
    message = "Lista de cosas:\n"
    if araiteklist:
        for element in araiteklist:
            message += f"- {element}\n"
    else:
        message += "Aún no hay nada en la lista"
    keyboard = [[InlineKeyboardButton("Volver al inicio", callback_data="home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def delete_from_list(update: Update, context: CallbackContext):
    araitek_list = load_araitek_list()

    if not araitek_list:
        await update.callback_query.message.reply_text("La lista está vacía.")
        return

    # Create the list of inline buttons for deleting items
    buttons = [
        [InlineKeyboardButton(text=value, callback_data=f"delete_{idx}")]
        for idx, value in enumerate(araitek_list)
    ]
    buttons.append([InlineKeyboardButton("❌ Cancelar", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(buttons)
    
    await update.callback_query.message.reply_text(
        "Selecciona el elemento que deseas eliminar:",
        reply_markup=reply_markup,
    )

async def handle_delete(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.startswith("delete_"):
        # Get the item name from callback data
        item_to_delete = int(data[len("delete_"):])
        # Load the list, remove the item, and save the updated list
        araiteklist = load_araitek_list()
        if item_to_delete < len(araiteklist):
            del araiteklist[item_to_delete]
            save_araitek_list(araiteklist)
            await query.message.edit_text("Elemento eliminado")
        else:
            print("item to delete!!!! ", item_to_delete)
            await query.message.edit_text("Elemento no encontrado en la lista.")
        return ConversationHandler.END  # End the conversation
