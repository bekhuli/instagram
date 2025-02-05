from django.urls import path
from .views import RegisterView, ProfileDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('my_profile/', ProfileDetailView.as_view(), name='my-profile-detail'),
]