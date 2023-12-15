import random
import string
import logging
import datetime
import requests
from io import BytesIO
from apis.utils import *
from django.db.models import Q
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from apis.users.models import User, AnonymousUser
from .models import Applicant, AchievementDocument
from apis.students.serializers import StudentSerializer
from rest_framework.decorators import permission_classes
from django.contrib.auth.models import Group, Permission
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import ApplicantSerializer, AchievementDocumentSerializer

logger = logging.getLogger("myLogger")


# Create your views here.
class ApplicantViewSet(viewsets.ModelViewSet):

    queryset = Applicant.objects.all().filter(
                is_deleted=False,
                ).order_by('-created_at')
    serializer_class = ApplicantSerializer


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
            
            # Include achievement documents in each applicant's serialized data
            for data in serializer.data:
                applicant_id = data['applicant_id']
                achievement_documents = AchievementDocument.objects.filter(applicant__applicant_id=applicant_id)
                data['past_achievement_documents'] = AchievementDocumentSerializer(achievement_documents, many=True).data
                
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)

        # Include achievement documents in each applicant's serialized data
        for data in serializer.data:
            applicant_id = data['applicant_id']
            achievement_documents = AchievementDocument.objects.filter(applicant__applicant_id=applicant_id)
            data['past_achievement_documents'] = AchievementDocumentSerializer(achievement_documents, many=True).data

        logger.info(
            "List of applicants returned successfully.",
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
            instance = Applicant.objects.get(id=kwargs['pk'])
        except Applicant.DoesNotExist:
            logger.error(
                "Applicant not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Applicant Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Retrieve achievement documents related to the applicant
        achievement_documents = AchievementDocument.objects.filter(applicant=instance)
        serializer = self.get_serializer(instance)
        serialized_data = serializer.data

        # Include serialized achievement documents in the response
        serialized_data['past_achievement_documents'] = AchievementDocumentSerializer(achievement_documents, many=True).data

        # serializer = self.get_serializer(instance)
        logger.info(
            "Applicant details returned successfully!",
            extra={
                'user': request.user.id
            }
        )
        return Response(serialized_data)

    
    def create(self, request, *args, **kwargs):
        
        user = request.user
        try:
            with transaction.atomic():
                applicant_serializer = self.get_serializer(data=request.data)
                if applicant_serializer.is_valid(raise_exception=True):
                    
                    # Create applicant
                    applicant = applicant_serializer.save()

                    scanned_id_document_url = request.data.get("scanned_id_document_url")

                    # Extract documents data from the request
                    documents_data = request.data.get('documents', [])


                    # Handling documents separately
                    achievement_documents = []
                    for doc_data in documents_data:
                        name = doc_data.get('name')
                        document_path = doc_data.get('document_path')

                        # Create and save AchievementDocument object
                        achievement = AchievementDocument.objects.create(
                            applicant=applicant,
                            document=document_path,
                            name=name
                        )
                        achievement_documents.append(achievement)

                    #Serialize and return response
                    serialized_data = applicant_serializer.data
                    
                    # Include serialized achievement documents in the response
                    serialized_data['documents'] = AchievementDocumentSerializer(achievement_documents, many=True).data

                    headers = self.get_success_headers(applicant_serializer.data)
                    
                    logger.info(
                        "Applicant created successfully!",
                        extra={
                            'user': user.id
                        }
                    )
                    return Response(
                        serialized_data,
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


    # def update(self, request, *args, **kwargs):
        
    #     user = self.request.user
    #     if not user.is_authenticated:
    #         logger.error(
    #             "You must provide valid authentication credentials.",
    #             extra={
    #                 'user': 'Anonymous'
    #             }
    #         )
    #         return Response(
    #             {"error": "You must provide valid authentication credentials."},
    #             status=status.HTTP_401_UNAUTHORIZED
    #         )

    #     if request.user.is_admin is False:
    #         logger.warning(
    #             "You do not have the necessary rights!",
    #             extra={
    #                 'user': request.user.id
    #             }
    #         )
    #         return Response(
    #             {"error": "You do not have the necessary rights"},
    #             status.HTTP_403_FORBIDDEN
    #         )

    #     partial = kwargs.pop('partial', True)
    #     try:
    #         instance = Applicant.objects.get(id=kwargs['pk'])
    #     except Applicant.DoesNotExist:
    #         logger.error(
    #             "Applicant not Found.",
    #             extra={
    #                 'user': user.id
    #             }
    #         )
    #         return Response(
    #             {"error": "Applicant Not Found."},
    #             status=status.HTTP_404_NOT_FOUND
    #         )
    #     print(instance)
        
    #     applicant_serializer = self.get_serializer(instance, 
    #             data=request.data,
    #             partial=partial)
    #     if applicant_serializer.is_valid() is True:

    #         applicant_serializer.save(modified_by=user)

    #         if getattr(instance, '_prefetched_objects_cache', None):
    #             instance._prefetched_objects_cache = {}
    #         logger.info(
    #             "Applicant Info modified successfully!",
    #             extra={
    #                 'user': request.user.id
    #             }
    #         )
    #         return Response(applicant_serializer.data)
    #     else:
    #         logger.error(
    #             str(applicant_serializer.errors),
    #             extra={
    #                 'user': request.user.id
    #             }
    #         )
    #         return Response(applicant_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            instance = Applicant.objects.get(id=kwargs['pk'])
        except Applicant.DoesNotExist:
            logger.error(
                "Applicant not Found.",
                extra={
                    'user': user.id
                }
            )
            return Response(
                {"error": "Applicant Not Found."},
                status=status.HTTP_404_NOT_FOUND
            )
        instance.is_deleted = True
        instance.save()

        logger.info(
            "Applicant marked as deleted successfully",
            extra={
                'user': user.id
            }
        )
        return Response(
            {"message": "Applicant marked as Deleted"},
            status=status.HTTP_200_OK)

