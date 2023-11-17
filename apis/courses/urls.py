from .views import CourseViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('assign_teacher/<int:teacher_id>/course/<str:course_id>/', assign_teacher, name='assign_teacher'),
    path('unassign_teacher/<int:teacher_id>/course/<str:course_id>/', unassign_teacher, name='unassign_teacher'),
]