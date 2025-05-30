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
