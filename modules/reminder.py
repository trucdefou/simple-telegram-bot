import json
from telegram.ext import CallbackContext
import datetime
from telegram import Update
import logging
def load_tasks():
    try:
        with open("tasks.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
# Save tasks to JSON file
def save_tasks(tasks):
    with open("tasks.json", "w") as file:
        json.dump(tasks, file, indent=4)
# Add task command
async def add_task(update: Update, context: CallbackContext):
    try:
        task = context.args[0]
        due_date = datetime.datetime.strptime(context.args[1], "%Y-%m-%d").date()
        tasks = load_tasks()
        tasks[task] = str(due_date)
        save_tasks(tasks)
        await update.message.reply_text(f"Task '{task}' added for {due_date}.")
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /add <task_name> <due_date YYYY-MM-DD>")
# Delete task command
async def delete_task(update: Update, context: CallbackContext):
    try:
        task_to_delete = context.args[0]
        due_date_to_delete = datetime.datetime.strptime(context.args[1], "%Y-%m-%d").date()
        tasks = load_tasks()
        # Check if the task with the specified due date exists
        if task_to_delete in tasks and tasks[task_to_delete] == str(due_date_to_delete):
            del tasks[task_to_delete]
            save_tasks(tasks)
            await update.message.reply_text(f"Task '{task_to_delete}' for {due_date_to_delete} deleted.")
        else:
            await update.message.reply_text(f"No task found with name '{task_to_delete}' for {due_date_to_delete}.")
    
    except (IndexError, ValueError):
        await update.message.reply_text("Usage: /delete <task_name> <due_date YYYY-MM-DD>")

# List all tasks command
async def list_tasks(update: Update, context: CallbackContext):
    tasks = load_tasks()
    message = "All Tasks:\n"

    if tasks:
        for task, due_date in tasks.items():
            message += f"- {task}: due {due_date}\n"
    else:
        message += "No tasks available."

    await update.message.reply_text(message)

# Daily reminder job
async def daily_reminder(context: CallbackContext):
    tasks = load_tasks()
    today = datetime.date.today()
    message = "Tasks Reminder:\n"
    has_task = False

    for task, due_date in list(tasks.items()):
        due_date = datetime.datetime.strptime(due_date, "%Y-%m-%d").date()
        if due_date < today:
            del tasks[task]  # Delete past tasks
        else:
            message += f"- {task}: due {due_date}\n"
            has_task = True
    message = "Buen día mi corazón"
    save_tasks(tasks)

    if has_task:
        # Accessing chat_id from the job context
        chat_id = context.job.chat_id
        await context.bot.send_message(chat_id=chat_id, text=message)
        logging.info("Daily reminder sent.")
    else:
        logging.info("No daily reminder sent.")