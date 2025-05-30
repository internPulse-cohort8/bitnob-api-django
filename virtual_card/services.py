import requests
import uuid
from django.conf import settings

BITNOB_BASE_URL = settings.BITNOB_BASE_URL
BITNOB_API_KEY = settings.BITNOB_API_KEY

headers = {
        "Authorization": f"Bearer {BITNOB_API_KEY}",
        "accept": "application/json",
        "Content-Type": "application/json",
    }

def create_virtual_card(customer_email, first_name, last_name, card_brand, card_type, amount):
    url = f"{BITNOB_BASE_URL}/virtualcards/create"
    payload = {
        "customerEmail": customer_email,
        "firstName": first_name,
        "lastName": last_name,
        "cardBrand": card_brand,
        "cardType": card_type,
        "amount": amount,
        "reference": str(uuid.uuid4()),  # unique reference for tracking
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def fund_virtual_card(card_id, amount, reference):
    url = f"{BITNOB_BASE_URL}/virtualcards/topup"
    data = {
        "cardId": card_id,
        "amount": amount,
        "reference": reference
    }
    response = requests.post(url, json=data, headers=headers)
    return response.status_code, response.json()


def get_card_transactions(bitnob_card_id, page=1):
    url = f"{BITNOB_BASE_URL}/virtualcards/cards/{bitnob_card_id}/transactions"
    params = {
        "page": page,
    }
    response = requests.get(url, params=params, headers=headers)
    return response.json()

def list_cards(page=1):        #the list_cards function receives an HttpRequest object "request" as its first argument and it contains information about the incoming HTTP request. It assigns the endpoint for the Bitnob API that is used to list virtual cards
    url = f"{BITNOB_BASE_URL}/virtualcards/cards"
    params = {
        "page": page,
    }                            
    response = requests.get(url, params=params, headers=headers)           #This is where the actual HTTP GET request is made
    return response.json()
    
    