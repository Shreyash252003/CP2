from django.shortcuts import render, HttpResponse
from home.models import Contact
# Create your views here.
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

def sign_in(request):
    return render(request, 'sign_in.html')

def sign_up(request):
    return render(request, 'sign_up.html')