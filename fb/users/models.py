from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='menu_items')
    image = models.ImageField(upload_to='static/users/images', blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    description = models.TextField(blank=True)
    quantity_type=models.CharField(max_length=100,default="Kg's")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
from django.contrib.auth.models import User
class Bag(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField('MenuItem', through='BagItem')

    def __str__(self):
        return f"{self.user.first_name}'s Bag"

class BagItem(models.Model):
    bag = models.ForeignKey(Bag, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.FloatField(default=1)

    def __str__(self):
        return f"{self.menu_item.name} ({self.quantity}) in {self.bag.user.first_name}'s Bag"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    day = models.CharField(max_length=10)
    name = models.CharField(max_length=50)
    quantity = models.CharField(max_length=50)
    price=models.FloatField()

    def __str__(self):
        return f"{self.user.first_name} {self.day} {self.name} {self.quantity} {self.price}"
    


    
class delivary_address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    Door_no=models.CharField(max_length=10)
    appartment_street=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    state=models.CharField(max_length=100)
    pincode=models.IntegerField()
    defult_address=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.first_name}'s address"

class subscription_details(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    address=models.ForeignKey(delivary_address,on_delete=models.CASCADE)
    from_date=models.DateField()
    to_date=models.DateField()
    amount=models.IntegerField()
    payment=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.first_name} Address {self.id}"
class cancelled_orders(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    day=models.CharField(max_length=100)
    date=models.CharField(max_length=100)
    def __str__(self):
        return f"{self.user}{self.day}"