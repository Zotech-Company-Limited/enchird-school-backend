from .models import Course
from apis.users.models import User
from rest_framework import serializers
from apis.users.serializers import UserSerializer




class CourseSerializer(serializers.ModelSerializer):
    
    instructors = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all().filter(
            is_deleted=False,
            is_a_teacher=True
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True,
        write_only=True
    )
    instructor_details = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_code', 'course_title', 'description', 'instructors',
                    'instructor_details', 'prerequisites', 'class_schedule', 'location', 'course_materials', 
                    'learning_objectives', 'assessment_and_grading', 'office_hours', 'term', 
                    'credits', 'is_deleted', 'course_status', 'created_at', 'created_by']
        read_only_fields = ['id', 'course_id', 'instructor_details']

