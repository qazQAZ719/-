from django.urls import re_path,include
from . import views

urlpatterns = [
    re_path('^$',views.index),
    re_path('^list(\d+)_(\d+)_(\d+)/$',views.list),
    re_path('^(\d+)/$',views.detail),
]