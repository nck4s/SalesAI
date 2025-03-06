from django.urls import path
from .views import get_chats

urlpatterns = [
    path('chats/', get_chats),
]
