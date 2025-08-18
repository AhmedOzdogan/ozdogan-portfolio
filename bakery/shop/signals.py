from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.db import transaction
from .models import Cart

@receiver(user_logged_in)
def merge_session_cart(sender, request, user, **kwargs):
    if not request.session.session_key:
        return
    session_key = request.session.session_key

    try:
        anon_cart = Cart.objects.get(user__isnull=True, session_key=session_key)
    except Cart.DoesNotExist:
        return

    with transaction.atomic():
        user_cart, _ = Cart.objects.get_or_create(user=user, session_key=None)
 
        for item in list(anon_cart.items.select_related("product")): # type:ignore
            existing = user_cart.items.filter(product=item.product).first() # type:ignore
            if existing:
                existing.quantity += item.quantity
                existing.save()
                item.delete()
            else:
                item.cart = user_cart
                item.save()

        # Delete empty anon cart
        if not anon_cart.items.exists(): # type:ignore
            anon_cart.delete()