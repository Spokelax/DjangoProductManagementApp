import os

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver


class Product(models.Model):
    name = models.CharField(max_length=160, unique=True)
    image = models.ImageField(upload_to="products/", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = "product"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name="price_gte_0"),
        ]

    def __str__(self):
        return self.name

    def total_stock(self):
        return sum(batch.available_stock() for batch in self.batches.all())


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name


class InventoryBatch(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="batches"
    )
    quantity = models.IntegerField()
    expiration_date = models.DateField(null=True, blank=True)

    class Meta:
        db_table = "inventory_batch"
        verbose_name_plural = "Inventory Batches"
        ordering = ["expiration_date"]
        indexes = [
            models.Index(fields=["product", "expiration_date"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0), name="batch_quantity_gte_0"
            ),
        ]

    def available_stock(self):
        used_quantity = sum(rp.quantity for rp in self.receiptproduct_set.all())
        print(
            "Available stock:",
            self.quantity,
            "Used stock:",
            used_quantity,
            "Available:",
            self.quantity - used_quantity,
        )
        return self.quantity - used_quantity

    def __str__(self):
        return f"{self.product.name} - {self.quantity} units expiring on {self.expiration_date}"


class Receipt(models.Model):
    total = models.DecimalField(
        max_digits=12, decimal_places=2, editable=False, default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = "receipt"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(total__gte=0), name="total_gte_0"),
        ]

    def update_total(self):
        total = sum(
            rp.quantity * rp.price_at_purchase for rp in self.receiptproduct_set.all()
        )
        if self.total != total:
            self.total = total
            self.save(update_fields=["total"])

    def get_receipt_text(self):
        lines = [
            "Web Shopping Receipt",
            f"Receipt #REC-{self.id}-{self.created_at.strftime('%Y%m%d%H%M%S')}",
            f"Date: {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}",
            "-" * 80,
            f"{'Item':<20} {'Batch':<8} {'Expires':<12} {'Qty':<5} {'Price':<10} {'Total':<10}",
            "-" * 80,
        ]

        for rp in self.receiptproduct_set.all():
            product_name = rp.batch.product.name[:20]
            batch_id = str(rp.batch.id)
            expiration = (
                rp.batch.expiration_date.strftime("%Y-%m-%d")
                if rp.batch.expiration_date
                else "N/A"
            )
            qty = rp.quantity
            price = rp.price_at_purchase
            total = qty * price

            lines.append(
                f"{product_name:<20} {batch_id:<8} {expiration:<12} {qty:<5} €{price:<9.2f} €{total:<9.2f}"
            )

        lines += [
            "-" * 80,
            f"{'Total:':>64} €{self.total:.2f}",
            "-" * 80,
            "Thank you for your purchase!",
        ]

        return "\n".join(lines)

    def __str__(self):
        return f"Receipt #{self.id} - €{self.total}"


class ProductCategory(models.Model):
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_category"
        verbose_name_plural = "Product ↔ Categories"
        unique_together = ("product", "category")
        ordering = ["product", "category"]
        indexes = [
            models.Index(fields=["product", "category"]),
        ]


class ReceiptProduct(models.Model):
    receipt = models.ForeignKey(Receipt, on_delete=models.RESTRICT)
    batch = models.ForeignKey(InventoryBatch, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False
    )

    class Meta:
        db_table = "receipt_product"
        verbose_name_plural = "Receipt ↔ Products"
        unique_together = ("receipt", "batch")
        ordering = ["receipt", "batch"]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0), name="quantity_gt_0"
            ),
            models.CheckConstraint(
                check=models.Q(price_at_purchase__gte=0), name="price_at_purchase_gte_0"
            ),
        ]

    def clean(self):
        available = self.batch.available_stock()
        if self.quantity > available:
            raise ValidationError(
                f"Cannot purchase {self.quantity} items; only {available} available in this batch."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.price_at_purchase:
            self.price_at_purchase = self.batch.product.price
        super().save(*args, **kwargs)


@receiver(post_save, sender=ReceiptProduct)
def update_receipt_total(sender, instance, **kwargs):
    instance.receipt.update_total()


@receiver(pre_save, sender=Product)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_instance = Product.objects.get(pk=instance.pk)
        old_image = old_instance.image
    except Product.DoesNotExist:
        return
    new_image = instance.image
    if old_image and (not new_image or old_image != new_image):
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)


@receiver(post_delete, sender=Product)
def delete_image_on_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)
