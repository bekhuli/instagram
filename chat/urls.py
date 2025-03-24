from django.urls import path
from .views import ChatHistoryView

urlpatterns = [
    path("<uuid:user_id>/history/", ChatHistoryView.as_view(), name="chat-history"),
]
