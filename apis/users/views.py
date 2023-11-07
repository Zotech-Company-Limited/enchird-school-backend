# import logging
# from uuid import uuid4
# from django.utils import timezone
# import datetime
# from rest_framework.response import Response
# from django.contrib.auth.models import Permission
# from rest_framework.views import APIView
# from rest_framework import status
# from django.contrib.auth import get_user_model
# from rest_framework.authtoken.models import Token
# from accounts.models.user import User, Group
# from accounts.serializers.vendor import VendorSerializer, VendorUpdateSerializer
# from accounts.models.vendor import Vendor, VendorCategory, VendorType
# from accounts.serializers.user import UserSerializer
# from rest_framework.authtoken.views import ObtainAuthToken
# from urllib.parse import urlsplit
# from accounts.utils import *
# from accounts.serializers.authtokenserializer import PermissionSerializer, LoginSerializer, CustomAuthTokenSerializer

# logger = logging.getLogger("myLogger")



# class Authview(ObtainAuthToken):
#     """Docstring for class."""
#     serializer_class = CustomAuthTokenSerializer

#     # def post(self, request,  *args, **kwargs):
#     #     """Docstring for function."""
#     #     try:
#     #         serializer = LoginSerializer(
#     #             data=request.data
#     #         )
#     #         serializer.is_valid(raise_exception=True)

#     #         data = {
#     #             "username": serializer.validated_data['phone'],
#     #             "password": serializer.validated_data['password'],
#     #             "role": serializer.validated_data['role']
#     #         }
#     #         serializer = self.serializer_class(
#     #             data=data,
#     #             context={'request': request}
#     #         )
#     #         serializer.is_valid(raise_exception=True)
            
#     #         user = serializer.validated_data['user']
#     #         user.reset_token = None

#     #         if user.failed_attempts >= 5:
#     #             logger.error(
#     #                 "Your account has been locked",
#     #                 extra={
#     #                     'vendor': user.vendor,
#     #                     'user': user.id
#     #                 }
#     #             )
#     #             return Response(
#     #                 {'message': 'Your account has been locked, contact admin'}, 
#     #                     status=status.HTTP_412_PRECONDITION_FAILED)
   
#     #         if user.reset_token is not None:
#     #             logger.error(
#     #                 "Please validate your account",
#     #                 extra={
#     #                     'vendor': user.vendor,
#     #                     'user': user.id
#     #                 }
#     #             )
#     #             return Response(
#     #                 {
#     #                     "message": "Please validate your account"
#     #                 },
#     #                 status.HTTP_400_BAD_REQUEST
#     #             )
            
#     #         user.last_login = timezone.now()
#     #         user.save()

#     #         # Fetch group permissions and user permissions
#     #         group_permissions = Permission.objects.filter(group__user=user)
#     #         user_permissions = user.user_permissions.all()
            
#     #         # Serialize the permissions
#     #         group_permissions_serializer = PermissionSerializer(group_permissions, many=True)
#     #         user_permissions_serializer = PermissionSerializer(user_permissions, many=True)

#     #         token, created = Token.objects.get_or_create(user=user)
#     #         if user.vendor is None:
#     #             vendor = ''
#     #             vendor_id = ''
#     #         else:
#     #             vendor = user.vendor.name
#     #             vendor_id = user.vendor.id
#     #         if user.is_super():
#     #             role = "superAdmin"
#     #         elif user.is_staff:
#     #             role = "Vendor"
#     #         elif user.is_client:
#     #             role = "client"
#     #         elif user.is_delivery:
#     #             role = "livreur"
#     #         else:
#     #             role = "user"
            
#     #         vendor_data = None
#     #         if user.vendor is not None:
#     #             ser_data = VendorUpdateSerializer(user.vendor).data
#     #             vendor_data = get_vendor(user.vendor, ser_data)
#     #         else:
#     #             resto_data = None

#     #         logger.info(
#     #             "User returned sucessfully.",
#     #             extra={
#     #                 'vendor': vendor,
#     #                 'user': user.id
#     #             }
#     #         )
#     #         serializer = UserSerializer(user).data
#     #         picture = None
#     #         if user.picture is not None:
#     #             picture = serializer['picture']
                
#     #         return Response({
#     #             'token': token.key,
#     #             'user_id': user.pk,
#     #             'temporary_password': user.temporary_password,
#     #             'activated': user.activated,
#     #             'phone': user.phone,
#     #             'email': user.email,
#     #             'last_name': user.last_name,
#     #             'first_name': user.first_name,
#     #             'vendor_id': vendor_id,
#     #             'role': role,
#     #             'is_active': user.is_active,
#     #             'groups': serializer['groups'],
#     #             'is_client': user.is_client,
#     #             'vendor_data': vendor_data,
#     #             'user/group_permissions': group_permissions_serializer.data,
#     #         })

#     #     except Exception as e:
#     #         logger.error(
#     #             str(e),
#     #             extra={
#     #                 'vendor': None,
#     #                 'user': None
#     #             }
#     #         ) 
#     #         return Response(
#     #             {'message': str(e)},
#     #             status=status.HTTP_412_PRECONDITION_FAILED)


#     def get_cleaned_url(drink):
#         # Parse the drink picture URL
#         parsed_url = urlsplit(drink)

#         # Reconstruct the URL without the query string
#         cleaned_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

#         return cleaned_url
    

#     def get_cleaned_urls(urls):
#         cleaned_urls = []

#         for url in urls:
#             parsed_url = urlsplit(url)

#             # Reconstruct the URL without the query string
#             cleaned_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"
#             cleaned_urls.append(cleaned_url)

#         return cleaned_urls

