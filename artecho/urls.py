from django.urls import path
from artecho import views

app_name = 'artecho'

urlpatterns = [
    path('', views.index, name='index'),
    # added for html test viewing:
    path('addroot', views.add_root, name='add_root'),
    path('card', views.card, name='card'),
    path('login/', views.user_login, name='login'),
    path('about/', views.about, name='about'),
    # html test urlpatters end here---
]