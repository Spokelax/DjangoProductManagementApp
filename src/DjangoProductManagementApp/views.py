from django.shortcuts import render

from DjangoProductManagementApp.inventory.models import Product


def home(request):
    products = Product.objects.all()
    return render(
        request, "inventory/home.html", {"title": "Home", "products": products}
    )
