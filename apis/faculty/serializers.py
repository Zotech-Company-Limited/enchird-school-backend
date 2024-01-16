from .models import *
from apis.users.models import User
from rest_framework import serializers
from apis.users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer



class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Level
        fields = ['id', 'name']
        
        

class FacultySerializer(WritableNestedModelSerializer):

    name = serializers.CharField(allow_null=False, required=True)
    abbrev = serializers.CharField(required=True)
    levels = LevelSerializer(many=True, required=False, read_only=True)

    class Meta:

        model = Faculty
        fields = ['id', 'name', 'faculty_id', 'abbrev', 'description',
                   'levels', 'about', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'faculty_id', 'created_at', 'levels']

    # def create(self, validated_data):
    #     levels_data = validated_data.pop('levels', [])
    #     faculty = super().create(validated_data)

    #     # Add levels to the faculty instance
    #     for level_data in levels_data:
    #         level_name = level_data.get('name')
            
    #         # Check for uniqueness within the current faculty
    #         if not Level.objects.filter(name=level_name, faculty=faculty).exists():
    #             level_instance, _ = Level.objects.get_or_create(name=level_name)
    #             faculty.levels.add(level_instance)

    #     return faculty


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = serializers.PrimaryKeyRelatedField(
        queryset=Faculty.objects.all().filter(
            is_deleted=False
        ),
        allow_null=True,
        allow_empty=True,
        required=False,
        write_only=True
    )
    faculty_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Department
        fields = ['id', 'name', 'department_id', 'faculty_details',
                  'faculty', 'about', 'description', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'department_id', 'created_at', 'faculty_details']

    def get_faculty_details(self, obj):
        faculty = obj.faculty
        if faculty:
            return FacultySerializer(faculty).data
        return None


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





