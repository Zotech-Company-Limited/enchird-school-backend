import ssl
import random
import string
import logging
import datetime
from uuid import uuid4
from apis.utils import *
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from apis.students.models import Student
from apis.utils import validate_password
from django.core.mail import EmailMessage
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apis.users.models import User, AnonymousUser
from core.email import send_student_verification_email
from apis.courses.models import Course
from apis.students.serializers import StudentSerializer
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from apis.users.serializers import UserSerializer, UserPasswordSerializer, UserUpdateSerializer


logger = logging.getLogger("myLogger")

logging.basicConfig(filename='app.log', level=logging.DEBUG) 



class StudentViewSet(viewsets.ModelViewSet):

    queryset = Student.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action in ['create']:
            # Allow unauthenticated access for create
            permission_classes = [AllowAny]
        else:
            # Require authentication and permissions for other actions
            permission_classes = [IsAuthenticated]  # You can add more permissions as needed
        return [permission() for permission in permission_classes]


    def list(self, request, *args, **kwargs):

        user = self.request.user

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

        if user.is_admin is False and user.is_superuser is False:
            logger.error(
                "You do not have the necessary rights.",
                extra={
                    'user': 'Anonymous'
                }
            )
            return Response(
                {
                    "error": "You do not have the necessary rights."
                },
                status.HTTP_403_FORBIDDEN
            )
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            "Students list returned successfully.",
            extra={
                'user': user.id
            }
        )

        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        """Docstring for function."""
        user = self.request.user
        print(user)
        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if user.is_admin is False and user.is_a_student is False:
            logger.error(
                "You do not have the necessary rights.",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {
                    "error": "You do not have the necessary rights."
                },
                status.HTTP_403_FORBIDDEN
            )
        
        if user.is_a_student is True and str(user.id) != kwargs['pk']:
            logger.warning(
                "You cannot view another student's information",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You cannot view another student's information"},
                status.HTTP_403_FORBIDDEN
            )

        instance = Student.objects.get(user=kwargs['pk'])
        serializer = self.get_serializer(instance)
        logger.info(
            "Student details returned successfully!",
            extra={
                'user': request.user.id
            }
        )
        return Response(serializer.data)

    
    def create(self, request, *args, **kwargs):
        
        try:
            with transaction.atomic():
                student_serializer = self.get_serializer(data=request.data)
                user_serializer = UserSerializer(data=request.data)
                password_serializer = UserPasswordSerializer(data=request.data)
                if student_serializer.is_valid(raise_exception=True):
                    if user_serializer.is_valid(raise_exception=True):
                        if password_serializer.is_valid(raise_exception=True):
                            print("1")
                            password = password_serializer.validated_data['password']
                            try:
                                validate_password(password)
                                # If valid, proceed with user creation
                            except ValueError as e:
                                error_message = e.args[0]  # Access the error message from the exception
                                return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
                            
                            reset_token = uuid4()
                            print("1")
                            
                            # Verify uniqueness of email address
                            num = User.objects.all().filter(
                                    email=user_serializer.validated_data['email']
                                ).count()
                            if num > 0:
                                logger.warning(
                                    "A student/teacher with this email address already exists.",
                                    extra={
                                        'user': 'anonymous'
                                    }
                                )
                                return Response({"error": "A student/teacher with this email address already exists."},
                                                status=status.HTTP_409_CONFLICT)

                            # Create user
                            logging.debug('Your message here')
                            user = user_serializer.save(is_a_student=True)

                            # Create of Student
                            student = student_serializer.save(user=user)

                            user.reset_token = reset_token
                            user.password_requested_at = timezone.now()
                            user.is_admin = False
                            user.role = "student"
                            password = password_serializer.validated_data['password']
                            user.set_password(password)
                            user.save()
                            print(user)
                            headers = self.get_success_headers(student_serializer.data)

                            # Create or get Student group
                            all_permissions = Permission.objects.all()
                            student_group, created = Group.objects.get_or_create(name='Student')

                            # Add the student to the Student Group
                            user.groups.add(student_group)

                            # Send activation email.
                            try:
                                send_student_verification_email(user, reset_token)
                            except Exception as e:
                                print(e)
                                logger.error(
                                    e,
                                    extra={
                                        'user': user.id
                                    }
                                )
                            
                            logger.info(
                                "Student created successfully!",
                                extra={
                                    'user': user.id
                                }
                            )
                            return Response(
                                student_serializer.data,
                                status.HTTP_201_CREATED,
                                headers=headers)
                
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

    def perform_create(self, serializer):
        """Docstring for function."""
        return serializer.save()


    def update(self, request, *args, **kwargs):

        user = self.request.user

        if request.user.is_a_student is False:
            logger.warning(
                "You do not have the necessary rights!",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You do not have the necessary rights"},
                status.HTTP_403_FORBIDDEN
            )
        
        if request.user.id != int(kwargs['pk']):
            logger.error(
                "You cannot edit another student's information",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You cannot edit another student's information"},
                status.HTTP_400_BAD_REQUEST
            )

        partial = kwargs.pop('partial', True)
        instance = User.objects.get(id=kwargs['pk'])
        print(instance)
        try:
            student = Student.objects.get(user=kwargs['pk'], is_deleted=False)
        except Student.DoesNotExist:
            logger.warning(
                "Student not found",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Student not found"},
                status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserUpdateSerializer(
            instance, data=request.data,
            partial=partial)
        student_serializer = self.get_serializer(student)
        if user_serializer.is_valid() is True:
            self.perform_update(user_serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            logger.info(
                "Student modified successfully!",
                extra={
                    'user': request.user.id
                }
            )
            return Response(student_serializer.data)
        else:
            logger.error(
                str(user_serializer.errors),
                extra={
                    'user': request.user.id
                }
            )
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
       
        return serializer.save()


    def destroy(self, request, *args, **kwargs):
        
        user = self.request.user
        if not user.is_a_student:
            logger.warning(
                "You do not have the necessary rights!",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "You do not have the necessary rights"},
                status.HTTP_403_FORBIDDEN
            )
        if user.is_a_student is True and user.id != int(kwargs['pk']):
            logger.warning(
                "You cannot delete another student's account",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You cannot delete another student's account"},
                status.HTTP_403_FORBIDDEN
            )

        instance = User.objects.get(id=kwargs['pk'])
        print(instance)
        instance.is_active = False
        instance.is_deleted = True
        instance.save()

        student = Student.objects.get(user=instance.id, is_deleted=False)
        print(student)
        student.is_active = False
        student.is_deleted = True
        student.save()

        logger.info(
            "Student marked as deleted successfully",
            extra={
                'user': user.id
            }
        )
        return Response(
            {"message": "Student marked as Deleted"},
            status=status.HTTP_200_OK)


@api_view(['POST'])
def register_course(request, course_id):
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
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=course_id, course_status='open')
    except Student.DoesNotExist:
        logger.info(
            "Student not found.",
            extra={
                'user': user.id
            }
        )
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        logger.error(
            "Course not found or not open for registration.",
            extra={
                'user': user.id
            }
        )
        return Response({'error': 'Course not found or not open for registration'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the student is registered for the course
    if course in student.registered_courses.all():
        logger.error(
            "Student is already registed for this course.",
            extra={
                'user': user.id
            }
        )
        return Response({'error': 'Student is already registered for this course'}, status=status.HTTP_400_BAD_REQUEST)


    student.registered_courses.add(course)
    student.save()

    serializer = StudentSerializer(student)
    logger.info(
        "Student successfully registered course.",
        extra={
            'user': user.id
        }
    )
    return Response({'message': 'Student successfully registered this course'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def drop_course(request, course_id):
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
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=course_id, course_status='open')
    except Student.DoesNotExist:
        logger.error(
            "Student not found.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
    except Course.DoesNotExist:
        logger.error(
            "Course not found or course closed for dropping.",
            extra={
                'user': 'Anonymous'
            }
        )
        return Response({'error': 'Course not found or closed for dropping'}, status=status.HTTP_404_NOT_FOUND)

    # Check if the student is registered for the course
    if course not in student.registered_courses.all():
        logger.error(
            "Student not registed for this course.",
            extra={
                'user': user.id
            }
        )
        return Response({'error': 'Student is not registered for this course'}, status=status.HTTP_400_BAD_REQUEST)

    # If the course is registered, proceed with dropping
    student.registered_courses.remove(course)
    student.save()

    serializer = StudentSerializer(student)
    logger.info(
            "Student successfully dropped course.",
            extra={
                'user': user.id
            }
        )
    return Response({'message': 'Student successfully dropped this course'}, status=status.HTTP_200_OK)



