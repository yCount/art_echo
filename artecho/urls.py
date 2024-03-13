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
    path('signup/', views.signup, name='signup'),
    path('tree', views.tree_view, name='tree'),
    path('profile', views.profile, name='profile'),
    path('profileedit', views.profile_edit, name='profile_edit'),
    # html test urlpatters end here---
]