from .models import *
from apis.users.models import User
from rest_framework import serializers
from apis.users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer



class FacultySerializer(WritableNestedModelSerializer):

    name = serializers.CharField(allow_null=False, required=True)
    abbrev = serializers.CharField(required=True)

    class Meta:

        model = Faculty
        fields = ['id', 'name', 'faculty_id', 'abbrev', 'description',
                  'about', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'faculty_id', 'created_at']


class DepartmentSerializer(serializers.ModelSerializer):
    # faculty = FacultySerializer()  # Nested serializer for Faculty
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )

    class Meta:
        model = Department
        fields = ['id', 'name', 'department_id', 'faculty', 'about',
                  'description', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'department_id', 'created_at']


class FacultyMemberSerializer(WritableNestedModelSerializer):

    user = UserSerializer(read_only=True)
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
    department = serializers.PrimaryKeyRelatedField(
        queryset=Department.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )
    department_details = DepartmentSerializer(source='department', read_only=True)

    class Meta:

        model = Faculty_Member
        fields = ['user', 'faculty_member_id', 'highest_degree', 'post_at_faculty', 'faculty', 'faculty_details', 'department', 'department_details', 'is_deleted', 'created_at']
        read_only_fields = ['user', 'faculty_member_id', 'faculty_details', 'department_details']





