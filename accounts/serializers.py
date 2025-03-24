import re
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'username', 'first_name', 'last_name', 'avatar', 'bio', 'website')
        read_only_fields = ('username', )

    def remove_avatar(self):
        profile = self.instance
        if profile.avatar.name != "avatars/default_avatar.jpg":
            profile.avatar.delete(save=False)
            profile.avatar = "avatars/default_avatar.jpg"
            profile.save(update_fields=["avatar"])


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_username(self, value):
        value = value.lower()

        if len(value) > 30:
            raise serializers.ValidationError("Username cannot exceed 30 characters.")

        if not re.match(r'^[a-z0-9_]+$', value):
            raise serializers.ValidationError("Username can only contain lowercase Latin letters, numbers, and underscores.")

        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Password must match!")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        return user
