from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Product, Category, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm

def update_info(request):
  if request.user.is_authenticated:
    current_user = Profile.objects.get(user__id=request.user.id)
    form = UserInfoForm(request.POST or None, instance=current_user)

    if form.is_valid():
      form.save()
      
      messages.success(request, ('Profile info saved successfully'))
      return redirect('home')
    
    return render(request, 'update_info.html', {'form':form})
  else:
    messages.success(request, ('Access denied, please login first'))
    return redirect('login')

def update_password(request):
  if request.user.is_authenticated:
    current_user = request.user

    if request.method == "POST":
      form = ChangePasswordForm(current_user, request.POST)
      if form.is_valid():
        form.save()
        messages.success(request, ('Password updated successfully'))
        login(request, current_user)
        return redirect('home')
      else:
        for error in list(form.errors.values()):
          messages.error(request, error)
          return redirect('update_password')

    else:
      form = ChangePasswordForm(current_user)
      return render(request, 'update_password.html', {'form':form})
  else:
    messages.success(request, ('Access denied, please login first'))
    return redirect('login')

def update_user(request):
  if request.user.is_authenticated:
    current_user = User.objects.get(id=request.user.id)
    user_form = UpdateUserForm(request.POST or None, instance=current_user)

    if user_form.is_valid():
      user_form.save()
      login(request, current_user)
      messages.success(request, ('Profile details saved successfully'))
      return redirect('home')
    
    return render(request, 'update_user.html', {'user_form':user_form})
  else:
    messages.success(request, ('Access denied, please login first'))
    return redirect('home')
  
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
  if request.user.is_authenticated:
    return redirect('home')
  
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
      messages.success(request, ('You have registered succesfully! Please add your billing information below.'))
      return redirect('update_info')
    else:
      messages.success(request, ('There was a problem registering your account, please try again.'))
      return redirect('register')

  else:
    return render(request, 'register.html', {'form': form})
  
def search(request):
  if request.method == 'POST':
    searched = request.POST['searched']

    if searched:
      products = Product.objects.filter(name__icontains=searched)
      if products:
        return render(request, 'search.html', {'products':products})
      
      messages.success(request, ('No products matched your search, please try a different term'))
      return render(request, 'search.html', {})

    messages.success(request, ('Please enter a search term'))
    return render(request, 'search.html', {})

  else:
    return render(request, 'search.html', {})