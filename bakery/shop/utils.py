# shop/utils.py
from .models import Cart, CartItem

def _ensure_session_key(request):
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user, session_key=None)
        return cart
    # anonymous → session cart
    session_key = _ensure_session_key(request)
    cart, _ = Cart.objects.get_or_create(user=None, session_key=session_key)
    return cart

def make_signature(product_id, addon_ids):
    ids = sorted(int(x) for x in (addon_ids or []))
    return f"{int(product_id)}|{','.join(map(str, ids))}"