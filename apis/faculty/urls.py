from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router
router = DefaultRouter()

# Register the FacultyViewSet
router.register(r'admin/faculty', FacultyViewSet)
router.register(r'department', DepartmentViewSet)
router.register(r'admin/faculty-member', FacultyMemberViewSet)

urlpatterns = [
    path('', include(router.urls)),
]