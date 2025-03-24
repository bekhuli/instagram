from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Profile, CustomUser
from .serializers import RegisterSerializer, ProfileSerializer

USER = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer


class ProfileDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer

    def get(self, request, user_id, *args, **kwargs):
        user = get_object_or_404(CustomUser, id=user_id)
        profile = get_object_or_404(Profile, user=user)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserSearchView(generics.ListAPIView):
    queryset = Profile.objects.select_related("user").all()
    serializer_class = ProfileSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["user__username", "first_name", "last_name"]


class RemoveAvatarView(APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def delete(self, request, *args, **kwargs):
        profile = request.user.profile
        serializer = ProfileSerializer(profile)
        serializer.remove_avatar()
        return Response(
            {"message": "Avatar removed successfully.", "avatar": serializer.data["avatar"]},
            status=status.HTTP_200_OK,
        )