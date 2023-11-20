from apis.users.models import User
from rest_framework import serializers
from .models import Course
from apis.users.serializers import UserSerializer
# from apis.courses.serializers import CourseSerializer




class CourseSerializer(serializers.ModelSerializer):
    
    instructors = serializers.PrimaryKeyRelatedField(
        # queryset=User.objects.all().filter(
        #     is_deleted=False,
        #     is_a_teacher=True
        # ),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True,
        read_only=True
    )
    instructor_details = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_code', 'course_title', 'description', 'instructors',
                    'instructor_details', 'prerequisites', 'class_schedule', 'location', 'course_materials', 
                    'learning_objectives', 'assessment_and_grading', 'office_hours', 'term', 
                    'credits', 'is_deleted', 'course_status', 'created_at', 'created_by', 'modified_by']
        read_only_fields = ['id', 'course_id', 'instructor_details']

    def to_representation(self, instance):
        representation = super(CourseSerializer, self).to_representation(instance)

        # Override the created_by field to only include the user's email
        representation['created_by'] = instance.created_by.email if instance.created_by else None
        representation['modified_by'] = instance.modified_by.email if instance.modified_by else None

        return representation



