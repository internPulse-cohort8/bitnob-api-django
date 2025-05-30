import json
import hmac
import os
from hashlib import sha512
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from virtual_card.models import VirtualCard

User = get_user_model()

class VirtualCardTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_url = reverse('create-card')
        self.topup_url = reverse('topup-virtual-card')
        self.webhook_url = "/api/v1/webhooks/bitnob/virtualcards/"

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="strongpassword123"
        )
        self.client.force_authenticate(user=self.user)

    def test_create_virtual_card_endpoint(self):
        payload = {
            "customerEmail": "abc@gmail.com",
            "firstName": "Nana",
            "lastName": "Mends",
            "amount": 500,
            "cardBrand": "visa",
            "cardType": "giftcard",
            "reference": "'49e35586-be8b-462d-a17c-f4285dfb45f2'",
        }
        response = self.client.post(self.create_url, payload, format='json')
        print(response.status_code)
        print(response.json())
        self.assertIn(response.status_code, [200, 201, 400])

    def test_fund_virtual_card_endpoint(self):
        payload = {
            "cardId": '18d02b6b-a924-4edf-b27a-3a3d5539853c',
            "amount": 1000,
            "reference": "bf02ea65-d200-46ff-afc6-673287a0d2ef"
        }
        response = self.client.post(self.topup_url, payload, format='json')
        print(response.status_code)
        print(response.json())
        self.assertIn(response.status_code, [200, 201, 400])