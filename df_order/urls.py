from django.urls import re_path
from . import views

urlpatterns =[
    re_path(r'^$',views.order),
    re_path(r'^buy_handle/$',views.buy_handle),
    re_path(r'^pay&(\d+)/$',views.pay),
]