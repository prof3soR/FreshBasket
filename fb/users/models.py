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