

import json
from telegram.ext import CallbackContext, ConversationHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import sys
from static.const import get_add_to_reminder, get_delete_from_list, get_date_for_reminder, get_text_for_reminder
from modules.main import start
import datetime
import logging
sys.path.append('..')
def load_araitek_reminder():
    try:
        with open("araitek_reminder.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

        
def save_araitek_reminder(list):
    with open("araitek_reminder.json", "w") as file:
        json.dump(list, file, indent=4)

# Start the conversation (triggered by CallbackQuery or command)
async def handle_add_to_reminder_start(update: Update, context: CallbackContext):
    await update.callback_query.message.reply_text(
        "Por favor, introduce la fecha para el recordatorio (formato: DD-MM-YYYY):"
    )
    return get_date_for_reminder  # Move to the date input state

# Step 1: Get the date
async def handle_get_date(update: Update, context: CallbackContext):
    user_input = update.message.text

    # Validate the date format
    try:
        reminder_date = datetime.datetime.strptime(user_input, "%d-%m-%Y")
        context.user_data["reminder_date"] = reminder_date  # Save the date for later
        await update.message.reply_text(
            "Fecha registrada exitosamente. Ahora, introduce el texto para el recordatorio:"
        )
        return get_text_for_reminder  # Move to the text input state
    except ValueError:
        await update.message.reply_text(
            "Formato de fecha inválido. Por favor, inténtalo de nuevo (DD-MM-YYYY):"
        )
        return get_date_for_reminder  # Repeat the date input state

# Step 2: Get the reminder text
async def handle_get_text(update: Update, context: CallbackContext):
    try:
        reminder_text = update.message.text
        reminder_date = context.user_data.get("reminder_date")

        # Convert `reminder_date` to a string
        reminder_entry = {
            "date": reminder_date.strftime("%Y-%m-%d"),  # Format the date for JSON
            "text": reminder_text,
        }

        # Load and save the reminder
        araitek_reminder = load_araitek_reminder()
        araitek_reminder.append(reminder_entry)  # Append the serialized reminder
        save_araitek_reminder(araitek_reminder)

        await update.message.reply_text(
            f"Recordatorio añadido exitosamente:\n"
            f"- Fecha: {reminder_date.strftime('%d-%m-%Y')}\n"
            f"- Texto: {reminder_text}",
            parse_mode="HTML",
        )
        await start(update, context)
        return ConversationHandler.END  # End the conversation
    except Exception as e:
        await update.message.reply_text(
            f"Ha ocurrido un error: {str(e)}. Por favor, inténtalo de nuevo."
        )
        return get_text_for_reminder  # Repeat the text input state
# Cancel the conversation
async def cancel_conversation(update: Update, context: CallbackContext):
    await update.message.reply_text("Operación cancelada.")
    return ConversationHandler.END

async def araitek_reminder(update: Update, context: CallbackContext):
    araitereminder = load_araitek_reminder()
    message = "Recordatorios:\n"
    if araitereminder:
        for element in araitereminder:
            message += f"- {element}\n"
    else:
        message += "Aún no hay nada en los recordatorios"
    keyboard = [[InlineKeyboardButton("Volver al inicio", callback_data="home")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text(message, parse_mode='HTML', reply_markup=reply_markup)

async def delete_from_reminder(update: Update, context: CallbackContext):
    araitek_reminder = load_araitek_reminder()

    if not araitek_reminder:
        await update.callback_query.message.reply_text("No hay recordatorios.")
        return
    # Create the list of inline buttons for deleting items
    buttons = [
        [InlineKeyboardButton(text=str(value), callback_data=f"delete_{idx}")]
        for idx, value in enumerate(araitek_reminder)
    ]
    buttons.append([InlineKeyboardButton("❌ Cancelar", callback_data="home")])
    reply_markup = InlineKeyboardMarkup(buttons)

    await update.callback_query.message.reply_text(
        "Selecciona el elemento que deseas eliminar:",
        reply_markup=reply_markup,
    )
async def handle_delete_reminder(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    if data.startswith("delete_"):
        # Get the item name from callback data
        item_to_delete = int(data[len("delete_"):])
        # Load the list, remove the item, and save the updated list
        araitereminder = load_araitek_reminder()
        if item_to_delete < len(araitereminder):
            del araitereminder[item_to_delete]
            save_araitek_reminder(araitereminder)
            await query.message.edit_text("Elemento eliminado")
        else:
            print("item to delete!!!! ", item_to_delete)
            await query.message.edit_text("Elemento no encontrado entre los recordatorios.")
        return ConversationHandler.END  # End the conversation

async def daily_reminder(context: CallbackContext):
    try:
        tasks = load_araitek_reminder()
        today = datetime.date.today()
        message = "📅 **Recordatorios:**\n"
        has_task = False

        # Filter today's tasks and remove overdue ones
        updated_tasks = []
        for task in tasks:
            task_date = datetime.datetime.strptime(task["date"], "%Y-%m-%d").date()
            if task_date < today:
                # Skip past tasks (do not add them back to the list)
                continue
            elif task_date == today:
                # Add today's tasks to the message
                message += f"- {task['text']} (Fecha: {task_date.strftime('%d-%m-%Y')})\n"
                has_task = True
            # Add future tasks back to the updated list
            updated_tasks.append(task)

        # Save updated tasks (removing past ones)
        save_araitek_reminder(updated_tasks)

        if has_task:
            # Send the message if there are tasks for today
            chat_id = context.job.chat_id  # Retrieve `chat_id` from the job context
            await context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
            logging.info("Daily reminder sent successfully.")
        else:
            logging.info("No tasks for today. No reminder sent.")
    except Exception as e:
        logging.error(f"Error in daily reminder: {e}")