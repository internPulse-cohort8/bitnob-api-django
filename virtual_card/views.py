from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import get_user_model
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status

from .services import create_virtual_card, fund_virtual_card, get_card_transactions, list_cards
from .models import VirtualCard

from django.urls import reverse

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
        permission_classes = [AllowAny]

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
        permission_classes = [AllowAny]

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

    
class GetCardTransactionsView(APIView):
    """
    API endpoint to retrieve transactions for a specific virtual card.
    """
    def get(self, request, bitnob_card_id, *args, **kwargs):
        try:
            virtual_card_record = VirtualCard.objects.get(bitnob_card_id=bitnob_card_id)
        except VirtualCard.DoesNotExist:
            return Response(
                {"detail": "Virtual card not found in your system."},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            print(f"Error checking internal card record: {e}")
            return Response(
                {"detail": "An internal error occurred while verifying card internally."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        

        try:
             bitnob_transactions_data = get_card_transactions(
                bitnob_card_id=bitnob_card_id
             )
             
             transactions_list = bitnob_transactions_data.get('data', [])
             
             return Response(transactions_list, status=status.HTTP_200_OK)

        except requests.exceptions.HTTPError as e:
            error_message = f"Bitnob API error: {e}"
            if e.response is not None:
                try:
                    error_json = e.response.json()
                    error_message = error_json.get('message', error_message)
                    print(f"Bitnob error details: {error_json}")
                except Exception:
                    pass # Couldn't parse error JSON
            print(f"Error fetching card transactions from Bitnob: {e}")
            return Response(
                {"detail": f"Failed to retrieve transactions: {error_message}"},
                status=e.response.status_code if e.response else status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except requests.exceptions.RequestException as e:
            print(f"Network error contacting Bitnob API: {e}")
            return Response(
                {"detail": f"Network error contacting payment provider: {e}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return Response(
                {"detail": f"An unexpected error occurred: {e}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class ListCardsView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            page = request.GET.get("page", 1)
            cards = list_cards(page=page)
            return Response(cards)
        except Exception as e:
            return Response({"error": str(e)}, status=500)


def home(request):
    html = f"""
    <html>
        <head><title>Payment Gateway API</title></head>
        <body>
            <h1>Welcome to the Payment Gateway API</h1>
            <ul>
                <li><a href="{reverse('create-card')}">Create Card</a></li>
                <li><a href="{reverse('topup-virtual-card')}">Top Up</a></li>
                <li><a href="{reverse('list_cards')}">List Cards</a></li>
                <li> To use get-card-transactions, use virtualcards/bitnob_card_id/transactions/ Remember to replace bitnob_card_id with your card ID generated at the create-card endpoint </li?
            </ul>
        </body>
    </html>
    """
    return HttpResponse(html)




