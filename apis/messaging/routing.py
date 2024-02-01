from django.urls import path
from .consumers import ChatConsumer, GroupChatConsumer

# ENDPOINT FOR FRONTEND TO USE

websocket_urlpatterns = [
    path('ws/chat/<str:other_user>/<str:user_id>/', ChatConsumer.as_asgi()),
    path('ws/group/<str:group_id>/<str:user_id>/', GroupChatConsumer.as_asgi()),
] 