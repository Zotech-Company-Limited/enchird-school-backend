from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StudentViewSet

# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]