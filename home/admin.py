import imp
from itertools import product
from django.contrib import admin
from .models import *

# Register your models here.
from .models import Contact, Order
admin.site.register(Contact)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Item)
