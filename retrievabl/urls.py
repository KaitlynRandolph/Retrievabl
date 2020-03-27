from django.urls import path
from . import views


app_name = 'retrievabl'
urlpatterns = [
    path('', views.index, name='index'),
    path('search/', views.search, name='search'),
    path('our_mission/', views.mission, name='our_mission'),
]