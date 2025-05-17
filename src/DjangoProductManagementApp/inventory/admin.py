from django.contrib import admin

from .models import Category, Product, ProductCategory, Receipt, ReceiptProduct

# Basic registration
admin.site.register(Product)
admin.site.register(Receipt)
admin.site.register(Category)
admin.site.register(ProductCategory)
admin.site.register(ReceiptProduct)
