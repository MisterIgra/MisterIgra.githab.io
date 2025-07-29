import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from telegram.ext import Application, CommandHandler
# ==================================================
# КОНФИГУРАЦИЯ
# ==================================================
TOKEN = "8352098356:AAHS4ceBu0-ryWKv5HInp300pSMyIK0oWI0"
PORT = 8080
HOST = "0.0.0.0"

# Используйте один из вариантов:
# 1. Для localtunnel: https://pixelbid.loca.lt
# 2. Для Serveo: https://pixelbid.serveo.net
# 3. Для GitHub Pages: https://ваш_логин.github.io/pixelbid-editor
PUBLIC_URL = "https://MisterIgra.github.io/pixelbid-editor"  # ЗАМЕНИТЕ НА РЕАЛЬНЫЙ URL

# ==================================================
# ВСТРОЕННОЕ ВЕБ-ПРИЛОЖЕНИЕ
# ==================================================
# HTML_EDITOR остается без изменений (как в предыдущем коде)
# ...
HTML_EDITOR = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>PixelBid Editor</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        h1 { text-align: center; margin-bottom: 20px; color: #333; }
        #canvas { 
            display: grid; 
            grid-template-columns: repeat(16, 20px);
            gap: 1px; 
            margin: 0 auto 20px;
            width: fit-content;
        }
        .pixel { 
            width: 20px; 
            height: 20px; 
            border: 1px solid #ddd;
            cursor: pointer;
            background: white;
        }
        .controls { 
            text-align: center; 
            margin: 20px 0; 
        }
        button { 
            padding: 10px 20px; 
            background: #007bff; 
            color: white; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer;
            font-size: 16px;
        }
        button:hover { background: #0069d9; }
    </style>
</head>
<body>
    <h1>🎨 PixelBid Editor</h1>
    
    <div class="controls">
        <button onclick="clearCanvas()">Очистить</button>
        <button onclick="saveArt()">Сохранить арт</button>
    </div>
    
    <div id="canvas"></div>
    
    <script>
        // Инициализация редактора
        function initEditor() {
            const canvas = document.getElementById('canvas');
            
            // Создаем сетку 16x16 пикселей
            for (let i = 0; i < 256; i++) {
                const pixel = document.createElement('div');
                pixel.className = 'pixel';
                pixel.addEventListener('click', () => {
                    pixel.style.backgroundColor = 'black';
                });
                canvas.appendChild(pixel);
            }
        }
        
        // Очистка холста
        function clearCanvas() {
            document.querySelectorAll('.pixel').forEach(pixel => {
                pixel.style.backgroundColor = '';
            });
        }
        
        // Сохранение арта
        function saveArt() {
            const pixels = [];
            document.querySelectorAll('.pixel').forEach(pixel => {
                pixels.push(pixel.style.backgroundColor || '');
            });
            
            Telegram.WebApp.sendData(JSON.stringify(pixels));
            Telegram.WebApp.close();
        }
        
        // Запуск при загрузке
        window.onload = initEditor;
    </script>
</body>
</html>
"""

# Веб-сервер для мини-приложения
class WebAppHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(HTML_EDITOR.encode('utf-8'))

# ==================================================
# ТЕЛЕГРАМ БОТ
# ==================================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(
            "🎨 Открыть редактор", 
            web_app=WebAppInfo(url=PUBLIC_URL)  # Используем постоянный URL
        )]
    ]
    
    await update.message.reply_text(
        f"👋 Привет, {update.effective_user.first_name}!\n"
        "Добро пожаловать в PixelBid - аукцион пиксельного искусства!\n\n"
        "Нажми кнопку ниже, чтобы начать рисовать:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# Остальной код без изменений
# ...




async def start(update, context):
    await update.message.reply_text("✅ Бот работает!")

def main():
    print("🔍 Проверка подключения...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    
    print("🚀 Бот запущен! Напишите /start в Telegram")
    app.run_polling()

if __name__ == "__main__":
    main()