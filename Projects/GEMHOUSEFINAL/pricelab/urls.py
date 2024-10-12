from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet

# Create a router to register your viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
