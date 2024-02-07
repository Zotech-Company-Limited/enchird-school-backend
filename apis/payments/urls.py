from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *


# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
# router.register(r'student/checkout/', StripeCheckoutSession, basename='checkout_session')
# router.register(r'student/checkout/', StripeCheckoutSession)

urlpatterns = [
    # path('', include(router.urls)),
    path('checkout/', StripeCheckoutSession.as_view(), name='checkout_session'),
    path('webhook/', stripe_webhook_view, name='stripe-webhook'),
    path('student-payments/', successful_payments, name='student-payments'),
]