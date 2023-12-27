from .models import *
from rest_framework import serializers
from apis.users.serializers import UserSerializer



class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']


class SimplifiedChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)
    assessment = serializers.PrimaryKeyRelatedField(
        #queryset=Assessment.objects.all(), #.filter(is_deleted=False),
        allow_null=True,
        allow_empty=True,
        required=False,
        read_only=True
    )

    class Meta:
        model = Question
        fields = ['id', 'assessment', 'text', 'image', 'created_at', 'choices']


class AssessmentSerializer(serializers.ModelSerializer):
    # questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'description', 'assessment_type', 'instructor', 'course', 'created_at']
        read_only_fields = ['instructor']


class StudentResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentResponse
        fields = '__all__'
        # fields = ['id', 'assess']


class StudentAssessmentScoreSerializer(serializers.ModelSerializer):
    # student = UserSerializer(fields=['first_name', 'last_name'])#.data['last_name']
    student_first_name = serializers.ReadOnlyField(source='student.first_name')
    student_last_name = serializers.ReadOnlyField(source='student.last_name')
    score = serializers.SerializerMethodField()

    def get_score(self, obj):
        return f"{obj.score}%"

    class Meta:
        model = StudentAssessmentScore 
        fields = ['id', 'score', 'student_first_name', 'student_last_name', 'assessment' ]


class GradeSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeSystem
        fields = ['id', 'grade', 'max_score', 'min_score']



