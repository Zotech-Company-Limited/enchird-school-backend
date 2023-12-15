from apis.users.models import User
from rest_framework import serializers
from apis.faculty.models import Faculty, Department
from drf_writable_nested import WritableNestedModelSerializer



class FacultySerializer(WritableNestedModelSerializer):

    name = serializers.CharField(allow_null=False, required=True)
    abbrev = serializers.CharField(required=True)

    class Meta:

        model = Faculty
        fields = ['id', 'name', 'faculty_id', 'abbrev', 'is_deleted', 'created_at']
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
        fields = ['id', 'name', 'department_id', 'faculty', 'is_deleted', 'created_at']
        read_only_fields = ['id', 'department_id', 'created_at']

