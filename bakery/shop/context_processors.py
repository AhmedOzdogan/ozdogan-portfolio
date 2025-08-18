from .utils import get_or_create_cart

def cart_context(request):
    try:
        cart = get_or_create_cart(request)
        items = cart.items.select_related("product") # type: ignore
        total = sum(i.quantity * i.unit_price for i in items)
        count = sum(i.quantity for i in items)
    except Exception:
        cart, items, total, count = None, [], 0, 0

    return {
        "cart_items": items,
        "cart_total": total,
        "cart_count": count,
    }