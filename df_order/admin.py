from django.contrib import admin
from .models import OrderInfo,OrderDetailInfo


class OrderInfoAdmin(admin.ModelAdmin):
    list_display = ['user','odate','oIsPay','ototal','oaddress']

admin.site.register(OrderInfo,OrderInfoAdmin)
