from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods, require_GET
from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.db import transaction

from main.models import Product, Address
from .forms import LoginForm, SignupForm, ProfileForm, AddressForm
from shop.models import Cart, CartItem

def index(request):
    return render(request, 'main/index.html')

def menu(request):
    return render(request, 'main/menu.html')

@login_required
@require_http_methods(["GET", "POST"])
def profile(request):
    user = request.user

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect("main:profile")
    else:
        form = ProfileForm(instance=user)

    addresses = getattr(user, "addresses", None)
    addresses = addresses.all() if addresses is not None else []

    return render(request, "main/profile.html", {
        "profile_form": form,
        "addresses": addresses,
    })

@require_GET
def cart_snapshot(request):
    user_id = request.user.id
    session_id = request.session.session_key

    # Ensure we have a session key for anonymous users
    if not session_id:
        request.session.save()
        session_id = request.session.session_key

    # Get cart for logged-in user or session
    cart = None
    if user_id:
        cart = Cart.objects.filter(user_id=user_id).first()
    if not cart:
        cart = Cart.objects.filter(session_key=session_id).first()

    # If no cart exists yet, create it
    if not cart:
        cart = Cart.objects.create(
            user_id=user_id if user_id else None,
            session_key=None if user_id else session_id
        )

    items = cart.items.select_related("product").prefetch_related("addons") #type:ignore
 
    count = sum(i.quantity for i in items)
    total = sum((i.line_total) for i in items) or Decimal("0.00")

    data_items = [{
        "id": i.id,
        "name": i.product.name,
        "qty": i.quantity,
        "unit_price": f"{i.unit_price:.2f}",
        "line_total": f"{(i.line_total):.2f}",
        "addons": [a.name for a in i.addons.all()]
    } for i in items]

    return JsonResponse({
        "count": count,
        "total": f"{total:.2f}",
        "items": data_items
    })


def menu_item(request, item_id):
    product = get_object_or_404(Product, pk=item_id)
    return render(request, "main/menu_item.html", {"product": product})

def get_or_create_user_cart(user):

    cart = (Cart.objects
                .filter(user=user)
                .order_by("-created_at")
                .first())
    if cart:
        return cart, False
    return Cart.objects.get_or_create(user=user)


def get_anonymous_cart_for_request(request):
    
    if not request.session.session_key:
        request.session.save()
    sk = request.session.session_key
    return Cart.objects.filter(user__isnull=True, session_key=sk).order_by("-created_at").first()

@transaction.atomic
def merge_cart_from_session_key(old_session_key: str | None, user):
    if not old_session_key:
        return

    anon_cart = (Cart.objects
                 .filter(user__isnull=True, session_key=old_session_key)
                 .order_by("-created_at")
                 .first())
    if not anon_cart:
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    # map existing user items by (product_id, signature)
    existing = {(ci.product_id, ci.signature): ci for ci in user_cart.items.all()}

    for item in anon_cart.items.select_related("product").prefetch_related("addons"):
        key = (item.product_id, item.signature)
        if key in existing:
            dst = existing[key]
            dst.quantity += item.quantity
            dst.save(update_fields=["quantity"])
            item.delete()
        else:
            item.cart = user_cart
            item.save(update_fields=["cart"])

    if not anon_cart.items.exists():
        anon_cart.delete()


        
def login(request):
    form = LoginForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].strip()
        password = form.cleaned_data["password"]

        if not request.session.session_key:
            request.session.save()
        old_session_key = request.session.session_key

        try:
            user_obj = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            form.add_error("password", "Incorrect email/password.")
        else:
            user = authenticate(request, username=user_obj.username, password=password)
            if user is not None:
                auth_login(request, user)
                merge_cart_from_session_key(old_session_key, user)
                messages.success(request, "Logged in successfully.")
                return redirect("main:index")
            form.add_error("password", "Incorrect email/password.")
    return render(request, "main/login.html", {"form": form})


def signup(request):
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Account created. You can now log in.")
        return redirect("main:login") 
    return render(request, "main/signup.html", {"form": form})

def logout(request):
    auth_logout(request)
    return redirect("main:index")

def add_address(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, "Address added successfully.")
        return redirect("main:profile")
    return render(request, "main/address.html", {"form": form})

def edit_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Address updated successfully.")
        return redirect("main:profile")
    return render(request, "main/address.html", {"form": form})

def delete_address(request, address_id):
    address = get_object_or_404(Address, pk=address_id, user=request.user)
    if request.method == "POST":
        address.delete()
        messages.success(request, "Address deleted successfully.")
        return redirect("main:profile")
    return render(request, "main/address_confirm_delete.html", {"address": address})

def address_list(request):
    addresses = Address.objects.filter(user=request.user)
    return render(request, "main/address_list.html", {"addresses": addresses})
