import logging
import pandas as pd
from .serializers import *
from django.db import transaction
from django.shortcuts import render
from apis.courses.models import Course
from apis.students.models import Student
from rest_framework import status, viewsets
from rest_framework.response import Response
from apis.assessment.models import Assessment
from rest_framework.decorators import api_view
from .models import Question, Choice, StudentResponse
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
@transaction.atomic
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
        logger.error(
            "Assessment not Found.",
            extra={
                'user': user.id
            }
        )
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
        try:
            student = Student.objects.get(user=user)
        except Student.DoesNotExist:
            logger.error(
                "Student not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
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


# @api_view(['POST'])
# def submit_assessment_responses(request, assessment_id):
#     user = request.user

#     if not user.is_authenticated:
#         logger.error(
#             "You do not have the necessary rights.",
#             extra={
#                 'user': 'Anonymous'
#             }
#         )
#         return Response(
#             {'error': "You must provide valid authentication credentials."},
#             status=status.HTTP_401_UNAUTHORIZED
#         )

#     if user.is_a_student is False:
#         logger.error(
#             "Only students can register courses.",
#             extra={
#                 'user': 'Anonymous'
#             }
#         )
#         return Response(
#             {
#                 "error": "Only students can register courses."
#             },
#             status.HTTP_403_FORBIDDEN
#         )
    

#     try:
#         assessment = Assessment.objects.get(pk=assessment_id)
#     except Assessment.DoesNotExist:
#         logger.error(
#             "Assessment not found.",
#             extra={
#                 'user': user.id
#             }
#         )
#         return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'POST':
#         serializer = StudentResponseSerializer(data=request.data)
#         if serializer.is_valid():
#             # Ensure that the user is the student for whom the response is being submitted
#             if serializer.validated_data['student'] != user:
#                 return Response({'error': 'Invalid student for the response'}, status=status.HTTP_403_FORBIDDEN)

#             # Check if responses already exist for the assessment by the student
#             existing_responses = StudentResponse.objects.filter(student=user, question__assessment=assessment)
#             if existing_responses.exists():
#                 logger.error(
#                     "Responses for this assessment already submitted.",
#                     extra={
#                         'user': user.id
#                     }
#                 )
#                 return Response({'error': 'Responses for this assessment already submitted'}, status=status.HTTP_400_BAD_REQUEST)

#             # Save the responses
#             serializer.save(student=user)
#             logger.info(
#                 "Responses submitted successfully.",
#                 extra={
#                     'user': user.id
#                 }
#             )
#             return Response({'message': 'Responses submitted successfully'}, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@transaction.atomic
def submit_assessment_responses(request, assessment_id):
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

    if user.is_a_student is False:
        logger.error(
            "Only students can register courses.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response(
            {
                "error": "Only students can register courses."
            },
            status.HTTP_403_FORBIDDEN
        )
    
    try:
        assessment = Assessment.objects.get(pk=assessment_id)
    except Assessment.DoesNotExist:
        logger.error(
            "Assessment not found.",
            extra={
                'user': user.id
            }
        )
        return Response({'error': 'Assessment not found'}, status=status.HTTP_404_NOT_FOUND)
    try:
        with transaction.atomic():
            # Check if responses already exist for the assessment by the student
            existing_responses = StudentResponse.objects.filter(student=user, assessment=assessment)
            if existing_responses.exists():
                logger.error(
                    "Responses for this assessment already submitted.",
                    extra={
                        'user': user.id
                    }
                )
                return Response({'error': 'Responses for this assessment already submitted'}, status=status.HTTP_400_BAD_REQUEST)

            responses_data = request.data.get('responses', [])

            # Assuming the 'responses' data is a list of dictionaries with question_id and selected_choice_id
            for response_data in responses_data:
                question_id = response_data.get('question_id')
                selected_choice_id = response_data.get('selected_choice_id')

                try:
                    question = Question.objects.get(pk=question_id)
                    selected_choice = Choice.objects.get(pk=selected_choice_id)
                except Question.DoesNotExist:
                    logger.error(
                        "Invalid Question ID.",
                        extra={
                            'user': user.id
                        }
                    )
                    return Response({'error': 'Invalid question ID'}, status=status.HTTP_400_BAD_REQUEST)
                except Choice.DoesNotExist:
                    logger.error(
                        "Invalid Choice ID.",
                        extra={
                            'user': user.id
                        }
                    )
                    return Response({'error': 'Invalid Choice ID'}, status=status.HTTP_400_BAD_REQUEST)



                # Create or update the student response
                response, created = StudentResponse.objects.get_or_create(
                    student=user,
                    assessment=assessment,
                    question=question,
                    defaults={'selected_choice': selected_choice}
                )

                if not created:
                    # Update the selected choice if the response already exists
                    response.selected_choice = selected_choice
                    response.save()

            return Response({'message': 'Responses submitted successfully'}, status=status.HTTP_200_OK)

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



