from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FacultyViewSet, DepartmentViewSet

# Create a router
router = DefaultRouter()

# Register the FacultyViewSet
router.register(r'admin/faculty', FacultyViewSet)
router.register(r'department', DepartmentViewSet)

urlpatterns = [
    path('', include(router.urls)),
]