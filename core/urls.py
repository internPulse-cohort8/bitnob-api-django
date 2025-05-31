from django.contrib import admin
from django.urls import path, include
from virtual_card.views import home

urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path("api/v1/", include("virtual_card.urls")),
]
