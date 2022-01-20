from django.shortcuts import render
from django.http import JsonResponse
import re
import json

# Create your views here.

def home(request):
    return render(request, 'core/home.html')

def portfolio(request):
    return render(request, 'core/portfolio.html')

def contact(request):
    data = json.loads(request.body)
    if not (bool(data.get('name', False)) and bool(data.get('email', False)) and bool(data.get('message', False))):
        return JsonResponse({'error': 'All fields are required.'}, status=400)
    email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    if(not email.match(data['email'])):
        return JsonResponse({'error': 'Email is not valid. Provide a valid email address.'}, status=400)
    return JsonResponse(request.POST, status=200)