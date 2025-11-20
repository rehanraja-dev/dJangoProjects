from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib import messages
from .models import StudentProfile

def is_principal(user):
    return user.is_superuser

@login_required(login_url='login')
def profile_view(request):
    if request.user.is_superuser:
        return redirect('all_students')
    print(request.user)
    profile = StudentProfile.objects.get(user=request.user)
    print(profile)
    if request.method == 'POST':
        profile.phone = request.POST.get('phone')
        profile.department = request.POST.get('department')
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    return render(request, 'users/profile.html', {'profile': profile})

@user_passes_test(is_principal, login_url='login')
def all_students(request):
    students = StudentProfile.objects.all()
    return render(request, 'users/all_students.html', {'students': students})


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in!!')
        return redirect('profile')
    
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            StudentProfile.objects.create(user=user)
            login(request, user)
            messages.success(request, 'Signup successful! Welcome.')
            return redirect('profile')
        else:
            messages.error(request, 'Signup failed. Please correct the error below.')
            
    else:
        form = UserCreationForm()

    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
          return redirect('all_students')
        return redirect('profile')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request,f"welcomeback {user.username}")
            if user.is_superuser:
                return redirect('all_students')
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials.')
    
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form' : form})

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')


