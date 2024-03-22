from django.shortcuts import render
from django.http import HttpResponse, FileResponse, Http404, JsonResponse
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
from datetime import datetime
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def index(request):
    try:
        display_images = Image.objects.order_by('-likes')[:30]
        user_profile=UserProfile.objects.get(user=request.user)
        context_dict = {'boldmessage': 'Welcome to ArtEcho!',
                        'user_profile': user_profile,
                        'display_images': display_images
                        }
    except:
        display_images = Image.objects.order_by('-likes')[:30]
        context_dict = {'boldmessage': 'Welcome to ArtEcho!',
                        'display_images': display_images
                        }
    return render(request, 'artecho/index.html', context=context_dict)


# added for html test viewing:
def card(request):
    return render(request, 'artecho/base-card.html')

  
def search_results(request):
    context = {}
    try:
        context['user_profile'] = UserProfile.objects.get(user=request.user)
    except:
        pass
    return render(request, 'artecho/search-results.html', context = context)
# html test views end here---

def about(request):
    context_dict = {'boldmessage': "This is about ArtEcho"}
    print(request.method)
    print(request.user)
    return render(request, 'artecho/about.html', context=context_dict)

def tree_view(request, user_name, image_title):
    slug = f"{user_name}-{image_title}"
    image = Image.objects.filter(slug=slug).first()


    if image is None:
        raise Http404("Image does not exist")
    

    context = {
        'image': image,
        'parent':image.parent,
        'children': Image.objects.filter(parent = image)
    }
    try:
        context['user_profile'] = UserProfile.objects.get(user=request.user)
    except:
        pass
    return render(request, 'artecho/tree-view.html', context)

def user_logout(request):
    logout(request)
    return(redirect(reverse('artecho:index')))

def signup(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
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
                           'registered': registered})

def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days >= 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        request.session['last_visit'] = last_visit_cookie
    
    request.session['visits'] = visits
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
                    response = redirect(reverse('artecho:index'))
                    response.set_cookie('auth_token', 'repsonse_token', max_age=3600)
                    return response
                else:
                    return HttpResponse("Your artecho account is disabled.")
            else:
                print(f"Invalid login details: {username}, {password}")
                return HttpResponse("Invalid login details supplied.")
    else:
        form = AuthenticationForm()
    return render(request, 'artecho/login.html', {'form': form})

@login_required
def add_root(request):
    
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.poster = request.user
            image.save()
            return redirect(reverse('artecho:index'))
        else:
            print(form.errors)
    else:
        form = ImageForm()
    return render(request, 'artecho/add-root.html', {'form': form, 'user_profile': UserProfile.objects.get(user=request.user)})

@login_required
def add_child(request, user_name, image_title):
    slug = f"{user_name}-{image_title}"
    parent = Image.objects.filter(slug=slug).first()

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.poster = request.user
            image.parent= parent
            image.save()
            return redirect(reverse('artecho:index'))
        else:
            print(form.errors)
    else:
        form = ImageForm()
    context = {'form': form, 'user_profile': UserProfile.objects.get(user=request.user), 'parent': parent}
    return render(request, 'artecho/add-child.html', context=context)


def search_results(request):
    query = request.GET.get('q')
    
    users = User.objects.filter(username__icontains=query) if query else []
    
    categories = Category.objects.filter(name__icontains=query) if query else []
    
    images = Image.objects.filter(category__in=categories) if categories else []

    image_search_results = Image.objects.filter(name__icontains=query) if query else []
    context = {'users': users, 'images': images,'image_search_results': image_search_results, 'query': query}
    try:
        context['user_profile'] = UserProfile.objects.get(user=request.user)
    except:
        pass
    
    return render(request, 'artecho/search_results.html', context=context)

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
    current_user_profile = get_object_or_404(UserProfile, slug=slug)
    current_user= current_user_profile.user
    images = Image.objects.filter(poster = current_user_profile.user)[:10]
    context_dict = {'current_user_profile': current_user_profile,
                    'current_slug': slug,
                    'images': images,
                    'current_user': current_user
                    }
    try:
        context_dict['user_profile'] = UserProfile.objects.get(user=request.user)
    except:
        pass
    return render(request, 'artecho/profile.html', context_dict)

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    if request.user != image.poster:
        return redirect('index')
    if request.method == 'POST':
        image.file.delete(save=True)
        image.delete()
        return redirect('profile', slug=request.user.userprofile.slug)


def download_image(request, slug):
    image = get_object_or_404(Image, slug=slug)
    file_path = image.file.path
    response = FileResponse(open(file_path, 'rb'))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = f'attachment; filename="{image.name}"'
    return response

@csrf_exempt
@require_POST
def like_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    image.likes += 1
    image.save()
    return JsonResponse({'likes': image.likes})