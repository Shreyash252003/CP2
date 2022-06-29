from django.contrib import admin
from django.urls import path
from home import views
from .views import (product, hom,add_to_cart)
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('index', views.index, name='index'),
    path('contact', views.contact, name='contact'),
    path('sign_up', views.sign_up, name='sign_up'),
    path('logout',views.logout,name="logout"),
    path('hom',views.hom,name="hom"),
    path('product/<slug>',views.product,name="product"),
    path("add-to-cart/<slug>",add_to_cart,name="add_to_cart"),
    path("remove-from-cart/<slug>",views.remove_from_cart,name="remove_from_cart"),


]