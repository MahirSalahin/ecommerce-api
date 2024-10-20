from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.db.models import Count
from django.http import HttpRequest
from django.urls import reverse
from django.utils.html import format_html, urlencode
from store import models

admin.site.site_header = "Storefront Admin"
admin.site.site_title = "Admin"

admin.site.register(models.Promotion)


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                   'collection__id': str(collection.id)
               }))

        return format_html('<a href = "{}"> {}</a>', url, collection.products_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


class PriceFilter(admin.SimpleListFilter):
    title = 'price'
    parameter_name = 'price'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ("<10", "<10"),
            ("<100", "<100"),
            ("<1000", "<1000")
        ]

    def queryset(self, request: Any, queryset: Any) -> QuerySet[Any]:
        value = self.value()
        if value == "<10":
            return queryset.filter(price__lt=10)
        if value == "<100":
            return queryset.filter(price__lt=100)
        if value == "<1000":
            return queryset.filter(price__lt=1000)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    autocomplete_fields = ['collection']
    search_fields = ['title']
    prepopulated_fields = {
        'slug' : ['title']
    }

    actions = ['clear_inventory']
    list_display = ["title", 'price', 'inventory_status']
    list_editable = ['price']
    list_filter = ["last_update", PriceFilter]
    list_per_page = 50

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        return "OK" if product.inventory >= 10 else "Low"
    
    @admin.action(description="Clear Inventory")
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} products were successfully updated"
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    search_fields = ['first_name', 'last_name']
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 50
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    model = models.OrderItem
    min_num = 1
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at',
                    'payment_status', 'customer', 'order_item']

    @admin.display(description='orderitem', ordering='orderitem')
    def order_item(self, obj):
        return [str(item) for item in obj.orderitem_set.all()]

@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_at', 'cart_items']
    ordering = ['id']
    @admin.display()
    def cart_items(self, obj):
        return [str(item) for item in obj.items.all()]


admin.site.register(models.OrderItem)
admin.site.register(models.Address)
admin.site.register(models.CartItem)
admin.site.register(models.Review)
