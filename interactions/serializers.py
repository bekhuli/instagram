from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'sender', 'post', 'message', 'is_read', 'created_at']