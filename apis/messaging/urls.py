from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
# router.register(r'course', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('send-direct-message/<int:receiver_id>/', send_direct_message, name='send_direct_message'),
    path('groups/<int:group_id>/messages/', MessageListAPIView.as_view(), name='message-list'),
    path('courses/<int:course_id>/create-group/', create_group, name='create_group'),
    path('groups/<int:group_id>/send-message/', send_message, name='send_message'),
    path('messages/<int:user_id>/', list_user_messages, name='list_user_messages'),
    path('inbox/', inbox_messages, name='inbox_messages'),
    path('join-group/', join_group, name='join_group'),
]