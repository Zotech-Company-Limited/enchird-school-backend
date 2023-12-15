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
    path('registered_courses/', get_registered_courses, name='get_registered_courses'),
    path('view_course_materials/<str:course_id>/', view_course_materials, name='view_course_materials'),
    path('admin/accept-application/', StudentViewSet.as_view({'post': 'accept'}), name='accept_application'),
    path('admin/reject-application/', StudentViewSet.as_view({'post': 'reject'}), name='reject_application'),
]