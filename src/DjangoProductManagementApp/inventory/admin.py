from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category,
    InventoryBatch,
    Product,
    ProductCategory,
    Receipt,
    ReceiptProduct,
)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "image_thumbnail",
        "name",
        "price",
        "total_stock_display",
        "image",
        "archived",
    ]
    list_editable = [
        "price",
        "archived",
        "image",
    ]
    list_filter = ["archived"]
    search_fields = ["name"]
    fields = ["name", "price", "image", "archived"]
    list_per_page = 25

    def total_stock_display(self, obj):
        return obj.total_stock()

    total_stock_display.short_description = "Total Stock"

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 200px; height: auto;" />', obj.image.url
            )
        return "<No Image>"

    image_thumbnail.short_description = "Image"


@admin.register(InventoryBatch)
class InventoryBatchAdmin(admin.ModelAdmin):
    list_display = ["product", "quantity", "expiration_date"]
    list_filter = ["expiration_date", "product"]
    search_fields = ["product__name"]
    fields = ["product", "quantity", "expiration_date"]
    list_per_page = 25


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ["id", "total", "created_at", "archived"]
    list_filter = ["created_at", "archived"]
    search_fields = ["id"]
    readonly_fields = ["total", "created_at"]
    fields = ["archived"]
    list_per_page = 25


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    fields = ["name"]
    list_per_page = 25


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ["product", "category"]
    list_filter = ["category"]
    search_fields = ["product__name", "category__name"]
    fields = ["product", "category"]
    list_per_page = 25


@admin.register(ReceiptProduct)
class ReceiptProductAdmin(admin.ModelAdmin):
    list_display = ["receipt", "batch", "quantity", "price_at_purchase"]
    list_filter = ["receipt", "batch__product"]
    search_fields = ["batch__product__name", "receipt__id"]
    fields = ["receipt", "batch", "quantity"]
    list_per_page = 25
