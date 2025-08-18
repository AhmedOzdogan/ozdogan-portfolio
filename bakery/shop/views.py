from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST, require_GET
from django.contrib import messages
from django.db import transaction
from main.models import Product, AddOn, Address
from .models import CartItem, Order, OrderItem, Cart
from .utils import get_or_create_cart, make_signature
from decimal import ROUND_HALF_UP, Decimal
import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required

def cart_detail(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product") #type: ignore
    subtotal = sum(i.line_total for i in items)
    return render(request, "shop/cart.html", {
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
    })

@require_POST
@transaction.atomic
def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = get_object_or_404(Product, pk=product_id)

    qty = max(1, int(request.POST.get("qty", 1)))
    addon_ids = [int(x) for x in request.POST.getlist("addons[]")]
    addons_qs = list(AddOn.objects.filter(id__in=addon_ids))

    # snapshot per-unit price (product + selected addons)
    unit_price = Decimal(str(product.price))
    
    print(product.price, addons_qs, unit_price)
    
    # distinct line identity: product + addon set
    sig = make_signature(product.id, addon_ids) #type:ignore

    # include signature
    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        signature=sig,
        defaults={"quantity": qty, "unit_price": unit_price},
    )

    if created:
        item.addons.set(addons_qs)
    else:
        item.quantity += qty
        item.save(update_fields=["quantity"])

    return redirect(request.POST.get("next") or "shop:cart_detail")

@require_POST
def update_cart_item(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    qty = int(request.POST.get("qty", 1))
    if qty <= 0:
        item.delete()
    else:
        item.quantity = qty
        item.save()
    return redirect(request.POST.get("next") or "shop:cart_detail")

@require_POST
def remove_from_cart(request, item_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    item.delete()
    return redirect(request.POST.get("next") or "shop:cart_detail")

@require_POST
def remove_addons(request, item_id, addon_id):
    cart = get_or_create_cart(request)
    item = get_object_or_404(CartItem, pk=item_id, cart=cart)
    addon = get_object_or_404(AddOn, pk=addon_id)
    item.addons.remove(addon)
    return redirect(request.POST.get("next") or "shop:cart_detail")

@require_POST
def empty_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete() #type:ignore
    return redirect(request.POST.get("next") or "shop:cart_detail")

def _q2(d: Decimal) -> Decimal:
    return d.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

def checkout(request):
    cart = get_or_create_cart(request)
    items = cart.items.select_related("product") #type: ignore
    subtotal = Decimal("0.00")
    for item in items:
        subtotal += item.line_total
    print(f"Subtotal: {subtotal}")
    default_address = Address.objects.filter(user=request.user, is_default=True).first()
    return render(request, "shop/checkout.html", {
        "cart": cart,
        "items": items,
        "subtotal": subtotal,
        "default_address": default_address,
    })

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_checkout_session(request):
    success_url = request.build_absolute_uri(
        reverse("shop:success")
    ) + "?session_id={CHECKOUT_SESSION_ID}"

    cancel_url = request.build_absolute_uri(reverse("shop:cancel"))

    user = request.user
    cart = Cart.objects.filter(user=user).first()
    cart_items = cart.items.select_related("product").prefetch_related("addons") #type:ignore

    subtotal = Decimal("0.00")
    for item in cart_items:
        subtotal += item.line_total

    # shipping fee
    shipping_method = request.POST.get("shipping_method", "regular")
    shipping_fee = Decimal("24.99") if shipping_method == "fast" else Decimal("9.99")

    # tax 20%
    tax_amount = (subtotal + shipping_fee) * Decimal("0.20")

    total = subtotal + shipping_fee + tax_amount

    # round to cents
    total = total.quantize(Decimal("0.01"))

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {'name': 'Order Checkout'},
                'unit_amount': int(total * 100),  # convert dollars → cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=success_url,
        cancel_url=cancel_url,
        metadata={
            "shipping_method": shipping_method,
        },
    )
    return redirect(checkout_session.url, code=303)



@require_GET
@transaction.atomic
def success_view(request):
    session_id = request.GET.get("session_id")
    if not session_id:
        messages.error(request, "Missing payment session.")
        return redirect("shop:cart")

    created_flag = f"order_created_for_{session_id}"
    if request.session.get(created_flag):
        return render(request, "shop/success.html")

    # Verify with Stripe (no webhook)
    try:
        session = stripe.checkout.Session.retrieve(session_id)
    except Exception:
        messages.error(request, "Could not verify payment session.")
        return redirect("shop:cart")

    if getattr(session, "payment_status", "") != "paid":
        messages.error(request, "Payment not completed.")
        return redirect("shop:cart")

    user = request.user

    shipping_method = (session.metadata or {}).get("shipping_method") or request.session.get("shipping_method") or "regular"
    shipping_method = "fast" if shipping_method == "fast" else "regular"  # normalize
    shipping_fee = Decimal("24.99") if shipping_method == "fast" else Decimal("9.99")

    shipping_address = Address.objects.filter(user=user, is_default=True).first()
    if not shipping_address:
        messages.error(request, "Please add a shipping address.")
        return redirect("main:add_address")

    cart = Cart.objects.filter(user=user).first()

    items= cart.items.select_related("product").prefetch_related("addons") #type:ignore


    subtotal = Decimal("0.00")
    for item in items:
        subtotal += item.line_total
        # Update Stock
        item.product.stock = item.product.stock - item.quantity
        item.product.save(update_fields=["stock"])

    subtotal = _q2(subtotal)
    tax_amount = _q2(subtotal * Decimal("0.20"))  # 20% tax
    total = _q2(subtotal + tax_amount + shipping_fee)

    # Create Order
    order = Order.objects.create(
        user=user,
        subtotal=subtotal,
        shipping_address=shipping_address,
        shipping_method=shipping_method,
        shipping_fee=_q2(shipping_fee),
        tax_amount=tax_amount,
        total=total,

    )

    for item in items:
        qty = int(item.quantity)
        if qty <= 0:
            continue

        addons_snapshot = []
        if hasattr(item, "addons") and hasattr(item.addons, "all"):
            for addon in item.addons.all():
                addons_snapshot.append({
                    "id": addon.id,
                    "name": addon.name,
                    "unit_price": str(Decimal(str(addon.price))),
                    "quantity": 1,
                })

        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            unit_price=_q2(Decimal(str(item.unit_price))),
            quantity=qty,
            addons=addons_snapshot,
        )

    cart.items.all().delete()  # type:ignore

    request.session[created_flag] = order.id # type:ignore
    request.session.modified = True

    return render(request, "shop/success.html", {
        "order": order,
        "shipping_method": shipping_method,
    })

def cancel_view(request):
    return render(request, "shop/cancel.html", {})

@login_required
def order_list_view(request):

    role = request.user.profile.role
    
    if not role:
        return HttpResponseForbidden("You don't have permission to view orders.")
    
    print(role)

    if role == "CUSTOMER":
        orders = Order.objects.filter(user=request.user).order_by("-created_at")
        template = "shop/customer_order_list.html"
    elif role == "MANAGER":
        status_choices = Order._meta.get_field("order_status").choices
        restaurant = getattr(request.user, "restaurant", None)
        qs = Order.objects.select_related("user")
        orders = qs.filter(restaurant=restaurant).order_by("-created_at") if restaurant else qs.order_by("-created_at")
        template = "shop/manager_order_list.html"
    else:
        return HttpResponseForbidden("You don't have permission to view orders.")

    return render(request, template, {"orders": orders, "status_choices": status_choices})

def update_order_status(request, order_id):
    if request.method == "POST":
        order = get_object_or_404(Order, id=order_id)
        status_choices = Order._meta.get_field("order_status").choices
        new_status = request.POST.get("order_status")
        if new_status in dict(status_choices):  # type: ignore
            order.order_status = new_status
            order.save()
            messages.success(request, "Order status updated successfully.")
        else:
            messages.error(request, "Invalid order status.")
    return redirect("shop:order_list")
