from django.urls import re_path
from . import views


urlpatterns = [
    re_path(r'^register/$',views.register),
    re_path(r'^register_handle/$',views.register_handle),
    re_path(r'^login/$',views.login),
    re_path(r'^logout/$',views.logout),
    re_path(r'^login_handle/$',views.login_handle),
    re_path(r'^info/$',views.info),
    re_path(r'^info/order/$',views.order),
    re_path(r'^info/site/$',views.site),
    re_path(r'^info/add_site/$',views.add_site),
]