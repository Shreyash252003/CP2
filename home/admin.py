import imp
from itertools import product
from django.contrib import admin

# Register your models here.
from .models import Contact
admin.site.register(Contact)
