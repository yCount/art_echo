from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from artecho.forms import UserProfileForm, ImageForm, ProfileForm, UserForm
from artecho.models import Image, Category, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404

def index(request):
    context_dict = {'boldmessage': 'Welcome to ArtEcho!'}
    display_images = Image.objects.order_by('-likes')[:10]
    context_dict['display_images'] = display_images
    return render(request, 'artecho/index.html', context=context_dict)

# added for html test viewing:
def card(request):
    return render(request, 'artecho/base-card.html')

# html test views end here---

def about(request):
    context_dict = {'boldmessage': "This is about ArtEcho"}
    print(request.method)
    print(request.user)
    return render(request, 'artecho/about.html', context=context_dict)

def tree_view(request):
    return render(request, 'artecho/tree-view.html')

def user_logout(request):
    logout(request)
    return(redirect(reverse('artecho:index')))


def signup(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'artecho/signup.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
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
        form = AuthenticationForm()
    return render(request, 'artecho/login.html', {'form': form})
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
def profile_edit(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    profile = UserProfile.objects.get(slug=slug)
    if request.user != profile.user:
        return redirect('login')
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', slug=slug)
    else:
        form = ProfileForm(instance=user_profile)
    return render(request, 'artecho/profile-edit.html', {'form': form})

def profile(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    return render(request, 'artecho/profile.html', {'user_profile': user_profile})