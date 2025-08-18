
from datetime import datetime, timedelta, timezone
from decimal import ROUND_HALF_UP, Decimal
from django.conf import settings
from django.db import models
from django.forms import ValidationError

class Cart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.CASCADE, related_name="carts"
    )
    session_key = models.CharField(max_length=40, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            # Ensure that a cart has either a user or a session key
            models.CheckConstraint(
                check=models.Q(user__isnull=False) | models.Q(session_key__isnull=False),
                name="cart_has_user_or_session"
            )
        ]

    def __str__(self):
        return f"Cart(user={self.user_id}, session={self.session_key})" #type:ignore
    
    def delete_cart(self):
        two_hours_ago = datetime.now(timezone.utc) - timedelta(hours=2)
        Cart.objects.filter(created_at__lt=two_hours_ago).delete()
        

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("main.Product", on_delete=models.PROTECT)
    addons = models.ManyToManyField("main.Addon", blank=True, related_name="cart_items")
    
    signature = models.CharField(max_length=255, db_index=True, blank=True, default="")
    
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ("cart", "product","signature")  # merge-friendly
        
    @property
    def item_total(self):
        addons_total = sum(addon.price for addon in self.addons.all())
        return (self.unit_price + addons_total)

    @property
    def line_total(self):
        return (self.item_total * self.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    shipping_address = models.ForeignKey("main.Address",on_delete=models.PROTECT,related_name="orders")
    shipping_method = models.CharField(max_length=20, choices=[("regular", "Regular"), ("fast", "Fast")], default="regular")
    shipping_fee = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal("0.00"))
    order_status = models.CharField(max_length=20, choices=[("Pending shipment", "Pending shipment"), ('On the way', 'On the way'), ("Completed", "Completed"), ("Canceled", "Canceled")], default="Pending shipment")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order {self.pk} by {self.user}"
    
    def clean(self):
        if self.shipping_address.user != self.user:
            raise ValidationError("Shipping address must belong to the order user.")
        return super().clean()
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")

    product = models.ForeignKey("main.Product", on_delete=models.SET_NULL, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    # Add-ons stored as JSON snapshot:
    addons = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"Item {self.pk} for Order {self.order_id}" #type:ignore
    
    @property
    def addons_list(self):
        return self.addons if isinstance(self.addons, list) else []

    @property
    def base_total(self) -> Decimal:
        return (self.unit_price * self.quantity).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def addons_total(self) -> Decimal:
        total = Decimal("0.00")
        for a in (self.addons or []):
            qty = int(a.get("quantity", 0) or 0)
            if qty <= 0:
                continue
            price = Decimal(str(a.get("unit_price", "0.00")))
            total += price * qty
        return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @property
    def line_total(self) -> Decimal:
        return (self.base_total + self.addons_total).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)