from cProfile import label
from urllib.request import CacheFTPHandler
from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.shortcuts import reverse

# Create your models here.

CATEGORY_CHOICES = [
    ['B','Beverage'],
    ['S','Snack'],
    ['M','Meal'],
]

LABEL_CHOICES = [
    ['P','primary'],
    ['S','secondary'],
    ['D','danger'],
]
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50,default="")
    message = models.CharField(max_length=300,default="")

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2,null=True)
    label = models.CharField(choices=LABEL_CHOICES,max_length=10,null=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(null=True,blank=True)
    slug = models.SlugField()
    

    def __str__(self):
        return self.title

    def  get_absolute_url(self):
        return reverse("home:product",kwargs={
            'slug':self.slug
        })
    def get_add_to_cart_url(self):
        return reverse("home:add_to_cart",kwargs={
            'slug':self.slug
        })
    def get_remove_from_cart_url(self):
        return reverse("home:remove_from_cart",kwargs={
            'slug':self.slug
        })



class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item , on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    

    def __str__(self):
        return f"Order by {self.user}"



