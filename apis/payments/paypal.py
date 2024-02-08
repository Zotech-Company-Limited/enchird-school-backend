import requests, json, pprint
from django.conf import settings
from requests.auth import HTTPBasicAuth



def get_paypal_access_token(client_id, client_secret):
    # PayPal OAuth 2.0 Token Endpoint
    token_url = settings.AUTH_URL

    # PayPal API credentials
    auth = HTTPBasicAuth(client_id, client_secret)

    # Token request payload
    data = {
        'grant_type': 'client_credentials'
    }

    # Make the request to obtain the access token
    response = requests.post(token_url, auth=auth, data=data)

    if response.status_code == 200:
        # Parse the JSON response to extract the access token
        access_token = response.json().get('access_token')
        return access_token
    else:
        # Print the error details if the request fails
        print(f"Failed to get access token. Status code: {response.status_code}")
        print(response.text)
        return None
    
    
    
def create_paypal_order(client_id, client_secret, amount, currency='USD'):
    # PayPal API credentials
    auth = HTTPBasicAuth(client_id, client_secret)

    # PayPal Orders API endpoint
    orders_url = settings.ORDER_URL

    # Order creation payload
    data = {
        "intent": "CAPTURE",
        "purchase_units": [
            {
                "amount": {
                    "currency_code": currency,
                    "value": str(amount)
                },
                "redirect_urls": {
                    "return_url": return_url,
                    "cancel_url": cancel_url
                }
            }
        ]
    }

    # Make the request to create the order
    response = requests.post(orders_url, auth=auth, json=data, headers={'Content-Type': 'application/json'})

    if response.status_code == 201:
        # Parse the JSON response to extract the order ID
        order_id = response.json().get('id')
        # return order_id
        print(response.json())
        return response.json()
    else:
        # Print the error details if the request fails
        print(f"Failed to create order. Status code: {response.status_code}")
        print(response.text)
        return None
    
    