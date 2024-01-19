from apis.faculty.models import *
from apis.users.models import User
from rest_framework import serializers
from apis.faculty.serializers import *
from apis.users.serializers import UserSerializer
from .models import Course, CourseMaterial, Message, ChatGroup
# from apis.courses.serializers import CourseSerializer




class CourseSerializer(serializers.ModelSerializer):
    
    instructor_details = UserSerializer(many=True, read_only=True, source='tutors') 
    faculty_details = serializers.SerializerMethodField(read_only=True)
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )
    department_details = serializers.SerializerMethodField(read_only=True)
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Course
        fields = ['id', 'course_id', 'course_code', 'course_title', 'faculty_details', 
                    'faculty', 'instructor_details', 'class_schedule', 'description', #'course_materials', 
                    'course_level', 'term', 'department', 'department_details', 'location', 'credits',
                    'is_deleted', 'course_status', 'created_at', 'created_by', 'modified_by']
        read_only_fields = ['id', 'course_id', 'instructor_details'] 

    def get_faculty_details(self, obj):
        faculty = obj.faculty
        if faculty:
            return FacultySerializer(faculty).data
        return None
    
    def get_department_details(self, obj):
        department = obj.department
        if department:
            return DepartmentSerializer(department).data
        return None

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


class ChatGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGroup
        fields = ['id', 'name', 'course', 'code']
        read_only_fields = ['code']
        

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    group = serializers.PrimaryKeyRelatedField(
        queryset=ChatGroup.objects.all(), 
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )
    group_info = serializers.SerializerMethodField(read_only=True)
    response_to_info = serializers.SerializerMethodField(read_only=True)
    # group_info = ChatGroupSerializer(read_only=True)
    
    class Meta:
        model = Message
        fields = ['id', 'content', 'sender', 'group_info', 'group', 'attachment', 'response_to', 'response_to_info', 'timestamp']
        read_only_fields = ['sender', 'response_to_info']
        write_only_fields = ['response_to']

    def get_group_info(self, obj):
        group = obj.group
        if group:
            return ChatGroupSerializer(group).data
        return None 
    
    def get_response_to_info(self, obj):
        response_to = obj.response_to
        if response_to:
            return self.__class__(response_to).data
        return None

