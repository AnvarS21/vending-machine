from django.contrib import admin
from .models import Product, Transaction

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'deposit', 'change', 'amount', 'created_dt', 'status')
    list_filter = ('created_dt',)
    search_fields = ('product_name',)
    date_hierarchy = 'created_dt'