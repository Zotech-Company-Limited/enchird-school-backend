from rest_framework import serializers
from .models import Assessment, Question, Choice, StudentResponse



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


# class CourseAssessmentSerializer(serializers.ModelSerializer):
#     assessments = AssessmentSerializer(many=True, read_only=True)

#     class Meta:
#         model = Course
#         fields = '__all__'

