import json
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логов
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "8352098356:AAHS4ceBu0-ryWKv5HInp300pSMyIK0oWI0"  # Замените на ваш реальный токен

# URL вашего мини-приложения (позже замените на реальный)
WEB_APP_URL = "https://MisterIgra.github.io/pixelbid-editor"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отправляем сообщение с кнопкой для открытия мини-приложения"""
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Открыть редактор", 
            web_app=WebAppInfo(url=WEB_APP_URL)
        )]
    ]
    
    await update.message.reply_text(
        f"👋 Привет, {update.effective_user.first_name}!\n\n"
        "Добро пожаловать в PixelBid - аукцион пиксельного искусства!\n\n"
        "Нажми кнопку ниже, чтобы начать рисовать:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатываем данные из мини-приложения"""
    try:
        # Получаем данные из веб-приложения
        data = json.loads(update.effective_message.web_app_data.data)
        
        # Простая обработка: считаем количество закрашенных пикселей
        pixel_count = sum(1 for color in data if color != '')
        
        await update.message.reply_text(
            f"🎉 Ваш арт сохранен!\n"
            f"Закрашено пикселей: {pixel_count}/256\n\n"
            "Скоро вы сможете выставить его на аукцион!"
        )
    except Exception as e:
        logger.error(f"Ошибка обработки данных: {e}")
        await update.message.reply_text("❌ Произошла ошибка при сохранении арта")

def main():
    app = Application.builder().token(TOKEN).build()
    
    # Регистрируем обработчики
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_web_app_data))
    
    logger.info("Бот запущен! Напишите /start в Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()