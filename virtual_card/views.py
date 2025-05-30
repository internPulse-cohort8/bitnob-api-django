from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .services import create_virtual_card, fund_virtual_card
from .models import VirtualCard


class CreateVirtualCardView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data

        customer_email = data.get("customerEmail")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        card_brand = data.get("cardBrand", "visa")
        card_type = data.get("cardType", "virtual")
        amount = data.get("amount")

        if not all([customer_email, first_name, last_name, amount]):
            return Response(
                {"detail": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        result = create_virtual_card(customer_email, first_name, last_name, card_brand, card_type, amount)

        if result.get("status"):
            card_data = result.get("data", {})
            # Save card in DB
            card = VirtualCard.objects.create(
                user=request.user,
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
    permission_classes = [IsAuthenticated]

    def post(self, request):
        card_id = request.data.get("cardId")
        amount = request.data.get("amount")
        reference = request.data.get("reference")

        if not all([card_id, amount, reference]):
            return Response(
                {"detail": "Missing required fields"},
                status=status.HTTP_400_BAD_REQUEST
            )

        status_code, result = fund_virtual_card(card_id, amount, reference)
        return Response(result, status=status_code)
