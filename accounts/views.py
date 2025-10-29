from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from .forms import UserRegistrationForm, UserLoginForm


@require_http_methods(["GET", "POST"])
def register_view(request):
    """
    User registration view.
    GET: Display registration form
    POST: Process registration and create user
    """
    if request.user.is_authenticated:
        # Already logged in, redirect to home
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in automatically after registration
            login(request, user)
            
            # Success message
            messages.success(
                request,
                f'Welcome {user.name}! Your account has been created successfully.'
            )
            
            # Redirect to home page
            return redirect('home')
        else:
            # Form has errors, they will be displayed in the template
            messages.error(
                request,
                'Please correct the errors below.'
            )
    else:
        form = UserRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@require_http_methods(["GET", "POST"])
def login_view(request):
    """
    User login view.
    GET: Display login form
    POST: Authenticate and log in user
    """
    if request.user.is_authenticated:
        # Already logged in, redirect to home
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')  # 'username' field contains email
            password = form.cleaned_data.get('password')
            
            # Authenticate user
            user = authenticate(request, email=email, password=password)
            
            if user is not None:
                # Login successful
                login(request, user)
                
                # Success message
                messages.success(request, f'Welcome back, {user.name}!')
                
                # Redirect to next page or home
                next_url = request.GET.get('next', 'home')
                return redirect(next_url)
            else:
                # Authentication failed
                messages.error(request, 'Invalid email or password.')
        else:
            # Form validation failed
            messages.error(request, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """
    User logout view.
    Logs out the user and redirects to home page.
    """
    user_name = request.user.name
    logout(request)
    messages.info(request, f'You have been logged out. Goodbye, {user_name}!')
    return redirect('home')


@login_required
def profile_view(request):
    """
    User profile view - placeholder for TICKET-008.
    Shows basic user information.
    """
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })