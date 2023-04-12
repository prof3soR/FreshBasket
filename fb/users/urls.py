from django.urls import path
from . import views

urlpatterns=[
    path("",views.index,name="index"),
    path("user_profile/",views.user_profile,name="user_profile"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("signup",views.signup,name="signup"),
    path("menu",views.menu,name="menu"),
    path("add_to_bag",views.add_to_bag,name="add_to_bag"),
    path('checkout/', views.checkout, name='checkout'),
    path('bag/', views.bag, name='bag'),
    path('save_items/', views.save_items, name='save_items'),
    path('review_order/',views.review_order,name="review_order"),
    path('payment/',views.payment,name="payment"),
    path("save_sub",views.save_subscrition,name="save_sub"),
    path("sub_details",views.sub_details,name="sub_details"),
    path("pricing",views.pricing,name="pricing"),
    path("address",views.add_delivery_address,name="address"),
    path("save_sub",views.save_subscrition,name="save_subs"),
    path("payment",views.payment,name="payment"),
    path("cancle_order",views.cancle_order,name="cancle_order"),
    path("todays_deliveries",views.todays_deliveries,name="todays_deliveries")
]