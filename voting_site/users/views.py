from django.shortcuts import render
from .models import User

# Create your views here.
def register(request):
    return render(request, 'users/registration.html')
