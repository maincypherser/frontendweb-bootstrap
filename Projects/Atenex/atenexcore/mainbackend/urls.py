from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrganizationViewSet, AgentViewSet, LogViewSet, OrgUserViewSet, PolicyViewSet

# Create a router to register your viewsets
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'agents', AgentViewSet, basename='agent')
router.register(r'logs', LogViewSet, basename='log')
router.register(r'orgusers', OrgUserViewSet, basename='orguser')
router.register(r'policies', PolicyViewSet, basename='policy')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),  # Include the router-generated URLs
]
