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
from apis.faculty.models import Faculty
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apis.users.models import User, AnonymousUser
from apis.faculty.serializers import FacultySerializer
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from apis.users.serializers import UserSerializer, UserPasswordSerializer, UserUpdateSerializer

logger = logging.getLogger("myLogger")

# Create your views here.
class FacultyViewSet(viewsets.ModelViewSet):

    queryset = Faculty.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = FacultySerializer

    # def get_permissions(self):
    #     if self.action in ['create', 'list', 'retrieve', 'delete', 'update']:
    #         # Allow unauthenticated access for create
    #         permission_classes = [IsAuthenticated]
    #     # else:
    #     #     # Require authentication and permissions for other actions
    #     #     permission_classes = [IsAuthenticated]  # You can add more permissions as needed
    #     return [permission() for permission in permission_classes]


    def list(self, request, *args, **kwargs):
        """Docstring for function."""
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

        if user.is_admin is False:
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
                    'user': request.user.id
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
        """Docstring for function."""
        return serializer.save(created_by=user)


    def update(self, request, *args, **kwargs):
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


