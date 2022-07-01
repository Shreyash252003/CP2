from cProfile import label
from urllib.request import CacheFTPHandler
from django.db import models
from django.conf import settings
from django.forms import ImageField
from django.shortcuts import reverse
from django.db.models.fields import CharField
from django.utils.translation import gettext_lazy as _
from .constants import PaymentStatus


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

    def get_total_item_quantity(self):
        return self.quantity*self.item.price

    def get_total_discount_item_quantity(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_quantity()-self.get_total_discount_item_quantity()    

    def get_final_price(self): 
        if self.item.discount_price:
            return self.get_total_discount_item_quantity()
        return  self.get_total_item_quantity()   


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    

    def __str__(self):
        return f"Order by {self.user}"

    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total +=order_item.get_final_price()
        return total

class Payment(models.Model):
    name = CharField(_("Customer Name"), max_length=254, blank=False, null=False)
    amount = models.FloatField(_("Amount"), null=False, blank=False)
    status = CharField(
        _("Payment Status"),
        default=PaymentStatus.PENDING,
        max_length=254,
        blank=False,
        null=False,
    )
    provider_order_id = models.CharField(
        _("Order ID"), max_length=40, null=False, blank=False
    )
    payment_id = models.CharField(
        _("Payment ID"), max_length=36, null=False, blank=False
    )
    signature_id = models.CharField(
        _("Signature ID"), max_length=128, null=False, blank=False
    )

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"


