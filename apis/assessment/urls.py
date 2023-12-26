from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router
router = DefaultRouter()

# Register the StudentViewSet with a base name 'student'
# router.register(r'assessment', StudentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_assessment/', create_assessment, name='create_assessment'),
    path('assessments/<int:assessment_id>/', get_assessment_details, name='get_assessment'),
    path('assessments/<int:assessment_id>/add_question/', create_question_with_choices, name='add_question'),
    path('assessment-results/<int:assessment_id>/', get_assessment_results, name='get_assessment_results'),
    path('assessments/<int:assessment_id>/submit/', submit_assessment_responses, name='submit_assessment_responses'),
]