import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User  # Replace with your user model


logger = logging.getLogger("myLogger")


class EmailVerificationView(APIView):
    def get(self, request, verification_token):
        try:
            user = User.objects.get(reset_token=verification_token)
        except User.DoesNotExist:
            logger.error(
                "Invalid verification token.",
                extra={
                    'user': 'Anonymous'
                }
            )
            return Response(
                {'error': "Invalid verification token."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.is_active = True
        user.reset_token = None
        user.save()
        logger.error(
            "Email Verified Successfully.",
            extra={
                'user': user.id
            }
        )

        return Response({"message": "Email verified successfully"})
