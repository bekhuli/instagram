from rest_framework import serializers
from .models import Post, PostMedia, Comment, Reply


class PostMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostMedia
        fields = ('file', )


class PostSerializer(serializers.ModelSerializer):
    media = PostMediaSerializer(many=True, read_only=True)
    uploaded_files = serializers.ListField(child=serializers.FileField(), write_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)
    liked = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ("id", "author", "nickname", "avatar", "description", "created_at", "media", "uploaded_files", "likes_count", "liked")
        read_only_fields = ('author', )

    def validate_upload_files(self, value):
        if not value:
            raise serializers.ValidationError("At least one image or video is required.")
        return value

    def create(self, validated_data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            validated_data["author"] = request.user
        else:
            raise serializers.ValidationError({"author": "User must be authenticated."})

        uploaded_files = validated_data.pop('uploaded_files', [])
        if not uploaded_files:
            raise serializers.ValidationError({"uploaded_files": "At least one image or video is required."})

        post = Post.objects.create(**validated_data)

        for file in uploaded_files:
            PostMedia.objects.create(post=post, file=file)

        return post

    def get_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.likes.all()
        return False


    def get_nickname(self, obj):
        if obj.author.username:
            return obj.author.username
        return None

    def get_avatar(self, obj):
        if obj.author.profile.avatar:
            return obj.author.profile.avatar.url
        return None


class CommentSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ("id", "post", "user_id", "user", "avatar", "text", "created_at")
        read_only_fields = ("id", "post", "user_id", "avatar", "user", "created_at")

    def get_avatar(self, obj):
        if obj.user.profile.avatar:
            return obj.user.profile.avatar.url
        return None


class ReplySerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ("id", "comment", "user_id", "user", "avatar", "text", "created_at")
        read_only_fields = ("id", "comment", "user_id", "user", "avatar", "created_at")

    def get_avatar(self, obj):
        if obj.user.profile.avatar:
            return obj.user.profile.avatar.url
        return None