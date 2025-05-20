import json
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .inventory.models import InventoryBatch, Product, Receipt, ReceiptProduct

# batches = InventoryBatch.objects.all()
# for batch in batches:
#    print(
#        f"Batch ID: {batch.id}, Product: {batch.product.name}, Quantity: {batch.quantity}, Available: {batch.available_stock()}"
#    )


@ensure_csrf_cookie
def home(request):
    products = Product.objects.all()
    return render(
        request, "inventory/home.html", {"title": "Home", "products": products}
    )


def receipt_page(request):
    receipts = Receipt.objects.all()
    open_receipt_id = request.GET.get("open")
    return render(
        request,
        "inventory/receipts.html",
        {
            "title": "Receipts",
            "receipts": receipts,
            "open_receipt_id": open_receipt_id,
        },
    )


def get_product_batches(request, product_id):
    try:
        product = Product.objects.get(id=product_id)
        batches = product.batches.all()
        batch_data = [
            {
                "id": batch.id,
                "expiration_date": batch.expiration_date.strftime("%Y-%m-%d")
                if batch.expiration_date
                else None,
                "available_stock": batch.available_stock(),
            }
            for batch in batches
        ]
        return JsonResponse(
            {
                "product_name": product.name,
                "price": float(product.price),
                "batches": batch_data,
            }
        )
    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)


@require_POST
def checkout(request):
    try:
        data = json.loads(request.body)
        items = data.get("items", [])
        if not items:
            return JsonResponse({"error": "Cart is empty"}, status=400)

        with transaction.atomic():
            receipt = Receipt.objects.create()
            for item in items:
                batch = InventoryBatch.objects.select_for_update().get(
                    id=item["batchId"]
                )
                available = batch.available_stock()
                if item["quantity"] > available:
                    return JsonResponse(
                        {
                            "error": f"Only {available} items available for {item['productName']} (Batch ID: {item['batchId']})"
                        },
                        status=400,
                    )

                price_at_purchase = Decimal(str(item["price"])).quantize(
                    Decimal("0.01")
                )

                ReceiptProduct.objects.create(
                    receipt=receipt,
                    batch=batch,
                    quantity=item["quantity"],
                    price_at_purchase=price_at_purchase,
                )

            receipt.update_total()
            receipt.save()

            return JsonResponse({"success": True})
    except InventoryBatch.DoesNotExist:
        return JsonResponse({"error": "Invalid batch"}, status=400)
    except ValidationError as e:
        return JsonResponse({"error": str(e)}, status=400)
    except Exception as e:
        return JsonResponse({"error": "An error occurred"}, status=500)
