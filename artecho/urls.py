from django.urls import path
from artecho import views

app_name = 'artecho'

urlpatterns = [
    path('', views.index, name='index'),
    # added for html test viewing:
    path('addroot', views.add_root, name='add_root'),
    path('card', views.card, name='card'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'), 
    path('about/', views.about, name='about'),
    path('signup/', views.signup, name='signup'),
    path('<str:user_name>/<str:image_title>/', views.tree_view, name='tree'),
    path('profile/<slug:slug>/', views.profile, name='profile'),
    path('profileedit/<slug:slug>/', views.profile_edit, name='profile_edit'),
    path('search/', views.search_results, name="search"),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    # html test urlpatters end here---
]