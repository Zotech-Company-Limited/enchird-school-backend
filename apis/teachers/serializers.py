from apis.users.models import User
from rest_framework import serializers
from apis.teachers.models import Teacher
from apis.users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer



class TeacherSerializer(WritableNestedModelSerializer):

    user = UserSerializer(read_only=True) 

    class Meta:

        model = Teacher
        fields = ['user', 'teacher_id', 'highest_degree', 'is_deleted', 'created_at']
        read_only_fields = ['user', 'teacher_id']




