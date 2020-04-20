from django.urls import path
from . import views


app_name = 'retrievabl'
urlpatterns = [
    path('', views.index, name='index'),
    path('?q=<str:query>&neg=<int:neg>', views.ArticleListView.as_view(), name='search'),
    path('our_mission/', views.mission, name='our_mission'),
    path('contact_us/', views.contact, name='contact_us'),
]