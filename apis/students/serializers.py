from apis.users.models import User
from rest_framework import serializers
from apis.students.models import Student
from apis.users.serializers import UserSerializer
from drf_writable_nested import WritableNestedModelSerializer



class StudentSerializer(WritableNestedModelSerializer):

    user = UserSerializer(read_only=True) 

    class Meta:

        model = Student
        fields = ['user', 'student_id', 'is_deleted', 'created_at']
        read_only_fields = ['user', 'student_id']




