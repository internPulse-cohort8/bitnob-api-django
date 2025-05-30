from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .services import create_virtual_card, fund_virtual_card
from .models import VirtualCard

User = get_user_model()

def get_mock_user():
    """Used as auth is not yet wired up, only in DEBUG mode"""
    user, _ = User.objects.get_or_create(
        email="testuser@example.com",
        defaults={"first_name": "Test", "last_name": "User", "username": "testuser"}
    )
    return user


class CreateVirtualCardView(APIView):
    # Enforce auth only when DEBUG is False (i.e., in production)
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Get or mock user
        user = request.user
        if user.is_anonymous and settings.DEBUG:
            user = get_mock_user()

        customer_email = user.email
        first_name = user.first_name or "John"
        last_name = user.last_name or "Doe"

        card_brand = data.get("cardBrand", "visa")
        card_type = data.get("cardType", "virtual")
        amount = data.get("amount")

        if not amount:
            return Response(
                {"detail": "Amount is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = create_virtual_card(
            customer_email, first_name, last_name,
            card_brand, card_type, amount
        )

        if result.get("status"):
            card_data = result.get("data", {})

            card = VirtualCard.objects.create(
                user=user,
                bitnob_card_id=card_data.get("id"),
                card_brand=card_data.get("cardBrand", ""),
                card_type=card_data.get("cardType", ""),
                status=card_data.get("createdStatus", "pending"),
                reference=card_data.get("reference", ""),
            )

            return Response({
                "detail": "Card creation in progress",
                "card": {
                    "id": card.bitnob_card_id,
                    "status": card.status,
                    "reference": card.reference,
                }
            }, status=status.HTTP_201_CREATED)

        return Response(result, status=status.HTTP_400_BAD_REQUEST)


class FundVirtualCardView(APIView):
    if not settings.DEBUG:
        permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        # Get or mock user
        user = request.user
        if user.is_anonymous and settings.DEBUG:
            user = get_mock_user()

        card_id = data.get("cardId")
        amount = data.get("amount")
        reference = data.get("reference")

        if not all([card_id, amount, reference]):
            return Response(
                {"detail": "cardId, amount, and reference are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        status_code, result = fund_virtual_card(card_id, amount, reference)
        return Response(result, status=status_code)
