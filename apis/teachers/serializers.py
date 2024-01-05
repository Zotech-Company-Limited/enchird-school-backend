from apis.users.models import User
from rest_framework import serializers
from apis.courses.models import Course
from apis.faculty.models import Faculty
from apis.teachers.models import Teacher
from apis.users.serializers import UserSerializer
from apis.faculty.serializers import FacultySerializer
from drf_writable_nested import WritableNestedModelSerializer



class TeacherSerializer(WritableNestedModelSerializer):

    user = UserSerializer(read_only=True)
    courses = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        many=True,
        # read_only=True
    )
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )
    faculty_details = FacultySerializer(source='faculty', read_only=True)

    class Meta:

        model = Teacher
        fields = ['user', 'teacher_id', 'highest_degree', 'about', 'description', 
                  'courses', 'faculty', 'faculty_details', 'is_deleted', 'created_at']
        read_only_fields = ['user', 'teacher_id', 'faculty_details']



