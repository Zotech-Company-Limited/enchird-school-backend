from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

# Create a router
router = DefaultRouter()

# Register the GradeSystemViewSet
router.register(r'grade-system', GradeSystemViewSet)
# router.register(r'courses/student/grades', CourseGradeViewSet, basename='course-grades')


urlpatterns = [
    path('', include(router.urls)),
    path('create_assessment/', create_assessment, name='create_assessment'),
    path('assessments/<int:assessment_id>/', get_assessment_details, name='get_assessment'),
    path('courses/<int:course_id>/student/grades', calculate_student_grade, name='student-course-grade'),
    path('assessments/<int:assessment_id>/add_question/', create_question_with_choices, name='add_question'),
    path('assessment-results/<int:assessment_id>/', get_assessment_results, name='get_assessment_results'),
    path('assessments/<int:assessment_id>/submit/', submit_assessment_responses, name='submit_assessment_responses'),
]