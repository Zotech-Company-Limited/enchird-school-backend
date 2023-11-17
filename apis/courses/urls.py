from .views import CourseViewSet
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
]