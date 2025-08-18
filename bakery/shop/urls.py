from django.urls import path
from .views import (
    cart_detail,
    add_to_cart,
    create_checkout_session,
    success_view,
    update_cart_item,
    remove_from_cart,
    remove_addons,
    empty_cart,
    checkout,
    cancel_view,
    order_list_view,
    update_order_status,
)

app_name = "shop"

urlpatterns = [
    path("cart/", cart_detail, name="cart_detail"),
    path("cart/add/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("cart/update/<int:item_id>/", update_cart_item, name="update_cart_item"),
    path("cart/remove/<int:item_id>/", remove_from_cart, name="remove_from_cart"),
    path("cart/remove_addons/<int:item_id>/<int:addon_id>/", remove_addons, name="remove_addons"),
    path("cart/empty_cart/", empty_cart, name="empty_cart"),
    path("checkout/", checkout, name="checkout"),
    path("create-checkout-session/", create_checkout_session, name="create_checkout_session"),
    path("success/", success_view, name="success"),
    path("cancel/", cancel_view, name="cancel"),
    path("orders/", order_list_view, name="order_list"),
    path("orders/update/<int:order_id>/", update_order_status, name="update_order_status"),
]