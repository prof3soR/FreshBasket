from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("signup",views.signup,name="signup"),
    path("menu",views.menu,name="menu"),
    path("add_to_bag",views.add_to_bag,name="add_to_bag"),
    path('checkout/', views.checkout, name='checkout'),
    path('bag/', views.bag, name='bag'),
]