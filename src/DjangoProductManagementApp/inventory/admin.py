from django.contrib import admin

from .models import Category, Product, ProductCategory, Receipt, ReceiptProduct


def all_fields(model):
    return [field.name for field in model._meta.fields]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = all_fields(Product)


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = all_fields(Receipt)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = all_fields(Category)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = all_fields(ProductCategory)


@admin.register(ReceiptProduct)
class ReceiptProductAdmin(admin.ModelAdmin):
    list_display = all_fields(ReceiptProduct)
