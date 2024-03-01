from django.urls import path
from artecho import views

app_name = 'artecho'

urlpatterns = [
    path('', views.index, name='index'),
]