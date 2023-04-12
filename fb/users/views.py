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
        return render(request,"users/index.html")
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
            sub_details=subscription_details.objects.filter(user=user).first()
            if sub_details is None:
                messages.add_message(request, messages.SUCCESS, 'Login successfull!')
                return HttpResponseRedirect(reverse('menu'))
            else:
                messages.add_message(request, messages.SUCCESS, 'Login successfull!')
                return HttpResponseRedirect("sub_details")
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials!')
            return render(request,"users/login.html",)
    else:
        return render(request,"users/login.html")
        
    
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
    
import datetime

def check_date(input_date):
    # get today's date
    today = datetime.date.today()

    # convert input date to a datetime.date object
    input_date = datetime.datetime.strptime(str(input_date), '%Y-%m-%d').date()

    # calculate the number of days between input date and today's date
    days_diff = (input_date - today).days

    # compare input date with today's date
    if days_diff >= 0:
        # if input date is greater than or equal to today's date, return input date
        result_date = input_date
    else:
        # if input date is less than today's date, return today's date + 1 day
        result_date = today + datetime.timedelta(days=1)

    # get the weekday of the input or next day
    weekday = result_date.strftime('%A')


    return result_date, weekday

def sub_details(request):
    user=request.user
    sub_details=subscription_details.objects.get(user=user)
    date,day=check_date(sub_details.from_date)
    items_details=Order.objects.filter(user=user,day=day)
    return render(request,"users/sub_details.html",{"sub_details":sub_details,
                                                    "date":date,"day":day,
                                                    "items":items_details})
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
        messages.add_message(request, messages.INFO, 'Items are successfully saved in respective baskets!')
        return redirect("review_order")



def review_order(request):
    user = request.user
    orders = Order.objects.filter(user=user)
    address_list=delivary_address.objects.filter(user=user)
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
        "tot_price":tot_price,
        "amount":tot_price*100,
        "payment":False,
        "address_list":address_list,
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
            'amount': int(amount),
            'currency': 'INR',
            'payment_capture': 1
        }
        razorpay_order = client.order.create(data=payment_data)
        context = {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_key_id': "rzp_test_FOQ1egNAlDEuhn",
            'amount': amount
        }
        
    return render(request, 'users/review_order.html')

def save_subscrition(request):
    if request.method=="POST":
        user=request.user
        address_id=request.POST.get("address_id")
        address=delivary_address.objects.get(pk=address_id)
        from_date=request.POST.get("from_date")
        to_date=request.POST.get("to_date")
        amount=request.POST.get("amount")
        new_sub=subscription_details(user=user,
                                     address=address,
                                     from_date=from_date,
                                     to_date=to_date,
                                     amount=float(amount))
        new_sub.save()
        return redirect("payment")
def payment(request):
    user=request.user
    subscription=subscription_details.objects.get(user=user)
    price=subscription.amount//100
    return render(request,"users/payment.html",{"subs":subscription,"price":price})


def pricing(request):
    return render(request,"users/pricing.html")

def add_delivery_address(request):
    if request.method == 'POST':
        user = request.user
        door_no = request.POST.get('door_no')
        appartment_street = request.POST.get('appartment_street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        default_address = request.POST.get('default_address')
        
        # Convert default_address string to boolean
        default_address = True if default_address == 'on' else False
        
        # Set all other addresses to non-default if this address is the default
        if default_address:
            delivary_address.objects.filter(user=user).update(defult_address=False)
        
        # Save the new delivery address
        new_address = delivary_address(user=user, Door_no=door_no, appartment_street=appartment_street, city=city, state=state, pincode=pincode, defult_address=default_address)
        new_address.save()
        
        return redirect('review_order')  # Redirect to a success page
    else:
        return render(request, 'users/address.html')
    
def cancle_order(request):
    if request.method=="POST":
        day=request.POST.get("day")
        date=request.POST.get("date")
        user=request.user
        if cancelled_orders.objects.filter(user=user,day=day,date=date).exists():
            messages.add_message(request, messages.ERROR, 'Order already cancelled!!')
            return redirect("sub_details")
        else:
            new_cancle_order=cancelled_orders(user=user,day=day,date=date)
            new_cancle_order.save()
            messages.add_message(request, messages.ERROR, 'Order successfully cancelled!!')
            return redirect("sub_details")
    else:
        orders_list=cancelled_orders.objects.all()
        return render(request,"users/can_orders.html",{"orders":orders_list})
    

def todays_deliveries(request):
    today = datetime.date.today()
    weekday = today.strftime('%A')
    orders = Order.objects.filter(day=weekday)
    return render(request, 'users/todays_deliveries.html', {'orders': orders})