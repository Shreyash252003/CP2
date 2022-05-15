from django.contrib import admin
from django.urls import path
from home import views
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('index', views.index, name='index'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('logout',views.logout,name="logout")
]