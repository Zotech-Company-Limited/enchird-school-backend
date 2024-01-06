from apis.users.models import User
from rest_framework import serializers
from .models import Course, CourseMaterial
from apis.users.serializers import UserSerializer
# from apis.courses.serializers import CourseSerializer




class CourseSerializer(serializers.ModelSerializer):
    
    instructor_details = UserSerializer(many=True, read_only=True, source='tutors') 

    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_code', 'course_title', 'description', 'faculty', #'instructors',
                    'instructor_details', 'class_schedule', 'location', 'course_level', #'course_materials', 
                    'learning_objectives', 'assessment_and_grading', 'term', 'department', 
                    'credits', 'is_deleted', 'course_status', 'created_at', 'created_by', 'modified_by']
        read_only_fields = ['id', 'course_id', 'instructor_details']

    def to_representation(self, instance):
        representation = super(CourseSerializer, self).to_representation(instance)

        # Override the created_by field to only include the user's email
        representation['created_by'] = instance.created_by.email if instance.created_by else None
        representation['modified_by'] = instance.modified_by.email if instance.modified_by else None

        return representation


class CourseMaterialSerializer(serializers.ModelSerializer):
    material_file = serializers.FileField(required=True)
    course = CourseSerializer(read_only=True)
    class Meta:
        model = CourseMaterial
        fields = ['id', 'material_file', 'description', 'course', 'uploaded_by', 'uploaded_at']

    def to_representation(self, instance):
        representation = super(CourseMaterialSerializer, self).to_representation(instance)

        # Override the course field to only include the course title
        representation['course'] = instance.course.course_title if instance.course else None

        return representation

