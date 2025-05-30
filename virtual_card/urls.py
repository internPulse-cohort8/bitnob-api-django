from django.urls import path
from .views import CreateVirtualCardView, FundVirtualCardView, GetCardTransactionsView

urlpatterns = [
    path("virtualcards/create/", CreateVirtualCardView.as_view(), name="create-card"),
    path('virtualcards/topup/', FundVirtualCardView.as_view(), name='topup-virtual-card'),
    path('virtualcards/<str:bitnob_card_id>/transactions/', GetCardTransactionsView.as_view(), name='get-card-transactions'),
]
