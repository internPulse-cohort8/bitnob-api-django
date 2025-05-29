import requests #HTTP library for Python, used for making web requests (like GET, POST, etc.) to external APIs or websites.
from decouple import config
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET'])              #Decorators are a way to modify or enhance functions. It tells that this list_cards view should only respond to HTTP GET requests. no POST, DELETE.
def list_cards(request):        #the list_cards function receives an HttpRequest object "request" as its first argument and it contains information about the incoming HTTP request. It assigns the endpoint for the Bitnob API that is used to list virtual cards
    url = "https://sandboxapi.bitnob.co/api/v1/virtualcards/cards"
    api_key = settings.BITNOB_API_KEY
    headers = {                                             
        "Authorization": f"Bearer {api_key}",     #The Bitnob uses this to verify that your application is authorized to make the request

        "Accept": "application/json"        #this line tells the Bitnob API that your application prefers to recieve the response in JSON format.
    }                                       
    response = requests.get(url, headers=headers)           #This is where the actual HTTP GET request is made

    if response.status_code == 200:             #If the request was successful (status code 200)
        return Response(response.json(), status=status.HTTP_200_OK)
    else:
        return Response({
            "status": "error",
            "message": "Failed to fetch cards",
            "details": response.json()
        }, status=response.status_code)


