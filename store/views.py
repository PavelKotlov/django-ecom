from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product


# Create your views here.
def home(request):
  products = Product.objects.all()

  return render(request, 'home.html', {'products':products})

def about(request):
  return render(request, 'about.html', {})

def login_user(request):
  # If login form was submitted process login request, else render login.html template.
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is not None:
      login(request, user)
      messages.success(request, ('You have been logged in succesfully'))
      return redirect('home')
    else:
      messages.success(request, ('Login unsuccessful'))
      return redirect('login')
    
  else:
    return render(request, 'login.html', {})

def logout_user(request):
  logout(request)
  messages.success(request, ('You have been logged out successfully.'))
  return redirect('home')

def register_user(request):
  return render(request, 'register.html', {})