import os
import tempfile
from io import BytesIO
from django.conf import settings
from django.utils import timezone
from apis.users.models import User
from datetime import datetime, timedelta
from apis.payments.models import UserPayment
from apis.payments.paypal import check_paypal_order



def check_paypal_payments():
    # retention_period = timedelta(days=30)
    pending_paypal_payments = UserPayment.objects.filter(has_paid=False, status="pending", payment_method="paypal")

    for payment in pending_paypal_payments:
        print(payment)
        txn_id = payment.paypal_checkout_id
        
        client_id = settings.PAYPAL_CLIENT_ID
        client_secret = settings.PAYPAL_CLIENT_SECRET
        
        response = check_paypal_order(client_id=client_id, client_secret=client_secret, txn_id=txn_id)
        print("tyron")
        print(response.status_code)
        if response.status_code == 404:
            payment.status = "failed"
            payment.save()
            
            # # Parse the JSON response to extract the access token
            # access_token = response.json().get('access_token')
            # return access_token
        
        




