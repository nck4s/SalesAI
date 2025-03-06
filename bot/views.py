import os
import json
import logging
import requests
from dotenv import load_dotenv
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ChatMessage


load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


if not TELEGRAM_BOT_TOKEN:
    raise ValueError("❌ Ошибка: TELEGRAM_BOT_TOKEN не найден в .env!")

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            logger.info(f"📩 Получено сообщение от Telegram: {data}")
            print(f"📩 Получено сообщение от Telegram: {data}")

            chat_id = data["message"]["chat"]["id"]
            message_text = data["message"]["text"]

            response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": f"Вы сказали: {message_text}"})
            logger.info(f"📤 Ответ в Telegram: {response.json()}")
            print(f"📤 Ответ в Telegram: {response.json()}")

            return JsonResponse({"status": "ok"})
        except Exception as e:
            logger.error(f"❌ Ошибка обработки Telegram Webhook: {e}")
            print(f"❌ Ошибка обработки Telegram Webhook: {e}")
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request"}, status=400)


def get_chats(request):
    chats = ChatMessage.objects.order_by("-created_at").values("id", "user", "message")
    return JsonResponse(list(chats), safe=False)

def send_telegram_message(chat_id, text):
    response = requests.post(TELEGRAM_API_URL, json={"chat_id": chat_id, "text": text})
    return response.json()
