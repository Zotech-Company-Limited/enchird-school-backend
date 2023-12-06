import logging
import pandas as pd
from .serializers import *
from django.db import transaction
from django.shortcuts import render
from .models import Question, Choice
from apis.courses.models import Course
from apis.students.models import Student
from rest_framework import status, viewsets
from rest_framework.response import Response
from apis.assessment.models import Assessment
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from apis.assessment.serializers import AssessmentSerializer


logger = logging.getLogger("myLogger")

# Create your views here.

@api_view(['POST'])
def create_assessment(request):
    user = request.user

    if not user.is_authenticated:
        logger.error(
            "You do not have the necessary rights.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response(
            {'error': "You must provide valid authentication credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.is_a_teacher is False:
        logger.error(
            "Only teachers can create assessments.",
            extra={
                'user': user.id
            }
        )
        return Response(
            {
                "error": "Only teachers can create assessments."
            },
            status.HTTP_403_FORBIDDEN
        )
    
    serializer = AssessmentSerializer(data=request.data)

    if serializer.is_valid():
        
        serializer.save(instructor=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_question_with_choices(request, assessment_id):
    user = request.user
    if not user.is_authenticated:
        logger.error(
            "You do not have the necessary rights.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response(
            {'error': "You must provide valid authentication credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.is_a_teacher is False:
        logger.error(
            "Only teachers can add questions.",
            extra={
                'user': user.id
            }
        )
        return Response(
            {
                "error": "Only teachers can add questions."
            },
            status.HTTP_403_FORBIDDEN
        )
    
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
        return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'file' in request.data:
        try:
            with transaction.atomic():
                file = request.data['file']
                print(file)
                df = pd.read_excel(file)

                for index, row in df.iterrows():
                    question_text = row['Question']
                    choices = [row['Choice1'], row['Choice2'], row['Choice3']]
                    correct_choice = row['CorrectChoice']

                    # Save the question first
                    question_data = {'text': question_text, 'assessment': assessment.id}
                    question_serializer = QuestionSerializer(data=question_data)
                    if question_serializer.is_valid():
                        question = question_serializer.save(assessment=assessment)

                    # Save choices for the question
                    for choice_text in choices:
                        is_correct = choice_text == correct_choice
                        print(is_correct)
                        choice_data = {'question': question.id, 'text': choice_text, 'is_correct': is_correct}
                        choice_serializer = SimplifiedChoiceSerializer(data=choice_data)
                        if choice_serializer.is_valid():
                            choice_serializer.save(question=question)

            return Response({'message': 'Questions and choices created successfully'}, status=status.HTTP_201_CREATED)

        except Exception as e:
            logger.error(
                str(e),
                extra={
                    'user': None
                }
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    if 'file' not in request.data:
        try:
            with transaction.atomic():
                question_data = request.data.get('question', {})
                choices_data = request.data.get('choices', [])

                question_serializer = QuestionSerializer(data=question_data)
                if question_serializer.is_valid():
                    # Save the question first
                    question = question_serializer.save(assessment=assessment)
                    print(question)

                    # Save choices for the question
                    for choice_data in choices_data:
                        # Associate the choice with the saved question
                        choice_data['question'] = question.id
                        choice_serializer = SimplifiedChoiceSerializer(data=choice_data)
                        if choice_serializer.is_valid():
                            choice_serializer.save(question=question)

                    return Response({'message': 'Question and choices created successfully'}, status=status.HTTP_201_CREATED)

                return Response({'error': question_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            
        except Exception as e:
            # Rollback transaction and raise validation error
            transaction.rollback()
            logger.error(
                str(e),
                extra={
                    'user': None
                }
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_412_PRECONDITION_FAILED)


@api_view(['GET'])
def get_assessment_details(request, assessment_id):
    user = request.user

    is_student = request.user.is_a_student
    is_instructor = request.user.is_a_teacher
    if not user.is_authenticated:
        logger.error(
            "You do not have the necessary rights.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response(
            {'error': "You must provide valid authentication credentials."},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if user.is_a_teacher is False and user.is_a_student is False:
        logger.warning(
            "You do not have the necessary rights! (Not a lecturer nor student)",
            extra={
                'user': request.user.id
            }
        )
        return Response(
            {"error": "You do not have the necessary rights (Not a lecturer nor student)"},
            status.HTTP_403_FORBIDDEN
        )
   
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
        return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

    if is_instructor:
        if user not in assessment.course.instructors.all():
            logger.warning(
                "You are not a lecturer of this course",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You are not a lecturer of this course."},
                status.HTTP_403_FORBIDDEN
            )
        
    if is_student:
        if assessment.course not in student.registered_courses.all():
            logger.error(
                "Student not registed for this course.",
                extra={
                    'user': user.id
                }
            )
            return Response({'error': 'Student is not registered for this course'}, status=status.HTTP_400_BAD_REQUEST)

    assessment_serializer = AssessmentSerializer(assessment)
    questions = Question.objects.filter(assessment=assessment)
    question_serializer = QuestionSerializer(questions, many=True)
    
    # Retrieve only questions and choices without correct responses
    question_data = question_serializer.data
    for question in question_data:
        choices = Choice.objects.filter(question=question['id'])
        choice_serializer = SimplifiedChoiceSerializer(choices, many=True)
        question['choices'] = choice_serializer.data

    # You can customize the structure of the response based on your needs
    response_data = {
        'assessment_details': assessment_serializer.data,
        'questions': question_data,
        # Add other relevant information if needed
    }

    return Response(response_data, status=status.HTTP_200_OK)


