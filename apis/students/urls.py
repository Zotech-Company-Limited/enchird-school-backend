from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
router.register(r'student', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register_course/<str:course_id>/', register_course, name='register_course'),
    path('drop_course/<str:course_id>/', drop_course, name='drop_course'),
]