from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyViewSet

# Create a router
router = DefaultRouter()

# Register the FacultyViewSet
router.register(r'admin/faculty', FacultyViewSet)

urlpatterns = [
    path('', include(router.urls)),
]