from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.shortcuts import redirect



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

def user_login(request):
    if request.method == 'POST':
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
        return render(request, 'artecho/login.html')