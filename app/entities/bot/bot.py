import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, ContextTypes
from app.entities.tasks.controller import Task
from dotenv import load_dotenv


def delete_task(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    try:
        task_index = int(context.args[0]) - 1  # Индексация начинается с 0
    except (IndexError, ValueError):
        update.message.reply_text(
            "Пожалуйста, укажите корректный номер задачи для удаления. Используйте команду /list для просмотра номеров задач.")
        return

    success, message = Task.delete_task(user_id, task_index)
    update.message.reply_text(message)


class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        self.updater = Updater(token=self.token, use_context=True)
        self.dispatcher = self.updater.dispatcher

    def start(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Привет! Я бот для управления задачами. Используй /add для добавления задачи, /list для просмотра задач и /delete для удаления.")

    # Команда /help
    def help_command(self, update: Update, context: CallbackContext):
        update.message.reply_text(
            "Команды:\n/add - добавить задачу\n/list - показать список задач\n/delete - удалить задачу\n/clear - очистить список задач")

    # Команда для добавления задачи
    def add_task(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id
        task_desc = " ".join(context.args)

        if not task_desc:
            update.message.reply_text("Пожалуйста, укажите задачу после команды /add")
            return

        success, message = Task.add_task(user_id, task_desc)
        update.message.reply_text(message)

    # Команда для вывода списка задач
    def list_tasks(self, update: Update, context: CallbackContext):
        user_id = update.message.from_user.id

        tasks = Task.get_tasks(user_id)

        if not tasks:
            update.message.reply_text("У вас нет задач.")
            return

        task_list = "\n".join(f"{i + 1}. {task.description}" for i, task in enumerate(tasks))
        update.message.reply_text(f"Ваши задачи:\n{task_list}")

    # Команда для удаления задачи

    def clear(self, update: Update, context: CallbackContext) -> None:
        Task.clear_tasks()
        update.message.reply_text('Все задачи очищены.')

    def run(self):
        """Запуск бота."""
        self.dispatcher.add_handler(CommandHandler("start", self.start))
        self.dispatcher.add_handler(CommandHandler("add", self.add_task))
        self.dispatcher.add_handler(CommandHandler("list", self.list_tasks))
        self.dispatcher.add_handler(CommandHandler("delete", delete_task))
        self.dispatcher.add_handler(CommandHandler("clear", self.clear))

        self.updater.start_polling()
        self.updater.idle()