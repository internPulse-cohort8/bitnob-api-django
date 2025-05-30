from django.urls import path
from .views import CreateVirtualCardView, FundVirtualCardView

urlpatterns = [
    path("virtualcards/create", CreateVirtualCardView.as_view(), name="create-card"),
    path('virtualcards/topup', FundVirtualCardView.as_view(), name='topup-virtual-card'),
]
