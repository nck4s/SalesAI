import os
import json
import logging
import requests
import openai
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

load_dotenv()

# Загружаем API-ключи из .env
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env!")

if not OPENAI_API_KEY:
    raise ValueError("❌ Ошибка: OPENAI_API_KEY не найден в .env!")

# URL API Telegram
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

# Настраиваем OpenAI API
openai.api_key = OPENAI_API_KEY

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    """ Обрабатывает входящие сообщения из Telegram. """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            chat_id = data["message"]["chat"]["id"]
            message_text = data["message"]["text"]

            ai_response = get_ai_response(message_text)

            response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": ai_response})
            logger.info(f"📤 Ответ в Telegram: {response.json()}")

            return JsonResponse({"status": "ok", "response": response.json()})
        except Exception as e:
            logger.error(f"❌ Ошибка обработки Telegram Webhook: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)

def send_telegram_message(chat_id, text):
    """ Отправляет сообщение в Telegram. """
    response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
    return response.json()

def get_ai_response(message):
    """ Получает ответ от OpenAI API. """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": message}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"❌ Ошибка OpenAI API: {e}")
        return "Произошла ошибка. Попробуйте позже."
