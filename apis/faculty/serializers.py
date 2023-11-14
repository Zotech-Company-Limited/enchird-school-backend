from apis.users.models import User
from rest_framework import serializers
from apis.faculty.models import Faculty
from drf_writable_nested import WritableNestedModelSerializer



class FacultySerializer(WritableNestedModelSerializer):

    name = serializers.CharField(allow_null=False, required=True)
    abbrev = serializers.CharField(required=True)

    class Meta:

        model = Faculty
        fields = ['name', 'faculty_id', 'abbrev', 'is_deleted', 'created_at']
        read_only_fields = ['faculty_id', 'created_at']




