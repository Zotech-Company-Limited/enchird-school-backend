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
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apis.users.models import User, AnonymousUser
from core.email import send_faculty_verification_email
from .models import Faculty, Department, Faculty_Member
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import FacultySerializer, DepartmentSerializer, FacultyMemberSerializer
from apis.users.serializers import UserSerializer, UserPasswordSerializer, UserUpdateSerializer

logger = logging.getLogger("myLogger")

# Create your views here.
class FacultyViewSet(viewsets.ModelViewSet):

    queryset = Faculty.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = FacultySerializer


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
        
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            "List of faculties returned successfully.",
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
        
        if user.is_admin is False:
            logger.error(
                "You do not have the necessary rights/Not Admin.",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {
                    "error": "You do not have the necessary rights/Not Admin."
                },
                status.HTTP_403_FORBIDDEN
            )

        instance = Faculty.objects.get(id=kwargs['pk'])
        serializer = self.get_serializer(instance)
        logger.info(
            "Faculty details returned successfully!",
            extra={
                'user': request.user.id
            }
        )
        return Response(serializer.data)


    def create(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={
                    'user': 'Anonymous'
                }
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.is_admin is False:
            logger.error(
                "You do not have the necessary rights/Not an Admin.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {
                    "error": "You do not have the necessary rights/Not an Admin."
                },
                status.HTTP_403_FORBIDDEN
            )
        
        try:
            with transaction.atomic():
                faculty_serializer = self.get_serializer(data=request.data)
                if faculty_serializer.is_valid(raise_exception=True):
                
                    # Verify uniqueness of faculty name
                    num = Faculty.objects.all().filter(
                            name=faculty_serializer.validated_data['name']
                        ).count()
                    if num > 0:
                        logger.warning(
                            "A faculty with this name already exists.",
                            extra={
                                'user': 'anonymous'
                            }
                        )
                        return Response({"error": "A faculty with this name already exists."},
                                        status=status.HTTP_409_CONFLICT)

                    # Verify uniqueness of faculty abbreviation
                    num = Faculty.objects.all().filter(
                            abbrev=faculty_serializer.validated_data['abbrev']
                        ).count()
                    if num > 0:
                        logger.warning(
                            "A faculty with this name already exists.",
                            extra={
                                'user': 'anonymous'
                            }
                        )
                        return Response({"error": "A faculty with this name already exists."},
                                        status=status.HTTP_409_CONFLICT)

                    # Create user
                    self.perform_create(faculty_serializer, user)
                    
                    headers = self.get_success_headers(faculty_serializer.data)
                    
                    logger.info(
                        "Faculty created successfully!",
                        extra={
                            'user': user.id
                        }
                    )
                    return Response(
                        faculty_serializer.data,
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

    def perform_create(self, serializer, user):

        return serializer.save(created_by=user)


    def update(self, request, *args, **kwargs):

        user = self.request.user

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

        if request.user.is_admin is False:
            logger.warning(
                "You do not have the necessary rights! (Not admin)",
                extra={
                    'user': request.user.id
                }
            )
            return Response(
                {"error": "You do not have the necessary rights (Not admin)"},
                status.HTTP_403_FORBIDDEN
            )

        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            print(instance)
            serializer = self.get_serializer(
                instance, data=request.data,
                partial=partial)
            serializer.is_valid(raise_exception=True)

            number = Faculty.objects.all().filter(
                ~Q(id=kwargs['pk']),
                name=serializer.validated_data['name'],
                is_deleted=False
            ).count()
            if number >= 1:
                logger.error(
                    "A Faculty already exists with this name.",
                    extra={
                        'user': request.user.id
                    }
                )
                return Response(
                    {'message': "A Faculty already exists with this name."},
                    status=status.HTTP_409_CONFLICT)
            
            num = Faculty.objects.all().filter(
                ~Q(id=kwargs['pk']),
                abbrev=serializer.validated_data['abbrev'],
                is_deleted=False
            ).count()
            if num >= 1:
                logger.error(
                    "A Faculty already exists with this abbreviation.",
                    extra={
                        'user': request.user.id
                    }
                )
                return Response(
                    {'message': "A Faculty already exists with this abbreviation."},
                    status=status.HTTP_409_CONFLICT)
            
            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            logger.info(
                "Faculty info Modified successfully!",
                extra={
                    'user': user.id
                }
            )
            return Response(serializer.data)

        except Exception as e:
            logger.error(
                str(e),
                extra={
                    'user': user.id
                }
            )
            return Response(
                {'message': str(e)},
                status=status.HTTP_412_PRECONDITION_FAILED)
            
        
    def perform_update(self, serializer):
        """Docstring for function."""
        return serializer.save()


    def destroy(self, request, *args, **kwargs):
        """Docstring for function."""
        user = self.request.user

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

        if not user.is_admin:
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

        instance = self.get_object()
        print(instance)
        instance.is_deleted = True
        instance.save()

        logger.info(
            "Faculty marked as deleted successfully",
            extra={
                'user': user.id
            }
        )
        return Response(
            {"message": "Faculty marked as Deleted"},
            status=status.HTTP_200_OK)



class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all().filter(is_deleted=False).order_by('-created_at')
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': 'Anonymous'}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_admin:
            logger.error(
                "You do not have the necessary rights.",
                extra={'user': 'Anonymous'}
            )
            return Response(
                {"error": "You do not have the necessary rights."},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            "List of departments returned successfully.",
            extra={'user': user.id}
        )

        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': request.user.id}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_admin:
            logger.error(
                "You do not have the necessary rights/Not Admin.",
                extra={'user': request.user.id}
            )
            return Response(
                {"error": "You do not have the necessary rights/Not Admin."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            instance = Department.objects.get(id=kwargs['pk'], is_deleted=False)
            serializer = self.get_serializer(instance)
            logger.info(
                "Department details returned successfully!",
                extra={'user': request.user.id}
            )
            return Response(serializer.data)

        except Department.DoesNotExist:
            logger.info(
                "Department Not Found",
                extra={'user': user.id}
            )
            return Response(
                {"message": "Department Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )


    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': 'Anonymous'}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_admin:
            logger.error(
                "You do not have the necessary rights/Not an Admin.",
                extra={'user': user.id}
            )
            return Response(
                {"error": "You do not have the necessary rights/Not an Admin."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            with transaction.atomic():
                print("here")
                department_serializer = self.get_serializer(data=request.data)
                print(department_serializer)
                if department_serializer.is_valid(raise_exception=True):
                    
                    # Verify uniqueness of department name within the same faculty
                    num = Department.objects.filter(
                        Q(faculty=department_serializer.validated_data['faculty']),
                        Q(name=department_serializer.validated_data['name']),
                        Q(is_deleted=False)
                    ).count()
                    if num > 0:
                        logger.warning(
                            "A department with this name already exists under the same faculty.",
                            extra={'user': 'anonymous'}
                        )
                        return Response(
                            {"error": "A department with this name already exists under the same faculty."},
                            status=status.HTTP_409_CONFLICT
                        )

                    self.perform_create(department_serializer, user)

                    headers = self.get_success_headers(department_serializer.data)

                    logger.info(
                        "Department created successfully!",
                        extra={'user': user.id}
                    )
                    return Response(
                        department_serializer.data,
                        status=status.HTTP_201_CREATED,
                        headers=headers
                    )

        except Exception as e:
            # Rollback transaction and raise validation error
            transaction.rollback()
            logger.error(
                str(e),
                extra={'user': None}
            )
            return Response(
                {"error": str(e)},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

    def perform_create(self, serializer, user):
        return serializer.save(created_by=user)

    def update(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': request.user.id}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if request.user.is_admin is False:
            logger.warning(
                "You do not have the necessary rights! (Not admin)",
                extra={'user': request.user.id}
            )
            return Response(
                {"error": "You do not have the necessary rights! (Not admin)"},
                status.HTTP_403_FORBIDDEN
            )

        try:
            partial = kwargs.pop('partial', True)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Verify uniqueness of department name within the same faculty
            number = Department.objects.filter(
                ~Q(id=kwargs['pk']),
                Q(faculty=serializer.validated_data['faculty']),
                Q(name=serializer.validated_data['name']),
                Q(is_deleted=False)
            ).count()
            if number >= 1:
                logger.error(
                    "A department already exists with this name under the same faculty.",
                    extra={'user': request.user.id}
                )
                return Response(
                    {'message': "A department already exists with this name under the same faculty."},
                    status=status.HTTP_409_CONFLICT
                )

            self.perform_update(serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}

            logger.info(
                "Department info modified successfully!",
                extra={'user': user.id}
            )
            return Response(serializer.data)

        except Exception as e:
            logger.error(
                str(e),
                extra={'user': user.id}
            )
            return Response(
                {'message': str(e)},
                status=status.HTTP_412_PRECONDITION_FAILED
            )

    def perform_update(self, serializer):
        return serializer.save()

    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': request.user.id}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_admin:
            logger.warning(
                "You do not have the necessary rights!",
                extra={'user': user.id}
            )
            return Response(
                {"error": "You do not have the necessary rights"},
                status.HTTP_403_FORBIDDEN
            )

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        logger.info(
            "Department marked as deleted successfully",
            extra={'user': user.id}
        )
        return Response(
            {"message": "Department marked as Deleted"},
            status=status.HTTP_200_OK
        )


class FacultyMemberViewSet(viewsets.ModelViewSet):
    queryset = Faculty_Member.objects.all().filter(is_deleted=False).order_by('-created_at')
    serializer_class = FacultyMemberSerializer

    def list(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error( "You must provide valid authentication credentials.",extra={'user': 'Anonymous'} )
            return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED )

        if not user.is_admin:
            logger.error(
                "You do not have the necessary rights.",
                extra={'user': 'Anonymous'}
            )
            return Response(
                {"error": "You do not have the necessary rights."},
                status=status.HTTP_403_FORBIDDEN
            )

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        logger.info(
            "List of faculty members returned successfully.",
            extra={'user': user.id}
        )

        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error( "You must provide valid authentication credentials.", extra={'user': request.user.id} )
            return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED )

        if user.is_admin is False and user.is_faculty_member is False:
            logger.error( "You do not have the necessary rights/Not Admin.", extra={'user': request.user.id} )
            return Response( {"error": "You do not have the necessary rights/Not Admin."}, status=status.HTTP_403_FORBIDDEN)

        if user.is_faculty_member is True and str(user.id) != kwargs['pk']:
            logger.warning( "You cannot view another faculty member's information", extra={ 'user': request.user.id} )
            return Response( {"error": "You cannot view another student's information"}, status.HTTP_403_FORBIDDEN  )

        try:
            instance = Faculty_Member.objects.get(id=kwargs['pk'], is_deleted=False)
            serializer = self.get_serializer(instance)
            logger.info(
                "Faculty member details returned successfully!",
                extra={'user': request.user.id}
            )
            return Response(serializer.data)

        except Faculty_Member.DoesNotExist:
            logger.info(
                "Faculty Member Not Found",
                extra={'user': user.id}
            )
            return Response(
                {"message": "Faculty Member Not Found"},
                status=status.HTTP_404_NOT_FOUND
            )


    def create(self, request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            logger.error(
                "You must provide valid authentication credentials.",
                extra={'user': 'Anonymous'}
            )
            return Response(
                {"error": "You must provide valid authentication credentials."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_admin:
            logger.error(
                "You do not have the necessary rights/Not an Admin.",
                extra={'user': user.id}
            )
            return Response(
                {"error": "You do not have the necessary rights/Not an Admin."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            with transaction.atomic():
                fac_mem_serializer = self.get_serializer(data=request.data)
                user_serializer = UserSerializer(data=request.data)
                if fac_mem_serializer.is_valid(raise_exception=True):
                    if user_serializer.is_valid(raise_exception=True):
                        
                        reset_token = uuid4()

                        # Verify uniqueness of email address
                        num = User.objects.all().filter(
                                email=user_serializer.validated_data['email']
                            ).count()
                        if num > 0:
                            logger.warning( "An account with this email address already exists.", extra={ 'user': 'anonymous' })
                            return Response({"error": "An account with this email address already exists."}, status=status.HTTP_409_CONFLICT)
                        # Create user
                        user = user_serializer.save(is_faculty_member=True, role='faculty')

                        # Create Teacher
                        faculty = fac_mem_serializer.save(user=user)

                        user.reset_token = reset_token
                        user.password_requested_at = timezone.now()
                        user.is_admin = False
                        user.is_active = True
                        password = User.objects.make_random_password()
                        print(password)
                        user.set_password(password)
                        user.save()

                        headers = self.get_success_headers(fac_mem_serializer.data)

                        # Create or get Faculty Members group
                        all_permissions = Permission.objects.all()
                        faculty_group, created = Group.objects.get_or_create(name='Faculty')

                        # Add the teacher to the Teacher Group
                        user.groups.add(faculty_group)

                        # Send activation email.
                        try:
                            send_faculty_verification_email(user, password)
                        except Exception as e:
                            logger.error( e, extra={ 'user': user.id })
                            

                        logger.info( "Faculty Member created successfully!", extra={'user': user.id} )
                        return Response(fac_mem_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            # Rollback transaction and raise validation error
            transaction.rollback()
            logger.error( str(e), extra={'user': None})
            return Response( {"error": str(e)}, status=status.HTTP_412_PRECONDITION_FAILED)

    def perform_create(self, serializer, user):
        return serializer.save(created_by=user)


    def update(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error( "You must provide valid authentication credentials.", extra={'user': request.user.id})
            return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        if user.is_faculty_member is False:
            logger.warning( "You do not have the necessary rights!", extra={'user': request.user.id} )
            return Response( {"error": "You do not have the necessary rights! "}, status.HTTP_403_FORBIDDEN )

        if request.user.id != int(kwargs['pk']):
            logger.error( "You cannot edit another faculty member's information", extra={ 'user': request.user.id } )
            return Response( {"error": "You cannot edit another faculty member's information"}, status.HTTP_400_BAD_REQUEST )

        partial = kwargs.pop('partial', True)
        instance = User.objects.get(id=kwargs['pk'])
        print(instance)
        try:
            faculty = Faculty_Member.objects.get(user=kwargs['pk'], is_deleted=False)
        except Student.DoesNotExist:
            logger.warning(
                "Faculty Member not found",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Faculty Member Not found"},
                status=status.HTTP_400_BAD_REQUEST)
        
        user_serializer = UserUpdateSerializer(
            instance, data=request.data,
            partial=partial)
        fac_mem_serializer = self.get_serializer(faculty)
        if user_serializer.is_valid() is True:
            self.perform_update(user_serializer)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            logger.info(
                "Faculty Member Info modified successfully!",
                extra={'user': request.user.id })
            return Response(fac_mem_serializer.data)
        else:
            logger.error( str(user_serializer.errors), extra={ 'user': request.user.id })
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def perform_update(self, serializer):
        return serializer.save()


    def destroy(self, request, *args, **kwargs):
        user = self.request.user

        if not user.is_authenticated:
            logger.error( "You must provide valid authentication credentials.", extra={'user': request.user.id} )
            return Response( {"error": "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED )

        if not user.is_admin:
            logger.warning( "You do not have the necessary rights!", extra={'user': user.id} )
            return Response( {"error": "You do not have the necessary rights"}, status.HTTP_403_FORBIDDEN )

        instance = self.get_object()
        instance.is_deleted = True
        instance.save()

        logger.info(
            "Department marked as deleted successfully",
            extra={'user': user.id}
        )
        return Response(
            {"message": "Department marked as Deleted"},
            status=status.HTTP_200_OK
        )




