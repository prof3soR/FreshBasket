from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,"users/index.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST["mobile"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return HttpResponseRedirect(reverse('menu'))
        return render(request,"users/menu.html")
    else:
        return render(request,"users/login.html",{
            "message":"Invalid credentials!"
        })
    

def logout_view(request):
    logout(request)
    return render(request,"users/login.html",{
        "message":"Logged out!"
    })


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('mobile')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the username is available
        if User.objects.filter(username=username).exists():
            return render(request, 'users/signup.html', {'message': 'This mobile number is already exits! Try loging in.'})

        # Create the new user object
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()

        # Log the user in
        user = authenticate(request, username=username, password=password)
        login(request, user)
        # Redirect to the home page
        return HttpResponseRedirect(reverse('index'))
    else:
        return render(request, 'users/signup.html')
    




    



@login_required
def menu(request):
    query = request.GET.get('query')
    category = request.GET.get('category')
    items = MenuItem.objects.all()

    if category:
        items = items.filter(category__name=category)

    if query:
        items = items.filter(name__icontains=query)

    categories = Category.objects.all()

    return render(request, 'users/menu.html', {'items': items, 'categories': categories, 'category': category, 'query': query})



@login_required
def add_to_bag(request):
    if request.method == 'POST':
        menu_item_id = request.POST.get('item_id')
        quantity = float(request.POST.get('quantity'))
        menu_item = MenuItem.objects.get(name=menu_item_id)

        # Get or create the bag for the user
        bag, created = Bag.objects.get_or_create(user=request.user)

        # Get the bag item or create a new one if it doesn't exist
        bag_item, created = BagItem.objects.get_or_create(bag=bag, menu_item=menu_item)

        # If the bag item already exists, update its quantity
        if not created:
            bag_item.quantity += quantity
            bag_item.save()

        # Otherwise, set the quantity to the specified value
        else:
            bag_item.quantity = quantity
            bag_item.save()

        return redirect('menu')
    
from decimal import Decimal



def checkout(request):
    bag = Bag.objects.get(user=request.user)
    bag_items = BagItem.objects.filter(bag=bag)
    total_price = sum(Decimal(bag_item.quantity) * bag_item.menu_item.price for bag_item in bag_items)

    return render(request, 'users/checkout.html', {
        'bag_items': bag_items,
        'total_price': total_price
    })

def bag(request):
    bag = Bag.objects.get(user=request.user)
    bag_items = BagItem.objects.filter(bag=bag)
    return render(request,"users/bag.html",{"bag_items" : bag_items})