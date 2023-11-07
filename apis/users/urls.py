from django.urls import path
from apis.users.views import *
from apis.users.login import *
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .logout import Logout
from .login import LoginView
from knox import views as knox_views


# Create a router
router = DefaultRouter()

# Register the ProductViewSet with a base name 'product'
# router.register(r'login', CustomTokenObtainPairView.as_view(), basename="login")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', LoginView.as_view(), name='Login'),
    path('auth/logout/', knox_views.LogoutView.as_view(), name='Logout'),
    path('auth/logoutall/', knox_views.LogoutAllView.as_view(), name="Logout all sessions"),
]