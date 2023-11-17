import random
import string
import logging
import datetime
from apis.utils import *
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from apis.courses.models import Course
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from apis.users.models import User, AnonymousUser
from apis.courses.serializers import CourseSerializer
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from apis.users.serializers import UserSerializer, UserUpdateSerializer


logger = logging.getLogger("myLogger")

logging.basicConfig(filename='app.log', level=logging.DEBUG) 



class CourseViewSet(viewsets.ModelViewSet):

    queryset = Course.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = CourseSerializer



    
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
                    print("0")
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
                    print("1")
                    
                    # Create course
                    logging.debug('Your message here')
                    course = course_serializer.save(created_by=user)
                    print("2")


                    headers = self.get_success_headers(course_serializer.data)
                    print("3")
                    
                    logger.info(
                        "Student created successfully!",
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



    


