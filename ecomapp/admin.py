# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ecomapp.models import Category, Author, Book, CartItem, Cart, Order

def make_payed(modeladmin, request, queryset):
    queryset.update(status='Оплачен')
make_payed.short_description = "Пометить как оплаченные"


class OrderAdmin(admin.ModelAdmin):
	list_filter = ['status']
	actions = [make_payed]


admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(CartItem)
admin.site.register(Cart)
admin.site.register(Order, OrderAdmin)

# Register your models here.
