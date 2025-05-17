""""""

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# TODO: Double check model
# TODO: Check if working in the admin panel


class Product(models.Model):
    name = models.CharField(max_length=160, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    expiration_date = models.DateTimeField(null=True, blank=True)
    stock = models.IntegerField()
    archived = models.BooleanField(default=False)

    class Meta:
        db_table = "product"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["expiration_date"]),
        ]
        constraints = [
            models.CheckConstraint(check=models.Q(price__gte=0), name="price_gte_0"),
            models.CheckConstraint(check=models.Q(stock__gte=0), name="stock_gte_0"),
        ]

    def __str__(self):
        return self.name


class Receipt(models.Model):
    total = models.DecimalField(max_digits=12, decimal_places=2)
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
        self.total = total
        self.save(update_fields=["total"])


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
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.IntegerField(default=1)
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = "receipt_product"
        verbose_name_plural = "Receipt ↔ Products"
        unique_together = ("receipt", "product")
        ordering = ["receipt", "product"]
        indexes = [
            models.Index(fields=["receipt", "product"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gt=0), name="quantity_gt_0"
            ),
            models.CheckConstraint(
                check=models.Q(price_at_purchase__gte=0), name="price_at_purchase_gte_0"
            ),
        ]

    def clean(self):
        if self.quantity > self.product.stock:
            raise ValidationError(
                f"Cannot purchase {self.quantity} items; only {self.product.stock} in stock."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        if not self.price_at_purchase:
            self.price_at_purchase = self.product.price
        super().save(*args, **kwargs)


@receiver(post_save, sender=ReceiptProduct)
def update_stock(sender, instance, created, **kwargs):
    if created:
        product = instance.product
        product.stock -= instance.quantity
        product.save()


@receiver(post_save, sender=ReceiptProduct)
def update_receipt_total(sender, instance, **kwargs):
    instance.receipt.update_total()
