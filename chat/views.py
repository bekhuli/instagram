from django.contrib.messages.storage.cookie import MessageSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import CustomUser
from chat.models import ChatRoom, Message


class ChatHistoryView(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, user_id):
        user1 = request.user
        user2 = CustomUser.objects.get(id=user_id)

        room = ChatRoom.objects.filter(
            user1=min(user1, user2, key=lambda x: x.id),
            user2=max(user1, user2, key=lambda x: x.id),
        ).first()

        if not room:
            return Response({"message": []})

        messages = Message.objects.filter(room=room).order_by("timestamp")
        return Response(MessageSerializer(messages, many=True).data)