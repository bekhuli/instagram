from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import RegisterView, ProfileDetailView, UserProfileView, RemoveAvatarView, UserSearchView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('my_profile/', ProfileDetailView.as_view(), name='my-profile-detail'),
    path('profile/<uuid:user_id>/', UserProfileView.as_view(), name='user-profile'),
    path('profile/remove_avatar/', RemoveAvatarView.as_view(), name='remove-avatar'),
    path('search_users/', UserSearchView.as_view(), name='search-users'),


    path('token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
]