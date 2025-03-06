import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

TOKEN = "your_telegram_bot_token"
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

@csrf_exempt
def send_telegram_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
        chat_id = data.get("chat_id")
        message = data.get("message")

        if chat_id and message:
            response = requests.post(
                TELEGRAM_API_URL,
                json={"chat_id": chat_id, "text": message}
            )
            return JsonResponse(response.json())
    
    return JsonResponse({"error": "Invalid request"}, status=400)

from django.http import JsonResponse

def get_chats(request):
    sample_chats = [
        {"id": 1, "user": "Alice", "message": "Привет!"},
        {"id": 2, "user": "Bob", "message": "Как дела?"}
    ]
    return JsonResponse(sample_chats, safe=False)
