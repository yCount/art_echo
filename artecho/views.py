from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect
from django.views.generic import ListView
from artecho.forms import UserForm, UserProfileForm, LoginForm
from django.db import models
from artecho.models import User, Image, Category


def index(request):
    context_dict = {'boldmessage': 'Welcome to ArtEcho!'}
    return render(request, 'artecho/index.html', context=context_dict)

# added for html test viewing:
def card(request):
    return render(request, 'artecho/base-card.html')

def add_root(request):
    return render(request, 'artecho/add-root.html')

def search_results(request):
    return render(request, 'artecho/search-results.html')

# html test views end here---

def about(request):
    context_dict = {'boldmessage': "This is about ArtEcho"}
    print(request.method)
    print(request.user)
    return render(request, 'artecho/about.html', context=context_dict)

def tree_view(request):
    return render(request, 'artecho/tree-view.html')

def profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, 'artecho/profile.html', {'user': user})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('artecho:index'))
                else:
                    return HttpResponse("Your artecho account is disabled.")
            else:
                print(f"Invalid login details: {username}, {password}")
                return HttpResponse("Invalid login details supplied.")
    else:
        form = LoginForm()
    return render(request, 'artecho/login.html', {'form': form})

def signup(request):
    registered = False

    if request.method == 'POST':
        
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'artecho/signup.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'signedup': registered})
   
def search_results(request):
    query = request.GET.get('q')
    
    # Search for both users and images
    users = User.objects.filter(username__icontains=query) if query else []
    
    # Filter categories that match the query
    categories = Category.objects.filter(name__icontains=query) if query else []
    
    # Get images associated with matching categories
    images = Image.objects.filter(category__in=categories) if categories else []
    
    return render(request, 'artecho/search_results.html', {'users': users, 'images': images, 'query': query})