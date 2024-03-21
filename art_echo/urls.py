"""art_echo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from artecho import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    # added for html test viewing:
    path('card/', views.card, name='card'),
    path('add_root', views.add_root, name='add_root'),
    path('tree', views.tree_view, name='tree'),
    path('profileedit/<slug:slug>/', views.profile_edit, name='profile_edit'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    # html test urlpatters end here---
    path('artecho/', include('artecho.urls')),
    path('admin/', admin.site.urls),
    path('profile', views.profile, name='profile'),
    path('login/', LoginView.as_view(), name='login')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
