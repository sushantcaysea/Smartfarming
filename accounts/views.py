from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            next_page = request.GET.get('next', 'core:index')
            return redirect(next_page)
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'accounts/login.html')

def register_view(request):
    if request.user.is_authenticated:
        return redirect('core:index')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('accounts:register')
        
        user = User.objects.create_user(username=username, password=password)
        user.save()
        
        messages.success(request, 'Registration successful! Please log in.')
        return redirect('accounts:login')
    
    return render(request, 'accounts/register.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:login')

def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        messages.info(request, 'If an account exists with that email, a reset link has been sent')
        return redirect('accounts:login')
    
    return render(request, 'accounts/forgot_password.html')
