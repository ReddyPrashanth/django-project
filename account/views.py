from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='/account/login')
def account(request, user_id):
    return render(request, 'account/profile.html')
