from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.index, name='home'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('sign_in', views.sign_in, name='sign_in'),
    path('sign_up', views.sign_up, name='sign_up'),
]