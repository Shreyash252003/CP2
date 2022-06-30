from django.shortcuts import render, HttpResponse,redirect,get_object_or_404
from home.models import Contact
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, auth
from django .contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item,Order,OrderItem
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.contrib import messages

# Create your views here.
@login_required(login_url="/")
def index(request):
    return render(request, 'index.html')

def contact(request):
    if request.method=="POST":
        print(request)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        message = request.POST.get('message','')
        contact = Contact(name=name, email=email,message=message)
        contact.save()
    return render(request, 'contact.html')



def sign_up(request):
    if request.method=='POST':
        username=request.POST['username']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']
        if pass1==pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,"Email already exists")
                return redirect('sign_up')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Email id alredy used')
                return redirect('sign_up')
            else:
                user=User.objects.create_user(username=username,email=email,password=pass1)    
                user.save();
                return redirect('/')
        else:
            messages.info(request,'Password is not the same as previous')
            return redirect('sign_up')        
    else:
        return render(request,'sign_up.html')




def sign_in(request):
    if request.method=='POST':
        username=request.POST['username']
        pass1=request.POST['pass1']
        user=auth.authenticate(username=username,password=pass1)
        if user is not None:
            auth.login(request,user)
            return redirect('home:index')
        else:
            messages.info(request,'Credentials Invalid')  
            return redirect('/')  
    else:
        return render(request, 'sign_in.html')

def logout(request):
    auth.logout(request)
    return redirect("/")




def hom(request):
    context ={
        'items':Item.objects.all(),
    }
    return render(request ,"hom.html",context)

def OrderSummary(request):
    try:
        context = {
            'orders':Order.objects.get(user=request.user,ordered=False),
        }
        return render(request,'order_summary.html',context)
    except ObjectDoesNotExist:
        messages.error(request,"You do not have a active order")
        return redirect("hom")

    


def product(request,slug):
    context = {
        'items':Item.objects.all(),
        'slugs':Item.objects.get(slug=slug)
    }
    return render(request,"product.html",context)


def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item,created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.info(request,"This item quantity was updated")
        else:
            messages.info(request,"This item was added to your cart")
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request,"This item quantity was added to your cart")
    return redirect("home:product",slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # Check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request,"This item was removed from your cart")
            return redirect("home:product",slug=slug)
        else:
            messages.info(request,"This item was not present in your cart")
            return redirect("home:product",slug=slug)
    else:
        #add a message saying the user doesnt have an order
        messages.info(request,"The user has not placed an order yet")
        return redirect("home:product",slug=slug)


def checkout(request):
    return render(request,'checkout.html')


