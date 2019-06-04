from django.urls import path , include , re_path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'falsifier'

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('user_homepage/', views.user_homepage.as_view(), name='user_homepage'),
    path('search/', views.search.as_view(), name='search'),
    path('history/', views.history.as_view(), name='history'),

]
