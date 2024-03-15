from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.shortcuts import redirect
from artecho.forms import UserForm, UserProfileForm, LoginForm, SignUpForm


def index(request):
    context_dict = {'boldmessage': 'Welcome to ArtEcho!'}
    return render(request, 'artecho/index.html', context=context_dict)

# added for html test viewing:
def card(request):
    return render(request, 'artecho/base-card.html')

def add_root(request):
    return render(request, 'artecho/add-root.html')
# html test views end here---

def about(request):
    context_dict = {'boldmessage': "This is about ArtEcho"}
    print(request.method)
    print(request.user)
    return render(request, 'artecho/about.html', context=context_dict)

def tree_view(request):
    return render(request, 'artecho/tree-view.html')

def profile(request):
    return render(request, 'artecho/profile.html')

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