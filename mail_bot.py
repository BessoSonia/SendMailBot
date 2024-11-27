from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
import os
import re
import smtplib
from email.mime.text import MIMEText

# Загрузка переменных окружения
API_KEY = os.getenv("API_KEY")  # Токен Telegram-бота
SMTP_SERVER = os.getenv("SMTP_SERVER")  # SMTP-сервер
SMTP_PORT = os.getenv("SMTP_PORT")  # Порт SMTP
SMTP_USERNAME = os.getenv("SMTP_USERNAME")  # Имя пользователя SMTP
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")  # Пароль SMTP

EMAIL, MESSAGE = range(2)  # Состояния бота


# Проверка email
def is_valid_email(email):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email)

# Отправка письма через SMTP
def send_email(email, message_text):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.yandex.ru")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    msg = MIMEText(message_text)
    msg["Subject"] = "Сообщение от Telegram-бота"
    msg["From"] = smtp_username
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Привет! Укажите email получателя:")
    return EMAIL


async def get_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = update.message.text
    if not is_valid_email(email):
        await update.message.reply_text("Некорректный email. Попробуйте ещё раз:")
        return EMAIL
    context.user_data["email"] = email
    await update.message.reply_text("Введите текст сообщения:")
    return MESSAGE


# Получение сообщения и отправка письма
async def get_message_and_send_email(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    email = context.user_data.get("email")
    message_text = update.message.text

    # Отправка письма
    send_email(email, message_text)

    await update.message.reply_text(f"Сообщение отправлено на {email}!")
    await update.message.reply_text("Если хотите начать снова, используйте команду /start.")
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text("Диалог завершён. Если хотите начать снова, используйте команду /start.")
    return ConversationHandler.END


def main():
    API_KEY = os.getenv("API_KEY")
    if not API_KEY:
        raise ValueError("Переменная окружения API_KEY не задана!")

    application = ApplicationBuilder().token(API_KEY).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_email)],
            MESSAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_message_and_send_email)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()
