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
from artecho import views

urlpatterns = [
    path('', views.index, name='index'),
    # added for html test viewing:
    path('card/', views.card, name='card'),
    path('add_root', views.add_root, name='add_root'),
    # html test urlpatters end here---
    path('artecho/', include('artecho.urls')),
    path('admin/', admin.site.urls),
]
