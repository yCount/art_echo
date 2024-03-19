from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from artecho.forms import UserForm, UserProfileForm, LoginForm, SignUpForm, ImageForm, ProfileForm
from artecho.models import User, Image, Category, User
from django.views.generic import ListView
from django.db import models
from django.contrib.auth.decorators import login_required


def index(request):
    display_images = Image.objects.order_by('-likes')[:10]
    context = {
        'display_images': display_images,
    }
    return render(request, 'artecho/index.html', context)

# added for html test viewing:
def card(request):
    return render(request, 'artecho/base-card.html')

def add_root(request):
    return render(request, 'artecho/add-root.html')

def profile(request):
    return render(request, 'artecho/profile.html')

def profile_edit(request):
        return render(request, 'artecho/profile-edit.html')
  
def search_results(request):
    return render(request, 'artecho/search-results.html')
# html test views end here---

def about(request):
    context_dict = {'boldmessage': "This is about ArtEcho"}
    print(request.method)
    print(request.user)
    return render(request, 'artecho/about.html', context=context_dict)

def tree_view(request, user_name, image_title):
    # Reconstruct the slug from user_name and image_title
    slug = f"{user_name}-{image_title}"
    image = Image.objects.filter(slug=slug).first()

    if image is None:
        raise Http404("Image does not exist")

    context = {
        'image': image,
    }
    return render(request, 'artecho/tree-view.html', context)

def profile(request, slug):
    user = get_object_or_404(User, slug=slug)
    return render(request, 'artecho/profile.html', {'user': user})

def profile_edit(request):
    return render(request, 'artecho/profile-edit.html')

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

def user_logout(request):
    logout(request)
    return(redirect(reverse('artecho:index')))

def signup(request):
    registered = False

    if request.method == 'POST':
        
        user_form = SignUpForm(request.POST)
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

            return redirect(reverse('artecho:profile_edit'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = SignUpForm()
        profile_form = UserProfileForm()

    return render(request,
                  'artecho/signup.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'signedup': registered})
def add_root(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.save()
            return redirect(reverse('artecho:index'))
        else:
            print(form.errors)
    else:
        form = ImageForm()
    return render(request, 'artecho/add-root.html', {'form': form})
   
def search_results(request):
    query = request.GET.get('q')
    
    # Search for both users and images
    users = User.objects.filter(username__icontains=query) if query else []
    
    # Filter categories that match the query
    categories = Category.objects.filter(name__icontains=query) if query else []
    
    # Get images associated with matching categories
    images = Image.objects.filter(category__in=categories) if categories else []


    image_search_results = Image.objects.filter(name__icontains=query) if query else []
    
    return render(request, 'artecho/search_results.html', {'users': users, 'images': images,'image_search_results': image_search_results, 'query': query})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'artecho/profile-edit.html', {'form': form})

def profile(request, slug):
    user = User.objects.get(slug=slug)  # Fetch the User object
    return render(request, 'artecho/profile.html', {'user': user})  # Pass the User object to the template