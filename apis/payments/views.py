import stripe
import logging
from .models import *
from django.conf import settings
from rest_framework import status
from apis.users.models import User
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserPaymentSerializer
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger("myLogger")



# Create your views here.
class StripeCheckoutSession(APIView):
    
    queryset = UserPayment.objects.all().filter()
    serializer_class = UserPaymentSerializer
    allowed_methods = ['post']
    
    def post(self, request, *args, **kwargs): 
        user = request.user 
        
        if not user.is_authenticated:
            logger.error( "You must provide valid authentication credentials.", extra={ 'user': 'Anonymous' } )
            return Response( {'error': "You must provide valid authentication credentials."}, status=status.HTTP_401_UNAUTHORIZED )

        if not user.is_a_student:
            logger.error( "Only students can make this request.", extra={ 'user': 'Anonymous' } )
            return Response( {'error': "Only students can make this request."}, status=status.HTTP_401_UNAUTHORIZED )

        print(user)
        stripe.api_key = settings.STRIPE_SECRET_KEY
        serializer = UserPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        amount = serializer.validated_data['amount']
        
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data':{
                            'currency': 'xaf',
                            'unit_amount': int(amount),
                            'product_data':{
                                'name': f'{user.first_name} {user.last_name} - Enchird Fee Payment',
                                },
                            },
                        
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url='http://127.0.0.1:8000/api/messaging',
                cancel_url='http://127.0.0.1:8000/api/messaging',
                customer_email=user.email,
                
            )
            # Create a new UserPayment instance
            user_payment = UserPayment(user=user)
            user_payment.amount = amount
            user_payment.stripe_checkout_id = checkout_session.id
            
            # Save the instance to the database
            user_payment.save()
            response_data = {
                'checkout_session_id': checkout_session.id,
                'checkout_session_url': checkout_session.url,
            }
            # return redirect(checkout_session.url, code=303)
            return Response(response_data)
            # client_secret = checkout_session.client_secret
            
            # return Response({'client_secret': client_secret})
        except Exception as e:
            logger.error( str(e), extra={ 'user': user.id })
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def stripe_webhook_view(request):
    user = request.user
    print(user)
    
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    endpoint_secret = settings.WEBHOOK_SECRET
    event = None

    try:
        event = stripe.Webhook.construct_event(
        payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)
    
    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
        session = event['data']['object'] #['id']
        customer_email = session['customer_details']['email']
        checkout_id = session['id']
        print(checkout_id) 
        
        print("tyron")
        print(customer_email)
        
        try:
            user = User.objects.get(email=customer_email)
            user_payment = UserPayment.objects.get(stripe_checkout_id=checkout_id)
            
            user_payment.has_paid = True
            user_payment.status = "successful"
            user_payment.save()
            
        except User.DoesNotExist:
            logger.error( "User not Found.", extra={ 'user': user.id } )
            # return Response( {"error": "Applicant Not Found."}, status=status.HTTP_404_NOT_FOUND )
        except UserPayment.DoesNotExist:
            logger.error( "User did not initiate a payment.", extra={ 'user': user.id } )
            

        print(session)

    # Passed signature verification
    return HttpResponse(status=200)


