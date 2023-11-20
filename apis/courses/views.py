import random
import string
import logging
import datetime
from apis.utils import *
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from apis.users.models import User, AnonymousUser
from apis.courses.models import Course
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from apis.users.serializers import UserSerializer, UserUpdateSerializer
from apis.courses.serializers import CourseSerializer


logger = logging.getLogger("myLogger")

logging.basicConfig(filename='app.log', level=logging.DEBUG) 



class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = CourseSerializer


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
            "List of courses returned successfully.",
            extra={
                'user': user.id
            }
        )

        return Response(serializer.data)


    def retrieve(self, request, *args, **kwargs):

        user = self.request.user
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

        try: 
            instance = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            logger.error(
                "Course not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Course Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )


        serializer = self.get_serializer(instance)
        logger.info(
            "Course details returned successfully!",
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
                course_serializer = self.get_serializer(data=request.data)
                if course_serializer.is_valid(raise_exception=True):
                    # Verify uniqueness of course title
                    title_num = Course.objects.all().filter(
                            course_title=course_serializer.validated_data['course_title']
                        ).count()
                    if title_num > 0:
                        logger.warning(
                            "A course with this name already exists.",
                            extra={
                                'user': 'anonymous'
                            }
                        )
                        return Response({"error": "A course with this name already exists."},
                                        status=status.HTTP_409_CONFLICT)

                    # Verify uniqueness of course code
                    code_num = Course.objects.all().filter(
                            course_code=course_serializer.validated_data['course_code']
                        ).count()
                    if code_num > 0:
                        logger.warning(
                            "A course with this code already exists.",
                            extra={
                                'user': 'anonymous'
                            }
                        )
                        return Response({"error": "A course with this code already exists."},
                                        status=status.HTTP_409_CONFLICT)
                    
                    # Create course
                    logging.debug('Your message here')
                    course = course_serializer.save(created_by=user)

                    headers = self.get_success_headers(course_serializer.data)
                    
                    logger.info(
                        "Course created successfully!",
                        extra={
                            'user': user.id
                        }
                    )
                    return Response(
                        course_serializer.data,
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


    def update(self, request, *args, **kwargs):
        
        user = self.request.user
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


        if request.user.is_admin is False:
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

        partial = kwargs.pop('partial', True)
        try:
            instance = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            logger.error(
                "Course not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Course Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )
        print(instance)
        
        course_serializer = self.get_serializer(instance, 
                data=request.data,
                partial=partial)
        if course_serializer.is_valid() is True:

            number = Course.objects.all().filter(
                ~Q(id=kwargs['pk']),
                course_title=course_serializer.validated_data['course_title'],
                is_deleted=False
            ).count()
            if number >= 1:
                logger.error(
                    "A Course already exists with this name.",
                    extra={
                        'user': request.user.id
                    }
                )
                return Response(
                    {'message': "A Course already exists with this name."},
                    status=status.HTTP_409_CONFLICT)

            num = Course.objects.all().filter(
                ~Q(id=kwargs['pk']),
                course_code=course_serializer.validated_data['course_code'],
                is_deleted=False
            ).count()
            if num >= 1:
                logger.error(
                    "A Course already exists with this code.",
                    extra={
                        'user': request.user.id
                    }
                )
                return Response(
                    {'message': "A Course already exists with this code."},
                    status=status.HTTP_409_CONFLICT)

            course_serializer.save(modified_by=user)

            if getattr(instance, '_prefetched_objects_cache', None):
                instance._prefetched_objects_cache = {}
            logger.info(
                "Course Info modified successfully!",
                extra={
                    'user': request.user.id
                }
            )
            return Response(course_serializer.data)
        else:
            logger.error(
                str(course_serializer.errors),
                extra={
                    'user': request.user.id
                }
            )
            return Response(course_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, *args, **kwargs):

        user = self.request.user
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

        try:
            instance = Course.objects.get(id=kwargs['pk'])
        except Course.DoesNotExist:
            logger.error(
                "Course not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Course Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.is_deleted = True
        instance.save()

        logger.info(
            "Course marked as deleted successfully",
            extra={
                'user': user.id
            }
        )
        return Response(
            {"message": "Course marked as Deleted"},
            status=status.HTTP_200_OK)



@api_view(['POST'])
def assign_teacher(request, course_id, teacher_id):
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
        course = Course.objects.get(id=course_id, is_deleted=False)
        teacher = User.objects.get(id=teacher_id, is_deleted=False, is_a_teacher=True, is_active=True)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'Teacher not found or is not an active teacher'}, status=status.HTTP_404_NOT_FOUND)

    course.instructors.add(teacher)
    course.save()

    serializer = CourseSerializer(course)
    return Response(serializer.data)


@api_view(['POST'])
def unassign_teacher(request, course_id, teacher_id):
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
        course = Course.objects.get(id=course_id, is_deleted=False)
        teacher = User.objects.get(id=teacher_id, is_deleted=False, is_a_teacher=True, is_active=True)
    except Course.DoesNotExist:
        return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
    except User.DoesNotExist:
        return Response({'error': 'Teacher not found or is not an active teacher'}, status=status.HTTP_404_NOT_FOUND)

    course.instructors.remove(teacher)
    course.save()

    serializer = CourseSerializer(course)
    return Response(serializer.data)






