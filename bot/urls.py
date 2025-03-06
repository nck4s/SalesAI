from django.urls import path
from .views import get_chats
from bot.views import send_telegram_message

urlpatterns = [
    path('chats/', get_chats),
    path("send-message/", send_telegram_message, name="send-message"),
]
