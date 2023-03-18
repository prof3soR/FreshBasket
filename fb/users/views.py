from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.models import User
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    else:
        return render(request,"users/index.html")
    
def user_profile(request):
    return render(request,"users/user_profile.html")
def login_view(request):
    if request.method == "POST":
        username = request.POST["mobile"]
        password = request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.add_message(request, messages.SUCCESS, 'Login successfull!')
            return HttpResponseRedirect(reverse('menu'))
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
            return render(request,"users/login.html",)
    else:
        return render(request,"users/login.html",)
        

def logout_view(request):
    logout(request)
    messages.add_message(request, messages.INFO, 'Logged out!')
    return render(request,"users/login.html")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get('mobile')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        # Check if the username is available
        if User.objects.filter(username=username).exists():
            messages.add_message(request, messages.INFO, 'This mobile number is already exits! Try loging in.')
            return render(request, 'users/signup.html')

        # Create the new user object
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Account created! Please login')
        return HttpResponseRedirect(reverse('login'))
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
        messages.add_message(request, messages.INFO, 'Item added to bag!')
        return redirect("menu")
    
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


from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
import re
import json

@csrf_exempt
def save_items(request):
    if request.method == 'POST':
        monday_items = request.POST.get('monday_items')
        monday_items = json.loads(monday_items)
        tuesday_items = request.POST.get('tuesday_items')
        tuesday_items = json.loads(tuesday_items)
        wednesday_items = request.POST.get('wednesday_items')
        wednesday_items = json.loads(wednesday_items)
        thursday_items = request.POST.get('thursday_items')
        thursday_items = json.loads(thursday_items)
        friday_items = request.POST.get('friday_items')
        friday_items = json.loads(friday_items)
        saturday_items = request.POST.get('saturday_items')
        saturday_items = json.loads(saturday_items)
        user = request.user
        print(monday_items,tuesday_items)
        # Save the items for each day
        for item in monday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Monday', name=name, quantity=quantity,price=price)
            order.save()
        for item in tuesday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Tuesday', name=name, quantity=quantity,price=price)
            order.save()
        for item in wednesday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Wednesday', name=name, quantity=quantity,price=price)
            order.save()
        for item in thursday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Thrusday', name=name, quantity=quantity,price=price)
            order.save()
        for item in friday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Friday', name=name, quantity=quantity,price=price)
            order.save()
        for item in saturday_items:
            name = item['name']
            quantity = float(item['quantity'].replace('<td>', '').replace('</td>', '').replace("Kg's",'').strip())
            price=float(item['price'].replace('<td>', '').replace('</td>', '').replace('₹',''))
            order = Order(user=user, day='Saturday', name=name, quantity=quantity,price=price)
            order.save()
        
        # Send a success response
        return HttpResponseRedirect(reverse('review_order'))
    
    # Send an error response if the request is not POST
    return JsonResponse({'status': 'error'})


from django.db.models import Sum
from django.template import context_processors

def review_order(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    m_items=[]
    t_items=[]
    w_items=[]
    th_items=[]
    f_items=[]
    s_items=[]
    m_price=0
    t_price=0
    w_price=0
    th_price=0
    f_price=0
    s_price=0
    for i in orders:
        day=i.day
        item_name=i.name
        quantity=i.quantity
        price=i.price
        if day=="Monday":
            m_items.append({'name':item_name,'quantity': quantity,'price':price})
            m_price+=float(price)
        elif day=="Tuesday":
            t_items.append({'name':item_name,'quantity': quantity,'price':price})
            t_price+=float(price)
        elif day=="Wednesday":
            w_items.append({'name':item_name,'quantity': quantity,'price':price})
            w_price+=float(price)
        elif day=="Thrusday":
            th_items.append({'name':item_name,'quantity': quantity,'price':price})
            th_price+=float(price)
        elif day=="Friday":
            f_items.append({'name':item_name,'quantity': quantity,'price':price})
            f_price+=float(price)
        elif day=="Saturday":
            s_items.append({'name':item_name,'quantity': quantity,'price':price})
            s_price+=float(price)

    tot_price=m_price+t_price+w_price+th_price+f_price+s_price
        
        

    
    context={
        "m_items":m_items,
        "t_items":t_items,
        "w_items":w_items,
        "th_items":th_items,
        "f_items":f_items,
        "s_items": s_items,
        "m_price":m_price,
        "t_price":t_price,
        "w_price":w_price,
        "th_price":th_price,
        "f_price":f_price,
        "s_price":s_price,
        "tot_price":tot_price
    }
    return render(request,"users/review_order.html",context)

import razorpay

from django.http import JsonResponse
from django.shortcuts import render


def payment(request):
    if request.method == 'POST':
        amount = float(request.POST['amount']) * 100  # convert to paise
        client = razorpay.Client(auth=("rzp_test_FOQ1egNAlDEuhn","C7oxJQA4vaAvpKnTerprMvvA"))
        payment_data = {
            'amount': amount,
            'currency': 'INR',
            'payment_capture': 1
        }
        razorpay_order = client.order.create(data=payment_data)
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': "rzp_test_FOQ1egNAlDEuhn",
            'amount': amount
        }
        return JsonResponse(context)
    return render(request, 'users/payment.html')