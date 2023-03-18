from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Category)
admin.site.register(MenuItem)
admin.site.register(Bag)
admin.site.register(BagItem)
admin.site.register(Order)