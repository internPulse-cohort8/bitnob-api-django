from django.urls import path
from .views import list_cards

urlpatterns = [
    path('virtual_card/', list_cards, name='list_cards')            ##this is saying: if anyone visit /virtual_cards(as in makes a POST request) django should run the "list_cards" view
]