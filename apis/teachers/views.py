import string
import random
import logging
import datetime
from uuid import uuid4
from apis.utils import *
from django.db.models import Q
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.shortcuts import render
from core.views import PaginationClass
from apis.teachers.models import Teacher
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apis.users.models import User, AnonymousUser
from core.email import send_teacher_verification_email
from apis.teachers.serializers import TeacherSerializer
from django.contrib.auth.models import Group, Permission
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from apis.users.serializers import UserSerializer, UserPasswordSerializer, UserUpdateSerializer


logger = logging.getLogger("myLogger")



# Create your views here.
class TeacherViewSet(viewsets.ModelViewSet):

    queryset = Teacher.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    pagination_class = PaginationClass
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action in ['create', 'list', 'retrieve', 'delete', 'update']:
            # Allow unauthenticated access for create
            permission_classes = [IsAuthenticated]
        # else:
        #     # Require authentication and permissions for other actions
        #     permission_classes = [IsAuthenticated]  # You can add more permissions as needed
        return [permission() for permission in permission_classes]


    def list(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error(
                "You do not have the necessary rights.",
                extra={ 'user': 'Anonymous' }  )
            return Response(
                {'error': "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED )

        if user.is_superuser is False:
            logger.error(
                "You do not have the necessary rights.",
                extra={ 'user': 'Anonymous' } )
            return Response(
                { "error": "You do not have the necessary rights."}, status.HTTP_403_FORBIDDEN )
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            logger.info(
                "List of teachers returned successfully.",
                extra={ 'user': user.id } )
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            "List of teachers returned successfully.",
            extra={ 'user': user.id } )

        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
          
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
        
        if user.is_admin is False and user.is_a_teacher is False:
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
        
        if user.is_a_teacher is True and str(user.id) != kwargs['pk']:
            logger.warning(
                "You cannot view another teacher's information",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You cannot view another teacher's information"},
                status.HTTP_403_FORBIDDEN
            )

        instance = Teacher.objects.get(user=kwargs['pk'])
        serializer = self.get_serializer(instance)
        logger.info(
            "Teacher details returned successfully!",
            extra={
                'user': request.user.id
            }
        )
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        user = request.user

        if user.is_admin is False:
            logger.error( "You do not have the necessary rights.", extra={ 'user': user.id })
            return Response({ "error": "You do not have the necessary rights."}, status.HTTP_403_FORBIDDEN )
        
        try:
            with transaction.atomic():
                teacher_serializer = self.get_serializer(data=request.data)
                user_serializer = UserSerializer(data=request.data)
                if teacher_serializer.is_valid(raise_exception=True):
                    if user_serializer.is_valid(raise_exception=True):

                        reset_token = uuid4()
                    
                        # Verify uniqueness of email address
                        num = User.objects.all().filter( email=user_serializer.validated_data['email'] ).count()
                        if num > 0:
                            logger.warning( "A student/teacher with this email address already exists.", extra={ 'user': 'anonymous' })
                            return Response({"error": "A student/teacher with this email address already exists."}, status=status.HTTP_409_CONFLICT)

                        # Create user
                        user = user_serializer.save(is_a_teacher=True, role='teacher')
                        
                        # Create Teacher
                        teacher = teacher_serializer.save(user=user)

                        user.reset_token = reset_token
                        user.password_requested_at = timezone.now()
                        user.is_admin = False
                        user.is_active = True
                        password = User.objects.make_random_password()
                        print(password)
                        user.set_password(password)
                        user.save()
                        print(user)
                        headers = self.get_success_headers(teacher_serializer.data)

                        # Create or get Teacher group
                        all_permissions = Permission.objects.all()
                        teacher_group, created = Group.objects.get_or_create(name='Teacher')

                        # Add the teacher to the Teacher Group
                        user.groups.add(teacher_group)
                        
                        # Send activation email.
                        try:
                            send_teacher_verification_email(user, password)
                        except Exception as e:
                            logger.error( e, extra={ 'user': user.id })
                            
                        logger.info( "Teacher created successfully!", extra={ 'user': user.id } )
                        return Response(
                            teacher_serializer.data,
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
        """Docstring for function."""
        user = self.request.user

        if request.user.is_a_teacher is False:
            logger.warning(
                "You do not have the necessary rights! (Not a teacher)",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You do not have the necessary rights (Not a teacher)"},
                status.HTTP_403_FORBIDDEN
            )
        
        if request.user.id != int(kwargs['pk']):
            logger.error(
                "You cannot edit another teacher's information",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You cannot edit another teacher's information"},
                status.HTTP_400_BAD_REQUEST
            )

        partial = kwargs.pop('partial', True)
        instance = User.objects.get(id=kwargs['pk'])
        print(instance)
        try:
            teacher = Teacher.objects.get(user=kwargs['pk'], is_deleted=False)
        except Teacher.DoesNotExist:
            logger.warning(
                "Teacher not found",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Teacher not found"},
                status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserUpdateSerializer(
            instance, data=request.data,
            partial=partial)
        teacher_serializer = self.get_serializer(teacher)
        if user_serializer.is_valid() is True:
            self.perform_update(user_serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            logger.info(
                "Teacher info modified successfully!",
                extra={
                    'user': request.user.id
                }
            )
            return Response(teacher_serializer.data)
        else:
            logger.error(
                str(user_serializer.errors),
                extra={
                    'user': request.user.id
                }
            )
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        """Docstring for function."""
        return serializer.save()


    def destroy(self, request, *args, **kwargs):
        """Docstring for function."""
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


