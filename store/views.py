from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm

def category_summary(request):
  categories = Category.objects.all()

  return render(request, "category_summary.html", {"categories":categories})

def category(request, cat):
  # replace category name hyphens with spaces 
  cat = cat.replace('-', ' ')

  try:
    category = Category.objects.get(name=cat)
    products = Product.objects.filter(category=category)
    return render(request, 'category.html', {'products': products, 'category': category})
  except:
    messages.success(request, ('This category does not exist.'))
    return redirect('home')

def product(request, pk):
  product = Product.objects.get(id=pk)
  return render(request, 'product.html', {'product': product})

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
  form = SignUpForm()
  if request.method == "POST":
    form = SignUpForm(request.POST);
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      # log user in
      user = authenticate(username=username, password=password)
      login(request, user)
      messages.success(request, ('You have registered succesfully!'))
      return redirect('home')
    else:
      messages.success(request, ('There was a problem registering your account, please try again.'))
      return redirect('register')

  else:
    return render(request, 'register.html', {'form': form})
  