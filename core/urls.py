from django.urls import path, include
from .views import (
    AddToInventoryView,
    DeleteFromInventoryView,
    HomeView,
    ItemDetailView,
    OrderSummaryView,
    AddNewItemView,

    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    landing_page
)

app_name = 'core'

urlpatterns = [
    
    path("", HomeView.as_view(), name="home"),
    path("add-new-item/", AddNewItemView, name="add-new-item"),
    
    path("order-summary/", OrderSummaryView.as_view(), name="order-summary"),
    path("product/<slug>/", ItemDetailView.as_view(), name="product"),
    path("add-to-cart/<slug>", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<slug>", remove_from_cart, name="remove-from-cart"),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,
         name='remove-single-item-from-cart'),

    path(
        "add-to-inventory/",
        AddToInventoryView.as_view(),
        name="add-to-inventory"
    ),

    path(
        "delete-from-inventory/",
        DeleteFromInventoryView.as_view(),
        name="delete-from-inventory"
    ),

]
